import boto3
import os
import tweepy
import datetime
import json
import yaml
import re
import sys

from base64 import b64decode

def twitter_api_handle(twitter_config):
  auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
  auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
  return tweepy.API(auth)

twitter_config = {}

consumer_key_enc        = os.environ['consumer_key']
consumer_secret_enc     = os.environ['consumer_secret']
access_token_enc        = os.environ['access_token']
access_token_secret_enc = os.environ['access_token_secret']

print "fetching secrets..."
twitter_config['consumer_key']        = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_key_enc))['Plaintext']
twitter_config['consumer_secret']     = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_secret_enc))['Plaintext']
twitter_config['access_token']        = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_enc))['Plaintext']
twitter_config['access_token_secret'] = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_secret_enc))['Plaintext']

def handler(event,context):
    calendar_day = datetime.datetime.today().strftime('%m/%d/')
    #calendar_day = '01/17/'
    print "searching for shows matching: %s" % calendar_day
    day_regex = re.compile(calendar_day)

    print "fetching dark star shows..."
    s3 = boto3.client('s3')
    s3obj = s3.get_object(Bucket='everydarkstar.today', Key='data/shows.json')
    show_list_json = yaml.safe_load(s3obj['Body'].read())

    tweet = ''
    for date_key in sorted(show_list_json.keys(),reverse=True):
        if(day_regex.match(date_key)):
           tweet = date_key + " - " + show_list_json[date_key][0] + "\n" + tweet

    if tweet == '':
        return

    print "tweet: " + tweet
    
    print "setting up twitter api"
    api = twitter_api_handle(twitter_config)
    
    print "sending tweet"
    status = api.update_status(status=tweet) 

