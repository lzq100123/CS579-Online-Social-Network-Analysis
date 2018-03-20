# coding: utf-8

import os

def printInfo(collectInfo, clusterInfo, classifyInfo, classifyexample):
    num_users = 0
    num_tweets = 0
    num_cluster = 0
    avg_num_per_cluster = 0
    num_pos = 0
    num_neg = 0
    example_pos = ''
    example_neg = ''
    with open(collectInfo,'r') as f:
        num_users,num_tweets = [int(line) for line in f.readlines()]
    with open(clusterInfo,'r') as f:
        num_cluster,avg_num_per_cluster = [float(line) for line in f.readlines()]
    with open(classifyInfo,'r') as f:
        num_pos,num_neg = [line for line in f.readlines()]
    with open(classifyexample,'r') as f:
        example_pos,example_neg = [line for line in f.readlines()]
    print("Number of users collected: ", num_users)
    print("Number of messages collected: ", num_tweets)
    print("Number of communities discovered: ", num_cluster)
    print("Average number of users per community: ", avg_num_per_cluster)
    print("Number of instances in positive found: ", num_pos)
    print("Number of instances in negative found:", num_neg)
    print("One example from positive: ")
    print(example_pos)
    print("One example from negative: ")
    print(example_neg)

def main():
    collectInfo = 'collectresult' + os.sep + 'dataInfo.txt'
    clusterInfo = 'clusterresult' + os.sep + 'clusterInfo.txt'
    classifyInfo = 'classifyresult' + os.sep + 'num_pos_neg.txt'
    classifyexample = 'classifyresult' + os.sep + 'example.txt'
    printInfo(collectInfo, clusterInfo, classifyInfo,classifyexample)

if __name__ == '__main__':
    main()

