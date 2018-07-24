import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random
import pickle

N_THREADS = 16
LEN_INDEX = 6


def index(statistic_name):
    switcher = {
        "no start time":0,
        "no end time":1,
        "no official residence":2,
        "no label": 3,
        "no description": 4,
        "no human":5

    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0:"no start time",
        1:"no end time",
        2:"no official residence",
        3:"no label",
        4:"no description",
        5:"no human"
    }
    return switcher[statistic_id]


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# THREAD DEFINITION
class MayorDownloadThread(threading.Thread):
    def __init__(self, threadID, a, b):
        threading.Thread.__init__(self)
        self.id = threadID
        self.res_min = a
        self.res_max = b
        self.local_statistics = [0 for x in range(LEN_INDEX)]

    def run(self):
        count = 0
        for j in range(self.res_min, self.res_max):
            time.sleep(random.random() * 0.1)
            count += 1
            if (count % 100 == 0):
                print("[Thread " + str(self.id) + "]\t" + "mayor " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            mayor = mayors[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + mayor + ".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                    break
                except:
                    time.sleep(i*0.5)
                    continue

            # LABEL
            label = ""
            try:
                label = data['entities'][mayor]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][mayor]["claims"]):
                if ("en" in data['entities'][mayor]["claims"]["descriptions"]):
                    description = data['entities'][mayor]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][mayor]):
                if ("en" in data['entities'][mayor]["descriptions"]):
                    description = data['entities'][mayor]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # OFFICIAL RESIDENCE
            residence_name = ""
            if ("P263" in data['entities'][mayor]["claims"]):
                residence = data['entities'][mayor]["claims"]["P263"][0]["mainsnak"]["datavalue"]["value"]["id"]
                # retrieve residence name or retrieve and save it
                if residence in official_residence_dict:
                    residence_name = official_residence_dict[residence]
                else:
                    for i in range(3):
                        try:
                            url_residence = "http://www.wikidata.org/wiki/Special:EntityData/" + residence + ".json"
                            response_residence = requests.get(url_residence)
                            data_residence = response_residence.json()
                            break
                        except:
                            time.sleep(i*0.5)
                            continue
                    try:
                        residence_dict_lock.acquire()
                        residence_name = data_residence['entities'][residence]["labels"]["en"]["value"]
                        official_residence_dict[residence] = residence_name
                        residence_dict_lock.release()
                    except:
                        residence_dict_lock.release()
            else:
                self.local_statistics[index("no official residence")] += 1

            # START/END TIME
            start_time = ""
            end_time = ""
            if ("P1308" in data['entities'][mayor]["claims"]):
                pref_mayor = ""
                for mayor_data in data['entities'][mayor]["claims"]["P1308"]:
                    pref_mayor = mayor_data
                    if mayor_data["rank"] == "preferred":
                        break
                try:
                    has_role_lock.acquire()
                    human = pref_mayor["mainsnak"]["datavalue"]["value"]["id"]
                    has_role_file.write(human+";"+mayor+"\n")
                    has_role_lock.release()
                except:
                    print("exception human")
                    has_role_lock.release()
                    self.local_statistics[index("no human")] += 1
                try:
                    start_time = mayor_data["qualifiers"]["P580"]["datavalue"]["value"]["time"]
                except:
                    self.local_statistics[index("no start time")] += 1

                try:
                    end_time = mayor_data["qualifiers"]["P582"]["datavalue"]["value"]["time"]
                except:
                    self.local_statistics[index("no end time")] += 1


            mayors_file.write(str(
                mayor) + ";" + label.replace(";", " ") + ";" + description.replace(";", " ") + ";" + start_time.replace(";", " ") + ";" + end_time.replace(";", " ") + ";" + residence_name.replace(";", " ") + "\n")

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
mayors_lock = threading.Lock()
residence_dict_lock = threading.Lock()
has_role_lock = threading.Lock()
human_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
mayors_file_path = "../concepts/Mayor.txt"
has_role_file_path = "../roles/hasRole.txt"
log_file_path = "../log/log_Mayor.txt"


# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# DICTIONARIES LOADING
try:
    occupations_dict = load_obj("occupations") # occupation wikidata id to label
except:
    occupations_dict = {}
try:
    official_residence_dict = load_obj('official_residence')
except:
    official_residence_dict = {}

# RETRIEVING ALL MAYORS WIKIDATA IDs
has_mayor_file_path = "../roles/hasMayor.txt"
mayors = []
has_mayor_file = open(has_mayor_file_path, 'r')
mayors = set([x.strip().split(";")[1] for x in has_mayor_file.readlines()[1:]])
processed_mayors_file_path = "../processed/processedMayors.txt"
processed_mayors_file = open(processed_mayors_file_path, 'r')
processed_mayors = set([x.strip() for x in processed_mayors_file.readlines()[1:]])
mayors = list(mayors.difference(processed_mayors))
has_mayor_file.close()
processed_mayors_file.close()

if len(mayors)==0:
    sys.exit(1)

# OPENING OUTPUT FILES
mayors_file = open(mayors_file_path, 'a')
has_role_file = open(has_role_file_path, 'a')
log_file = open(log_file_path, 'a')

n_mayors = len(mayors)
print("Number of mayors: " + str(n_mayors))

# PARALLEL COMPUTATION INITIALIZATION
threads = []
prec = 0
step = math.ceil(n_mayors / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(MayorDownloadThread(i, min(prec, n_mayors), min(succ, n_mayors)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics,t.join())]

processed_mayors_file = open(processed_mayors_file_path, 'a')
for mayor in mayors:
    processed_mayors_file.write(mayor+"\n")
processed_mayors_file.close()

# CLOSING OUTPUT FILES
mayors_file.close()
has_role_file.close()


# UPDATING DICTIONARIES
save_obj(official_residence_dict, 'official_residence')
save_obj(occupations_dict, 'occupations')
# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_mayors, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")

# STATISTICS REPORTING
log_file.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    log_file.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_mayors, 2) * 100) + " %) \n")

log_file.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
log_file.close()

sys.exit(0)