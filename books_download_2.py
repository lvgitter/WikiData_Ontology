import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16

def index(statistic_name):
    switcher = {
        "no title":0,
        "no label":1,
        "no description":2,
        "no author":3,
        "multiple author":4,
        "no genre":5,
        "no subtitle":6,
        "no first line":7,
        "no id":8
    }
    return switcher[statistic_name]

def label(statistic_id):
    switcher = {
        0:"no title",
        1:"no label",
        2:"no description",
        3:"no author",
        4:"multiple author",
        5:"no genre",
        6:"no subtitle",
        7:"no first line",
        8:"no id"
    }
    return switcher[statistic_id]


#THREAD DEFINITION
class myThread (threading.Thread):

   def __init__(self, threadID, a, b):
       threading.Thread.__init__(self)
       self.id = threadID
       self.res_min = a
       self.res_max = b
       self.local_statistics = [0 for x in range(9)]

   def run(self):
        count=0
        for j in range(self.res_min, self.res_max):
            time.sleep(random.random()*0.5)
            count += 1
            if (count%100 != 0): #to modify
                print("[Thread "+str(self.id)+"]\t"+"book "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))


            result = results["results"]["bindings"][j]
            url = result['book']['value'].replace("/wiki/", "/wikiSpecial:EntityData/") + ".json"
            #start_time_get = time.time()
            response = requests.get(url) #timeout
            data = response.json()
            book_id = url.split(".json")[0].split("/")[-1]
            #print("[Thread " + str(self.id) + "]\t" + "book " + str(book_id))
            #end_time_get = time.time()
            #total_get_time += end_time_get - start_time_get
            # LABEL
            label = ""
            try:
                label = data['entities'][book_id]["labels"]["en"]["value"]
                #print(label)
            except:
                #print("-- missing label on wikidata--")
                self.local_statistics[index("no label")] += 1

            # DESCRPITION
            #print("Description")
            description = ""
            if ("descriptions" in data['entities'][book_id]["claims"]):
                if ("en" in data['entities'][book_id]["claims"]["descriptions"]):
                    #print("[Thread " + str(self.id) + "]\t"+"description")
                    description = data['entities'][book_id]["claims"]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # TITLE
            #print("Title")
            title = ""
            if ("P1476" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "title")
                title = (data['entities'][book_id]["claims"]["P1476"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                self.local_statistics[index("no title")] += 1

            # AUTHORS
            #print("Author")
            # print(json.dumps(data, indent=4, sort_keys=True))
            if ("P50" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "author")
                for author in data['entities'][book_id]["claims"]["P50"]:
                    try:
                        authors_file_lock.acquire()
                        file_authors_out.write(str(author["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        authors_file_lock.release()
                        #print(author["mainsnak"]["datavalue"]["value"]["id"])
                    except:
                        authors_file_lock.release()
                        #print("[Thread " + str(self.id) + "]"+ "problem author")
            else:
                #print("[Thread " + str(self.id) + "]" + "no author")
                self.local_statistics[index("no author")] += 1



            # SUBTITLE
            #print("Subtitle")
            subtitle = ""
            if ("P1680" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "subtitle")
                subtitle = data['entities'][book_id]["claims"]["P1680"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                self.local_statistics[index("no subtitle")] += 1

            # FIRST LINE
            #print("First line")
            first_line = ""
            if ("P1922" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "first line")
                first_line = data['entities'][book_id]["claims"]["P1922"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                self.local_statistics[index("no first line")] += 1

            # GENRES
            #print("Genres")
            genres = ""
            if ("P136" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "genres")
                for genre in data['entities'][book_id]["claims"]["P136"]:
                    genre = genre["mainsnak"]["datavalue"]["value"]["id"]
                    #print(genre)
                    # retrieve genre name or retrieve and save it
                    if genre in genre_dict:
                        gname = genre_dict[genre]
                    else:
                        urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + genre + ".json"
                        responseg = requests.get(urlg)
                        datag = responseg.json()
                        try:
                            genres_lock.acquire()
                            gname = datag['entities'][genre]["labels"]["en"]["value"]
                            genre_dict[genre] = gname
                            genres_lock.release()
                        except:
                            genres_lock.release()
                            #print("-- missing genre name on wikidata-- ")

                    #print(gname)
                    genres += gname + ","
                genres = genres[0:-1]
            else:
                self.local_statistics[index("no genre")] += 1

            # ID
            #print("Ids")
            id = ""
            if ("P227" in data['entities'][book_id]["claims"]):
                #print("[Thread " + str(self.id) + "]\t" + "id")
                id = data['entities'][book_id]["claims"]["P227"][0]["mainsnak"]["datavalue"]["value"]
                #print(id)
            else:
                self.local_statistics[index("no id")] += 1
            file_out_lock.acquire()
            file_out.write(label + ";" + description + ";" + title + ";" + subtitle + ";" + first_line + ";" + genres + ";" + id+"\n")
            file_out_lock.release()

   def join(self):
       Thread.join(self)
       return self.local_statistics

#LOCKS
genres_lock = threading.Lock()
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
authors_file_lock = threading.Lock()

#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_out_path = "books.txt"
file_log_path = "log.txt"
file_authors_path = "authors.txt" # format wikidata:book_id, wikidata:author_id

#STATISTICS VARIABLES
statistics = [0 for x in range(9)]
authors_list = []
genre_dict = {}  #genre widata id to label

#RETRIEVING ALL BOOKS WIKIDATA IDs
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


file_out = open(file_out_path, 'w')
file_authors_out=open(file_authors_path, 'w')
#file_log = open(file_log_path, 'w')
#print(results)
n_results = len(results["results"]["bindings"])
print("Number of results: " + str(n_results))

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
file_authors_out.close()
#file_log.close()


#STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %)")


total_time = time.time() - total_time
print("Total_time:\t"+str(round(total_time,2))+" sec")
