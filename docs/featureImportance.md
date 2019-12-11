---
title: Feature Importance
nav_include: 7
---

## Contents
{:.no_toc}
*  
{: toc}

## Introduction

In this section we are going to use random forest and tree methods to see the feature importance in this problem set.

## Feature importance 

We use feature importance from of each predictor in this random forest model. Whenever a feature is used in a tree in the forest, the algorithm will log the decrease in the splitting criterion (such as gini) and make use of this splitting criterion as a metric to meature the importance of variables.

## Results

![feature importance 1](pic/featureImportance/fp1.png)

From the figure above we can notice that the most important features when deciding whether the stock should go up or down is the favorite numbers, retweet numbers and the positive/negative counts we gain during the sentiment analysis. There are two reasons behind

![feature importance 2](pic/featureImportance/fp2.png)

