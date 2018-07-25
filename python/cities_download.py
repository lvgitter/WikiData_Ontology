import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 7

def index(statistic_name):
    switcher = {
        "no population":0,
        "no area":1,
        "no label":2,
        "no description":3,
        "no country":4,
        "no mayor":5,
        "fictional":6
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no population",
        1:"no area",
        2:"no label",
        3:"no description",
        4:"no country",
        5:"no mayor",
        6:"fictional"
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
                print("[Thread "+str(self.id)+"]\t"+"city "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))


            result = cities[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                    break
                except:
                    time.sleep(i*0.5)
                    continue
            city_id = result
            
            # LABEL
            label = ""
            try:
                label = data['entities'][city_id]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            try:
                description = ""
                if ("descriptions" in data['entities'][city_id]["claims"]):
                    if ("en" in data['entities'][city_id]["claims"]["descriptions"]):
                        description = data['entities'][city_id]["claims"]["descriptions"]["en"]["value"]
                elif ("descriptions" in data['entities'][city_id]):
                    if ("en" in data['entities'][city_id]["descriptions"]):
                        description = data['entities'][city_id]["descriptions"]["en"]["value"]
            except:
                self.local_statistics[index("no description")] += 1

            # REAL OR FICTIONAL CITY
            try:
                instance_of = []
                if ("P31" in data['entities'][city_id]["claims"]):
                    for iof in data['entities'][city_id]["claims"]["P31"]:
                        instance_of.append(iof["mainsnak"]["datavalue"]["value"]["id"])
                if "Q1964689" in instance_of:
                    self.local_statistics[index("fictional")] += 1
                    # HAS ANALOG (P1074)
                    if ("P1074" in data['entities'][city_id]["claims"]):
                        try:
                            has_analog_lock.acquire()
                            real_city = data['entities'][city_id]["claims"]["P1074"][0]["mainsnak"]["datavalue"]["value"]["id"]
                            file_has_analog.write(city_id+";"+real_city+"\n")
                            has_analog_lock.release()
                        except:
                            has_analog_lock.release()
                    file_fict_lock.acquire()
                    file_fictional_city.write(city_id + ";" + label + ";" + description + "\n")
                    file_fict_lock.release()
                    self.local_statistics[index("fictional")] += 1
                    continue
            except:
                pass

            # POPULATION
            population = ""
            try:
                population = (data['entities'][city_id]["claims"]["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            except:
                self.local_statistics[index("no population")] += 1
            
            
            # AREA
            area = ""
            try:
                if ("P2046" in data['entities'][city_id]["claims"]):
                    area = (data['entities'][city_id]["claims"]["P2046"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            except:
                self.local_statistics[index("no area")] += 1



            # MAYOR (P1313)
            try:
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
            except:
                self.local_statistics[index("no mayor")] += 1

            
            
            # COUNTRY
            try:
                if ("P17" in data['entities'][city_id]["claims"]):
                    coun = data['entities'][city_id]["claims"]["P17"][0] #take only the preferred one; assumption: it's the FIRST
                try:
                    couns_file_lock.acquire()
                    file_couns_out.write(str(city_id) + ";"+ str(coun["mainsnak"]["datavalue"]["value"]["id"]+"\n"))
                    couns_file_lock.release()
                except:
                    couns_file_lock.release()
                    self.local_statistics[index("no country")] += 1
            except:
                pass
                
            file_real_lock.acquire()
            file_real_city.write(city_id + ";" + label.replace(";", " ") + ";" + description.replace(";", " ") + ";" + area.replace(";", " ") + ";" + population.replace(";", " ") + "\n")
            file_real_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_real_lock = threading.Lock()
file_fict_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
has_mayor_lock = threading.Lock()
couns_file_lock = threading.Lock()
has_analog_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_death_file_path = "../roles/placeOfDeath.txt"
has_city_location_file_path = "../roles/hasCityLocation.txt"
processed_cities_file_path = "../processed/processedCities.txt"

place_of_birth_file = open(place_of_birth_file_path, 'r')
place_of_death_file = open(place_of_death_file_path, 'r')
has_city_location_file = open(has_city_location_file_path, 'r')
processed_cities_file = open(processed_cities_file_path, 'r')

PoB = set([x.strip().split(";")[1] for x in place_of_birth_file.readlines()[1:]])
PoD = set([x.strip().split(";")[1] for x in place_of_death_file.readlines()[1:]])
locations = set([x.strip().split(";")[1] for x in place_of_death_file.readlines()[1:] if x.strip().split(";")[2] == 'r'])
processed_cities = set([x.strip() for x in processed_cities_file.readlines()[1:]])
cities = list(PoB.union(PoD).union(locations).difference(processed_cities))
place_of_birth_file.close()
place_of_death_file.close()
has_city_location_file.close()
processed_cities_file.close()

if len(cities)==0:
    sys.exit(1)

#FILES OUTPUT PATH
file_real_city_path = "../concepts/RealCity.txt"
file_fictional_city_path = "../concepts/FictionalCity.txt"
file_log_path = "../log/log_City.txt"
file_couns_path = "../roles/hasCountry.txt"
file_has_mayor_path = "../roles/hasMayor.txt"
file_has_analog_path = "../roles/hasAnalog.txt"


#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#SAVING TO FILE
file_log = open(file_log_path, 'a')
file_real_city = open(file_real_city_path, 'a')
file_fictional_city = open(file_fictional_city_path, 'a')
file_couns_out = open(file_couns_path, 'a')
has_mayor_file = open(file_has_mayor_path, 'a')
file_has_analog = open(file_has_analog_path, 'a')

n_results = len(cities)
print("Number of cities: " + str(n_results)+"\n")
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

processed_cities_file = open(processed_cities_file_path, 'a')
for city in cities:
    processed_cities_file.write(city+"\n")
processed_cities_file.close()


#CLOSING OUTPUT FILES
file_real_city.close()
file_fictional_city.close()
file_couns_out.close()
has_mayor_file.close()
file_has_analog.close()
'''
#STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %)")


total_time = time.time() - total_time
print("Total_time:\t"+str(round(total_time,2))+" sec")'''


#STATISTICS REPORTING
file_log.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    file_log.write(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %) \n")

file_log.write("Total_time:\t"+str(round(total_time,2))+" sec" + "\n")
file_log.close()

sys.exit(0)