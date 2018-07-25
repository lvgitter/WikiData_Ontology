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
LEN_INDEX = 10


def index(statistic_name):
    switcher = {
        "no name": 0,
        "no sex": 1,
        "no DoB": 2,
        "no DoD": 3,
        "no occupation": 4,
        "no PoB": 5,
        "no PoD": 6,
        "no language":7,
        "no label": 8,
        "no description": 9
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0: "no name",
        1: "no sex",
        2: "no DoB",
        3: "no DoD",
        4: "no occupation",
        5: "no PoB",
        6: "no PoD",
        7:"no language",
        8: "no label",
        9: "no description"

    }
    return switcher[statistic_id]


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# THREAD DEFINITION
class TranslatorDownloadThread(threading.Thread):
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
                print("[Thread " + str(self.id) + "]\t" + "translator " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            translator = translators[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + translator + ".json"
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
                label = data['entities'][translator]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][translator]["claims"]):
                if ("en" in data['entities'][translator]["claims"]["descriptions"]):
                    description = data['entities'][translator]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][translator]):
                if ("en" in data['entities'][translator]["descriptions"]):
                    description = data['entities'][translator]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # NAME
            name = ""
            if ("P1559" in data['entities'][translator]["claims"]):
                name = (data['entities'][translator]["claims"]["P1559"][0]["mainsnak"]["datavalue"]["value"]["text"])
            elif ("P1477" in data['entities'][translator]["claims"]):
                name = (data['entities'][translator]["claims"]["P1477"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                name = label
                self.local_statistics[index("no name")] += 1

            # SEX
            sex = ""
            if ("P21" in data['entities'][translator]["claims"]):
                try:
                    sex = (data['entities'][translator]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
                    if sex == 'Q6581097':
                        sex = 'male'
                    elif sex == 'Q6581072':
                        sex = 'female'
                    else:
                        sex = 'unknown'
                        self.local_statistics[index("no sex")] += 1
                except:
                    self.local_statistics[index("no sex")] += 1

            # DoB
            DoB = ""
            try:
                DoB = data['entities'][translator]["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoB")] += 1

            # DoD
            DoD = ""
            try:
                DoD = data['entities'][translator]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoD")] += 1

            # PoB
            if ("P19" in data['entities'][translator]["claims"]):
                for place in data['entities'][translator]["claims"]["P19"]:
                    try:
                        place_of_birth_lock.acquire()
                        place_of_birth_file.write(
                            str(translator + ";" + place["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        place_of_birth_lock.release()
                        PoB = place["mainsnak"]["datavalue"]["value"]["id"]
                    except:
                        place_of_birth_lock.release()
            else:
                self.local_statistics[index("no PoB")] += 1

            # PoD
            if ("P20" in data['entities'][translator]["claims"]):
                for place in data['entities'][translator]["claims"]["P20"]:
                    try:
                        place_of_death_lock.acquire()
                        place_of_death_file.write(
                            str(translator + ";" + place["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        place_of_death_lock.release()
                        PoD = place["mainsnak"]["datavalue"]["value"]["id"]
                    except:
                        place_of_death_lock.release()
            else:
                self.local_statistics[index("no PoD")] += 1

            # OCCUPATION
            if ("P106" in data['entities'][translator]["claims"]):
                for occupation in data['entities'][translator]["claims"]["P106"]:
                    occupation = occupation["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve occupation name or retrieve and save it
                    if occupation in occupations_dict:
                        occupation_name = occupations_dict[occupation]
                        occupations_file.write(translator + ";" + occupation_name + "\n")
                    else:
                        for i in range(3):
                            try:
                                urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + occupation + ".json"
                                response_occupation = requests.get(urlg)
                                data_occupation = response_occupation.json()
                                break
                            except:
                                time.sleep(i*0.5)
                                continue
                        try:
                            occupations_dict_lock.acquire()
                            occupation_name = data_occupation['entities'][occupation]["labels"]["en"]["value"]
                            occupations_dict[occupation] = occupation_name
                            occupations_file.write(translator+";"+occupation_name+"\n")
                            occupations_dict_lock.release()
                        except:
                            occupations_dict_lock.release()

            else:
                self.local_statistics[index("no occupation")] += 1


            # SPEAKS
            if ("P1412" in data['entities'][translator]["claims"]):
                for language in data['entities'][translator]["claims"]["P1412"]:
                    try:
                        speaks_lock.acquire()
                        speaks_file.write(
                            str(translator + ";" + language["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        speaks_lock.release()
                    except:
                        speaks_lock.release()
            else:
                self.local_statistics[index("no PoD")] += 1

            translators_lock.acquire()
            translators_file.write(str(translator) + ";" + label.replace(";", " ") + ";" + description.replace(";", " ") + ";" + name.replace(";", " ") + ";" + sex + ";" + DoB + ";" + DoD + "\n")
            translators_lock.release()

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
translators_lock = threading.Lock()
place_of_birth_lock = threading.Lock()
place_of_death_lock = threading.Lock()
occupations_dict_lock = threading.Lock()
speaks_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
translators_file_path = "../concepts/Translator.txt"
translators_id_file_path = "../roles/hasTranslator.txt"
speaks_file_path = "../roles/speaks.txt"
place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_death_file_path = "../roles/placeOfDeath.txt"
log_file_path = "../log/log_Translator.txt"
occupations_file_path = "../roles/hasHumanOccupation.txt"

# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# DICTIONARIES LOADING
try:
    occupations_dict = load_obj("occupations") # occupation wikidata id to label
except:
    occupations_dict = {}

# RETRIEVING ALL TRANSLATORS WIKIDATA IDs
processed_translators_file_path = "../processed/processedTranslators.txt"
processed_translators_file = open(processed_translators_file_path, 'r')
processed_translators = set([x.strip() for x in processed_translators_file.readlines()[1:]])
translators_id_file = open(translators_id_file_path, 'r')
translators = set([x.strip().split(';')[1] for x in translators_id_file.readlines()[1:]])
translators = list(translators.difference(processed_translators))
translators_id_file.close()
processed_translators_file.close()

if len(translators)==0:
    sys.exit(1)

# OPENING OUTPUT FILES
translators_file = open(translators_file_path, 'a')
speaks_file = open(speaks_file_path, 'a')
place_of_birth_file = open(place_of_birth_file_path, 'a')
place_of_death_file = open(place_of_death_file_path, 'a')
occupations_file = open(occupations_file_path, 'a')
log_file = open(log_file_path, 'a')

n_translators = len(translators)
print("Number of translators: " + str(n_translators))

# PARALLEL COMPUTATION INITIALIZATION
threads = []
prec = 0
step = math.ceil(n_translators / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(TranslatorDownloadThread(i, min(prec, n_translators), min(succ, n_translators)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics, t.join())]


processed_translators_file = open(processed_translators_file_path, 'a')
for translator in translators:
    processed_translators_file.write(translator+"\n")
processed_translators_file.close()


# CLOSING OUTPUT FILES
translators_file.close()
speaks_file.close()
place_of_birth_file.close()
place_of_death_file.close()
occupations_file.close()


# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_translators, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")

# STATISTICS REPORTING
log_file.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    log_file.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_translators, 2) * 100) + " %) \n")

log_file.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
log_file.close()

sys.exit(0)