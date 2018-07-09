import json
with open('oliver_twist_Q164974.json', 'r') as handle:
	parsed = json.load(handle)
print(json.dumps(parsed, indent=4, sort_keys=False))
