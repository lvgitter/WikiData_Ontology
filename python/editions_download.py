import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random
import pickle

N_THREADS = 16
LEN_INDEX = 1


def index(statistic_name):
    switcher = {
        "no tra": 0
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0: "no tra"

    }
    return switcher[statistic_id]


def save_obj(obj, name):
    with open('../python/obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


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
            if (count % 10 == 0):  # to modify?
                print("[Thread " + str(self.id) + "]\t" + "edition " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            result = editions[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            # start_time_get = time.time()
            response = requests.get(url)  # timeout
            try:
                data = response.json()
            except:
                print("EXCEPTION " + url)
                continue
            book_id = url.split(".json")[0].split("/")[-1]
            # print("[Thread " + str(self.id) + "]\t" + "book " + str(book_id))
            # end_time_get = time.time()
            # total_get_time += end_time_get - start_time_get

           

            # TRANSLATOR (HUMANS)
            if ("P655" in data['entities'][book_id]["claims"]):
                for tra in data['entities'][book_id]["claims"]["P655"]:
                    try:
                        tras_file_lock.acquire()
                        file_tras_out.write(
                            str(tra["mainsnak"]["datavalue"]["value"]["id"]) + ";" + str(book_id) + "\n")
                        tras_file_lock.release()
                    except:
                        tras_file_lock.release()
            else:
                self.local_statistics[index("no tra")] += 1


    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS

tras_file_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
file_log_path = "../log/log_Edition.txt"
file_tras_path = "../roles/hasTranslator.txt"
# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]


# SAVING TO FILE

file_tras_out = open(file_tras_path, 'w')
file_tras_out.write("translator_id;" + "book_id" + "\n")

editions = []

with open("../roles/hasEdition.txt", "r")as hp:
	j = 0
	for line in hp:
		if j == 0:
			j += 1
			continue
		edition = line.split(";")[0]
		editions.append(edition)
		

#SAVING TO FILE
file_log = open(file_log_path, 'w')
file_tras_out.write("translator_id;" + "edition_id" + "\n")

n_results = len(editions)
print("Number of editions: " + str(n_results))
file_log.write("Number of editions: " + str(n_results) + "\n")
print("Number of  different editions: " + str(len(set(editions))) + "\n")
file_log.write("Number of different editions: " + str(len(set(editions))))

editions = list(set(editions))
n_results = len(editions)

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

# CLOSING OUTPUT FILES

file_tras_out.close()
# file_log.close()


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
