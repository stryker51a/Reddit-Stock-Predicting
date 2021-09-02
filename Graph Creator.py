import praw
import csv, codecs
import re
import time
import matplotlib.pyplot as plt
import threading

BLOCK_SIZE = 300
exitFlag = 0
need_csv_file = False

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


class myThread(threading.Thread):
    def __init__(self, threadID, name, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.filename = filename

    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.filename)
        print("Exiting " + self.name)


def process_data(threadName, filename):
    thread_stream = wallStreetBets.stream.comments(skip_existing=True)
    thread_fieldnames = ['id', 'tickers', 'score', 'group']
    while not exitFlag:
        csvLock.acquire(False)
        with open(filename, 'a', newline='') as thread_csvfile:
            thread_writer = csv.DictWriter(thread_csvfile, fieldnames=thread_fieldnames)
            for thread_comment in thread_stream:

                thread_edited_comment = emoji_pattern.sub(r'', thread_comment.body)
                thread_edited_comment = thread_edited_comment.replace(r'/', ' ')
                thread_edited_comment = just_letters.sub(r'', thread_edited_comment)

                thread_words = thread_edited_comment.split(" ")

                thread_tickers_list = ''

                for thread_potential_word in thread_words:
                    thread_word = thread_potential_word.lower()
                    if thread_word == '' or thread_word in common_words:
                        continue

                    if thread_word in stock_dict:
                        thread_tickers_list = thread_tickers_list + thread_word + " "
                        tickers_list_Lock.acquire(True)
                        all_tickers.add(thread_word)
                        tickers_list_Lock.release()
                    elif thread_word in company_dict:
                        thread_tickers_list = thread_tickers_list + company_dict[thread_word] + " "
                        tickers_list_Lock.acquire(True)
                        all_tickers.add(company_dict[thread_word])
                        tickers_list_Lock.release()

                time_created2 = thread_comment.created_utc

                if len(thread_tickers_list) != 0 and time_created2 > EARLIEST_TIME:
                    thread_writer.writerow({'id': thread_comment.id,
                                            'tickers': thread_tickers_list[0: len(thread_tickers_list) - 1],
                                            'score': thread_comment.score,
                                            'group': get_group_number(time_created2)})

                if need_csv_file:
                    break

        thread_csvfile.close()
        csvLock.release()
        time.sleep(1)


def get_group_number(cur_time):
    return int((cur_time - EARLIEST_TIME) / BLOCK_SIZE)


def add_to_graph(x2, y2, num):
    while len(x2) <= num:
            size = len(x2)
            x2.append(size)
            y2.append(0)

    y2[num] = y2[num] + 1

f = open("dictionary.txt", "r")

word_set = set([])

for word in f:
    word_set.add(word.replace('\n', '').lower())

f.close()

f2 = open("stocktickers.txt", "r")

just_letters = re.compile('[^a-zA-Z ]')

stock_dict = {}
company_dict = {}

for line in f2:
    stock = line.split(" - ")
    stock_dict[stock[0].lower()] = just_letters.sub(r'', stock[1].replace('\n', '').lower())
    company_dict[just_letters.sub(r'', stock[1].replace('\n', '').lower())] = stock[0].lower()

f2.close()

common_words = set([])

f3 = open("common_words.txt", "r")

for line in f3:
    common_words.add(line.replace('\n', ''))

f3.close()

start_time = time.time()
EARLIEST_TIME = start_time - float(24 * 60 * 60)

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

regex = re.compile('[^a-zA-Z!.?/ 0-9?$%=+]')

all_tickers = set()

with open('comment_list.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'tickers', 'score', 'group']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for submission in wallStreetBets.hot(limit=1):

        print(submission.id)
        print(submission.title)
        print(submission.num_comments)

        submission.comments.replace_more(limit=None)  # important line and takes a while

        for comment in submission.comments.list():

            edited_comment = emoji_pattern.sub(r'', comment.body)
            edited_comment = edited_comment.replace(r'/', ' ')
            edited_comment = just_letters.sub(r'', edited_comment)

            words = edited_comment.split(" ")

            tickers_list = ''

            for potential_word in words:
                word = potential_word.lower()
                if word == '' or word in common_words:
                    continue

                if word in stock_dict:
                    tickers_list = tickers_list + word + " "
                    all_tickers.add(word)
                elif word in company_dict:
                    tickers_list = tickers_list + company_dict[word] + " "
                    all_tickers.add(company_dict[word])

            time_created = comment.created_utc

            if len(tickers_list) != 0 and time_created > EARLIEST_TIME:
                writer.writerow({'id': comment.id, 'tickers': tickers_list[0: len(tickers_list) - 1],
                                 'score': comment.score, 'group': get_group_number(time_created)})

csvfile.close()

csvLock = threading.Lock()
tickers_list_Lock = threading.Lock()

thread = myThread(1, "Thread-1", 'comment_list.csv')

print("Here are the list of potential stock tickers to choose from: ")
for tick in all_tickers:
    print(tick)

thread.start()

done = False

while not done:

    chosen_ticker = input("What ticker would you like to look at: ")
    if chosen_ticker == done:
        break

    need_csv_file = True
    csvLock.acquire(True)

    x = list([])
    y = list([])

    times = 0

    with open('comment_list.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tick_list = row['tickers'].split(" ")
            if chosen_ticker in tick_list:
                group_num = int(row['group'])
                add_to_graph(x, y, group_num)
                times = times + 1

    print(times)
    csvfile.close()
    need_csv_file = False
    csvLock.release()

    # plotting the points
    plt.plot(x, y, color='green', linestyle='solid', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=10)

    # setting x and y axis range
    plt.ylim(0, 50)
    plt.xlim(0, 400)

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title('Some cool customizations!')

    # function to show the plot
    plt.show()

exitFlag = 1
