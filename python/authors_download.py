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
LEN_INDEX = 13


def index(statistic_name):
    switcher = {
        "no genre": 0,
        "no award": 1,
        "no name":2,
        "no surname":3,
        "no sex":4,
        "no DoB":5,
        "no DoD":6,
        "no occupation":7,
        "no PoB":8,
        "no PoD":9,
        "no influencing author":10,
        "no label":11,
        "no description":12
    }
    return switcher[statistic_name]


def label(statistic_id):
    switcher = {
        0:"no genre",
        1:"no award",
        2:"no name",
        3:"no surname",
        4:"no sex",
        5:"no DoB",
        6:"no DoD",
        7:"no occupation",
        8:"no PoB",
        9:"no PoD",
        10:"no influencing author",
        11:"no label",
        12:"no description"

    }
    return switcher[statistic_id]

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# THREAD DEFINITION
class AuthorDownloadThread(threading.Thread):
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
            if (count % 10 == 0):
                print("[Thread " + str(self.id) + "]\t" + "author " + str(j - self.res_min + 1) + "/" + str(
                    self.res_max - self.res_min))

            author = authors[j]
            url = "https://www.wikidata.org/wiki/Special:EntityData/" + author + ".json"
            for i in range(3):
                try:
                    response = requests.get(url)  # timeout
                    data = response.json()
                    break
                except:
                    print("EXCEPTION " + url)
                    time.sleep(i*0.5)
                    continue
            
            # LABEL
            label = ""
            try:
                label = data['entities'][author]["labels"]["en"]["value"]
                # print(label)
            except:
                # print("-- missing label on wikidata--")
                self.local_statistics[index("no label")] += 1

            # DESCRIPTION
            description = ""
            if ("descriptions" in data['entities'][author]["claims"]):
                if ("en" in data['entities'][author]["claims"]["descriptions"]):
                    description = data['entities'][author]["claims"]["descriptions"]["en"]["value"]
            elif ("descriptions" in data['entities'][author]):
                if ("en" in data['entities'][author]["descriptions"]):
                    description = data['entities'][author]["descriptions"]["en"]["value"]
            else:
                self.local_statistics[index("no description")] += 1

            # NAME
            name = ""
            if ("P1559" in data['entities'][author]["claims"]):
                name = (data['entities'][author]["claims"]["P1559"][0]["mainsnak"]["datavalue"]["value"]["text"])
            elif ("P1477" in data['entities'][author]["claims"]):
                name = (data['entities'][author]["claims"]["P1477"][0]["mainsnak"]["datavalue"]["value"]["text"])
            else:
                name = label
                self.local_statistics[index("no name")] += 1

            # SEX
            sex = ""
            if ("P21" in data['entities'][author]["claims"]):
                try:
                    sex = (data['entities'][author]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
                    if sex == 'Q6581097':
                        sex = 'male'
                    elif sex == 'Q6581072':
                        sex = 'female'
                    else:
                        self.local_statistics[index("no sex")] += 1
                except:
                    self.local_statistics[index("no sex")] += 1

            # DoB
            DoB = ""
            try:
                DoB = data['entities'][author]["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoB")] += 1

            # DoD
            DoD = ""
            try:
                DoD = data['entities'][author]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
            except:
                self.local_statistics[index("no DoD")] += 1

            # PoB
            if ("P19" in data['entities'][author]["claims"]):
                for place in data['entities'][author]["claims"]["P19"]:
                    try:
                        place_of_birth_lock.acquire()
                        place_of_birth_file.write(
                            str(author+";"+place["mainsnak"]["datavalue"]["value"]["id"])+"\n")
                        place_of_birth_lock.release()
                        PoB = place["mainsnak"]["datavalue"]["value"]["id"]
                    except:
                        place_of_birth_lock.release()
            else:
                self.local_statistics[index("no PoB")] += 1

            # PoD
            if ("P20" in data['entities'][author]["claims"]):
                for place in data['entities'][author]["claims"]["P20"]:
                    try:
                        place_of_death_lock.acquire()
                        place_of_death_file.write(
                            str(author+";"+place["mainsnak"]["datavalue"]["value"]["id"])+ "\n")
                        place_of_death_lock.release()
                        PoD=place["mainsnak"]["datavalue"]["value"]["id"]
                    except:
                        place_of_death_lock.release()
            else:
                self.local_statistics[index("no PoD")] += 1

            # OCCUPATION
            if ("P106" in data['entities'][author]["claims"]):
                for occupation in data['entities'][author]["claims"]["P106"]:
                    occupation = occupation["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve occupation name or retrieve and save it
                    if occupation in occupations_dict:
                        occupation_name = occupations_dict[occupation]
                        file_has_occupation.write(author + ";" + occupation_name + "\n")
                    else:
                        for i in range(3):
                            try:
                                urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + occupation + ".json"
                                response_occupation = requests.get(urlg)
                                data_occupation = response_occupation.json()
                                break
                            except:
                                print("EXCEPTION " + urlg)
                                time.sleep(i*0.5)
                                continue

                        try:
                            occupations_dict_lock.acquire()
                            occupation_name = data_occupation['entities'][occupation]["labels"]["en"]["value"]
                            occupations_dict[occupation] = occupation_name
                            file_has_occupation.write(author + ";" + occupation_name + "\n")
                            occupations_dict_lock.release()
                        except:
                            occupations_dict_lock.release()
            else:
                self.local_statistics[index("no occupation")] += 1

            # GENRES
            if ("P136" in data['entities'][author]["claims"]):
                for genre in data['entities'][author]["claims"]["P136"]:
                    genre = genre["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve genre name or retrieve and save it
                    if genre in genre_dict:
                        genres_lock.acquire()
                        gname = genre_dict[genre]
                        file_has_genres.write(author + ";" + gname + "\n")
                        genres_lock.release()
                    else:
                        for i in range(3):
                            try:
                                urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + genre + ".json"
                                responseg = requests.get(urlg)
                                datag = responseg.json()
                                break
                            except:
                                time.sleep(i*0.5)
                                continue
                        try:
                            genres_lock.acquire()
                            gname = datag['entities'][genre]["labels"]["en"]["value"]
                            genre_dict[genre] = gname
                            file_has_genres.write(author+";"+gname+"\n")
                            genres_lock.release()
                        except:
                            genres_lock.release()
            else:
                self.local_statistics[index("no genre")] += 1

            # AWARDS
            if ("P166" in data['entities'][author]["claims"]):
                for award in data['entities'][author]["claims"]["P166"]:
                    award = award["mainsnak"]["datavalue"]["value"]["id"]
                    # retrieve award name or retrieve and save it
                    if award in award_dict:
                        award_name = award_dict[award]
                        awards_dict_lock.acquire()
                        file_has_awards.write(author + ";" + award_name + "\n")
                        awards_dict_lock.release()
                    else:
                        for i in range(3):
                            try:
                                url_award = "http://www.wikidata.org/wiki/Special:EntityData/" + award + ".json"
                                response_award = requests.get(url_award)
                                data_award = response_award.json()
                                break
                            except:
                                time.sleep(i*0.5)
                                continue

                        try:
                            awards_dict_lock.acquire()
                            award_name = data_award['entities'][award]["labels"]["en"]["value"]
                            award_dict[award] = award_name
                            file_has_awards.write(author+";"+award_name+"\n")
                            awards_dict_lock.release()
                        except:
                            awards_dict_lock.release()
            else:
                self.local_statistics[index("no award")] += 1

            # INFLUENCING AUTHORS
            if ("P737" in data['entities'][author]["claims"]):
                for influencing_author  in data['entities'][author]["claims"]["P737"]:
                    try:
                        if influencing_author["mainsnak"]["datavalue"]["value"]["id"] in authors:
                            influenced_by_lock.acquire()
                            influenced_by_file.write(author + ";" + influencing_author["mainsnak"]["datavalue"]["value"]["id"] + "\n")
                            influenced_by_lock.release()
                    except:
                        influenced_by_lock.release()
            else:
                self.local_statistics[index("no PoB")] += 1
            
            # ID

            authors_file.write(str(author)+";"+label+";"+description+";"+name+";"+sex+";"+DoB+";"+DoD+"\n")

    def join(self):
        Thread.join(self)
        return self.local_statistics


# LOCKS
authors_lock = threading.Lock()
influenced_by_lock = threading.Lock()
place_of_birth_lock = threading.Lock()
place_of_death_lock = threading.Lock()
occupations_dict_lock = threading.Lock()
awards_dict_lock = threading.Lock()
genres_lock = threading.Lock()

# TIME MEASUREMENTS
total_time = time.time()

# FILES OUTPUT PATH
authors_file_path = "../concepts/Author.txt"
authors_id_file_path = "../authors.txt"
afterword_authors_id_file_path = "../roles/hasAfterwordAuthor.txt"
foreword_authors_id_file_path = "../roles/hasForewordAuthor.txt"
influenced_by_file_path = "../roles/influencedBy.txt"
place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_death_file_path = "../roles/placeOfDeath.txt"
file_has_awards_path = "../roles/_Author_has_awards.txt"
file_has_genres_path = "../roles/_Author_has_genres.txt"
processed_humans_file_path = "../tmp/processed_humans.txt"
file_has_occupation_path = "../roles/_Human_has_occupation.txt"
has_author_file_path = "../roles/hasAuthor.txt"
log_file_path = "../log/log_Author.txt"


# STATISTICS VARIABLES
statistics = [0 for x in range(LEN_INDEX)]

# DICTIONARIES LOADING
occupations_dict = load_obj("occupations") # occupation wikidata id to label
award_dict = load_obj("awards") # award wikidata id to label
genre_dict = load_obj("genres")

# RETRIEVING ALL AUTHORS WIKIDATA IDs
processed_authors_file_path = "../processed/processedAuthors.txt"
authors_id_file = open(has_author_file_path, 'r')
afterword_authors_id_file = open(afterword_authors_id_file_path, 'r')
foreword_authors_id_file = open(foreword_authors_id_file_path, 'r')
processed_authors_file = open(processed_authors_file_path, 'r')
authors = set([x.strip().split(';')[1] for x in authors_id_file.readlines()[1:]])
authors.union(set([x.strip().split(';')[0] for x in afterword_authors_id_file.readlines()[1:]]))
authors.union(set([x.strip().split(';')[0] for x in foreword_authors_id_file.readlines()[1:]]))
processed_authors = set([x.strip() for x in processed_authors_file.readlines()[1:]])
authors = list(authors.difference(processed_authors))
authors_id_file.close()
afterword_authors_id_file.close()
foreword_authors_id_file.close()
processed_authors_file.close()

if len(authors)==0:
    sys.exit(1)

# OPENING OUTPUT FILES
authors_file = open(authors_file_path, 'a')
influenced_by_file = open(influenced_by_file_path, 'a')
place_of_birth_file = open(place_of_birth_file_path, 'a')
place_of_death_file = open(place_of_death_file_path, 'a')
file_has_awards = open(file_has_awards_path, 'a')
file_has_genres = open(file_has_genres_path, 'a')
file_has_occupation = open(file_has_occupation_path, 'a')
processed_humans_file = open(processed_humans_file_path, 'a')
log_file = open(log_file_path, 'a')


n_authors = len(authors)
print("Number of authors: " + str(n_authors))

# PARALLEL COMPUTATION
threads = []
prec = 0
step = math.ceil(n_authors / N_THREADS)
succ = step
for i in range(N_THREADS):
    threads.append(AuthorDownloadThread(i, min(prec, n_authors), min(succ, n_authors)))
    prec = succ
    succ = succ + step

for t in threads:
    t.start()

for t in threads:
    statistics = [sum(x) for x in zip(statistics, t.join())]


processed_authors_file = open(processed_authors_file_path, 'a')
for author in authors:
    processed_authors_file.write(author+"\n")
processed_authors_file.close()


# CLOSING OUTPUT FILES
authors_file.close()
influenced_by_file.close()
place_of_birth_file.close()
place_of_death_file.close()
file_has_awards.close()
file_has_genres.close()
file_has_occupation.close()
processed_humans_file.close()

# UPDATING DICTIONARIES
save_obj(occupations_dict, 'occupations')
save_obj(award_dict, 'awards')
save_obj(genre_dict, 'genres')

# STATISTICS REPORTING
print("\n\n*** STATISTICS ***\n")
for i in range(len(statistics)):
    print(
        label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(round(statistics[i] / n_authors, 2) * 100) + " %)")

total_time = time.time() - total_time
print("Total_time:\t" + str(round(total_time, 2)) + " sec")

# STATISTICS REPORTING
log_file.write("\n\n*** STATISTICS *** \n")
for i in range(len(statistics)):
    log_file.write(label(i).ljust(16) + ":" + str(statistics[i]) + "  (" + str(
        round(statistics[i] / n_authors, 2) * 100) + " %) \n")

log_file.write("Total_time:\t" + str(round(total_time, 2)) + " sec" + "\n")
log_file.close()

sys.exit(0)