"""
This script can be used to update the superuser policy template.

It reads the response of privacyIDEA's /policy/defs/admin endpoint from stdin
and checks if it contains any boolean rights that are missing in the current
superuser template. If this is the case, it prints all rights that should be
added to the superuser template.

Use with:
$ http GET 'http://localhost:5000/policy/defs/admin' Authorization:$TOKEN | python update-superuser-template.py

Example output:
    Missing actions: {'eventhandling_read', 'resolverread', 'periodictask_read',
    'smtpserver_read', 'policyread', 'privacyideaserver_read', 'configread',
    'smsgateway_read', 'radiusserver_read', 'mresolverread', 'tokenlist'}
    Add to superuser.json:
                "eventhandling_read": true,
                "resolverread": true,
                "periodictask_read": true,
                "smtpserver_read": true,
                "policyread": true,
                "privacyideaserver_read": true,
                "configread": true,
                "smsgateway_read": true,
                "radiusserver_read": true,
                "mresolverread": true,
                "tokenlist": true
"""
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
if missing_actions:
    print('Add to superuser.json:')
    first = True
    for action in missing_actions:
        if not first:
            print(',')
        first = False
        print('            "{}": true'.format(action), end='')
    print()
