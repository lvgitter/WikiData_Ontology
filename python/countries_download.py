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
        "no population":0,
        "no area":1,
        "no label":2,
        "no description":3,
        "no language":4
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no population",
        1:"no area",
        2:"no label",
        3:"no description",
        4:"no language"
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
                print("[Thread "+str(self.id)+"]\t"+"country "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))

            result = countries[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + result +".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                except:
                    print ("EXCEPTION " + url)
                    time.sleep(0.5)
                    continue
            country_id = result
            
            # LABEL
            label = ""
            try:
                label = data['entities'][country_id]["labels"]["en"]["value"]
            except:
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][country_id]["claims"]):
                if ("en" in data['entities'][country_id]["claims"]["descriptions"]):
                    description = data['entities'][country_id]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][country_id]):
                if ("en" in data['entities'][country_id]["descriptions"]):
                    description = data['entities'][country_id]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # POPULATION
            population = ""
            if ("P1082" in data['entities'][country_id]["claims"]):
                population = (data['entities'][country_id]["claims"]["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            else:
                self.local_statistics[index("no population")] += 1
            
            
            # AREA
            area = ""
            if ("P2046" in data['entities'][country_id]["claims"]):
                area = (data['entities'][country_id]["claims"]["P2046"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
            else:
            	self.local_statistics[index("no area")] += 1

            
            # LANGUAGE
            if ("P37" in data['entities'][country_id]["claims"]):
                for lang in data['entities'][country_id]["claims"]["P37"]:
                    try:
                        langs_file_lock.acquire()
                        file_langs_out.write(
                            str(str(country_id)+";"+lang["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        langs_file_lock.release()
                    except:
                        langs_file_lock.release()
            else:
                self.local_statistics[index("no language")] += 1
                
            file_out_lock.acquire()
            file_out.write(country_id + ";" + label + ";" + description + ";" + area + ";" + population + ";" + "\n")
            file_out_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
langs_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_out_path = "../concepts/Country.txt"
file_log_path = "../log/log_Country.txt"
file_langs_path = "../roles/hasUsedLanguage.txt"

#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#RETRIEVING ALL PUBLISHERs WIKIDATA IDs and QUERY THEM
has_country_location_file_path = "../roles/hasCountryLocation.txt"
has_country_location_file = open(has_country_location_file_path, 'r')
located_in_file_path = "../roles/locatedIn.txt"
located_in_file = open(located_in_file_path, 'r')
processed_countries_file_path = "../processed/processedCountries.txt"
processed_countries_file = open(processed_countries_file_path, 'r')
processed_countries = [x.strip() for x in processed_countries_file.readlines()[1:]]
countries = set([x.strip().split(';')[1] for x in has_country_location_file.readlines()[1:]])
countries = list(set([x.strip().split(';')[1] for x in located_in_file.readlines()[1:]]).union(countries).difference(processed_countries))
has_country_location_file.close()
located_in_file.close()
processed_countries_file.close()

if len(countries)==0:
    sys.exit(1)

#SAVING TO FILE
file_log = open(file_log_path, 'a')
file_out = open(file_out_path, 'a')
file_langs_out = open(file_langs_path, 'a')

n_results = len(countries)

print("Number of countries: " + str(n_results))
file_log.write("Number of countries: " + str(n_results))

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


processed_countries_file = open(processed_countries_file_path, 'a')
for country in countries:
    processed_countries_file.write(country+"\n")
processed_countries_file.close()



#CLOSING OUTPUT FILES
file_out.close()
file_langs_out.close()

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