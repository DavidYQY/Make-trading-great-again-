---
title: Regression
nav_include: 4
---

## Contents
{:.no_toc}
*  
{: toc}

## Introduction 

Now let us venture into the territory of actually predicting the S&P 500 Index returns after each tweet.

First, the returns are defined as $$(P_b-P_a)/P_a$$, where $P_a$ is the nearest pre-tweet price (up to one minute, which is the granularity of our data), and $P_b$ is the price $m$ minutes after $P_a.$ The distribution of *training set* returns is shown in Figure 1 below, with $m$ equal to 5. Since the returns are typically *very* small in decimals, we instead quote them in *basis points (bps)*, where each basis point is 1/100 of 1%. For example, 10bps is 0.1% change in S&P 500 Index.  

![returns_hist](pic/regression/returns_hist.png)
<center>Figure 1: S&P 500 Index 5-min-post-tweet Returns Histogram</center>

We also need to recognize that it is very easy to data snoop, and thus extreme care is needed. For example, our data [source](http://www.trumptwitterarchive.com) documents that even though tweets are collected "[every 1 minute](http://www.trumptwitterarchive.com/about)", [ "favorite counts and retweet counts" are continuously updated until they fall out of the the most recent 100 tweets](https://github.com/bpb27/trump_tweet_data_archive). This means that the data we get for these two features are the count a few *days* after that tweet was out. This implies that they cannot be used to predict stock market movement *minutes* after the tweet. Another way to think about this is that the tens of thousands of retweet/favorite counts in our data set are almost entirely realizations *after* our stock movement realizations! Similar reasons apply to comments (and any feature derived thereof), and hence are excluded in our model.

To conclude, the final model included the sensitiment analysis result (posive and negative word counts in each tweet), as well as the 20 key-word (one-hot encoded).

## Modeling

### Preliminaries

The first step in modeling is to figure out the $m$ that our model performs the best. We ran basic Linear Regression, Lasso regression, and Random Forest Regressor on the training set with $m$ from 1 minute up to 60 minutes. The test set MSE result is shown below in Figure 2. 

![mse over m](pic/regression/test_set_mse.png)
<center>Figure 2: MSE of Predicting Returns with Different Time Intervals </center>

Seemingly contradictory results from predicting Up or Down in the previous section, where as $m$ increases the prediction accuracy tend to increase. But this actually makes sense in that as more time elapses after each tweet, the returns should have higher standard deviations (think of a random walk model), and thus leading to higher MSE in our regression prediction. At the same time, more and more people interpret the tweet and react (hopefully) in the *direction* of what our model predicts, and hence leading to higher prediction *accuracy* in general as $m$ increases.

For a more realistic set up, instead of predicting 1-minute ahead return, we choose $m = 5$ to take into account of potential human intervention before trade execution.

Next, 

### Key Model Results

