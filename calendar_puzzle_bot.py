import tweepy
from time import sleep

BOT_CONSUMER_KEY = '6B6DIWP08RxVQReZrj5p7fWNT'
BOT_CONSUMER_SECRET = 'CP68nP2vpqyNhca8v6uGAOYRXspmP4JYkCexYv3CQG8G9YqJe6'

BOT_ACCESS_TOKEN = '1472264006786236425-xYn1QtFhjG5J91bKfcYBUaCUa3zBZY'
BOT_ACCESS_TOKEN_SECRET = 'jhnBsk4KOTvpsVHZnPMTVFYl1zW8I7Cd0S3QXAX4nq2F3'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(BOT_CONSUMER_KEY, BOT_CONSUMER_SECRET)
auth.set_access_token(BOT_ACCESS_TOKEN, BOT_ACCESS_TOKEN_SECRET)

# Create API object

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

filename = 'Dec/19/Dec-19_000.png'
message = "1 of 59 solutions for today"
media = api.media_upload(filename)
sleep(10)
api.update_status(message, media_ids = [media.media_id])


c = 0

