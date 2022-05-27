"""
Encodes all the raw transcripts in base64.
"""

import os
import csv
import ast

import base64

_transcript = 'transcript'
_label = 'label'
_title = 'title'
_keywords = 'keywords'
_seconds = 'seconds'
_sentiment = 'sentiment'
_hashtags = 'hashtags'
_features = 'features'
_title_sentiment = 'title_sentiment'


# ------------ other services ----------------


def read_text_file(pathway, label):
    oldPath = os.getcwd()
    os.chdir(pathway)

    arr = []
    for file in os.listdir():
        dataset = dict()
        if file.endswith(".txt"):
            with open(file, 'r') as f:
                dataset[_title] = file[0:len(file)-4]
                dataset[_transcript] = f.read()
                dataset[_label] = label
                arr.append(dataset)
    os.chdir(oldPath)
    return arr


def encode_text_file(dataset, pathway):
    for item in dataset:
        file = open(pathway + '/' + item[_title] + '.txt', 'w+')
        transcript = item[_transcript]
        base64_str = base64.b64encode(transcript.encode('utf-8', 'backslashreplace'))
        base64_str = base64_str.decode('utf-8', 'backslashreplace')
        file.write(base64_str)
        file.close()


# ------------ classifier ----------------


def run():
    true_pathway = 'data/genuine'
    false_pathway = 'data/misinformation'
    data_set_true = read_text_file(true_pathway, 'genuine')
    data_set_false = read_text_file(false_pathway, 'misinformation')

    # base 64 encode then put back in file
    encode_text_file(data_set_true, true_pathway)
    encode_text_file(data_set_false, false_pathway)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

