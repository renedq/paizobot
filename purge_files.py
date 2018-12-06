from slackclient import SlackClient
import requests
import os
import json
import configparser

c = configparser.ConfigParser()
c.read("config.ini")

slack_token = c["Prod"]["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

filelist = sc.api_call(
        "files.list"
    )

count_text=0;
count_del=0

for f in list(filelist.items())[1][1]:
    if f['name'].endswith(".txt") or 'pinned_to' in f:
        count_text+=1
        print("Keeping {}".format(f['name']))
    else:
        print("Deleting {}".format(f['name']))
        r = sc.api_call(
                "files.delete",
                file=f['id']
            )
        print(r)
        count_del+=1

print("Kept {} text or pinned files".format(count_text))
print("Deleted {} files".format(count_del))
