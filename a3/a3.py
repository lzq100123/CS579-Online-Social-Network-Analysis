# coding: utf-8

# # Assignment 3:  Recommendation systems
#
# Here we'll implement a content-based recommendation algorithm.
# It will use the list of genres for a movie as the content.
# The data come from the MovieLens project: http://grouplens.org/datasets/movielens/

# Please only use these imports.
from collections import Counter, defaultdict
import math
import numpy as np
import os
import pandas as pd
import re
from scipy.sparse import csr_matrix
import urllib.request
import zipfile

def download_data():
    """ DONE. Download and unzip data.
    """
    url = 'https://www.dropbox.com/s/h9ubx22ftdkyvd5/ml-latest-small.zip?dl=1'
    urllib.request.urlretrieve(url, 'ml-latest-small.zip')
    zfile = zipfile.ZipFile('ml-latest-small.zip')
    zfile.extractall()
    zfile.close()


def tokenize_string(my_string):
    """ DONE. You should use this in your tokenize function.
    """
    return re.findall('[\w\-]+', my_string.lower())


def tokenize(movies):
    """
    Append a new column to the movies DataFrame with header 'tokens'.
    This will contain a list of strings, one per token, extracted
    from the 'genre' field of each movie. Use the tokenize_string method above.

    Note: you may modify the movies parameter directly; no need to make
    a new copy.
    Params:
      movies...The movies DataFrame
    Returns:
      The movies DataFrame, augmented to include a new column called 'tokens'.

    >>> movies = pd.DataFrame([[123, 'Horror|Romance'], [456, 'Sci-Fi']], columns=['movieId', 'genres'])
    >>> movies = tokenize(movies)
    >>> movies['tokens'].tolist()
    [['horror', 'romance'], ['sci-fi']]
    """
    ###TODO
    genrelist = [tokenize_string(movies.loc[index]['genres']) for index in range(len(movies))]
    movies['tokens'] = pd.Series(genrelist)
    return movies


def featurize(movies):
    """
    Append a new column to the movies DataFrame with header 'features'.
    Each row will contain a csr_matrix of shape (1, num_features). Each
    entry in this matrix will contain the tf-idf value of the term, as
    defined in class:
    tfidf(i, d) := tf(i, d) / max_k tf(k, d) * log10(N/df(i))
    where:
    i is a term
    d is a document (movie)
    tf(i, d) is the frequency of term i in document d
    max_k tf(k, d) is the maximum frequency of any term in document d
    N is the number of documents (movies)
    df(i) is the number of unique documents containing term i

    Params:
      movies...The movies DataFrame
    Returns:
      A tuple containing:
      - The movies DataFrame, which has been modified to include a column named 'features'.
      - The vocab, a dict from term to int. Make sure the vocab is sorted alphabetically as in a2 (e.g., {'aardvark': 0, 'boy': 1, ...})
    """
    ###TODO
    vocablist = []
    termlist = []
    for index in range(len(movies)):
    	genres = tokenize_string(movies.loc[index]['genres'])
    	termlist.append(genres)
    	vocablist += genres
    vocablist = sorted(list(set(vocablist)))
    vocab = defaultdict(lambda : len(vocab))
    for vo in vocablist:
    	vocab[vo]
    N = len(movies)
    datas = []
    cols = []
    docs_counter = defaultdict(lambda : 0)
    for vo in vocab.keys():
    	for terms in termlist:
    		if vo in terms:
    			docs_counter[vo] += 1
    for terms in termlist:
    	max_k = Counter(terms).most_common()[0][1]
    	data = []
    	col = []
    	for term in terms:
    		tfidf = terms.count(term) / max_k * np.log(N / docs_counter[term])
    		if tfidf is not 0:
    			data.append(tfidf)
    			col.append(vocab[term])
    	datas.append(data)
    	cols.append(col)
    csr_matrices = []
    for i in range(len(datas)):
    	csr_m = csr_matrix((datas[i],([0]*len(cols[i]), cols[i])),shape = (1,len(vocab)), dtype = np.float64)
    	csr_matrices.append(csr_m)
    movies['feature'] = pd.Series(csr_matrices)
    return  (movies, vocab)


