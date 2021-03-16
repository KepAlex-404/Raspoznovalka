# -*- coding: utf-8 -*-

import csv
import pickle
import random
from string import punctuation
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.svm import LinearSVC
from sklearn.tree import ExtraTreeClassifier
from textblob import TextBlob
from transliterate import translit

nltk.download('punkt')
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')

mystem = Mystem()
eng_stopwords = stopwords.words("english")
min_acc = 90

# move this up heres
all_words = []
documents = []

#  j is adject, r is adverb, and v is verb
# allowed_word_types = ["J","R","V"]
allowed_word_types = ['A', 'V', 'S']
p, n, nt = 0, 0, 0


def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token
              not in eng_stopwords
              and token != " "
              and token.strip() not in punctuation]
    text = " ".join(tokens)
    return text


with open('training.1600000.processed.noemoticon.csv', 'r', newline='', encoding='latin-1') as f:
    spam = csv.reader(f, delimiter=',')
    try:
        for i, row in enumerate(spam):
            print(row[0], row[5])
            row[5] = preprocess_text(row[5])

            if row[0] == '0':
                documents.append((row[5], "neg"))
                words = nltk.word_tokenize(row[5], language='english')
                pos = nltk.pos_tag(words, lang='eng')
                for w in pos:
                    if w[1][0] in allowed_word_types:
                        all_words.append(w[0].lower())
                        n += 1

            elif row[0] == '4':
                documents.append((row[5], "pos"))
                words = nltk.word_tokenize(row[5], language='english')
                pos = nltk.pos_tag(words, lang='eng')
                for w in pos:
                    if w[1][0] in allowed_word_types:
                        all_words.append(w[0].lower())
                        p += 1

    except Exception as e:
        print(i, e)
print(p, n)

save_documents = open("algos/documents.pickle", "wb")
pickle.dump(documents, save_documents)
save_documents.close()
all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:int(len(all_words)*0.5)]

save_word_features = open("algos/word_features5k.pickle", "wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


def find_features(document):
    words = word_tokenize(document, language='english')
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)
print(len(featuresets))

training_set = featuresets[:int(len(featuresets)*0.8)]
print(training_set)
testing_set = featuresets[int(len(featuresets)*0.8):]
print(testing_set)
classifier = nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(15)


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

save_classifier = open("algos/MNB_classifier5k.pickle", "wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()


#################################################
ComplementNB_classifier = SklearnClassifier(ComplementNB())
ComplementNB_classifier.train(training_set)

print("ComplementNB accuracy percent:", (nltk.classify.accuracy(ComplementNB_classifier, testing_set)) * 100)
save_classifier = open("algos/ComplementNB_classifier.pickle", "wb")
pickle.dump(ComplementNB_classifier, save_classifier)
save_classifier.close()


################################################
LogisticRegression_classifier = SklearnClassifier(LogisticRegression(max_iter=1000, warm_start=True))
LogisticRegression_classifier.train(training_set)

print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
save_classifier = open("algos/LogisticRegression_classifier5k.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


################################################
LinearSVC_classifier = SklearnClassifier(LinearSVC(max_iter=1000))
LinearSVC_classifier.train(training_set)

print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
save_classifier = open("algos/LinearSVC_classifier5k.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

###############################################
SGDC_classifier = SklearnClassifier(SGDClassifier(max_iter=1000, warm_start=True))
SGDC_classifier.train(training_set)


print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)
save_classifier = open("algos/SGDC_classifier5k.pickle", "wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()

###############################################
ExtraTreeClassifier = SklearnClassifier(ExtraTreeClassifier())
ExtraTreeClassifier.train(training_set)


print("ExtraTreeClassifier accuracy percent:", nltk.classify.accuracy(ExtraTreeClassifier, testing_set) * 100)
save_classifier = open("algos/ExtraTreeClassifier.pickle", "wb")
pickle.dump(ExtraTreeClassifier, save_classifier)
save_classifier.close()

