#!/usr/bin/env python3
import tweepy
import json
import time
import ast

print("Starting twitter bot!")

CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

print(api.me().name)

#user = "jplsek"
#print("Sending %s a message!" % user)
#api.send_direct_message(screen_name=user, text="Hello Creator!")
#dms = api.direct_messages()
#print(dms)

def runHelp(user, message=""):
    if (message != ""):
        message = message + ", "

    sendDM(user, message + "The Available commands are: Math")

def sendDM(user, message):
    print("Sending message (to %s): %s" % (user, message))
    api.send_direct_message(user=user, text=message)
    # sleep the script to not spam
    time.sleep(10)

class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connected!")

    def on_disconnect(self, notice):
        print(notice)

    def on_status(self, status):
        status = json.loads(status)
        print(status.keys())

    def on_data(self, status):
        status = json.loads(status)

        if ("direct_message" in status.keys()):
            message = status["direct_message"]["text"].lower()
            user = status["direct_message"]["sender"]["id"]
            print("Message received (from %s): %s" % (str(user), message))

            # don't message myself
            if (user == 829050530928418816):
                print("Dont message myself")
                return

            words = message.split(" ")

            if (words[0] == "help"):
                runHelp(user)
            elif (words[0] == "math"):
                words.remove("math")
                expression = ' '.join(words)
                ret = ""
                try:
                    ret = ast.literal_eval(expression)
                except:
                    ret = "Error evaluating expression!"
                sendDM(user, ret)
            else:
                runHelp(user, "Unknown command")


    def on_error(self, status):
        print(status)

stream = tweepy.Stream(auth, StreamListener())
stream.userstream()
