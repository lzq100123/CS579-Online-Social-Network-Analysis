# coding: utf-8
import os, io, re, random, glob
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def get_files(path):
    return sorted([f for f in glob.glob(path)])

def labelFiles(files):
    return np.array([1 if 'pos' in file else 0 for file in files])

def file2string(file):
    return io.open(file, encoding='utf8').readlines()[0]


def tweetsCollection(files):
    docs = []
    for file in files:
        docs.append(file2string(file))
    return docs

def tokenize(doc):
    docclean = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)', ' ',doc).split())
    return re.findall('\w+', docclean.lower())


def do_vectorize(files, func =tokenize, min_df=1,
                 max_df=1., binary=True, ngram_range=(1,1)):
    
    vector = CountVectorizer(input='filename', tokenizer= func,
                          binary=binary, min_df=min_df, max_df=max_df,
                          ngram_range=ngram_range)
    X = vector.fit_transform(files)
    return (X, vector)


def shuffle(X, y):
    random.seed(42)
    indices = sorted(range(X.shape[0]), key=lambda x: random.random())
    return X[indices], y[indices]

def fit_Classifier(X, y, c=1, penalty='l2'):
    clf = LogisticRegression(random_state=42, C=c, penalty=penalty)
    return clf.fit(X, y)


def tweetsClassification(docs, X, clf):
    pos = []
    neg = []
    maxpos = 0
    maxneg = 0
    poseg = ''
    negeg = ''
    for indx in range(X.shape[0]):
        predict = clf.predict(X[indx])
        prob = clf.predict_proba(X[indx])[0][0]
        if predict == 1:
            if maxpos < prob:
                maxpos = prob
                poseg = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)', ' ',docs[indx]).split())
            pos.append(docs[indx])
        else:
            if maxneg < prob:
                maxneg = prob
                negeg = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)', ' ',docs[indx]).split())
            neg.append(docs[indx])
    return pos, neg,poseg,negeg


def write2Txt(path,files):
    with open(path,'w+',encoding='utf-8') as f:
        for indx, file in enumerate(files):
            if indx == len(files):
                f.write(str(file))
            else:
                f.write(str(file) + '\n')

def main():
    trainfiles = get_files('train'+os.sep+'neg'+os.sep+'*.txt') + get_files('train'+os.sep+'pos'+os.sep+'*.txt')
    testfiles = get_files('test'+os.sep+'*.txt')
    labels = labelFiles(trainfiles)
    tweets = tweetsCollection(testfiles)
    X_train, vec = do_vectorize(trainfiles)
    X_train, labels = shuffle(X_train, labels)
    clf = fit_Classifier(X_train, labels)
    X_test = vec.transform(testfiles)
    pos, neg, poseg, negeg = tweetsClassification(tweets, X_test, clf)
    write2Txt('classifyresult' + os.sep + 'num_pos_neg.txt',[len(pos),len(neg)])
    write2Txt('classifyresult' + os.sep + 'tweets_pos.txt',pos)
    write2Txt('classifyresult' + os.sep + 'tweets_neg.txt',neg)
    write2Txt('classifyresult' + os.sep + 'example.txt',[poseg,negeg])
    print('results have been written into text file, check classifyresult folder')

if __name__ == '__main__':
    main()

