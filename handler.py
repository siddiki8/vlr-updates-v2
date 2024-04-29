import os
import vlrbeta as vlr
import imgen
import tweepy
from dotenv import load_dotenv

load_dotenv('.env')

class Tweet:

    def __init__(self):
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        bearer_token = os.getenv('BEARER_TOKEN')

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret, wait_on_rate_limit=True)

    # rest of your code
    def tweet_match(self, match_link):
        match = vlr.Match(match_link)  # Create a match object
        pic = imgen.Twimage(match).construct_image()  # Generate the image for the match

        # Save the image to a file
        image_path = "temp.png"
        pic.save(image_path)

        # Upload the image to Twitter
        media_id = self.api.media_upload(filename=image_path).media_id_string

        # Tweet the match with the uploaded image
        match_string = str(match)  # Create a string representation of the match
        self.client.create_tweet(text=match_string, media_ids=[media_id])
        print("Tweeted")

        # Remove the image file after tweeting
        os.remove(image_path)
