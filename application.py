from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, jsonify

import random
import json
import time
import urllib2
import psycopg2
import datetime



application = Flask(__name__)
#execfile('../credentials_DO_NOT_PUSH_TO_REMOTE.py')

global updt
updt = 0

pg_conn = psycopg2.connect("dbname='tweets' user='master' host='tweetsdb.cqsdwi54slnc.us-east-1.rds.amazonaws.com' password='f0rthewin'")
cur = pg_conn.cursor()

#def get_tweets_for_disply():


def get_neg_tweets_for_heatmap():
  neg_query = '''SELECT * FROM processed_tweets_table_sent where cast(sentiment as float) < 0 AND cast(sentiment as float) > -1'''
  #neg_query = '''SELECT * FROM processed_tweets_table_sent '''
  cur.execute(neg_query)
  rows = cur.fetchall()

  neg_json_string = '['
  neg_ts = []
  neg_lat = []
  neg_long = []
  for row in rows:
    neg_ts.append(row[1])
    neg_lat.append(row[3])
    neg_long.append(row[2])
    neg_json_string =  neg_json_string + '[%f, %f],' %(float(row[3]), float(row[2]))
  neg_json_string = neg_json_string[:-1] + ']'
  return(neg_json_string)


def get_pos_tweets_for_heatmap():
  pos_query = '''SELECT * FROM processed_tweets_table_sent where cast(sentiment as float) > 0'''
  cur.execute(pos_query)
  rows = cur.fetchall()

  pos_json_string = '['
  pos_ts = []
  pos_lat = []
  pos_long = []
  for row in rows:
    pos_ts.append(row[1])
    pos_lat.append(row[3])
    pos_long.append(row[2])
    pos_json_string =  pos_json_string + '[%f, %f],' %(float(row[3]), float(row[2]))
  pos_json_string = pos_json_string[:-1] + ']'
  return(pos_json_string)



# @application.route('/new', methods=['POST'])
# def get_new_tweets():
#   if(request.headers.get('x-amz-sns-message-type') is 'SubscriptionConfirmation'):
#     #confirm request
#     url = request.get_json()['SubscribeURL'] #get url from json to confirm
#     urllib2.urlopen(url).read() #send get request
#   elif(request.headers.get('x-amz-sns-message-type') is 'Notification'):
#       #update update
#     update = request.get_json()['Message']
#   else:
#     text = "do nothing!"




def query_three_most_recent_tweets():
  pos_query = '''SELECT tweet_id, tweet_text, timestamp_ms
                    FROM processed_tweets_table_sent
                    ORDER BY timestamp_ms DESC
                    LIMIT 3'''
  cur.execute(pos_query)
  tweets = cur.fetchall()
  return tweets

@application.route('/')
def get_tweets(filter=None):
  tweets = query_three_most_recent_tweets()
  tweets = [
    {'tweet_id':tweets[0][0], 'text':tweets[0][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[0][2])/1000).strftime('%I:%M'), 'lat_long':(73, 38)},
    {'tweet_id':tweets[1][0], 'text':tweets[1][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[1][2])/1000).strftime('%I:%M'),'lat_long':(73, 38)},
    {'tweet_id':tweets[2][0], 'text':tweets[2][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[2][2])/1000).strftime('%I:%M'), 'lat_long':(73, 32)}
  ]
  return render_template('show_tweets.html', tweets=tweets, points_pos=get_pos_tweets_for_heatmap(),points_neg=get_neg_tweets_for_heatmap())




@application.route('/new', methods=['POST'])
def get_new_tweets(update=updt):
  global updt
  if(request.headers.get('x-amz-sns-message-type') is 'SubscriptionConfirmation'):
    #confirm request
    url = request.get_json()['SubscribeURL'] #get url from json to confirm
    urllib2.urlopen(url).read() #send get request
  elif(request.headers.get('x-amz-sns-message-type') is 'Notification'):
    #update update
    updt = request.get_json()['tweets']

  else: #reached via JS from show_tweets.html
    data = request.get_json()
    updt+=1
    if(data==updt):
      return(jsonify(result=False))
    else:
      #get latest 3 tweets and return them
      #3 tweets + update
      #return(jsonify(result=update and 3 tweets))
      tweets = query_three_most_recent_tweets()
      tweets = [
        {'tweet_id':tweets[0][0], 'text':tweets[0][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[0][2])/1000).strftime('%I:%M'), 'lat_long':(73, 38)},
        {'tweet_id':tweets[1][0], 'text':tweets[1][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[1][2])/1000).strftime('%I:%M'),'lat_long':(73, 38)},
        {'tweet_id':tweets[2][0], 'text':tweets[2][1], 'tweet_time':datetime.datetime.fromtimestamp(int(tweets[2][2])/1000).strftime('%I:%M'), 'lat_long':(73, 32)},
        {'tweet_id':-1, 'text':tweets[0][0], 'tweet_time':0, 'lat_long':(0,0)}
      ]
      return(jsonify(result=tweets))

# def get_new_tweets():
#   if(request.headers.get('x-amz-sns-message-type') is 'SubscriptionConfirmation'):
#     #confirm request
#     url = request.get_json()['SubscribeURL'] #get url from json to confirm
#     urllib2.urlopen(url).read() #send get request
#   elif(request.headers.get('x-amz-sns-message-type') is 'Notification'):
#       #update update
#     update = request.get_json()['Message']
#   else:
#     text = "do nothing!"


if __name__ == '__main__':
    update=0
    application.run(debug=True)


datetime.datetime.fromtimestamp(int(tweets[1][2])).strftime('%H:%M:%S')
print(
    datetime.datetime.fromtimestamp(
        int("1284101485")
    ).strftime('%Y-%m-%d %H:%M:%S')
)
1417572523761
1284101485