import tweepy

from setting import *
from dataAnalysis import *

def twitterNotification(mag, startStr):
    msg = ""
    if(startStr.find("TEST") != -1):
        msg = "[QUAKTEST]Message for test purpose."
    elif (mag >= 5.5):
        msg = "[QUAKWARNING]Take cover now! Strong shake possible."
    elif (mag >= 4.5):
        msg = "[QUAKWATCH]Medium shake possible."
    elif (mag >= 1.0):
        msg = "[QUAKEADVISORY]Gentle Shake Possible."

    if (mag >= 1.0 or startStr.find("TEST") != -1):
        timeSent = UTCDateTime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg += "SLA station magnitude: " + str(mag) + ". Event time: " + startStr + "."
        msg += "Alert Time: " + timeSent + "UTC."
        msg += "©IEWS Alpha v0.1"

        tweetQuakeinfo(msg)

        ########################################################
        #  tweetQuakeinfo: set everything at /* setting.py */  #
        ########################################################

def tweetQuakeinfo(msg):
    # Set up OAuth and integrate with API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Write a tweet to push to our Twitter account
    tweet = msg
    api.update_with_media("latest_CI.SLA..BHZ.png", status=tweet)
    print("tweet complete")