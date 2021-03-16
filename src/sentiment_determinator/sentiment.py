# -*- coding: utf-8 -*-

import pickle
from abc import ABC
from statistics import mode
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from typing import List


class VoteClassifier(ClassifierI, ABC):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


def prepare(folder: str) -> VoteClassifier:
    open_file = open(f"{folder}/ExtraTreeClassifier.pickle", "rb")
    ExtraTreeClassifier = pickle.load(open_file)
    open_file.close()

    open_file = open(f"{folder}/MNB_classifier5k.pickle", "rb")
    MNB_classifier = pickle.load(open_file)
    open_file.close()

    open_file = open(f"{folder}/ComplementNB_classifier.pickle", "rb")
    ComplementNB_classifier = pickle.load(open_file)
    open_file.close()

    open_file = open(f"{folder}/LogisticRegression_classifier5k.pickle", "rb")
    LogisticRegression_classifier = pickle.load(open_file)
    open_file.close()

    open_file = open(f"{folder}/LinearSVC_classifier5k.pickle", "rb")
    LinearSVC_classifier = pickle.load(open_file)
    open_file.close()

    open_file = open(f"{folder}/SGDC_classifier5k.pickle", "rb")
    SGDC_classifier = pickle.load(open_file)
    open_file.close()

    voted_classifier = VoteClassifier(
        ExtraTreeClassifier,
        LinearSVC_classifier,
        MNB_classifier,
        ComplementNB_classifier,
        LogisticRegression_classifier,
        SGDC_classifier)
    return voted_classifier


def sentiment(text: str, folder_with_pickle: str, keys: List[str]) -> tuple:
    word_features5k_f = open(f"{folder_with_pickle}/word_features5k.pickle", "rb")
    word_features = pickle.load(word_features5k_f)
    word_features5k_f.close()

    def find_features(document):
        words = word_tokenize(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return features

    voted_classifier = prepare(folder_with_pickle)
    temp_text = text
    # print(text)
    # temp_text = scrapper(text, keys)
    feats = find_features(temp_text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

