import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 3

def index(statistic_name):
    switcher = {
        "no speakers":0,
        "no label":1,
        "no description":2
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no speakers",
        1:"no label",
        2:"no description"
    }
    return switcher[statistic_id]


#THREAD DEFINITION
class myThread (threading.Thread):

   def __init__(self, threadID, a, b):
       threading.Thread.__init__(self)
       self.id = threadID
       self.res_min = a
       self.res_max = b
       self.local_statistics = [0 for x in range(LEN_INDEX)]

   def run(self):
        count=0
        for j in range(self.res_min, self.res_max):
            time.sleep(random.random()*0.1)
            count += 1
            if (count%5 == 0): #to modify?
                print("[Thread "+str(self.id)+"]\t"+"language "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))
            result = languages[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                except:
                    print ("EXCEPTION " + url)
                    time.sleep(0.5)
                    continue

            language_id = result
            
            # LABEL
            label = ""
            try:
                label = data['entities'][language_id]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][language_id]["claims"]):
                if ("en" in data['entities'][language_id]["claims"]["descriptions"]):
                    description = data['entities'][language_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][language_id]):
                if ("en" in data['entities'][language_id]["descriptions"]):
                    description = data['entities'][language_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # SPEAKERS
            speakers = ""
            if ("P1098" in data['entities'][language_id]["claims"]):
                speakers = (data['entities'][language_id]["claims"]["P1098"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            else:
                self.local_statistics[index("no speakers")] += 1

                
            file_out_lock.acquire()
            file_out.write(language_id + ";" + label + ";" + description + ";" + speakers + "\n")
            file_out_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
couns_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_out_path = "../concepts/Language.txt"
file_log_path = "../log/log_Language.txt"

#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING ALL LANGUAGESs WIKIDATA IDs and QUERY THEM
written_in_file_path = "../roles/writtenIn.txt"
written_in_file = open(written_in_file_path, "r")
languages = set([x.strip().split(';')[1] for x in written_in_file.readlines()[1:]])
has_used_language_file_path = "../roles/hasUsedLanguage.txt"
has_used_language_file = open(has_used_language_file_path, "r")
languages = languages.union(set([x.strip().split(';')[1] for x in has_used_language_file.readlines()[1:]]))
speaks_file_path = "../roles/speaks.txt"
speaks_file = open(speaks_file_path, "r")
languages = languages.union(set([x.strip().split(';')[1] for x in speaks_file.readlines()[1:]]))
processed_languages_file_path = "../processed/processedLanguages.txt"
processed_languages_file = open(processed_languages_file_path, 'r')
processed_languages = set([x.strip() for x in processed_languages_file.readlines()[1:]])
languages = list(languages.difference(processed_languages))
written_in_file.close()
speaks_file.close()
processed_languages_file.close()

if len(languages)==0:
    sys.exit(1)

# OUTPUT FILES
file_log = open(file_log_path, 'a')
file_out = open(file_out_path, 'a')

n_results = len(languages)
print("Number of languages: " + str(n_results))
file_log.write("Number of languages: " + str(n_results))

n_results = len(languages)


#PARALLEL COMPUTATION INITIALIZATION
threads = []
prec=0
step = math.ceil(n_results/N_THREADS)
succ= step
for i in range(N_THREADS):
    threads.append(myThread(i, min(prec, n_results), min(succ,n_results)))
    prec=succ
    succ=succ+step

for t in threads:
    t.start()

for t in threads:
    statistics =  [sum(x) for x in zip(statistics, t.join())]


processed_languages_file = open(processed_languages_file_path, 'a')
for language in languages:
    processed_languages_file.write(language+"\n")
processed_languages_file.close()


#CLOSING OUTPUT FILES
file_out.close()

#STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %)")

total_time = time.time() - total_time
print("Total_time:\t"+str(round(total_time,2))+" sec")

#STATISTICS REPORTING
file_log.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    file_log.write(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %) \n")

file_log.write("Total_time:\t"+str(round(total_time,2))+" sec" + "\n")
file_log.close()

sys.exit(0)