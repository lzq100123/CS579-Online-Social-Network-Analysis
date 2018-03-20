## Assignment 4

## Personal information:
1. OS: Windows
2. Compiler: Python 3.5
3. ID: A20381063
4. Name: Zhiquan Li

## Instruction:
1. Download/clone/sync folder a4
2. Set parameter for collect.py and cluster.py or Use the default.
3. Open your command
4. Go to the a4 directory 
5. Run collect.py, cluster.py classify.py and summarize.py by Typing "python3 "filename" in order.

## Result:
1. you can see the result in command line and corresponding result folder. Note the collected tweets are stored in test folder.

## Default parameters:
1. In collect.py, it collects 15 users, 200 followers and 200 tweets for each users since the twitter limits and the runtime of collection and GN alogrithm.
You can modify these parameters in get_users, add_all_friends and tweepy.user_timeline in getTweets method.
2. In cluster.py, it puts users into 4 clusters with 3 depth. You could modify these parameter in girvan_newman method.