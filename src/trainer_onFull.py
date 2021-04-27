# -*- coding: utf-8 -*-

import csv
import os
import pickle
import random
from string import punctuation, digits
import nltk
import numpy as np
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.svm import LinearSVC
from sklearn.tree import ExtraTreeClassifier

"""токенізатор"""
nltk.download('punkt', quiet=True)
"""список стоп-слів"""
nltk.download("stopwords", quiet=True)
"""розподіл по частинам мови"""
nltk.download('averaged_perceptron_tagger', quiet=True)

mystem = Mystem()
eng_stopwords = stopwords.words("english")

all_words = []
documents = []

"""частини мови які ми будемо брати до уваги"""
allowed_word_types = ('JJ', 'JJS', 'RB', 'VB')


def preprocess_text(spam):
    """попереднє оброблення тексту"""

    lol = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    txtpart = lol(spam, 1000)
    res = []  # обработанный текст

    for txtp in txtpart:
        alltexts = ' '.join([txt + ' br ' for txt in txtp])

        words = mystem.lemmatize(alltexts)
        tokens = [token for token in words if token
                  not in eng_stopwords
                  and token != " "
                  and token.strip() not in punctuation
                  and token.strip() not in digits]
        doc = []
        for txt in tokens:
            if txt != '\n' and txt.strip() != '':
                if txt == 'br':
                    res.append(doc)
                    doc = []
                else:
                    doc.append(txt)
    res = [' '.join(i) for i in res]
    """список обработанных отзывов"""
    return res


"""об'єм інформації"""
quantity = 1200
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '', r'..\resources\reviews.csv')), 'r', newline='',
          encoding='latin-1') as f:
    spam = list(csv.reader(f, delimiter=','))[1:]
    spam = np.array(spam)
    preprocessed_revs = preprocess_text(spam[:quantity, 0])

p, n, nt = 0, 0, 0
try:
    """Сполучимо по грапах по 1000 речень для швидшої обробки"""
    stream = list(zip(preprocessed_revs, spam[:quantity, 1]))
    for i, row in enumerate(stream):
        """розподіл по тональності контенту з датасету"""
        if row[1] == '1':
            documents.append((row[0], "neg"))
            words = nltk.word_tokenize(row[0], language='english')
            pos = tuple(nltk.pos_tag(words, lang='eng'))

            for w in pos:
                if w[1] in allowed_word_types:
                    all_words.append(w[0].lower())
                    n += 1

        elif row[1] == '2':
            documents.append((row[0], "pos"))
            words = nltk.word_tokenize(row[0], language='english')
            pos = tuple(nltk.pos_tag(words, lang='eng'))

            for w in pos:
                if w[1] in allowed_word_types:
                    all_words.append(w[0].lower())
                    p += 1

        elif row[1] == '3':
            documents.append((row[0], "ntr"))
            words = nltk.word_tokenize(row[0], language='english')
            pos = tuple(nltk.pos_tag(words, lang='eng'))

            for w in pos:
                if w[1] in allowed_word_types:
                    all_words.append(w[0].lower())
                    nt += 1

except Exception as e:
    print(i, e)

print(n, p, nt)  # к-ть речень різноїх тональності

"""зберегти результат попереднього оброблення"""
save_documents = open("algos/documents.pickle", "wb")
pickle.dump(documents, save_documents, protocol=pickle.HIGHEST_PROTOCOL)
save_documents.close()
del save_documents

"""частотний аналіз текстів"""
all_words = nltk.FreqDist(all_words)
documents = tuple(documents)
word_features = tuple(all_words.keys())[:int(len(all_words) * 0.5)]

del all_words

"""збереження найвживаніших слів"""
save_word_features = open("algos/word_features5k.pickle", "wb")
pickle.dump(word_features, save_word_features, protocol=pickle.HIGHEST_PROTOCOL)
save_word_features.close()


def find_features(document):
    words = word_tokenize(document, language='english')
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


"""збирання набору даних"""
featuresets = [(find_features(rev), category) for (rev, category) in documents]
del documents
del word_features

random.shuffle(featuresets)
print(len(featuresets))

"""розбиття на тестовий та тренувальний набір"""
training_set = featuresets[:int(len(featuresets) * 0.8)]
testing_set = featuresets[int(len(featuresets) * 0.8):]

"""навчання на наївному алгоритмі"""
classifier = nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(15)
del classifier

"""навчання на наївному поліноміальному алгоритмі"""
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

save_classifier = open("algos/MNB_classifier5k.pickle", "wb")
pickle.dump(MNB_classifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del MNB_classifier

#################################################
"""навчання на додатковому наївному поліноміальному алгоритмі"""
ComplementNB_classifier = SklearnClassifier(ComplementNB())
ComplementNB_classifier.train(training_set)

print("ComplementNB accuracy percent:", (nltk.classify.accuracy(ComplementNB_classifier, testing_set)) * 100)
save_classifier = open("algos/ComplementNB_classifier.pickle", "wb")
pickle.dump(ComplementNB_classifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del ComplementNB_classifier

################################################
"""навчання за допомогою логістичної регресії"""
LogisticRegression_classifier = SklearnClassifier(LogisticRegression(max_iter=10000, warm_start=True))
LogisticRegression_classifier.train(training_set)

print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
save_classifier = open("algos/LogisticRegression_classifier5k.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del LogisticRegression_classifier

################################################
"""навчання за допомогою класифікації лінійних опорних векторів"""
LinearSVC_classifier = SklearnClassifier(LinearSVC(max_iter=10000))
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
save_classifier = open("algos/LinearSVC_classifier5k.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del LinearSVC_classifier

###############################################
"""навчання за допомогою лінійних моделей з використанням градієнтних спусків"""
SGDC_classifier = SklearnClassifier(SGDClassifier(max_iter=1000, warm_start=True))
SGDC_classifier.train(training_set)

print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)
save_classifier = open("algos/SGDC_classifier5k.pickle", "wb")
pickle.dump(SGDC_classifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del SGDC_classifier

###############################################
"""навчання за допомогою випадкових дерев"""
ExtraTreeClassifier = SklearnClassifier(ExtraTreeClassifier())
ExtraTreeClassifier.train(training_set)

print("ExtraTreeClassifier accuracy percent:", nltk.classify.accuracy(ExtraTreeClassifier, testing_set) * 100)
save_classifier = open("algos/ExtraTreeClassifier.pickle", "wb")
pickle.dump(ExtraTreeClassifier, save_classifier, protocol=pickle.HIGHEST_PROTOCOL)
save_classifier.close()
del ExtraTreeClassifier
