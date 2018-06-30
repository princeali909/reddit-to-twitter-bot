import praw
import tweepy
import time
import os


# Place your Twitter API keys here
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

#Here is the max amount of characters we can put in a tweet
tweet_max_char = 240
#Here is the amount of characters a shortlink takes up
shortlink_max_char = 24

#Subreddit we are trying to extraxt posts from (no need to add the r/ in the beggining)
subreddit_to_watch = ''

#Every reddit post has an ID, here we want to store these ID's in a .txt file to avoid tweeting the same post twice.
posted_reddit_ids = 'example.txt'

#Duration your bot will wait before tweeting again in seconds
time_between_tweets = 


def setup_connection_reddit(subreddit):
    '''Connects to Reddit API'''
    print('[bot] Setting up connection with reddit')
    reddit_api = praw.Reddit(user_agent = 'Twitter Bot'.format(subreddit),
                              client_id = '', client_secret = '')
    return reddit_api.subreddit(subreddit)


def shorten_title(title,character_count):
    '''Shortens title if too long so that it will fit into a tweet'''
    if len(title) >= character_count:
        return title[:character_count - 1] + '…'
    else:
        return title


def tweet_creator(subreddit_info):
    '''Goes through posts on reddit and extracts a shortened link, title & ID'''
    post_links = [] #list to store our links
    post_titles = [] #list to store our titles
    post_ids = [] #list to store our id's
    print("[bot] extracting posts from sub-reddit")

    for submission in subreddit_info.new(limit=5):
        if not already_tweeted(submission.id):
            post_titles.append(submission.title)
            post_links.append(submission.shortlink)
            post_ids.append(submission.id)

        else:
            print("Already Tweeted")
    return post_links, post_titles, post_ids


def record_id(id):
    '''Logs reddit post ID's into our .txt file'''
    with open(posted_reddit_ids, 'a') as f:
        f.write(str(id)+ '\n')


def already_tweeted(id):
    '''reads through our .txt file and determines if tweet has already been posted'''
    found = 0
    with open(posted_reddit_ids, 'r') as f:
        for line in f:
            if id in line:
                found = 1
                break
    return found



def tweeter(post_links,post_titles,post_ids):
    '''Tweets our reddit posts'''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    for post_title, post_link, post_id in zip(post_titles, post_links, post_ids):
        extra_text = ' ' + post_link #space needed to seperate the link and the title
        post_text = shorten_title(post_title, tweet_max_char - shortlink_max_char - 1) + extra_text
        print('[bot] Posting this tweet to Twitter:')
        print(post_text)
        api.update_status(status = post_text)
        time.sleep(time_between_tweets)
        record_id(post_id)




def main():
    '''Main function'''
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(posted_reddit_ids):
        with open(posted_reddit_ids, 'w'):
            pass

    subreddit = setup_connection_reddit(subreddit_to_watch)
    post_links, post_titles, post_ids = tweet_creator(subreddit)
    tweeter(post_links, post_titles, post_ids)

if __name__ == '__main__':
    main()