def train_test_split(ratings):
    """DONE.
    Returns a random split of the ratings matrix into a training and testing set.
    """
    test = set(range(len(ratings))[::1000])
    train = sorted(set(range(len(ratings))) - test)
    test = sorted(test)
    return ratings.iloc[train], ratings.iloc[test]


def cosine_sim(a, b):
    """
    Compute the cosine similarity between two 1-d csr_matrices.
    Each matrix represents the tf-idf feature vector of a movie.
    Params:
      a...A csr_matrix with shape (1, number_features)
      b...A csr_matrix with shape (1, number_features)
    Returns:
      The cosine similarity, defined as: dot(a, b) / ||a|| * ||b||
      where ||a|| indicates the Euclidean norm (aka L2 norm) of vector a.
    """
    ###TODO
    dot_product = 0
    norma = 0
    normb = 0
    for i, j in zip(a.toarray()[0], b.toarray()[0]):
        dot_product += i * j
        norma += np.linalg.norm(i)
        norma += np.linalg.norm(j)
    if norma == 0 or normb == 0:
        return None
    else:
        return dot_product / ((norma * normb) ** 0.5)


def make_predictions(movies, ratings_train, ratings_test):
    """
    Using the ratings in ratings_train, predict the ratings for each
    row in ratings_test.

    To predict the rating of user u for movie i: Compute the weighted average
    rating for every other movie that u has rated.  Restrict this weighted
    average to movies that have a positive cosine similarity with movie
    i. The weight for movie m corresponds to the cosine similarity between m
    and i.

    If there are no other movies with positive cosine similarity to use in the
    prediction, use the mean rating of the target user in ratings_train as the
    prediction.

    Params:
      movies..........The movies DataFrame.
      ratings_train...The subset of ratings used for making predictions. These are the "historical" data.
      ratings_test....The subset of ratings that need to predicted. These are the "future" data.
    Returns:
      A numpy array containing one predicted rating for each element of ratings_test.
    """
    ###TODO
    prediction = np.zeros(len(ratings_test))
    index = 0
    for userId, movieId in zip(ratings_test.userId, ratings_test.movieId):
        ur = 0
        corr = 0
        for m in ratings_train[ratings_train.userId == userId].movieId.tolist():
            msim = cosine_sim(movies[movies.movieId == movieId].feature.tolist()[0], movies[movies.movieId == m].feature.tolist()[0])
            if msim is not None and msim > 0 and msim < 1:
                ur += msim * ratings_train[ratings_train.movieId == m][ratings_train.userId == userId].rating.tolist()[0]
                corr += msim
        if corr == 0:
            prediction[index] = np.mean(ratings_train[ratings_train.userId == userId].rating.tolist())
        else:
            prediction[index] = ur / corr
        index += 1
    return prediction


def mean_absolute_error(predictions, ratings_test):
    """DONE.
    Return the mean absolute error of the predictions.
    """
    return np.abs(predictions - np.array(ratings_test.rating)).mean()


def main():
    download_data()
    path = 'ml-latest-small'
    ratings = pd.read_csv(path + os.path.sep + 'ratings.csv')
    movies = pd.read_csv(path + os.path.sep + 'movies.csv')
    movies = tokenize(movies)
    movies, vocab = featurize(movies)
    print('vocab:')
    print(sorted(vocab.items())[:10])
    ratings_train, ratings_test = train_test_split(ratings)
    print('%d training ratings; %d testing ratings' % (len(ratings_train), len(ratings_test)))
    predictions = make_predictions(movies, ratings_train, ratings_test)
    print('error=%f' % mean_absolute_error(predictions, ratings_test))
    print(predictions[:10])


if __name__ == '__main__':
    main()
