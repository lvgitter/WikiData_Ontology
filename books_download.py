#pip install sparqlwrapper
#https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import json
import re

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
    limit 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print("Number of results: "+ str(len(results["results"]["bindings"])))

for result in results["results"]["bindings"]:
    url = result['book']['value'].replace("/wiki/", "/wikiSpecial:EntityData/") +".json"
    print(url)
    response = requests.get(url)
    data = response.json()
    book_id = url.split(".json")[0].split("/")[-1]


    # TITLE
    print("Title")
    if ("P1476" in data['entities'][book_id]["claims"]):
        for title in  data['entities'][book_id]["claims"]["P1476"]:
            print(title["mainsnak"]["datavalue"]["value"]["text"])

    #AUTHORS
    print("Author")
    #print(json.dumps(data, indent=4, sort_keys=True))
    if ("P50" in data['entities'][book_id]["claims"]):
        for author in  data['entities'][book_id]["claims"]["P50"]:
            print(author["mainsnak"]["datavalue"]["value"]["id"])



    #SUBTITLE
    print("Title")
    if ("P1476" in data['entities'][book_id]["claims"]):
        for title in data['entities'][book_id]["claims"]["P1476"]:
            print(title["mainsnak"]["datavalue"]["value"]["text"])

    #GENRES

    #ISBN-13 ID