import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random
import pickle

N_THREADS = 8
LEN_INDEX = 7


def index(statistic_name):
    switcher = {
        "no name": 0,
        "no label": 1,
        "no description": 2,
        "fictional":3,
        "no DoB":4,
        "no DoD":5,
        "no sex":6
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0:"no name",
        1:"no label",
        2:"no description",
        3:"fictional",
        4:"no DoB",
        5:"no DoD",
        6:"no sex"

    }
    return switcher[statistic_id]


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


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
            if (count % 10 == 0):
                print("[Thread " + str(self.id) + "]\t" + "character " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            character = characters[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + character + ".json"
            response = requests.get(url)  # timeout
            try:
                data = response.json()
            except:
                print("EXCEPTION " + url)
                continue
            # print("[Thread " + str(self.id) + "]\t" + "book " + str(character))
            # end_time_get = time.time()
            # total_get_time += end_time_get - start_time_get


            if ("P31" in data['entities'][character]["claims"]):
                if data['entities'][character]["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"] == 'Q5':
                    humans_file_lock.acquire()
                    humans_file.write(character+"\n")
                    humans_file_lock.release()
                else:
                    self.local_statistics[index("fictional")] += 1
                    # LABEL
                    label = ""
                    try:
                        label = data['entities'][character]["labels"]["en"]["value"]
                        # print(label)
                    except:
                        # print("-- missing label on wikidata--")
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
                        print("bad date character: " + character)
                        self.local_statistics[index("no DoB")] += 1

                    # DoD
                    DoD = ""
                    try:
                        DoD = data['entities'][character]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
                    except:
                        self.local_statistics[index("no DoD")] += 1


                    fictional_characters_file.write(str(
                        character) + ";" + label + ";" + description + ";" + name + ";" + sex + ";" + DoB + ";" + DoD + ";" + "\n")

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
characters_lock = threading.Lock()
humans_file_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
human_id_file_path = "../humans.txt"
characters_file_path = "../roles/hasCharacter.txt"
fictional_characters_file_path = "../concepts/FictionalCharacter.txt"
log_file_path = "../log/Characters_download_log.txt"

# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# DICTIONARIES LOADING
occupations_dict = load_obj("occupations")  # occupation wikidata id to label


# RETRIEVING ALL HUMANS WIKIDATA IDs
characters = []
characters_file = open(characters_file_path, 'r')
characters = set([x.split(';')[0] for x in characters_file.readlines()[1:]])
characters = list(characters)
print(characters)
characters_file.close()

# OPENING OUTPUT FILES
fictional_characters_file = open(fictional_characters_file_path, 'w')
fictional_characters_file.write('fictional_character_id;label;description;name;sex;DoB;DoD;\n')
humans_file = open(human_id_file_path, 'a')
log_file = open(log_file_path, 'w')

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
characters_file.close()
humans_file.close()

# UPDATING DICTIONARIES
save_obj(occupations_dict, 'occupations')


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