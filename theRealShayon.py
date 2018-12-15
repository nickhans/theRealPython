import twitter
import Generator
import subprocess
import time

# get twitter login
credential_file = open('credentials.txt', 'r')
credentials = credential_file.readlines()

CONSUMER_KEY = credentials[0].strip()
CONSUMER_SECRET = credentials[1].strip()
ACCESS_TOKEN = credentials[2].strip()
ACCESS_TOKEN_SECRET = credentials[3].strip()

tweet = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

# get delay time
delay_input = input("Tweet Delay (mins): ")
print('')
delay = int(delay_input) * 60
# print(delay)

g = Generator.Generator()
g.populate("Shayon.txt")
g.set_probability()

while (True):
    while (True):
        generated_sentence = g.generate_sentence()
        if (len(generated_sentence) <= 280):
            break

    print("Tweet: " + generated_sentence)

    # check if generated sentence has already been tweeted
    try:
        # tweet.PostUpdate(generated_sentence)
        print("\nTweet Tweeted.\n")
        time.sleep(delay)
    except twitter.error.TwitterError as err:
        print(err)
        print("\nTweet Failed, Generating New Tweet\n")
