import time
import math

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
from threading import Thread
import requests
import random
import pickle

N_THREADS = 16
LEN_INDEX = 16


def index(statistic_name):
    switcher = {
        "no title": 0,
        "no label": 1,
        "no description": 2,
        "no author": 3,
        "multiple author": 4,
        "no genre": 5,
        "no subtitle": 6,
        "no first line": 7,
        "no character": 8,
        "no loc": 9,
        "no afterauthor": 10,
        "no foreauthor": 11,
        "no lang": 12,
        "no editions": 13,
        "no series": 14,
        "no follower": 15
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0: "no title",
        1: "no label",
        2: "no description",
        3: "no author",
        4: "multiple author",
        5: "no genre",
        6: "no subtitle",
        7: "no first line",
        8: "no character",
        9: "no loc",
        10: "no afterauthor",
        11: "no foreauthor",
        12: "no lang",
        13: "no editions",
        14: "no series",
        15: "no follower"

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
            if (count % 100 == 0):
                print("[Thread " + str(self.id) + "]\t" + "book " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            url = "https://www.wikidata.org/wiki/Special:EntityData/"+books[j]+".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                    break
                except:
                    print("EXCEPTION " + url)
                    time.sleep(0.5)
                    continue
            book_id = books[j]
            # LABEL
            label = ""
            try:
                label = data['entities'][book_id]["labels"]["en"]["value"]
            except:
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
            title = label
            if ("P1476" in data['entities'][book_id]["claims"]):
                title = (data['entities'][book_id]["claims"]["P1476"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                self.local_statistics[index("no title")] += 1


            # LOCATIONS
            if ("P840" in data['entities'][book_id]["claims"]):
                for loc in data['entities'][book_id]["claims"]["P840"]:
                    loc = loc["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve loc name or retrieve and save it
                    if loc in locations_dict:
                        if locations_dict[loc] == "real city":
                            locations_lock.acquire()
                            file_has_city_location.write(book_id + ";" + loc + ";r\n")
                            locations_lock.release()
                        elif locations_dict[loc] == "fictional city":
                            locations_lock.acquire()
                            file_has_city_location.write(book_id + ";" + loc + ";f\n")
                            locations_lock.release()
                        elif locations_dict[loc] == "country":
                            locations_lock.acquire()
                            file_has_genres.write(book_id + ";" + loc+ "\n")
                            locations_lock.release()
                    else:
                        url_loc = "http://www.wikidata.org/wiki/Special:EntityData/" + loc + ".json" #INSTANCE OF
                        response_loc = requests.get(url_loc)
                        data_loc = response_loc.json()

                        instances_of_location = []
                        if "P31" in data_loc['entities'][loc]["claims"]:
                            for instance in data_loc['entities'][loc]["claims"]["P31"]:
                                instances_of_location.append(instance["mainsnak"]["datavalue"]["value"]["id"])
                            try:
                                if "Q515" in instances_of_location:
                                    locations_lock.acquire()
                                    locations_dict[loc] = "real city"
                                    file_has_city_location.write(book_id + ";" + loc + ";r\n")
                                    locations_lock.release()
                                elif "Q1964689" in instances_of_location:
                                    locations_lock.acquire()
                                    locations_dict[loc] = "fictional city"
                                    file_has_city_location.write(book_id + ";" + loc + ";f\n")
                                    locations_lock.release()
                                elif "Q6256" in instances_of_location:
                                    locations_lock.acquire()
                                    locations_dict[loc] = "country"
                                    file_has_country_location.write(book_id + ";" + loc + "\n")
                                    locations_lock.release()
                            except:
                                locations_lock.release()
            else:
                self.local_statistics[index("no loc")] += 1

            # CHARACTERS
            if ("P674" in data['entities'][book_id]["claims"]):
                for loc in data['entities'][book_id]["claims"]["P674"]:
                    try:
                        chars_file_lock.acquire()
                        file_chars_out.write(
                            str(book_id + ";"+ loc["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        chars_file_lock.release()
                    except:
                        chars_file_lock.release()
            else:
                self.local_statistics[index("no character")] += 1

            # AUTHORS
            if ("P50" in data['entities'][book_id]["claims"]):
                for author in data['entities'][book_id]["claims"]["P50"]:
                    try:
                        authors_file_lock.acquire()
                        file_authors_out.write(
                            str(book_id + ";" + author["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
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
                        file_foreauthors_out.write(
                            str(book_id + foreauthor["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
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
                        file_afterauthors_out.write(
                            str(book_id+";"+afterauthor["mainsnak"]["datavalue"]["value"]["id"]) +"\n")
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
                        file_langs_out.write(
                            str(book_id + ";"+lang["mainsnak"]["datavalue"]["value"]["id"]) + "\n")
                        langs_file_lock.release()
                    except:
                        langs_file_lock.release()
            else:
                self.local_statistics[index("no lang")] += 1

            # EDITION
            if ("P747" in data['entities'][book_id]["claims"]):
                for edit in data['entities'][book_id]["claims"]["P747"]:
                    try:
                        edits_file_lock.acquire()
                        file_edits_out.write(
                            str(book_id+";"+edit["mainsnak"]["datavalue"]["value"]["id"])+"\n")
                        edits_file_lock.release()
                    except:
                        edits_file_lock.release()
            else:
                self.local_statistics[index("no editions")] += 1

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

            # SERIES
            series_name = ""
            if ("P179" in data['entities'][book_id]["claims"]):
                for ser in data['entities'][book_id]["claims"]["P179"]:
                    se = ser["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve genre name or retrieve and save it
                    if se in series_dict:
                        series_name = series_dict[se]
                    else:
                        urls = "http://www.wikidata.org/wiki/Special:EntityData/" + se + ".json"
                        responses = requests.get(urls)
                        datas = responses.json()
                        try:
                            series_lock.acquire()
                            series_name = datas['entities'][se]["labels"]["en"]["value"]
                            series_dict[se] = series_name
                            series_lock.release()
                        except:
                            series_lock.release()
            else:
                self.local_statistics[index("no series")] += 1

            if (series_name != ""):
                if ("qualifiers" in ser and "P156" in ser['qualifiers']):
                    try:
                        foll = ser['qualifiers']["P156"][0]["datavalue"]["value"]["id"]
                    except:
                        continue
                    try:
                        folls_file_lock.acquire()
                        file_folls_out.write(str(book_id) + ";"+ str(foll) + "\n")
                        folls_file_lock.release()
                    except:
                        folls_file_lock.release()
            else:
                self.local_statistics[index("no follower")] += 1

            # GENRES
            if ("P136" in data['entities'][book_id]["claims"]):
                for genre in data['entities'][book_id]["claims"]["P136"]:
                    genre = genre["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve genre name or retrieve and save it
                    if genre in genre_dict:
                        gname = genre_dict[genre]
                        genres_lock.acquire()
                        file_has_genres.write(book_id + ";" + gname + "\n")
                        genres_lock.release()
                    else:
                        urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + genre + ".json"
                        responseg = requests.get(urlg)
                        datag = responseg.json()
                        try:
                            genres_lock.acquire()
                            gname = datag['entities'][genre]["labels"]["en"]["value"]
                            genre_dict[genre] = gname
                            file_has_genres.write(book_id+";"+gname+"\n")
                            genres_lock.release()
                        except:
                            genres_lock.release()
            else:
                self.local_statistics[index("no genre")] += 1

            file_out_lock.acquire()
            file_out.write(
                book_id + ";" + label + ";" + description + ";" + title + ";" + subtitle + ";" + first_line + ";" + series_name + "\n")
            file_out_lock.release()

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
genres_lock = threading.Lock()
series_lock = threading.Lock()
locations_lock = threading.Lock()
file_out_lock = threading.Lock()
file_log_lock = threading.Lock()
statistics_lock = threading.Lock()
authors_file_lock = threading.Lock()
has_city_location_file_lock = threading.Lock()
has_country_location_file_lock = threading.Lock()
chars_file_lock = threading.Lock()
afterauthors_file_lock = threading.Lock()
foreauthors_file_lock = threading.Lock()
langs_file_lock = threading.Lock()
tras_file_lock = threading.Lock()
has_character_lock = threading.Lock()
edits_file_lock = threading.Lock()
folls_file_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
file_out_path = "../concepts/Book.txt"
file_log_path = "../log/log_Book.txt"
file_authors_path = "../roles/hasAuthor.txt"  # format wikidata:author_id,wikidata:book_id
file_has_city_location_path = "../roles/hasCityLocation.txt"
file_has_country_location_path = "../roles/hasCountryLocation.txt"
file_chars_path = "../roles/hasCharacter.txt"
file_afterauthors_path = "../roles/hasAfterwordAuthor.txt"
file_foreauthors_path = "../roles/hasForewordAuthor.txt"
file_langs_path = "../roles/writtenIn.txt"
file_tras_path = "../roles/hasTranslator.txt"
#file_has_characters_path = "../hasCharacter.txt"
file_edits_path = "../roles/hasEdition.txt"
file_folls_path = "../roles/follows.txt"
file_has_genres_path = "../roles/_Book_has_genres.txt"


# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# GENRE CONVERSION

try:
    genre_dict = load_obj("genres")
except:
    genre_dict = {}

# SERIES NAMES

try:
    series_dict = load_obj("series")
except:
    series_dict = {}

try:
    locations_dict = load_obj("locations")
except:
    locations_dict = {}


# RETRIEVING ALL BOOKS WIKIDATA IDs
processed_books_file_path = "../processed/processedBooks.txt"
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
    LIMIT 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

processed_books_file = open(processed_books_file_path, 'r')
processed_books = set([x.strip() for x in processed_books_file.readlines()[1:]])
books = set([x["book"]["value"].split('/')[-1] for x in results["results"]["bindings"]])
books = list(books.difference(processed_books))

if len(books)==0:
    sys.exit(1)

# SAVING TO FILE
file_log = open(file_log_path, 'a')
file_out = open(file_out_path, 'a')
file_authors_out = open(file_authors_path, 'a')
file_has_city_location = open(file_has_city_location_path, 'a')
file_has_country_location = open(file_has_country_location_path, 'a')
file_chars_out = open(file_chars_path, 'a')
file_afterauthors_out = open(file_afterauthors_path, 'a')
file_foreauthors_out = open(file_foreauthors_path, 'a')
file_langs_out = open(file_langs_path, 'a')
file_edits_out = open(file_edits_path, 'a')
file_folls_out = open(file_folls_path, 'a')
file_has_genres = open(file_has_genres_path, 'a')
file_processed_books = open(processed_books_file_path, 'a')


n_results = len(results["results"]["bindings"])

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

for book in books:
    file_processed_books.write(book+"\n")

# CLOSING OUTPUT FILES
file_out.close()
file_authors_out.close()
file_afterauthors_out.close()
file_foreauthors_out.close()
file_chars_out.close()
file_has_city_location.close()
file_has_country_location.close()
file_edits_out.close()
file_folls_out.close()
file_has_genres.close()
file_has_genres.close()
file_processed_books.close()
save_obj(genre_dict, "genres")
save_obj(series_dict, "series")
save_obj(locations_dict, "locations")

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

sys.exit(0)