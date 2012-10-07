import sys
import ConfigParser
import os
import shelve 
import StringIO 
import requests
from statsd import StatsClient
from twitter import *

#Read in the url from the config file.
sys.path.append(sys.path[0]) 
Config = ConfigParser.ConfigParser()
Config.read("../config.ini")

#Checking previously tweeted number of cups.
database = shelve.open("tmp_storage") 
cups_old = 0

try:
    cups_old = database['cups']
except KeyError:
    print "Temp storage file doesn't exist yet. Will tweet the current value and save it."

print "Previous number of cups was " + str(cups_old)

#Get current number of cups.
service = Config.get("PyCoffeeD", "url")
r = requests.get(service + "/cups")
assert r.status_code < 400, "Request to PyCoffeeD server failed."
cups_current = float(r.text)
print "Current number of cups is " + str(cups_current)

#Send the current number of cups to StatsD.
url = Config.get("StatsD", "url")
port = Config.get("StatsD", "port")
client = StatsClient(host=url, port=int(port), prefix="coffee.")
client.gauge("cups", value=cups_current, rate=1)

#Tweet the current number of cups, if it's changed significantly since the last tweet.
if (abs(cups_current - cups_old) > 1):
    print ("More than one cup difference between " + str(cups_current) 
        + " and " + str(cups_old) + ". Tweeting an update.")

    consumer_key = Config.get("Twitter", "consumer_key")
    consumer_secret = Config.get("Twitter", "consumer_secret")
    app_name = Config.get("Twitter", "app_name")

    twitter_creds = os.path.expanduser('./twitter_credentials')
    if not os.path.exists(twitter_creds):
        oauth_dance(app_name, consumer_key, consumer_secret,
                    twitter_creds)

    oauth_token, oauth_secret = read_token_file(twitter_creds)

    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    twitter.statuses.update(status="There are " + str(cups_current) + " cups of coffee left.")

    #Save the current number of cups to a file.
    database['cups'] = cups_current


