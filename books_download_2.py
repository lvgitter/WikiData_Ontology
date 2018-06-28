#verify indentation

from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import json
import re

authors_list = []
genre_dict = {} #genre widata id to label

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""SELECT ?book WHERE {
    ?book wdt:P31 wd:Q571
    }
    limit 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print results


print("Number of results: "+ str(len(results["results"]["bindings"])))

for result in results["results"]["bindings"]:
	url = result['book']['value'].replace("/wiki/", "/wikiSpecial:EntityData/") +".json"
	print
	print(url)
	response = requests.get(url)
	data = response.json()
	book_id = url.split(".json")[0].split("/")[-1]

	#LABEL
	print("Label")
	try:
		label = data['entities'][book_id]["labels"]["en"]["value"]
		print (label)
	except:
		print ("-- missing label on wikidata--")

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
	print("Subtitle")
	if ("P1680" in data['entities'][book_id]["claims"]):
		for subtitle in data['entities'][book_id]["claims"]["P1680"]:
	    		print(subtitle["mainsnak"]["datavalue"]["value"]["text"])

	# FIRST LINE
	print("First line")
	if ("P1922" in data['entities'][book_id]["claims"]):
		for fline in data['entities'][book_id]["claims"]["P1922"]:
	    		print(fline["mainsnak"]["datavalue"]["value"]["text"])
	    
	#GENRES
	print("Genres")
	if ("P136" in data['entities'][book_id]["claims"]):
		for genre in data['entities'][book_id]["claims"]["P136"]:
			genre = genre["mainsnak"]["datavalue"]["value"]["id"]
			print (genre)			
	    		#retrieve genre name or retrieve and save it
	    		if genre in genre_dict:
	    			gname = genre_dict[genre]
	    		else:
	    			urlg = "http://www.wikidata.org/wiki/Special:EntityData/" + genre + ".json"
				responseg = requests.get(urlg)
				datag = responseg.json()
				try:
					gname = datag['entities'][genre]["labels"]["en"]["value"]
				except:
					print ("-- missing genre name on wikidata-- ")
	    		genre_dict[genre] = gname
	    		print(gname)
	   
	#ID
	print("Ids")
	if ("P227" in data['entities'][book_id]["claims"]):
		for bid in data['entities'][book_id]["claims"]["P227"]:
	    		print(bid["mainsnak"]["datavalue"]["value"])

