import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 6

def index(statistic_name):
    switcher = {
        "no population":0,
        "no area":1,
        "no label":2,
        "no description":3,
        "no country":4,
        "no mayor":5
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no population",
        1:"no area",
        2:"no label",
        3:"no description",
        4:"no country",
        5:"no mayor"
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
            
            # LABEL
            label = ""
            try:
                label = data['entities'][city_id]["labels"]["en"]["value"]
                #print(label)
            except:
                #print("-- missing label on wikidata--")
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][city_id]["claims"]):
                if ("en" in data['entities'][city_id]["claims"]["descriptions"]):
                    description = data['entities'][city_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][city_id]):
                if ("en" in data['entities'][city_id]["descriptions"]):
                    description = data['entities'][city_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # POPULATION
            population = ""
            if ("P1082" in data['entities'][city_id]["claims"]):
                population = (data['entities'][city_id]["claims"]["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            else:
                self.local_statistics[index("no population")] += 1
            
            
            # AREA
            area = ""
            if ("P2046" in data['entities'][city_id]["claims"]):
                area = (data['entities'][city_id]["claims"]["P2046"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            else:
                self.local_statistics[index("no area")] += 1



            # MAYOR (P1313)
            if ("P1313" in data['entities'][city_id]["claims"]):
                for mayor in data['entities'][city_id]["claims"]["P1313"]:
                    try:
                        #if (mayor["mainsnak"]["datavalue"]["value"]["id"] in mayors):
                        has_mayor_lock.acquire()
                        has_mayor_file.write(
                            str(city_id + ";" + mayor["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        has_mayor_lock.release()

                    except:
                        has_mayor_lock.release()
            else:
                self.local_statistics[index("no mayor")] += 1

            
            
            # COUNTRY
            if ("P17" in data['entities'][city_id]["claims"]):
                coun = data['entities'][city_id]["claims"]["P17"][0] #take only the preferred one; assumption: it's the FIRST
            try:
                couns_file_lock.acquire()
                file_couns_out.write(str(coun["mainsnak"]["datavalue"]["value"]["id"])+";"+str(city_id)+"\n")
                couns_file_lock.release()
            except:
                couns_file_lock.release()
            else:
                self.local_statistics[index("no country")] += 1
                
            file_out_lock.acquire()
            file_out.write(city_id + ";" + label + ";" + description + ";" + area + ";" + population + "\n")
            file_out_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
has_mayor_lock = threading.Lock()
couns_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()


#ID OF ALL POSSIBLE MAYORS
#file_mayors_id_path = "../mayors_id.txt"

place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_death_file_path = "../roles/placeOfDeath.txt"
place_of_birth_file = open(place_of_birth_file_path, 'r')
place_of_death_file = open(place_of_death_file_path, 'r')
PoB = set([x.strip().split(";")[1] for x in place_of_birth_file.readlines()[1:]])
PoD = set([x.strip().split(";")[1] for x in place_of_death_file.readlines()[1:]])
cities = list(PoB.union(PoD))


#FILES OUTPUT PATH
file_out_path = "../concepts/RealCity.txt"
file_log_path = "../log/log_RealCity.txt"
file_couns_path = "../roles/hasCountry.txt"
file_has_mayor_path = "../roles/hasMayor.txt"


#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING ALL PUBLISHERs WIKIDATA IDs and QUERY THEM

with open("../roles/hasLocation.txt", "r")as hp:
    j = 0
    for line in hp:
        if j == 0:
            j += 1
            continue
        city = line.split(";")[0]
        cities.append(city)

# RETRIEVING ALL PUBLISHERs WIKIDATA IDs and QUERY THEM
#file_mayors_id = open(file_mayors_id_path, 'r')
#mayors = ([x.strip() for x in file_mayors_id.readlines()[1:]])

#SAVING TO FILE
file_log = open(file_log_path, 'w')
file_out = open(file_out_path, 'w')
file_couns_out = open(file_couns_path, 'w')
file_couns_out.write("country_id;" + "city_id" + "\n")
file_out.write("city_id" + ";" + "label" + ";" + "description" + ";" + "area" + ";" + "population" + "\n")
has_mayor_file = open(file_has_mayor_path, 'w')
has_mayor_file.write("city_id;mayor_id\n")
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
file_out.close()
file_couns_out.close()


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
