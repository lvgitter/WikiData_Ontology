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
LEN_INDEX = 9


def index(statistic_name):
    switcher = {
        "no name": 0,
        "no sex": 1,
        "no DoB": 2,
        "no DoD": 3,
        "no occupation": 4,
        "no PoB": 5,
        "no PoD": 6,
        "no label": 7,
        "no description": 8
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
        7: "no label",
        8: "no description"

    }
    return switcher[statistic_id]


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# THREAD DEFINITION
class HumanDownloadThread(threading.Thread):
    def __init__(self, threadID, a, b):
        threading.Thread.__init__(self)
        self.id = threadID
        self.res_min = a
        self.res_max = b
        self.local_statistics = [0 for x in range(LEN_INDEX)]
        self.influencing_humans = set([])

    def run(self):
        count = 0
        for j in range(self.res_min, self.res_max):
            time.sleep(random.random() * 0.1)
            count += 1
            if (count % 100 == 0):
                print("[Thread " + str(self.id) + "]\t" + "human " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            human = humans[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + human + ".json"
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
                label = data['entities'][human]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            try:
                if ("descriptions" in data['entities'][human]["claims"]):
                    if ("en" in data['entities'][human]["claims"]["descriptions"]):
                        description = data['entities'][human]["claims"]["descriptions"]["en"]["value"]
                elif ("descriptions" in data['entities'][human]):
                    if ("en" in data['entities'][human]["descriptions"]):
                        description = data['entities'][human]["descriptions"]["en"]["value"]
            except:
                self.local_statistics[index("no description")] += 1

            # NAME
            name = ""
            try:
                if ("P1559" in data['entities'][human]["claims"]):
                    name = (data['entities'][human]["claims"]["P1559"][0]["mainsnak"]["datavalue"]["value"]["text"])
                elif ("P1477" in data['entities'][human]["claims"]):
                    name = (data['entities'][human]["claims"]["P1477"][0]["mainsnak"]["datavalue"]["value"]["text"])
            except:
                name = label
                self.local_statistics[index("no name")] += 1

            # SEX
            sex = ""
            try:
                if ("P21" in data['entities'][human]["claims"]):
                    sex = (data['entities'][human]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
                    if sex == 'Q6581097':
                        sex = 'male'
                    elif sex == 'Q6581072':
                        sex = 'female'
                    else:
                        self.local_statistics[index("no sex")] += 1
            except:
                    self.local_statistics[index("no sex")] += 1

            # DoB
            DoB = ""
            try:
                DoB = data['entities'][human]["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoB")] += 1

            # DoD
            DoD = ""
            try:
                DoD = data['entities'][human]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoD")] += 1

            # PoB
            PoB = ""
            try:
                if ("P19" in data['entities'][human]["claims"]):
                    for place in data['entities'][human]["claims"]["P19"]:
                        try:
                            place_of_birth_lock.acquire()
                            place_of_birth_file.write(
                                str(human + ";" + place["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                            place_of_birth_lock.release()
                            PoB = place["mainsnak"]["datavalue"]["value"]["id"]
                        except:
                            place_of_birth_lock.release()
            except:
                self.local_statistics[index("no PoB")] += 1

            # PoD
            PoD = ""
            try:
                if ("P20" in data['entities'][human]["claims"]):
                    for place in data['entities'][human]["claims"]["P20"]:
                        try:
                            place_of_death_lock.acquire()
                            place_of_death_file.write(
                                str(human + ";" + place["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                            place_of_death_lock.release()
                            PoD = place["mainsnak"]["datavalue"]["value"]["id"]
                        except:
                            place_of_death_lock.release()
            except:
                self.local_statistics[index("no PoD")] += 1

            # OCCUPATION
            try:
                if ("P106" in data['entities'][human]["claims"]):
                    for occupation in data['entities'][human]["claims"]["P106"]:
                        occupation = occupation["mainsnak"]["datavalue"]["value"]["id"]
                        # retrieve occupation name or retrieve and save it
                        if occupation in occupations_dict:
                            occupations_dict_lock.acquire()
                            occupation_name = occupations_dict[occupation]
                            file_has_occupation.write(human + ";" + occupation_name + "\n")
                            occupations_dict_lock.release()
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
                                file_has_occupation.write(human + ";" + occupation_name + "\n")
                                occupations_dict_lock.release()
                            except:
                                occupations_dict_lock.release()
            except:
                self.local_statistics[index("no occupation")] += 1

            human_file_lock.acquire()
            humans_file.write(str(
                human) + ";" + label.replace(";", " ") + ";" + description.replace(";", " ") + ";" + name.replace(";", " ") + ";" + sex + ";" + DoB + ";" + DoD + ";" + "nc\n")
            human_file_lock.release()

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
has_role_lock = threading.Lock()
place_of_birth_lock = threading.Lock()
place_of_death_lock = threading.Lock()
occupations_dict_lock = threading.Lock()
human_file_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
humans_file_path = "../concepts/Human.txt"
place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_death_file_path = "../roles/placeOfDeath.txt"
processed_humans_file_path = "../processed/processedHumans.txt"
file_has_occupation_path = "../roles/hasHumanOccupation.txt"
log_file_path = "../log/log_Human.txt"

# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# DICTIONARIES LOADING
try:
    occupations_dict = load_obj("occupations")  # occupation wikidata id to label
except:
    occupations_dict = {}

# RETRIEVING ALL HUMANS WIKIDATA IDs ALREADY PROCESSED
processed_humans_file = open(processed_humans_file_path, 'r')
processed_humans = list(set([x.strip() for x in processed_humans_file.readlines()[1:]]))
processed_humans_file.close()


# RETRIEVING ALL HUMANS WIKIDATA IDs TO BE PROCESSED
humans = []
has_role_file_path = "../roles/hasRole.txt"
has_role_file = open(has_role_file_path, 'r')
humans = set([x.strip().split(";")[0] for x in has_role_file.readlines()[1:]])
human_characters_file = open("../tmp/human_character.txt", 'r')
has_illustrator_file_path = "../roles/hasIllustrator.txt"
has_illustrator_file = open(has_illustrator_file_path, 'r')
illustrators = set([x.strip().split(';')[1] for x in has_illustrator_file.readlines()[1:]])
humans = humans.union(illustrators)
humans = list(humans.union(set([x.strip() for x in human_characters_file.readlines()[1:]]).difference(processed_humans)).difference(processed_humans))
human_characters_file.close()
has_role_file.close()
has_illustrator_file.close()

if len(humans)==0:
    sys.exit(1)

# OPENING OUTPUT FILES
humans_file = open(humans_file_path, 'a')
place_of_birth_file = open(place_of_birth_file_path, 'a')
place_of_death_file = open(place_of_death_file_path, 'a')
processed_humans_file = open(processed_humans_file_path, 'a')
file_has_occupation = open(file_has_occupation_path, 'a')
log_file = open(log_file_path, 'a')


n_humans = len(humans)
print("Number of humans: " + str(n_humans)+"\n")
log_file.write("Number of humans: " + str(n_humans)+"\n")

# PARALLEL COMPUTATION
threads = []
prec = 0
step = math.ceil(n_humans / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(HumanDownloadThread(i, min(prec, n_humans), min(succ, n_humans)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics, t.join())]

# UPDATING PROCESSED HUMAN WIKIDATA IDS

for h in humans:
    processed_humans_file.write(h+"\n")

processed_humans_file = open(processed_humans_file_path, 'a')
for human in humans:
    processed_humans_file.write(human+"\n")
processed_humans_file.close()

# CLOSING OUTPUT FILES
humans_file.close()
place_of_birth_file.close()
place_of_death_file.close()
processed_humans_file.close()
file_has_occupation.close()

# UPDATING DICTIONARIES
save_obj(occupations_dict, 'occupations')
'''
# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_humans, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")'''

# STATISTICS REPORTING
log_file.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    log_file.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_humans, 2) * 100) + " %) \n")

log_file.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
log_file.close()

sys.exit(0)
