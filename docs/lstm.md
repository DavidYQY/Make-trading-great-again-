---
title: Long Short-Term Memory
nav_include: 2
---

## Contents
{:.no_toc}
*  
{: toc}

## Introduction 

Automatic text classification can be done in many different ways in machine learning field as we have showed before. We also explore the task using deep learning models.

### Recurrent Neural Networks
Recurrent Neural Networks (RNN) are good at modeling sequence data, achieving excellent performance in Natural Language Processing field. When humans read sentences, they understand each word based on the understanding of previous words. Traditional neural networks can not handle this but RNN breaks through the limitation.  

In the diagram, a chunk of neural network, $h_{t}$, takes input $x_{t}$ and outputs a value $o_{t}$. A loop allows information to be passed from one step of the network to the next. Actually, $o_{1}, o_{2}, ..., o_{\tau}$ are the output of hidden layers and we will get the final output label from the last hidden layer. 

![RNN](pic/lstm/rnn.png)
<center>Fig 1: A clasical RNN structure </center>

### Long Short-Term Memory
RNN often suffers from the situation when the gap between the relevant information and the needed point is really large. That means RNN is not capable of handling such “long-term dependencies”.

Long Short Term Memory network (LSTM) is a special kind of RNN, which has the competence to learn long-term dependencies. 

All RNNs have the form of a chain of repeating modules ($h$ in Fig 1) of neural network. In standard RNNs, thie module is simple with a single tanh layer.

LSTM has four layters, interacting in a special way as showing in Fig 2. The key idea is the cell state (the horizontal line going through the top of the module). It will remove or add information to the cell state, regulated by gate structuress.

![lstm](pic/lstm/lstm.jpeg)
<center>Fig 2: The repeating module in an LSTM </center>


- First, a sigmoid layer called the “forget gate layer” decide what information to throw away from the cell state. 
- Second, LSTM decides what new information to store in the cell state. A sigmoid layer called the “input gate layer” decides which values to update. A tanh layer creates a vector of new candidate values, that could be added to the state.
- Third, update the old cell state $C_{t−1}$ to new state $C_{t}$. LSTM multiply the old state by $f_{t}$ (forgetting the things) and we add $i_{t} * \tilde{C}_{t}$ (the new candidate values).
- Finally, decide what to output combining with sigmoid and tanh. A sigmoid layer which decides what parts of the cell state to output. Then, the cell state through tanh and multiply it by the output of the sigmoid gate, thus only output the parts we decided to.

## Model Implementation 

We use Pytorch to establish our LSTM model and use tensorboard to visualize our training process. 

The input of lstm model should be a sequence of numerical data. So we should map words to vectors and padding each tweet to same length.
### Word embedding
Word embedding is computing vector representations of words. An pre-trained Google News corpus (3 billion running words) word vector model (3 million 300-dimension English word vectors) was used as our initial vector representation of the word in tweets. These vector weights will also be update at the following training process. We follow the setting of 300 embedding dimension that Google News choosed.

![word2vec](pic/lstm/word2vec.png)
<center>Fig 3. word to vector using Google News model.
</center>

### Sentence padding
Different tweets have different length. In this situation, we should pad short sentences to the longest sentences or set a hyper-parameter as the max sample length. 
TODO:
<p align="center">
<img src="pic/lstm/padding.png" width="600"/> 
</p>
<center>Fig.4  </center>

### Important Hyper-parameter

TODO:

|  Name   | Setting | Explain |
|  ----  | ----  | ---- |
| vocab | 10,000 | Trump has used more than 20,000 words. When map word to id in dictionary, we select the top k frequency word he used by NLTK|
<center>Tab.1  </center>


## Experiment Result

### Ablation study

![acc-1](pic/lstm/accuracy-1.png)
<center>Fig.5  </center>
TODO:

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-cly1{text-align:left;vertical-align:middle}
.tg .tg-baqh{text-align:center;vertical-align:top}
.tg .tg-nrix{text-align:center;vertical-align:middle}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-cly1"></th>
    <th class="tg-cly1">Concat features True</th>
    <th class="tg-cly1">Concat features False</th>
  </tr>
  <tr>
    <td class="tg-cly1">Pre-trained True</td>
    <td class="tg-nrix">52.95%</td>
    <td class="tg-nrix">52.63%</td>
  </tr>
  <tr>
    <td class="tg-0lax">Pre-trained Flase</td>
    <td class="tg-baqh">52.71%</td>
    <td class="tg-baqh">51.38%</td>
  </tr>
</table>
<center>Tab.2  </center>
![loss-1](pic/lstm/loss-1.png)
<center>Fig.6  </center>
TODO:
### Comparison
TODO:

![all](pic/lstm/all.png)
<center>Fig.7  </center>

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-0pky"><span style="font-weight:bold">time interval</span></th>
    <th class="tg-0pky">5 min</th>
    <th class="tg-0pky">10 min</th>
    <th class="tg-0pky">15 min</th>
    <th class="tg-0pky">20 min</th>
    <th class="tg-0pky">30 min</th>
    <th class="tg-0pky">40 min</th>
  </tr>
  <tr>
    <td class="tg-0pky"><span style="font-weight:bold">Test accuracy</span></td>
    <td class="tg-0pky">52.95%</td>
    <td class="tg-0pky">53.82%</td>
    <td class="tg-0pky">53.31%</td>
    <td class="tg-0pky">55.28%</td>
    <td class="tg-0pky">50.92%</td>
    <td class="tg-0pky">53.22%</td>
  </tr>
</table>
<center>Tab.3  </center>