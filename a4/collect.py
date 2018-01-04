# coding: utf-8
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys, os, random, re ,time
from TwitterAPI import TwitterAPI
import tweepy as ty
import numpy as np

consumer_key = 'put your own key'
consumer_secret = 'put your own key'
access_token = 'put your own key'
access_token_secret = 'put your own key'

def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def get_tweepy():
    auth = ty.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return ty.API(auth)

def read_screen_names(filename):
    list = []
    with open(filename,'r') as f:
        for line in f.readlines():
            list.append(line.strip())
    return list   

def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

def get_users(twitter, screen_names,num = 80):
    names_dict = {'screen_name':screen_names}
    request = robust_request(twitter,'users/lookup',names_dict)
    users = [r for r in request]
    random.shuffle(users)
    return users[:num]

def add_all_friends(twitter, users, num):
    for u in users:
        follows = get_friends(twitter,u['screen_name'], num)
        u['friends'] = follows

def writeUsersToText(users,filename):
    lines = [u['screen_name']+ '\t'+str(fids) for u in users for fids in u['friends']]
    with open(filename,'w+',encoding = 'utf-8') as f:
        for indx, line in enumerate(lines):
            if indx == len(lines) - 1:
                f.write(str(line))
                break
            f.write(str(line) + '\n')

def getTweets(tweepy, users):
    alltweets = []
    for user in users:
        new_tweets = tweepy.user_timeline(screen_name = user['screen_name'], count = 200,tweet_mode = 'extended')
        alltweets.append([tweet.full_text for tweet in new_tweets])
    return alltweets

def get_friends(twitter, screen_name,num):
    request = robust_request(twitter,'followers/ids',{'screen_name':screen_name})
    fids = [r for r in request]
    return fids[:num]

def isValid(doc):
    docclean = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)', ' ',doc).split())
    array = re.findall('\w+', docclean.lower())
    if len(array) != 0:
        return True
    else:
        return False

def writeTweets2Txt(alltweets, filename):
    validtweets = []
    index = 0
    for tweets in alltweets:
        for tweet in tweets:
            if isValid(str(tweet)):
                with open(filename + str(index) + '.txt','w+',encoding='utf-8') as f:
                        f.write(tweet)
                index += 1

def count_friends(users):
    count = Counter()
    for u in users:
        count.update(u['friends'])
    return count

def create_graph(users, friend_counts):
    G = nx.Graph()
    G.add_nodes_from([u['screen_name'] for u in users])
    G.add_nodes_from([f[0] for f in friend_counts.most_common() if f[1] > 1])
    E = []
    for u in users:
        for f in G.nodes():
            if f in u['friends']:
                tmp = (u['screen_name'],f)
                E.append(tmp)
    G.add_edges_from(E)
    return G

def draw_network(graph, users, filename):
    labels = {}
    for u in users:
        labels[u['screen_name']] = u['screen_name']
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos,graph.nodes(),node_colors = 'r',node_size = 50,alpha = 0.5)
    nx.draw_networkx_edges(graph,pos,width = 0.5,alpha = 0.2)
    nx.draw_networkx_labels(graph,pos,labels,font_size = 6,font_color = 'k')
    plt.axis('off')
    plt.savefig(filename,dpi = 500)

def main():
    tapi = get_twitter()
    tyapi = get_tweepy()
    names = read_screen_names('top100.txt')
    users = get_users(tapi,names,15)
    alltweets = getTweets(tyapi, users)
    writeTweets2Txt(alltweets, 'test' + os.sep + 'testtweets_')
    add_all_friends(tapi, users,200)
    writeUsersToText(users,'collectresult' + os.sep + 'User2Friendsdata.txt')
    friend_counts = count_friends(users)
    graph = create_graph(users, friend_counts)
    draw_network(graph, users, 'collectresult' + os.sep + 'network.png')
    num_users = len(users) + np.sum(np.array([len(u['friends']) for u in users]))
    num_twitters = np.sum(np.array([len(tweets) for tweets in alltweets]))
    with open('collectresult' + os.sep + 'dataInfo.txt','w+',encoding = 'utf8') as f:
        for indx, info in enumerate([num_users, num_twitters]):
            if(indx == 1):
                f.write(str(info))
            else:
                f.write(str(info) + '\n')

if __name__ == '__main__':
    main()

