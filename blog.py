from slackclient import SlackClient
import requests
import os
import json
import configparser

def send_message(msg):
    c = configparser.ConfigParser()
    c.read("config.ini")
    
    #to slack
    slack_token = c["Prod"]["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel="C6U5PLJHE", #paizo
      #channel="C0W7NPCTY", #pathfinder
      #channel="CCEM7951Q", #testrene
      text=msg
    )
    

with open("blog.txt", "r") as blog_file:
    old_date=blog_file.read()

r = requests.get('https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fpaizo.com%2Fcommunity%2Fblog%26xml%3Datom&api_key=beiorasshpurtgmjcyl2glbiywgcfbiap5uvsst8', timeout=5)
latest_blog = r.json()['items'][0]

if latest_blog['pubDate'] != old_date:
    f = open("blog.txt", "w") 
    f.write(latest_blog['pubDate'])
    f.close()
    send_message("New blog: <{}|{}>".format(latest_blog['link'], latest_blog['title']))
