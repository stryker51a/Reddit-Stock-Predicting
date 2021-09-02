import csv
import re
import sys
import enchant

# def is_similar(word, name)

d = enchant.Dict("en_US")

f = open("dictionary.txt", "r")

word_set = set([])

for word in f:

    word_set.add(word.replace('\n', '').lower())

f.close()

f2 = open("stocktickers.txt", "r")

regex = re.compile('[^a-zA-Z ]')

stock_dict = {}
company_dict = {}

for line in f2:
    stock = line.split(" - ")
    stock_dict[stock[0].lower()] = regex.sub(r'', stock[1].replace('\n', '').lower())
    company_dict[regex.sub(r'', stock[1].replace('\n', '').lower())] = stock[0].lower()

f2.close()

common_words = set([])

f3 = open("common_words.txt", "r")

for line in f3:
    common_words.add(line.replace('\n', ''))

f3.close()

stock_resuts = {}

stock_resuts_with_score = {}

with open('test2.csv', 'r', newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        comment = regex.sub(r'', row['body'])

        words = comment.split(" ")

        for word in words:
            x = word.lower()
            if word == '' or x in common_words:
                continue

            if x in stock_dict:
                if x in stock_resuts:
                    stock_resuts[x] = stock_resuts[x] + 1
                    stock_resuts_with_score[x] = stock_resuts_with_score[x] + int(row['score'])
                else:
                    stock_resuts[x] = 1
                    stock_resuts_with_score[x] = int(row['score'])
            elif x in company_dict:
                ticker = company_dict[x]
                if ticker in stock_resuts:
                    stock_resuts[ticker] = stock_resuts[ticker] + 1
                    stock_resuts_with_score[ticker] = stock_resuts_with_score[ticker] + int(row['score'])
                else:
                    stock_resuts[ticker] = 1
                    stock_resuts_with_score[ticker] = int(row['score'])

            # elif not d.check(x):
            #     for sug in d.suggest(x):
            #         if sug in stock_dict:
            #             if sug in stock_resuts:
            #                 stock_resuts[sug] = stock_resuts[sug] + 1
            #             else:
            #                 stock_resuts[sug] = 1
            #             break
            #         elif sug in company_dict:
            #             ticker = company_dict[sug]
            #             if ticker in stock_resuts:
            #                 stock_resuts[ticker] = stock_resuts[ticker] + 1
            #             else:
            #                 stock_resuts[ticker] = 1
            #             break


csvfile.close()

print(stock_resuts)

for stock in stock_resuts_with_score:
    print(str(stock_dict[stock]) + " (" + str(stock) + "): " + str(stock_resuts_with_score[stock]))

print(stock_resuts_with_score)
