# Use with:
# http GET 'http://localhost:5000/policy/defs/admin' Authorization:$TOKEN | python update-policy-templates.py

import sys
import json

response = json.load(sys.stdin)
assert response["result"]["status"]
actions = response["result"]["value"]
boolean_actions = set(key for key, info in actions.items()
                      if "type" not in info or info["type"] == "bool")

# read current superuser template
with open("templates/superuser.json", "r") as f:
    superuser_template = json.load(f)

currently_defined_actions = set(superuser_template["action"].keys())

missing_actions = boolean_actions - currently_defined_actions
print('Missing actions: {}'.format(missing_actions))
print('Add to superuser.json:')
first = True
for action in missing_actions:
    if not first:
        print(',')
    first = False
    print('            "{}": true'.format(action), end='')
print()
