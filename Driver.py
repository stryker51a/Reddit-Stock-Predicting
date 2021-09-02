#! python3

import praw
import csv
import re

# Follow the instructions here:
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# to get your personal_use_script, secret, and name. You will pick the name yourself
# This: https://ssl.reddit.com/prefs/apps/ is the website where you can create your
# project and find the different strings.
# Then, you just need to enter your username and password for a reddit account.

personal_use_script = ''
secret = ''
name = ''
reddit_username = ''
reddit_password = ''


reddit = praw.Reddit(client_id=personal_use_script, \
                     client_secret=secret, \
                     user_agent=name, \
                     username=reddit_username, \
                     password=reddit_password)

wallStreetBets = reddit.subreddit('wallstreetbets')

for submission in wallStreetBets.hot(limit=10):
    print(submission.title, submission.id)


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

regex = re.compile('[^a-zA-Z!.?/ 0-9?$%=+]')
#First parameter is the replacement, second parameter is your input string
#regex.sub('', 'ab3d*E')
#Out: 'abdE'

with open('test2.csv', 'w', newline='') as csvfile:

    fieldnames = ['id', 'body', 'score']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for submission in wallStreetBets.hot(limit=1):

        print(submission.id)
        print(submission.title)
        print(submission.num_comments)

        submission.comments.replace_more(limit=None)  # important line

        for comment in submission.comments.list():

            edited_comment = emoji_pattern.sub(r'', comment.body)
            edited_comment = edited_comment.replace(r'/', ' ')
            edited_comment = regex.sub(r'', edited_comment)

            print(comment.created_utc)

            writer.writerow({'id': comment.id, 'body': edited_comment, 'score': comment.score})


csvfile.close()


