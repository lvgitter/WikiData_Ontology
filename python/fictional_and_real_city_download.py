import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 2

def index(statistic_name):
    switcher = {
        "real":0,
        "fictional":1
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"real",
        1:"fictional"
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
                print("[Thread "+str(self.id)+"]\t"+"city "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))


            result = cities[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            #start_time_get = time.time()
            response = requests.get(url) #timeout
            try:
                data = response.json()
            except:
                print ("EXCEPTION " + url)
                continue
            city_id = result
            #print("[Thread " + str(self.id) + "]\t" + "book " + str(book_id))
            #end_time_get = time.time()
            #total_get_time += end_time_get - start_time_get


            # INSTANCE OF
            instance_of = []
            if ("P31" in data['entities'][city_id]["claims"]):
                for iof in data['entities'][city_id]["claims"]["P31"]:
                    instance_of.append(iof["mainsnak"]["datavalue"]["value"]["id"])
            if "Q1964689" in iof:
                self.local_statistics[index("fictional")] += 1
                file_fict_lock.acquire()
                file_fict.write(city_id + "\n")
                file_fict_lock.release()
            else:
                self.local_statistics[index("real")] += 1
                file_real_lock.acquire()
                file_real.write(city_id + "\n")
                file_real_lock.release()
            

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_real_lock = threading.Lock()
file_fict_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
couns_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_real_path = "../concepts/RealCity.txt"
file_log_path = "../log/log_Real_And_Fictional_City.txt"
file_fict_path = "../concepts/FictionalCity.txt"

#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING ALL PUBLISHERs WIKIDATA IDs and QUERY THEM
cities = []
with open("../concepts/City.txt", "r")as hp:
    j = 0
    for line in hp:
        if j == 0:
            j += 1
            continue
        city = line.split(";")[0]
        cities.append(city)

#SAVING TO FILE
file_log = open(file_log_path, 'w')
file_real = open(file_real_path, 'w')
file_fict = open(file_fict_path, 'w')
file_real.write("real_city_id")
file_fict.write("fictional_city_id")

n_results = len(cities)
print("Number of cities: " + str(n_results))
file_log.write("Number of cities: " + str(n_results) + "\n")

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


#CLOSING OUTPUT FILES
file_real.close()
file_fict.close()


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
