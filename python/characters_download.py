import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random
import pickle

N_THREADS = 8
LEN_INDEX = 9


def index(statistic_name):
    switcher = {
        "no name": 0,
        "no label": 1,
        "no description": 2,
        "fictionalHuman":3,
        "no DoB":4,
        "no DoD":5,
        "no sex":6,
        "fictionalNotHuman":7,
        "human":8
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0:"no name",
        1:"no label",
        2:"no description",
        3:"fictionalHuman",
        4:"no DoB",
        5:"no DoD",
        6:"no sex",
        7:"fictionalNotHuman",
        8:"human"

    }
    return switcher[statistic_id]

# THREAD DEFINITION
class CharacterDownloadThread(threading.Thread):
    def __init__(self, threadID, a, b):
        threading.Thread.__init__(self)
        self.id = threadID
        self.res_min = a
        self.res_max = b
        self.local_statistics = [0 for x in range(LEN_INDEX)]
        self.influencing_characters = set([])

    def run(self):
        count = 0
        for j in range(self.res_min, self.res_max):
            time.sleep(random.random() * 0.1)
            count += 1
            if (count % 100 == 0):
                print("[Thread " + str(self.id) + "]\t" + "character " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            character = characters[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + character + ".json"
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
                label = data['entities'][character]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][character]["claims"]):
                if ("en" in data['entities'][character]["claims"]["descriptions"]):
                    description = data['entities'][character]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][character]):
                if ("en" in data['entities'][character]["descriptions"]):
                    description = data['entities'][character]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # NAME
            name = label
            if ("P1559" in data['entities'][character]["claims"]):
                name = (data['entities'][character]["claims"]["P1559"][0]["mainsnak"]["datavalue"]["value"]["text"])
            elif ("P1477" in data['entities'][character]["claims"]):
                name = (data['entities'][character]["claims"]["P1477"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                name = label
                self.local_statistics[index("no name")] += 1

            # SEX
            sex = ""
            if ("P21" in data['entities'][character]["claims"]):
                try:
                    sex = (data['entities'][character]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
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
                DoB = data['entities'][character]["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoB")] += 1

            # DoD
            DoD = ""
            try:
                DoD = data['entities'][character]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoD")] += 1



            if ("P31" in data['entities'][character]["claims"]):
                instance_of = []
                for iO in data['entities'][character]["claims"]["P31"]:
                    instance_of.append(iO["mainsnak"]["datavalue"]["value"]["id"])
                if "Q15632617" in instance_of:
                    fictional_human_lock.acquire()
                    fictional_human_file.write(str(
                character) + ";" + label + ";" + description + ";" + name + ";" + sex + ";" + DoB + ";" + DoD + "\n")
                    fictional_human_lock.release()
                    self.local_statistics[index("fictionalHuman")] += 1
                elif "Q5" in instance_of:
                    human_characters_lock.acquire()
                    human_character_file.write(character+"\n")
                    human_characters_lock.release()
                    self.local_statistics[index("human")] += 1
                else:
                    fictional_not_human_lock.acquire()
                    fictional_not_human_file.write(str(
                        character).replace(";", " ") + ";" + label.replace(";", " ") + ";" + description.replace(";", " ") + ";" + name.replace(";", " ") + ";" + sex + ";" + DoB + ";" + DoD + "\n")
                    fictional_not_human_lock.release()
                self.local_statistics[index("fictionalNotHuman")] += 1


    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
fictional_human_lock = threading.Lock()
fictional_not_human_lock = threading.Lock()
human_characters_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
fictional_human_file_path = "../concepts/FictionalHuman.txt"
fictional_not_human_file_path = "../concepts/FictionalNotHuman.txt"
log_file_path = "../log/log_Characters.txt"
human_character_file_path = "../tmp/human_character.txt"

# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# RETRIEVING ALL HUMANS WIKIDATA IDs
processed_characters_file_path = "../processed/processedCharacters.txt"
processed_characters_file = open(processed_characters_file_path, 'r')
processed_characters = [x.strip() for x in processed_characters_file.readlines()[1:]]
characters_file_path = "../roles/hasCharacter.txt"
characters_file = open(characters_file_path, 'r')
characters = list(set([x.strip().split(';')[1] for x in characters_file.readlines()[1:]]).difference(processed_characters))
processed_characters_file.close()
characters_file.close()

if len(characters)==0:
    sys.exit(1)

# OPENING OUTPUT FILES
fictional_human_file = open(fictional_human_file_path, 'a')
fictional_not_human_file = open(fictional_not_human_file_path, 'a')
human_character_file = open(human_character_file_path, 'a')
log_file = open(log_file_path, 'a')

n_characters = len(characters)
print("Number of characters: " + str(n_characters))

# PARALLEL COMPUTATION
threads = []
prec = 0
step = math.ceil(n_characters / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(CharacterDownloadThread(i, min(prec, n_characters), min(succ, n_characters)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics, t.join())]

# CLOSING OUTPUT FILES
fictional_human_file.close()
fictional_not_human_file.close()
human_character_file.close()

processed_characters_file = open(processed_characters_file_path, 'a')
for character in characters:
    processed_characters_file.write(character+"\n")
processed_characters_file.close()

# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_characters, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")

# STATISTICS REPORTING
log_file.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    log_file.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_characters, 2) * 100) + " %) \n")

log_file.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
log_file.close()

sys.exit(0)