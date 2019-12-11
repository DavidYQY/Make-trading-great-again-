---
title: Introduction
---

### Team 68: Rock Zhou, Jingyuan Liu, Yaoyang Lin, Qiuyang Yin
AC209a Fall 2019          
[GitHub Repository](https://github.com/DavidYQY/Make-trading-great-again-)

## Problem Statement and Motivation

Current U.S. President Trump is very different from his predecessors in at least one aspect: his Twitter account activity level. Indeed, he tweets about 20-30 times in a single day, and a lot of the policy announcements were actually made through tweets! Hence, if we assume that a sitting U.S. President's uttering has the potential to move markets, it is reasonable to hypothesize that Trump's tweets could have noticeable impact on the S&P 500 Index. 

In this study we test this hypothesis by trying to predict both the *magnitude* and the *direction* of S&P 500 Index immediately after each tweet.

## Introduction and Description of Data

TODO

### Twitter Dataset

Twitter dataset is collected from trumptwitterarchive.com. The dataset consists of 42,692 tweets from 2009 to 2019, and contains source, retweet count, favorite count, timestamp, and text. After collecting the tweets, we preprocess the tweets by tokenization, cleaning, and normalization. Speciﬁcally, we converted all letters to lower case, and removed numbers, punctuations, and stop words. Some particular patterns exist in Twitter, such as URLs, Hashtags, Mentions, Reserved words (RT, FAV), Emojis, and Smileys. During cleaning and parsing, we decided to only keep semantic related information in the text such as Hashtags(#MakeAmericaGreatAgain), Emojis, and Smileys, while URLs and Mentions were removed.

### S&P500 Dataset

S&P 500 Index represents about 500 of large-cap companies that cover roughly 80% of the U.S. equity market capitalization. Thus, this choice implies a good representation of the U.S. equity space. 

S&P dataset is purchased from ﬁrstratedata.com. The dataset consists of 670,830 rows of minute-by-minute S&P500 (ˆGSPC) data from January 2013 to November 2019 during trading hours (9:30 AM - 4:00 PM ET) of each trading day. For each minute, we have open, high, low, and close prices. To be consistent, we use only the close price for our analysis.

## Research Questions

The core of what we want to look at is whether Trump’s tweets (and the features of which, such as number of likes and comments under tweets, among others) provide information on broader stock market returns. We would model the inﬂuence Trump’s tweets have on stock market with statistic models, natural language processing knowledge and deep neural networks.

TODO

## Sources:

[1] M. Hu and B. Liu, “Mining and summarizing customer reviews,” in Proceedings of the tenth ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 168–177, ACM, 2004.

[2] J. Y. Munier Scalem, Henry St John, “Introducing the volfefe index,” J.P.Morgan Research, vol. Sep 6, pp. 144–151, 2019.
