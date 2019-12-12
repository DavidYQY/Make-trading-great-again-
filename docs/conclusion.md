---
title: Project Trajectory and Conclusion
nav_include: 7
---

## Contents
{:.no_toc}
*  
{: toc}

## Project Trajectory 

With this project we set out hoping to extract from Trump's tweets information that are related to the movement of the financial market. Our project is divided into two parts: First, we try to predict the *direction* of the S&P500 Index, and second the actual *returns* of the Index.

In the first part, we started off doing a sentiment analysis, extracting features such as positive and negative word counts in each tweet. We also referenced J.P. Morgan's research report and extracted 20 key words that could be impactful on the market. The baseline models we used are Logistic Regression (with CV), KNN, and Random Forest. The result was better than we thought: all of the model achieved somewhere between 52-54% accuracy on the test set. Also surprising to us at first was that as the number of minutes post tweet increases, our prediction accuracy increases on average. We also looked feature importance in our baseline models and compared with those used in J.P. Morgan Research.

Next, we employed Long Short-Term Memory (LSTM) model that takes in entire sentences. The model performed slightly better than the baseline model, which was surprising at first. We thought hard about it and listed our comments on the corresponding page. The main points are limited tweet data and lost information/context in our representation of dataset.

Finally, we attempted to directly predict the *returns* of the S&P500 Index. Not so surprisingly, the shorter time interval we predict ahead, the better the accuracy as measured by MSE. That said, the overall prediction result was surprisingly a disappointment. The best model yielded no positive predictive power which means that our feature set, entirely based on text, did not capture the relationship with the market. In the process we were also very cautious of any data snooping, and carefully taken out features that seem to make sense but actually should not be used; examples are favorite and retweet counts as well as comments -- they may be very rich in information, but unfortunately they will never be available *ex ante*.


## Conclusions

### Baseline models

For the baseline classification models, generally speaking the classification accuracy improves as the time interval gets longer. The potential reason behind this phenomenon is that it takes market to react in the direction our model predicts, and the longer we give the market to play out its dynamics, they better the prediction gets.

By adding a third class which represents effectively no change in market, we improve the accuracy of the classifier. This is more practical since many tweets do not have influence on the market at all.

With respect to the accuracy of different classifiers, we found that while random forest model has some advantage over other models for the binary prediction, it loses its superiority in three-class prediction.

### Feature Importance

For the feature importance section, we obtained top important variables from the random forest models and compared the results to the one we used in the baseline model (i.e. J. P. Morgan 20-words). We found that our results largely consistent with theirs.

### LSTM

Compare to baseline model, the LSTM model is slightly better overall. Specifically, when the time interval is shorter than 20 minutes, LSTM model performs better whereas when time interval is longer, the performance goes down because the noise confused the network to make a right choice. 

Why LSTM is not strikingly better than the baseline models:

- The size of our dataset is limited. It might have been more than sufficient for vanilla machine learning models but is perhaps not quite enough for deep learning models.
- Trump's tweets are sometimes much richer than can be represented in our dataset or mapped effectively to numerical values. For example, information such as links and videos was lost in our dataset, and emojis were possibly mapped to values that do not make much sense through word embedding. This way the powerful LSTM model could be confused. However, the abovementioned problem presents a different trade-off situation for our baseline models, which inherent have difficulty processing the lost context and noise.


### Regression

In our mini adventure into the prediction of actual returns of the S&P500 Index post Trump’s tweets, if we treat the Linear Regression as baseline, Lasso regression and Random Forest indeed outperformed. However, there is zero practical use of the models, since they have 0 or negative $R^2$ value in the test set.

## Future Work

- One of the structural breaks in our dataset that is not mentioned in previous parts is related to Twitter's change of character limit. Before November 2017, each tweet was limited to 140 characters, and it was expanded to be 280 afterwards. There is clear difference in the information content before and after, as illustrated in Figures 1 and 2. The 20 key-word count as well as positive and negative words count per tweet got noticeably higher after the change. In the future, researchers might want to then add this change as a feature to control for its effect.

<p align="center">
<img src="pic/conclusion/key_word.png" width="700"/> </p>
<center>Figure 1: Key Word Count Before and After Character Limit Change</center>
<br>

<p align="center">
<img src="pic/conclusion/pos_neg.png" width="700"/> </p>
<center>Figure 2: Positive and Negative Word Count Before and After Character Limit Change</center>
<br>

- For deep learning models, there are three things to improve.
	- Include hierarchical neural attention branch. Attention lets the network focus more on related words and filters out useless information. This will help reduce the noise which could confuse the network. Even though we know little about how human brain learns and remembers sequences, we could draw insights from human attention mechanism, which is widely used in current research fields.

	-  Leverage image as a learning bias to reason about language perception. A major difference between human and machine is that humans form a coherent and global understanding of a scene, where high-level knowledge provides resilience in the face of errors from low-level perception. Thus the combination of language and vision provides a prism to textual understanding. This will alleviate the information lost of emojis, images or videos.

	-  Use data augmentation. We could enlarge our datasets via generating more text data to boost the models. In natural language processing field, it is hard to augment text due to high complexity of human language. Future researchers can, for example, use synonyms as substitute or extract the main structure of the sentence. It is difficult to achieve but may of value for future research.

- One possible limitation of our project is that, as we discussed before, Trump’s tweets are not always posted by himself. The tweet posted by his staff could introduce more noise into the model since some studies showed that the tweets from his team would be less aggressive. One way to overcome this problem is that we could filter out the tweets that were not tweeted by him. This is difficult now since Trump has switched from Android to iPhone. In the future, we could possibly use the results from http://didtrumptweetit.com/ (which is a website contains the probability the tweet is posted by Trump) to do the filtering.
