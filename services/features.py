"""
Runs sentiment analysis on the video transcript as well as the titles of the videos and updates the feature
set files for each video with the sentiment analysis results.
"""

import os
import csv
import ast

from nltk.sentiment import SentimentIntensityAnalyzer

_transcript = 'transcript'
_label = 'label'
_title = 'title'
_keywords = 'keywords'
_seconds = 'seconds'
_sentiment = 'sentiment'
_hashtags = 'hashtags'
_features = 'features'
_title_sentiment = 'title_sentiment'


# ------------ feature set processing ----------------

def get_sentiment(dataset):
    for item in dataset:
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(item[_transcript])
        item[_sentiment] = sentiment
    return dataset


def get_title_sentiment(dataset):
    for item in dataset:
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(item[_title])
        item[_title_sentiment] = sentiment
    return dataset


# ------------ other services ----------------


def read_text_file(pathway, label):
    oldPath = os.getcwd()
    os.chdir(pathway)

    arr = []
    for file in os.listdir():
        dataset = dict()
        if file.endswith(".txt") or file.endswith(".rtf"):
            with open(file, 'r') as f:
                dataset[_title] = file[0:len(file)-4]
                dataset[_transcript] = f.read()
                dataset[_label] = label
                arr.append(dataset)
    os.chdir(oldPath)
    return arr


def read_keyword_file(dataset):
    pathway = 'data/keywords'
    oldPath = os.getcwd()
    os.chdir(pathway)

    for file in os.listdir():
        for item in dataset:
            if file.endswith(".csv") and file[0:len(file)-4] == item[_title]:
                with open(file, 'r', encoding="utf-8-sig") as f:
                    keywords = csv.reader(f)
                    keywords = list(keywords)
                    item[_keywords] = len(keywords)
                break
    os.chdir(oldPath)
    return dataset


def read_features_file(dataset):
    pathway = 'data/features'
    oldPath = os.getcwd()
    os.chdir(pathway)

    for file in os.listdir():
        for item in dataset:
            if file.endswith(".csv") and file[0:len(file)-4] == item[_title]:
                with open(file, 'r', encoding="utf-8-sig") as f:
                    dict_reader = csv.DictReader(f)
                    csv_dict = list(dict_reader)[0]
                    csv_dict = dict(csv_dict)
                    csv_dict[_sentiment] = ast.literal_eval(csv_dict[_sentiment])
                    item.update(csv_dict)
                break
    os.chdir(oldPath)
    return dataset


def update_features_file(dataset):
    for item in dataset:
        file = open('data/features/' + item[_title] + '.csv', 'w')
        writer = csv.writer(file)
        header = [_keywords, _seconds, _hashtags, _sentiment, _title_sentiment]
        writer.writerow(header)
        row = [item[_keywords], item[_seconds], item[_hashtags], item[_sentiment], item[_title_sentiment]]
        # save results to file
        writer.writerow(row)
        file.close()


# ------------ classifier ----------------


def run():
    data_set_true = read_features_file(read_text_file('data/genuine', 'genuine'))
    data_set_false = read_features_file(read_text_file('data/misinformation', 'misinformation'))

    data_set = data_set_true + data_set_false
    # run sentiment analysis
    data_set = get_title_sentiment(data_set)
    # update feature sets
    update_features_file(data_set)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

