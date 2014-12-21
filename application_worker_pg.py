    #change to application when pulling to new repo
from flask import Flask
from flask import copy_current_request_context
import boto
import boto.sqs
import boto.sns
import boto.dynamodb
import random
import json
import time
from alchemyapi import AlchemyAPI
import sys
import psycopg2
import pdb

app = Flask(__name__)

execfile('../credentials_DO_NOT_PUSH_TO_REMOTE.py')

def run():
    pg_conn = psycopg2.connect("dbname='tweets' user='master' host='tweetsdb.cqsdwi54slnc.us-east-1.rds.amazonaws.com' password='f0rthewin'")
    cur = pg_conn.cursor()
    #I was having difficulty executing the below from the python script so I will now just do it
    # directly in the db, before runing this

    # print ('creating table for tweets...')
    # try:
    #     cur.execute('''
    #         CREATE TABLE processed_tweets(
    #             tweet_id            text,
    #             timestamp_ms        bigint,
    #             coordinate_1    float,
    #             coordinate_2    float,
    #             sentiment       float,
    #             tweet_topic     text
    #         );
    #     ''')
    #     print ('Table created!')
    # except:
    #     print ('Just kidding, table already exists')
    #postgres setup



    #sqs setup
    conn2 = boto.sqs.connect_to_region("us-east-1", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    my_queue = conn2.get_queue('myqueue')
    print ('SQS setup')
    #sns setup
    conn3 = boto.sns.connect_to_region("us-east-1", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    topicname = "tweets"
    try:
        topicarn = conn3.create_topic("tweets")
        #do this here!!!!!
        #subscription = c.subribe(topicarn, "http", "http://localhost/new")
    except:
        #conn3.delete_topic("tweets")
        #topicarn = conn3.create_topic("tweets")
        topicarn = "arn:aws:sns:us-east-1:336679410093:tweets"
    print ('SNS setup')

    #alchemy stuff
    alchemyapi = AlchemyAPI()
    #pdb.set_trace()

    num = 0

    while(True):
        time.sleep(10) #10 second intervals
        rs = my_queue.get_messages(num_messages=10,message_attributes=['.*'])
        print "processing\n"
        for tweet in rs:
            print tweet.message_attributes
            print type(tweet.message_attributes['tweet_topic']['string_value'])
            text = tweet.message_attributes['text']['string_value']


            try:
                response = alchemyapi.sentiment("text", text)
                #print (response)
                sentiment_score = response['docSentiment']['score']
                #sentiment_score = random.uniform(-1, 1)
            except:
                sentiment_score = -99

            #store tweet here
            try:
                cur.execute(
                    """INSERT INTO processed_tweets_table_sent (tweet_id, timestamp_ms, coordinate_1, coordinate_2, tweet_text, sentiment, tweet_topic)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                        (str(tweet.message_attributes['id']['string_value']),
                        str(tweet.message_attributes['timestamp_ms']['string_value']),
                        str(tweet.message_attributes['coordinate1']['string_value']),
                        str(tweet.message_attributes['coordinate2']['string_value']),
                        str(tweet.message_attributes['text']['string_value']),
                        str(sentiment_score),
                        str(tweet.message_attributes['tweet_topic']['string_value'])
                        )
                )
                print("~~~ write worked~~~")
            except:
                print("something wrong!!!!")
                # cur.execute(
                #     """INSERT INTO processed_tweets_table (tweet_id, timestamp_ms, tweet_text, sentiment, tweet_topic)
                #         VALUES (%s, %s, %s, %s, %s);""",
                #         (str(tweet.message_attributes['id']['string_value']),
                #         str(tweet.message_attributes['timestamp_ms']['string_value']),
                #         str(tweet.message_attributes['text']['string_value']),
                #         str(sentiment_score),
                #         str(tweet.message_attributes['tweet_topic']['string_value'])
                #         )
                # )
            #delete from queue
            my_queue.delete_message(tweet)
            pg_conn.commit()



if __name__ == "__main__":
    run()



