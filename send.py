from slackclient import SlackClient
import requests

with open("status.txt", "r") as status_file:
    old_status=status_file.read()

r = requests.get('https://www.paizo.com')
if 'undergoing maintenance' in r.text:
    status = "down"
else:
    status = "up"

if status != old_status:
    f = open("status.txt", "w") 
    f.write(status)
    f.close()

    #slack_token = os.environ["SLACK_API_TOKEN"]
    slack_token = 'xoxp-30257646832-48832776913-324809606676-9fda3b03bda33f500baa34f55f004183'
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel="CCDRE8N7Q",
      text="https://www.paizo.com is {} :thumbs{}:".format(status, status)
    )
