import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 5

def index(statistic_name):
    switcher = {
        "no inception":0,
        "no loc":1,
        "no founder":2,
        "no label":3,
        "no description":4
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no inception",
        1:"no loc",
        2:"no founder",
        3:"no label",
        4:"no description"
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
            if (count%100 == 0):
                print("[Thread "+str(self.id)+"]\t"+"publisher "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))


            result = publishers[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                except:
                    print ("EXCEPTION " + url)
                    time.sleep(0.5)
                    continue
            pub_id = result
            
            # LABEL
            label = ""
            try:
                label = data['entities'][pub_id]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][pub_id]["claims"]):
                if ("en" in data['entities'][pub_id]["claims"]["descriptions"]):
                    description = data['entities'][pub_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][pub_id]):
                if ("en" in data['entities'][pub_id]["descriptions"]):
                    description = data['entities'][pub_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # INCEPTION
            inception = ""
            if ("P571" in data['entities'][pub_id]["claims"]):
                inception = (data['entities'][pub_id]["claims"]["P571"][0]["mainsnak"]["datavalue"]["value"]["time"].split("-")[0][1:])
            else:
                self.local_statistics[index("no inception")] += 1

            # LOCATION (COUNTRY)
            if ("P17" in data['entities'][pub_id]["claims"]):
                for loc in data['entities'][pub_id]["claims"]["P17"]:
                    try:
                        locs_file_lock.acquire()
                        file_locs_out.write(str(pub_id+";"+loc["mainsnak"]["datavalue"]["value"]["id"])+"\n")
                        locs_file_lock.release()
                    except:
                        locs_file_lock.release()
            else:
                self.local_statistics[index("no loc")] += 1
            
            
            # FOUNDER (HUMAN)
            if ("P112" in data['entities'][pub_id]["claims"]):
                for fou in data['entities'][pub_id]["claims"]["P112"]:
                    try:
                        fous_file_lock.acquire()
                        file_fous_out.write(str(pub_id+";"+fou["mainsnak"]["datavalue"]["value"]["id"])+"\n")
                        fous_file_lock.release()
                    except:
                        fous_file_lock.release()
            else:
                self.local_statistics[index("no founder")] += 1
                
            file_out_lock.acquire()
            file_out.write(pub_id + ";" + label + ";" + description + ";" + inception + "\n")
            file_out_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
fous_file_lock = threading.Lock()
locs_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_out_path = "../concepts/Publisher.txt"
file_log_path = "../log/log_Publisher.txt"
file_locs_path = "../roles/locatedIn.txt"
file_fous_path = "../roles/foundedBy.txt"

#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING ALL PUBLISHERs WIKIDATA IDs and QUERY THEM
has_publisher_file_path = "../roles/hasPublisher.txt"
processed_publishers_file_path = "../processed/processedPublishers.txt"
has_publisher_file = open(has_publisher_file_path, "r")
processed_publishers_file = open(processed_publishers_file_path, 'r')
processed_publishers = [x.strip() for x in processed_publishers_file.readlines()[1:]]
publishers = list(set([x.strip().split(';')[1] for x in has_publisher_file.readlines()[1:]]).difference(processed_publishers))
has_publisher_file.close()
processed_publishers_file.close()

if len(publishers)==0:
    sys.exit(1)

#SAVING TO FILE
file_log = open(file_log_path, 'a')
file_out = open(file_out_path, 'a')
file_locs_out = open(file_locs_path, 'a')
file_fous_out = open(file_fous_path, 'a')

n_results = len(publishers)
print("Number of publishers: " + str(n_results))
file_log.write("Number of publishers: " + str(n_results) + "\n")

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

processed_publishers_file = open(processed_publishers_file_path, 'a')
for publisher in publishers:
    processed_publishers_file.write(publisher+"\n")
processed_publishers_file.close()


#CLOSING OUTPUT FILES
file_out.close()
file_locs_out.close()
file_fous_out.close()


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