import time
import math
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
        "no title": 0,
        "no label": 1,
        "no description": 2,
        "no subtitle": 3,
        "no tra": 4,
        "no original": 5,
        "no first line":6,
        "no pub":7,
        "no ill":8
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0: "no title",
        1: "no label",
        2: "no description",
        3: "no subtitle",
        4: "no tra",
        5: "no original",
        6: "no first line",
        7:"no pub",
        8:"no ill"

    }
    return switcher[statistic_id]


def save_obj(obj, name):
    with open('../python/obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('../python/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


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

            # LABEL
            label = ""
            try:
                label = data['entities'][book_id]["labels"]["en"]["value"]
                # print(label)
            except:
                # print("-- missing label on wikidata--")
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][book_id]["claims"]):
                if ("en" in data['entities'][book_id]["claims"]["descriptions"]):
                    description = data['entities'][book_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][book_id]):
                if ("en" in data['entities'][book_id]["descriptions"]):
                    description = data['entities'][book_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # TITLE
            title = ""
            if ("P1476" in data['entities'][book_id]["claims"]):
                title = (data['entities'][book_id]["claims"]["P1476"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                self.local_statistics[index("no title")] += 1

            
            # SUBTITLE
            subtitle = ""
            if ("P1680" in data['entities'][book_id]["claims"]):
                subtitle = data['entities'][book_id]["claims"]["P1680"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                self.local_statistics[index("no subtitle")] += 1

            # FIRST LINE
            first_line = ""
            if ("P1922" in data['entities'][book_id]["claims"]):
                first_line = data['entities'][book_id]["claims"]["P1922"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                self.local_statistics[index("no first line")] += 1

                
                
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

            # PUBLISHERS
            if ("P123" in data['entities'][book_id]["claims"]):
                for pub in data['entities'][book_id]["claims"]["P123"]:
                    try:
                        pubs_file_lock.acquire()
                        file_pubs_out.write(
                            str(pub["mainsnak"]["datavalue"]["value"]["id"]) + ";" + str(book_id) + "\n")
                        pubs_file_lock.release()
                    except:
                        pubs_file_lock.release()
            else:
                self.local_statistics[index("no pub")] += 1

            # ILLUSTRATORS (HUMANS)
            if ("P110" in data['entities'][book_id]["claims"]):
                for ill in data['entities'][book_id]["claims"]["P110"]:
                    try:
                        ills_file_lock.acquire()
                        file_ills_out.write(
                            str(ill["mainsnak"]["datavalue"]["value"]["id"]) + ";" + str(book_id) + "\n")
                        ills_file_lock.release()
                    except:
                        ills_file_lock.release()
            else:
                self.local_statistics[index("no ill")] += 1

            # ORIGINAL (BOOK)
            if ("P629" in data['entities'][book_id]["claims"]):
                for tra in data['entities'][book_id]["claims"]["P629"]:
                    try:
                        oris_file_lock.acquire()
                        file_oris_out.write(
                            str(tra["mainsnak"]["datavalue"]["value"]["id"]) + ";" + str(book_id) + "\n")
                        oris_file_lock.release()
                    except:
                        oris_file_lock.release()
            else:
                self.local_statistics[index("no original")] += 1
                
                
            

            file_out_lock.acquire()
            file_out.write(
                book_id + ";" + label + ";" + description + ";" + title + ";" + subtitle + ";" + first_line + "\n")
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
file_authors_path = "../roles/hasAuthor.txt"  # format wikidata:author_id,wikidata:book_id
file_tras_path = "../roles/hasTranslator.txt"
file_oris_path = "../roles/hasOriginal.txt"
file_ills_path = "../roles/hasIllustrator.txt"
file_pubs_path = "../roles/hasPublisher.txt"


# SAVING TO FILE



# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

editions = []

with open("../roles/hasEdition.txt", "r")as hp:
	j = 0
	for line in hp:
		if j == 0:
			j += 1
			continue
		edition = line.split(";")[0]
		editions.append(edition)

# SAVING TO FILE
file_log = open(file_log_path, 'w')
file_out = open(file_out_path, 'w')
file_out.write(
    "edition_id" + ";" + "label" + ";" + "description" + ";" + "title" + ";" + "subtitle" + ";" + "first_line" +  "\n")

file_tras_out = open(file_tras_path, 'w')
file_tras_out.write("translator_id;" + "edition_id" + "\n")
file_oris_out = open(file_oris_path, 'w')
file_oris_out.write("book_id;" + "edition_id" + "\n")
file_pubs_out = open(file_pubs_path, 'w')
file_pubs_out.write("publisher_id;" + "book_id" + "\n")
file_ills_out = open(file_ills_path, 'w')
file_ills_out.write("illustror_id;" + "book_id" + "\n")

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

# CLOSING OUTPUT FILES
file_out.close()
file_tras_out.close()
file_oris_out.close()
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
