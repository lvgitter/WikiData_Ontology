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
        "no title": 0,
        "no label": 1,
        "no description": 2,
        "no translator": 3,
        "no publisher":4,
        "no illustrator":5
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0: "no title",
        1: "no label",
        2: "no description",
        3: "no translator",
        4:"no publisher",
        5:"no illustrator"

    }
    return switcher[statistic_id]

# THREAD DEFINITION
class myThread(threading.Thread):
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
                print("[Thread " + str(self.id) + "]\t" + "edition " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            result = editions[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                    break
                except:
                    time.sleep(i*0.5)
                    continue
            edition_id = editions[j]

            # LABEL
            label = ""
            try:
                label = data['entities'][edition_id]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][edition_id]["claims"]):
                if ("en" in data['entities'][edition_id]["claims"]["descriptions"]):
                    description = data['entities'][edition_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][edition_id]):
                if ("en" in data['entities'][edition_id]["descriptions"]):
                    description = data['entities'][edition_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # TRANSLATOR (HUMANS)
            if ("P655" in data['entities'][edition_id]["claims"]):
                for tra in data['entities'][edition_id]["claims"]["P655"]:
                    try:
                        tras_file_lock.acquire()
                        file_tras_out.write(
                            str(edition_id + ";"+tra["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        tras_file_lock.release()
                    except:
                        tras_file_lock.release()
            else:
                self.local_statistics[index("no translator")] += 1

            # PUBLISHERS
            if ("P123" in data['entities'][edition_id]["claims"]):
                for pub in data['entities'][edition_id]["claims"]["P123"]:
                    try:
                        pubs_file_lock.acquire()
                        file_pubs_out.write(
                            str(edition_id+";"+pub["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        pubs_file_lock.release()
                    except:
                        pubs_file_lock.release()
            else:
                self.local_statistics[index("no publisher")] += 1

            # ILLUSTRATORS (HUMANS)
            if ("P110" in data['entities'][edition_id]["claims"]):
                for ill in data['entities'][edition_id]["claims"]["P110"]:
                    try:
                        ills_file_lock.acquire()
                        file_ills_out.write(
                            str(edition_id+";"+ill["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        ills_file_lock.release()
                    except:
                        ills_file_lock.release()
            else:
                self.local_statistics[index("no illustrator")] += 1
                
            file_out_lock.acquire()
            file_out.write(
                edition_id + ";" + label + ";" + description + "\n")
            file_out_lock.release()

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
tras_file_lock = threading.Lock()
oris_file_lock = threading.Lock()
ills_file_lock = threading.Lock()
pubs_file_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()




# FILES OUTPUT PATH
file_out_path = "../concepts/Edition.txt"
file_log_path = "../log/log_Edition.txt"
file_tras_path = "../roles/hasTranslator.txt"
file_ills_path = "../roles/hasIllustrator.txt"
file_pubs_path = "../roles/hasPublisher.txt"


# SAVING TO FILE



# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING EDITIONS
has_edition_file_path = "../roles/hasEdition.txt"
processed_editions_file_path = "../processed/processedEditions.txt"
processed_editions_file = open(processed_editions_file_path, 'r')
processed_editions = [x.strip() for x in processed_editions_file.readlines()[1:]]
has_edition_file = open(has_edition_file_path, "r")
editions = list(set([x.strip().split(';')[1] for x in has_edition_file.readlines()[1:]]).difference(processed_editions))
has_edition_file.close()
processed_editions_file.close()

if len(editions)==0:
    sys.exit(1)

# SAVING TO FILE
file_log = open(file_log_path, 'a')
file_out = open(file_out_path, 'a')
file_tras_out = open(file_tras_path, 'a')
file_pubs_out = open(file_pubs_path, 'a')
file_ills_out = open(file_ills_path, 'a')

n_results = len(editions)
print("Number of results: " + str(n_results))
file_log.write("Number of results: " + str(n_results) + "\n")

# PARALLEL COMPUTATION INITIALIZATION
threads = []
prec = 0
step = math.ceil(n_results / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(myThread(i, min(prec, n_results), min(succ, n_results)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics, t.join())]


processed_editions_file = open(processed_editions_file_path, 'a')
for edition in editions:
    processed_editions_file.write(edition+"\n")
processed_editions_file.close()

# CLOSING OUTPUT FILES
file_out.close()
file_tras_out.close()
file_pubs_out.close()
file_ills_out.close()


# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_results, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")

# STATISTICS REPORTING
file_log.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    file_log.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_results, 2) * 100) + " %) \n")

file_log.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
file_log.close()

sys.exit(0)