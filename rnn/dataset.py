import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

import re
import sys
import itertools
from torch.utils.data import Dataset, DataLoader

import random
import os
import pickle
import codecs
from gensim import corpora
import gensim


#load data from files
with open('../data/processed_trumptwitterarchive.txt', 'r') as data_file:
    json_data = data_file.read()
data = json.loads(json_data)
#load label from files
labels = pd.read_csv('../data/label.csv', names =['label'])


class MyDataset(Dataset):
    def __init__(self):
        # the prcessed words for each tweet: delete none processed_text data
        self.texts = [sample['processed_text'] for sample in data if len(sample['processed_text'])!=0]
        self.retweet_count = [sample['retweet_count'] for sample in data if len(sample['processed_text'])!=0]
        self.favorite_count = [sample['favorite_count'] for sample in data if len(sample['processed_text'])!=0]

        #word dictionary
        dictionary = corpora.Dictionary(self.texts) 
        self.word2id_dict = dictionary.token2id  # transform to dict, like {"human":0, "a":1,...}

        #set lables from csv file: up is 1; down is 0
        self.lables = labels['label'].tolist()
        # delete
        examples_lables = [x for x in zip(self.texts, self.lables) if len(x[0])!= 0]
        random.shuffle(examples_lables)
        self.MyDataset_frame = examples_lables

        #transform word to id
        self.MyDataset_wordid = \
            [(
                np.array([self.word2id_dict[word] for word in sent[0]], dtype=np.int64), 
                sent[1]
            ) for sent in self.MyDataset_frame]
        
    def word_embeddings(self, path = './GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin'):
        #establish from google
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        print('Please wait ... (it could take a while to load the file : {})'.format(path))

        word_dict = self.word2id_dict
        embedding_weights = np.random.uniform(-0.25, 0.25, (len(self.word2id_dict), 300))

        for word in word_dict:
            word_id = word_dict[word]
            if word in model.wv.vocab:
                embedding_weights[word_id, :] = model[word]

        return embedding_weights

    def __len__(self):
        return len(self.MyDataset_frame)

    def __getitem__(self,idx):
        sample = self.MyDataset_wordid[idx]      
        return sample

    def getsent(self, idx):
        sample = self.MyDataset_wordid[idx][0]       
        return sample

    def getlabel(self, idx):
        label = self.MRDataset_wordid[idx][1]
        return label

    def word2id(self):
        return self.word2id_dict

    def id2word(self):
        id2word_dict = dict([val,key] for key,val in self.word2id_dict.items()) 
        return id2word_dict
    

class train_set(Dataset):
    def __init__(self, samples):
        self.train_frame = samples

    def __len__(self):
        return len(self.train_frame)

    def __getitem__(self, idx):
        return self.train_frame[idx]


class test_set(Dataset):
    def __init__(self, samples):
        self.test_frame = samples

    def __len__(self):
        return len(self.test_frame)

    def __getitem__(self, idx):
        return self.test_frame[idx]