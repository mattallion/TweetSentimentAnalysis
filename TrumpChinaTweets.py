import tweepy
from datetime import datetime, timedelta

auth = tweepy.OAuthHandler("", "")                                      #enter your tweepy authentication
auth.set_access_token("", "")                                           #enter your tweepy authentication
api = tweepy.API(auth)

searchTerm = "China"                                                    #change the searchTerm to analyze sentiment of different tweets
screenName = 'realDonaldTrump'                                          #enter a screenName of desired account

now = datetime.today().now()
print(now)
prev = now-timedelta(days=2)                                            #restricts search to past 2 days
print(prev)

tweets = []
for tweet in tweepy.Cursor(api.user_timeline,
                           screen_name = screenName,
                           tweet_mode = "extended").items(200):         #takes the most recent 200 tweets
    tweet.created_at=tweet.created_at-timedelta(hours=4)
    if tweet.created_at < prev:
        break
    elif searchTerm in tweet.full_text.lower():
        tweets.append(tweet)

if not tweets:
    print(str(screenName) + " has not tweeted about " + str(searchTerm) + " in the past 2 days.")
    exit()

tweetCount = 1
for tweet in tweets:
    print("TWEET #" + str(tweetCount))
    print(tweet.full_text)
    print("Tweeted at: " + str(tweet.created_at))
    print("")
    tweetCount += 1

sentimentScore = 0

posWords = open("positive-words.txt", "r")
pos = posWords.readlines()
for line in pos:
    line = line.strip()
    line = line.replace(" ", "")
    for tweet in tweets:
        if (" " + str(line)+ " ") in tweet.full_text.lower():
            print("POSITIVE: " + str(line))
            sentimentScore += 1
        elif (" " + str(line)+ ".") in tweet.full_text.lower():
            print("POSITIVE: " + str(line))
            sentimentScore += 1
        elif (" " + str(line)+ ",") in tweet.full_text.lower():
            print("POSITIVE: " + str(line))
            sentimentScore += 1
        else:
            firstLetter = line[0:1]
            firstLetter = firstLetter.upper()
            firstWord = firstLetter + line[1:len(line)]
            if (str(firstWord) + " ") in tweet.full_text:
                print("POSITIVE: " + str(firstWord))
                sentimentScore += 1

negWords = open("negative-words.txt", "r")
neg = negWords.readlines()
for line in neg:
    line = line.strip()
    line = line.replace(" ", "")
    for tweet in tweets:
        if (" " + str(line)+" ") in tweet.full_text.lower():
            print("NEGATIVE: " + str(line))
            sentimentScore -= 1
        elif (" " + str(line)+".") in tweet.full_text.lower():
            print("NEGATIVE: " + str(line))
            sentimentScore -= 1
        elif (" " + str(line)+",") in tweet.full_text.lower():
            print("NEGATIVE: " + str(line))
            sentimentScore -= 1
        else:
            firstLetter = line[0:1]
            firstLetter = firstLetter.upper()
            firstWord = firstLetter + line[1:len(line)]
            if (str(firstWord) + " ") in tweet.full_text:
                print("NEGATIVE: " + str(firstWord))
                sentimentScore -= 1

if sentimentScore > 0:
    print(str(screenName) + "'s tone has been positive about " + str(searchTerm) + " in the past 2 days.")
    print("Sentiment Score: +" + str(sentimentScore))

elif sentimentScore < 0:
    print(str(screenName) + "'s tone has been negative about " + str(searchTerm) + " in the past 2 days.")
    print("Sentiment Score: " + str(sentimentScore))

else:
    print(str(screenName) + "'s tone has been neutral about " + str(searchTerm) + " in the past 2 days.")
    print("Sentiment Score: " + str(sentimentScore))
