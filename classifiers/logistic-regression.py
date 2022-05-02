"""
Runs the logistic regression classifier. Must manually adjust features added to feature set for each run.
"""
import os
import datetime
import csv
import ast

from nltk.classify import accuracy
from sklearn.model_selection import train_test_split
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

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


def build_labeled_feature_set(dataset):
    classified_dataset = []
    for item in dataset:
        featureset = dict()
        featureset[_keywords] = item[_keywords]
        # featureset[_seconds] = item[_seconds]
        featureset[_hashtags] = item[_hashtags]
        featureset[_sentiment] = item[_sentiment]['neg']
        # featureset[_sentiment] = item[_sentiment]['neu']
        # featureset[_sentiment] = item[_sentiment]['pos']
        # featureset[_sentiment] = item[_sentiment]['compound']
        # featureset[_title_sentiment] = item[_title_sentiment]['neg']
        # featureset[_title_sentiment] = item[_title_sentiment]['neu']
        featureset[_title_sentiment] = item[_title_sentiment]['pos']
        # featureset[_title_sentiment] = item[_title_sentiment]['compound']
        #   1. number of MeSH terms generated by video transcript
        #   2. number of seconds in the video
        #   transcript sentiment analysis scores:
        #      3. negative sentiment
        #      4. positive sentiment
        #      5. neutral sentiment
        #      6. compound sentiment
        #   7. number of hashtags associated with video
        #   title sentiment analysis scores:
        #      8. negative sentiment
        #      9. positive sentiment
        #      10. neutral sentiment
        #      11. compound sentiment
        item[_features] = (featureset, item[_label])
        classified_dataset.append(item)
    return classified_dataset


def build_unlabeled_features(dataset):
    return dataset[0]


def strip_dataset(dataset):
    stripped = []
    for item in dataset:
        stripped.append(item[_features])
    return stripped


# ------------ other services ----------------


def read_text_file(pathway, label):
    oldPath = os.getcwd()
    os.chdir(pathway)

    arr = []
    for file in os.listdir():
        dataset = dict()
        if file.endswith(".txt") or file.endswith(".rtf"):
            with open(file, 'r') as f:
                dataset[_title] = file
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
            if file.endswith(".csv") and file[0:len(file)-4] == item[_title][0:len(item[_title])-4]:
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
            if file.endswith(".csv") and file[0:len(file) - 4] == item[_title][0:len(item[_title]) - 4]:
                with open(file, 'r', encoding="utf-8-sig") as f:
                    dict_reader = csv.DictReader(f)
                    csv_dict = list(dict_reader)[0]
                    csv_dict = dict(csv_dict)
                    csv_dict[_sentiment] = ast.literal_eval(csv_dict[_sentiment])
                    csv_dict[_title_sentiment] = ast.literal_eval(csv_dict[_title_sentiment])
                    item.update(csv_dict)
                break
    os.chdir(oldPath)
    return dataset


# ------------ classifier ----------------


def run_classifier():
    # read feature set files
    data_set_true = read_features_file(read_text_file('data/genuine', 'genuine'))
    data_set_false = read_features_file(read_text_file('data/misinformation', 'misinformation'))

    # label data
    data_set_true = build_labeled_feature_set(data_set_true)
    data_set_false = build_labeled_feature_set(data_set_false)

    data_set = data_set_true + data_set_false

    train_data, test_data = train_test_split(data_set, test_size=0.8, random_state=42)
    # training data should be 20%, testing data should be 80%,
    #   param test_size refers to testing data size

    classifier = SklearnClassifier(LogisticRegression(C=1000))

    # train classifier using training data
    train_data_only = strip_dataset(train_data)
    classifier.train(train_data_only)

    test_data_only = strip_dataset(test_data)  # still contains labels

    print('Accuracy:')
    result_accuracy = accuracy(classifier, test_data_only)
    print(result_accuracy)

    file = open('results/lr/results_' + str(datetime.datetime.utcnow()) + '.csv', 'w')
    writer = csv.writer(file)
    header = [_label, 'result', _title]
    writer.writerow(header)

    for item in test_data:
        # clean test data, should contain unlabeled features
        unlabeled_data_set = build_unlabeled_features(item[_features])
        # classify test data
        result = classifier.classify(unlabeled_data_set)
        row = [item[_label], result, item[_title]]
        # save results to file
        writer.writerow(row)
    row = ['Accuracy: ', result_accuracy]
    writer.writerow(row)
    row = ['Features: ', test_data[0][_features][0].keys()]
    writer.writerow(row)

    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_classifier()

