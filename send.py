from slackclient import SlackClient
import requests
import os
import time

def send_message(msg):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel="CCDRE8N7Q", #pathfinder
      #channel="CCEM7951Q", #testrene
      text=msg
    )

with open("status.txt", "r") as status_file:
    old_status=status_file.read()

r = requests.get('https://www.paizo.com')

if 'undergoing maintenance' in r.text:
    status = "down"
else:
    status = "up"

file_time = os.path.getmtime('status.txt')
current_time = time.time()
diff_time = current_time - file_time

if status != old_status:
    send_message("Oh SHIT! https://www.paizo.com is {} :thumbs{}:".format(status, status))
    f = open("status.txt", "w") 
    f.write(status)
    f.close()
elif int(diff_time) > 3600 and status == 'down':
    send_message("https://www.paizo.com is still down. Typical amirite?")
    f = open("status.txt", "w") 
    f.write(status)
    f.close()

