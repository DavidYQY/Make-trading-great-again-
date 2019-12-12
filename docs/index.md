---
title: Introduction
---

### Team 68: Rock Zhou, Jingyuan Liu, Yaoyang Lin, Qiuyang Yin
AC209a Fall 2019          
[GitHub Repository](https://github.com/DavidYQY/Make-trading-great-again-)

## Problem Statement and Motivation

The current U.S. President Donald J. Trump is very different from his predecessors in at least one aspect: his Twitter account activity level. Indeed, he tweets about 20-30 times on average in a single day, and some of the policy announcements were actually made through his tweets! Hence, if we assume that a sitting U.S. President's uttering has the potential to move markets, it is reasonable to hypothesize that Trump's tweets could have noticeable impact on the S&P 500 Index. 

In this study we test this hypothesis by trying to predict both the *direction* and actual *returns* of S&P 500 Index immediately after each tweet.

## Introduction and Roadmap

We live in a digital world where social media is ubiquitous. As an example, Twitter alone produces, on average, 500 million tweets a day. Individual tweets can have profound effects, particularly the ones coming from politicians. To this end, analyzing those tweets is important and significant.

In particular, we are interested in studying the relationship between Trump's tweets and S&P500 Index movements. Concretely, does his tweets have any predictive power on where the market is going? This is a challenging problem, not just that there are lots of tweets available, but more importantly, those tweets contain textual information that we have not encountered before.

Thus, our project is split into a few parts. We first conduct EDA to explore the structure of the data. Then we try to predict the *direction* (i.e. up or down) of the market movement through baseline models (with a special section dedicated to feature importance) and Long Short-Term Memory (LSTM) model. We finally briefly look at regression models to predict the actual *returns* of of the S&P 500 Index right after the tweet. Across all models we also explore the prediction accuracies across different time intervals post tweets (e.g. 5-minutes post tweet price movement vs 60-minute post tweet price movement). We finally conclude with a discussion of possible future improvements.

## Description of Data

### Twitter Dataset

Twitter dataset is collected from trumptwitterarchive.com. The dataset consists of 42,692 tweets from 2009 to 2019, and contains source, retweet count, favorite count, timestamp, and text. After collecting the tweets, we preprocess the tweets by tokenization, cleaning, and normalization. Speciﬁcally, we converted all letters to lower case, and removed numbers, punctuations, and stop words. Some particular patterns exist in Twitter, such as URLs, Hashtags, Mentions, Reserved words (RT, FAV), Emojis, and Smileys. During cleaning and parsing, we decided to only keep semantic related information in the text such as Hashtags(#MakeAmericaGreatAgain), Emojis, and Smileys, while URLs and Mentions were removed.

### S&P500 Dataset

S&P 500 Index represents about 500 of large-cap companies that cover roughly 80% of the U.S. equity market capitalization. Thus, this choice implies a good representation of the U.S. equity space. 

S&P dataset is purchased from ﬁrstratedata.com. The dataset consists of 670,830 rows of minute-by-minute S&P500 (ˆGSPC) data from January 2013 to November 2019 during trading hours (9:30 AM - 4:00 PM ET) of each trading day. For each minute, we have open, high, low, and close prices. To be consistent, we use only the close price for our analysis.


## Literature Review/Related Work


The relationship between social media and the stock market has been widely studied by other researchers. Many studies found that future stock return is related to social media such as Twitter. Hentschel et al. studied Twitter hashtags and NASDAQ and NYSE stocks [7]. They claimed that there is a correlation between tweet volume and market performance and found that Twitter can be an indicator of important events that impact the stock market. Gilbert and Karahalios [8] built and created the "Anxiety Index" and discovered that the increase of anxiety in blogs can negatively affect the S&P 500 Index even though the posts are not related to finance. Bartov et al. [4] proposed a method to use Twitter to predict firm-level earnings and stock returns.

The tweets of Trump have also been thoroughly analyzed in other researches. After he became the president, his impact dramatically increased on Twitter. Several methods have been proposed to utilize Trump's tweets to predict the stock market. J.P. Morgan Research [2] created the “Volfefe Index” and suggested that Trump tweet can have a statistically significant impact on the market. Juma’h et al. [9] used the effect of President Trump’s tweets to predict companies’ performance. These works support our hypothesis that the tweets from Donald Trump can be useful for stock market prediction.


## Sources:

[1] M. Hu and B. Liu, “Mining and summarizing customer reviews,” in Proceedings of the tenth ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 168–177, ACM, 2004.

[2] J. Y. Munier Scalem, Henry St John, “Introducing the volfefe index,” J.P.Morgan Research, vol. Sep 6, pp. 144–151, 2019.

[3] C. H. Liu, Applications of twitter emotion detection for stock market prediction.  PhD thesis, Massachusetts Institute of Technology, 2017.

[4] E. Bartov, L. Faurel, and P. S. Mohanram, “Can twitter help predict firm-level earningsand stock returns?,”The Accounting Review, vol. 93, no. 3, pp. 25–57, 2017.

[5] S.  Hochreiter  and  J.  Schmidhuber,  “Long  short-term  memory,”Neural computation,vol. 9, no. 8, pp. 1735–1780, 1997.

[6] A. Agarwal, B. Xie, I. Vovsha, O. Rambow, and R. Passonneau, “Sentiment analysis of twitter data,” inProceedings of the Workshop on Language in Social Media (LSM 2011),pp. 30–38, 2011.

[7] Hentschel, M., & Alonso, O. (2014). Follow the money: A study of cashtags on
Twitter. First Monday, 19(8).

[8] Gilbert, E., & Karahalios, K. (2010). Widespread worry and the stock market.
In Proceedings of the International Conference on Weblogs and Social.

[9] Juma’h, Ahmad H., and Yazan Alnsour. "Using Social Media Analytics: The Effect of President Trump’s Tweets On Companies’ Performance." Journal of Accounting and Management Information Systems 17.1 (2018): 100-121.

[10] Olah, Christopher. "Understanding lstm networks." (2015).