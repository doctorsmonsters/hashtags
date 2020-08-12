import tweepy as tw

consumer_key= [Your consumer key]
consumer_secret= [Your consumer secret]
access_token= [Your access token]
access_token_secret= [Your access token secret]
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def clean_input(tag):
    tag =tag.replace(" ","")
    if tag.startswith('#'):
        return tag[1:].lower()
    else:
        return tag.lower()

def return_all_hashtags(tweets, tag):
    all_hashtags=[]
    for tweet in tweets:
        for word in tweet.split():
            if word.startswith('#') and word.lower() != '#'+tag.lower():
                all_hashtags.append(word.lower())
    return all_hashtags

def get_hashtags(tag):
    search_tag=clean_input(tag)
    tweets = tw.Cursor(api.search,
                q='#'+search_tag,
                lang="en").items(200)
    tweets_list=[]
    for tweet in tweets:
        tweets_list.append(tweet.text)
    all_tags= return_all_hashtags(tweets_list, search_tag)
    frequency={}
    for item in set(all_tags):
        frequency[item]=all_tags.count(item)
    return {k: v for k, v in sorted(frequency.items(),
                key=lambda item: item[1], reverse= True)}

tag =str(input("Please enter your hashtag/text: "))

all_tags = get_hashtags(tag)
for item in all_tags:
    print(item, all_tags[item])
