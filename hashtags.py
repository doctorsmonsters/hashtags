import tweepy as tw
import re
import bs4
import requests
import json

consumer_key= [Your consumer key]
consumer_secret= [Your consumer secret]
access_token= [Your access token]
access_token_secret= [Your access token secret]
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def clean_input(tag):
    tag = tag.replace(" ", "")
    if tag.startswith('#'):
        return tag[1:].lower()
    else:
        return tag.lower()


def return_all_hashtags(tweets, tag):
    all_hashtags = []
    for tweet in tweets:
        for word in tweet.split():
            if word.startswith('#') and word.lower() != '#' + tag.lower():
                all_hashtags.append(word.lower())
    return all_hashtags

def extract_shared_data(doc):
    for script_tag in doc.find_all("script"):
        if script_tag.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\._sharedData = ", "", script_tag.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
            return shared_data

def get_hashtags(tag):
    search_tag = clean_input(tag)
    tweets = tw.Cursor(api.search,
                       q='#' + search_tag,
                       lang="en").items(200)
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(tweet.text)

    url_string = "https://www.instagram.com/explore/tags/%s/" % search_tag
    response = bs4.BeautifulSoup(requests.get(url_string).text, "html.parser")

    shared_data = extract_shared_data(response)
    media = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']

    captions = []
    for post in media:
        if post['node']['edge_media_to_caption']['edges'] != []:
            captions.append(post['node']['edge_media_to_caption']['edges'][0]['node']['text'])

    all_tags = return_all_hashtags(tweets_list + captions, tag)
    frequency = {}
    for item in set(all_tags):
        frequency[item] = all_tags.count(item)
    return {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}

tag =str(input("Please enter your hashtag/text: "))

all_tags = get_hashtags(tag)
for item in all_tags:
    print(item, all_tags[item])
