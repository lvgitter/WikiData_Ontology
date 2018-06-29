# verify indentation
import time

import math
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
import requests


N_THREADS = 12

class myThread (threading.Thread):
   def __init__(self, threadID, a, b):
       threading.Thread.__init__(self)
       self.id = threadID
       self.res_min = a
       self.res_max = b

   def run(self):
        #print("Thread "+str(self.id)+"\t"+"book "+str(self.res_min)+"-->"+str(self.res_max-1))
        for j in range(self.res_min, self.res_max):
            print("Thread "+str(self.id)+"\t"+"book "+str(j-self.res_min+1)+"/"+str(self.res_max-self.res_min))
            result = results["results"]["bindings"][j]
            url = result['book']['value'].replace("/wiki/", "/wikiSpecial:EntityData/") + ".json"
            #print(url)
            #start_time_get = time.time()
            response = requests.get(url)
            data = response.json()
            book_id = url.split(".json")[0].split("/")[-1]
            #end_time_get = time.time()
            #total_get_time += end_time_get - start_time_get
            # LABEL
            #print("Label")
            try:
                label = data['entities'][book_id]["labels"]["en"]["value"]
                #print(label)
            except:
                'print("-- missing label on wikidata--")'
                #without_label +=1

            # DESCRPITION
            #print("Description")
            description = ""
            if ("descriptions" in data['entities'][book_id]["claims"]):
                if ("en" in data['entities'][book_id]["claims"]["descriptions"]):
                    description = data['entities'][book_id]["claims"]["descriptions"]["en"]["value"]
            else:
                'without_description += 1'

            # TITLE
            #print("Title")
            title = ""
            if ("P1476" in data['entities'][book_id]["claims"]):
                title = (data['entities'][book_id]["claims"]["P1476"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                'without_title += 1'

            # AUTHORS
            #print("Author")
            # print(json.dumps(data, indent=4, sort_keys=True))
            if ("P50" in data['entities'][book_id]["claims"]):
                for author in data['entities'][book_id]["claims"]["P50"]:
                    'print(author["mainsnak"]["datavalue"]["value"]["id"])'


            # SUBTITLE
            #print("Subtitle")
            subtitle = ""
            if ("P1680" in data['entities'][book_id]["claims"]):
                subtitle = data['entities'][book_id]["claims"]["P1680"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                'without_subtitle += 1'

            # FIRST LINE
            #print("First line")
            first_line = ""
            if ("P1922" in data['entities'][book_id]["claims"]):
                first_line = data['entities'][book_id]["claims"]["P1922"][0]["mainsnak"]["datavalue"]["value"]["text"]
            else:
                'without_first_line += 1'

            # GENRES
            #print("Genres")
            genres = ""
            if ("P136" in data['entities'][book_id]["claims"]):
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
                            gname = datag['entities'][genre]["labels"]["en"]["value"]
                        except:
                            print("-- missing genre name on wikidata-- ")
                        genres_lock.acquire()
                        genre_dict[genre] = gname
                        genres_lock.release()
                    #print(gname)
                    genres += gname + ","
                genres = genres[0:-1]
            else:
                'without_genre += 1'

            # ID
            #print("Ids")
            id = ""
            if ("P227" in data['entities'][book_id]["claims"]):
                id = data['entities'][book_id]["claims"]["P227"][0]["mainsnak"]["datavalue"]["value"]
                #print(id)
            else:
                'without_id += 1'
            file_out_lock.acquire()
            file_out.write(label + ";" + description + ";" + title + ";" + subtitle + ";" + first_line + ";" + genres + ";" + id+"\n")
            file_out_lock.release()
genres_lock = threading.Lock()
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()


total_get_time=0
total_time=time.time()

file_out_path = "books.txt"
file_log_path = "log.txt"
without_title = without_id =without_description=without_subtitle=without_first_line=without_genre=without_label=0
authors_list = []
genre_dict = {}  #genre widata id to label

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
    limit 500
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


file_out = open(file_out_path, 'w')
#file_log = open(file_log_path, 'w')
#print(results)
n_results = len(results["results"]["bindings"])
print("Number of results: " + str(n_results))

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
    t.join()



file_out.close()
#file_log.close()

#total_time = time.time() - total_time

#print("no title:\t\t"+str(without_title))
#print("no id:\t\t\t"+str(without_id))
#print("no description:\t\t"+str(without_description))
#print("no subtitle:\t\t"+str(without_subtitle))
#print("no first_line:\t\t"+str(without_first_line))
#print("no genre:\t\t\t"+str(without_genre))
#print("total genres:\t\t"+str(len(genre_dict)))
#print(genre_dict.values())
#print("Total_time:\t"+str(total_time))
#print("Total request time: \t"+str(total_get_time))
