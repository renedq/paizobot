from slackclient import SlackClient
import requests
import os
import time
import json
import configparser
import twitter

def send_message(msg):
    c = configparser.ConfigParser()
    c.read("config.ini")
    
    #to slack
    slack_token = c["Prod"]["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel="CCDRE8N7Q", #pathfinder
      #channel="CCEM7951Q", #testrene
      text=msg
    )
    
    #to twitter @paizobot
    api = twitter.Api (consumer_key = c["Prod"]["CONS_API_KEY"],
                       consumer_secret = c["Prod"]["CONS_API_SEC_KEY"],
                       access_token_key = c["Prod"]["ACCESS_TOKEN"],
                       access_token_secret = c["Prod"]["ACCESS_TOKEN_SECRET"]) 
    #try:
    api.PostUpdate(msg)
    #except Exception as err:
    #    print(err.message)

with open("status.txt", "r") as status_file:
    old_status=status_file.read()

r = requests.get('https://www.paizo.com', timeout=5)

if r.status_code != 200:
    status = "super broke"
elif 'maintenance</title>' in r.text.lower():
    status = "down"
else:
    status = "up"

file_time = os.path.getmtime('status.txt')
current_time = time.time()
diff_time = current_time - file_time

if status != old_status:
    f = open("status.txt", "w") 
    f.write(status)
    f.close()
    send_message("Oh SHIT! https://www.paizo.com is {}".format(status, status))
elif int(diff_time) > 60*60*24 and (status == 'down' or status == 'super broke'):
    i = requests.get("https://insult.mattbas.org/api/insult.json")
    insult = i.json()['insult']
    send_message("https://www.paizo.com is still {}. {}".format(status, insult))
    f = open("status.txt", "w") 
    f.write(status)
    f.close()

