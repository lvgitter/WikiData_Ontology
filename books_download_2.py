import time
import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random

N_THREADS = 16
LEN_INDEX = 16

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
        "no id":8,
        "no pub":9,
        "no char":10,
        "no loc":11,
        "no afterauthor":12,
        "no foreauthor":13,
        "no lang":14,
        "no ill":15
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
        8:"no id",
        9:"no pub",
        10:"no char",
        11:"no loc",
        12:"no afterauthor",
        13:"no foreauthor",
        14:"no lang",
        15:"no ill"
        
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
            if (count%10 == 0): #to modify?
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
            
            
            # PUBLISHERS
            if ("P123" in data['entities'][book_id]["claims"]):
                for pub in data['entities'][book_id]["claims"]["P123"]:
                    try:
                        pubs_file_lock.acquire()
                        file_pubs_out.write(str(pub["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        pubs_file_lock.release()
                    except:
                        pubs_file_lock.release()
            else:
                self.local_statistics[index("no pub")] += 1
            
            # LOCATIONS
            if ("P840" in data['entities'][book_id]["claims"]):
                for loc in data['entities'][book_id]["claims"]["P840"]:
                    try:
                        locs_file_lock.acquire()
                        file_locs_out.write(str(loc["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        locs_file_lock.release()
                    except:
                        locs_file_lock.release()
            else:
                self.local_statistics[index("no loc")] += 1
                
           # CHARACTERS
            if ("P674" in data['entities'][book_id]["claims"]):
                for loc in data['entities'][book_id]["claims"]["P674"]:
                    try:
                        chars_file_lock.acquire()
                        file_chars_out.write(str(loc["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        chars_file_lock.release()
                    except:
                        chars_file_lock.release()
            else:
                self.local_statistics[index("no char")] += 1
                
                
           	# ILLUSTRATORS (HUMANS)
            if ("P110" in data['entities'][book_id]["claims"]):
                for ill in data['entities'][book_id]["claims"]["P110"]:
                    try:
                        ills_file_lock.acquire()
                        file_ills_out.write(str(ill["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        ills_file_lock.release()
                    except:
                        ills_file_lock.release()
            else:
                self.local_statistics[index("no ill")] += 1
           	

            # AUTHORS
            if ("P50" in data['entities'][book_id]["claims"]):
                for author in data['entities'][book_id]["claims"]["P50"]:
                    try:
                        authors_file_lock.acquire()
                        file_authors_out.write(str(author["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        authors_file_lock.release()
                    except:
                        authors_file_lock.release()
            else:
                self.local_statistics[index("no author")] += 1
                
                
            # FOREAUTHORS
            if ("P2679" in data['entities'][book_id]["claims"]):
                for foreauthor in data['entities'][book_id]["claims"]["P2679"]:
                    try:
                        foreauthors_file_lock.acquire()
                        file_foreauthors_out.write(str(foreauthor["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        foreauthors_file_lock.release()
                    except:
                        foreauthors_file_lock.release()
            else:
                self.local_statistics[index("no foreauthor")] += 1
                
            # AFTERAUTHORS
            if ("P2680" in data['entities'][book_id]["claims"]):
                for afterauthor in data['entities'][book_id]["claims"]["P2680"]:
                    try:
                        afterauthors_file_lock.acquire()
                        file_afterauthors_out.write(str(afterauthor["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        afterauthors_file_lock.release()
                    except:
                        afterauthors_file_lock.release()
            else:
                self.local_statistics[index("no afterauthor")] += 1

			# LANGUAGE
            if ("P407" in data['entities'][book_id]["claims"]):
                for lang in data['entities'][book_id]["claims"]["P407"]:
                    try:
                        langs_file_lock.acquire()
                        file_langs_out.write(str(lang["mainsnak"]["datavalue"]["value"]["id"])+","+str(book_id)+"\n")
                        langs_file_lock.release()
                    except:
                        langs_file_lock.release()
            else:
                self.local_statistics[index("no lang")] += 1


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

            # GENRES
            genres = ""
            if ("P136" in data['entities'][book_id]["claims"]):
                for genre in data['entities'][book_id]["claims"]["P136"]:
                    genre = genre["mainsnak"]["datavalue"]["value"]["id"]
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
                    genres += gname + ","
                genres = genres[0:-1]
            else:
                self.local_statistics[index("no genre")] += 1

            # ID
            id = ""
            if ("P212" in data['entities'][book_id]["claims"]):
                id = data['entities'][book_id]["claims"]["P212"][0]["mainsnak"]["datavalue"]["value"]
            else:
                self.local_statistics[index("no id")] += 1
            file_out_lock.acquire()
            file_out.write(book_id + ";" + label + ";" + description + ";" + title + ";" + subtitle + ";" + first_line + ";" + genres + ";" + id+"\n")
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
pubs_file_lock = threading.Lock()
locs_file_lock = threading.Lock()
chars_file_lock = threading.Lock()
afterauthors_file_lock = threading.Lock()
foreauthors_file_lock = threading.Lock()
langs_file_lock = threading.Lock()
ills_file_lock = threading.Lock()


#TIME MEASUREMENTS
total_time=time.time()

#FILES OUTPUT PATH
file_out_path = "books.txt"
file_log_path = "log.txt"
file_authors_path = "authors.txt" # format wikidata:author_id,wikidata:book_id
file_pubs_path = "publishers.txt"
file_locs_path = "locations.txt"
file_chars_path = "characters.txt"
file_afterauthors_path = "afterauthors.txt"
file_foreauthors_path = "foreauthors.txt"
file_langs_path = "languages.txt"
file_ills_path = "illustrators.txt"

#STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

#GENRE CONVERSION
genre_dict = {}  #genre widata id to label

#RETRIEVING ALL BOOKS WIKIDATA IDs
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
    LIMIT 400
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#SAVING TO FILE
file_out = open(file_out_path, 'w')
file_out.write("book_id" + ";" + "label" + ";" + "description" + ";" + "title" + ";" + "subtitle" + ";" + "first_line" + ";" + "genres" + ";" + "id" + "\n")
file_authors_out=open(file_authors_path, 'w')
file_authors_out.write( "author_id" + "book_id" + "\n")
file_pubs_out=open(file_pubs_path, 'w')
file_pubs_out.write("publisher_id" + "book_id" + "\n")
file_locs_out=open(file_locs_path, 'w')
file_locs_out.write( "location_id" + "book_id" + "\n")
file_chars_out=open(file_chars_path, 'w')
file_chars_out.write( "character_id" + "book_id" + "\n")
file_afterauthors_out=open(file_afterauthors_path, 'w')
file_afterauthors_out.write( "afterauthor_id" + "book_id" + "\n")
file_foreauthors_out=open(file_foreauthors_path, 'w')
file_foreauthors_out.write( "foreauthor_id" + "book_id" +"\n")
file_langs_out=open(file_langs_path, 'w')
file_langs_out.write( "language_id" + "book_id" + "\n")
file_ills_out=open(file_ills_path, 'w')
file_ills_out.write( "illustror_id" + "book_id" + "\n")
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
file_pubs_out.close()
file_afterauthors_out.close()
file_foreauthors_out.close()
file_chars_out.close()
file_locs_out.close()
file_ills_out.close()
#file_log.close()


#STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(label(i).ljust(16)+":"+str(statistics[i])+"  ("+str(round(statistics[i]/n_results,2)*100)+" %)")


total_time = time.time() - total_time
print("Total_time:\t"+str(round(total_time,2))+" sec")
