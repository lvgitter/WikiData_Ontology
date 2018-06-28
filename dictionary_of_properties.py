import pickle
d = {}
with open("all_properties_ids_to_name.csv") as ap:
	for line in ap:
		pid = line.split(",")[0].split("/")[-1]
		pname = line.rstrip().split(",")[1]
		d[pname] = pid
for k in d:
	print k + " -> " + d[k]
pickle.dump( d, open( "dictionary_of_properties_name_to_id.p", "wb" ) )
