import json
with open('/home/lv/Desktop/Q578895.json', 'r') as handle, open("prettified_json_file.txt", "w") as pp:
	parsed = json.load(handle)
	pp.write(json.dumps(parsed, indent=4, sort_keys=False))
