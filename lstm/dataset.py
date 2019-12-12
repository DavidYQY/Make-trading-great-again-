import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

import re
import sys
import itertools
from torch.utils.data import Dataset, DataLoader
import torch
import random
import os
import pickle
import codecs
from gensim import corpora
import gensim

import nltk

class Dictionary(object):
    '''
    Dictionary supports unknown token and retrieving embedding weights.
    If max_vocab_size is None, the max dictionary size won't be limited.
    There always exists an "_unk" for unknown tokens.
    e.g.:
        d = Dictionary(['a', 'a', 'b', 'b', 'c'], max_vocab_size=3)
        d.idx2word  # ['a', 'b', '_unk']
        d.word2idx  # {'a': 0, 'b': 1, '_unk': 2}
    '''

    def __init__(self, words, max_vocab_size=None):
        freq_dist = nltk.FreqDist(words)
        words_in_dict = list(map(lambda x: x[0], freq_dist.most_common(max_vocab_size)))
        if '_unk' not in words_in_dict:
            words_in_dict[-1] = '_unk'
        self.idx2word = []
        self.word2idx = {}
        for idx, word in enumerate(words_in_dict):
            self.idx2word.append(word)
            self.word2idx[word] = idx

    def __len__(self):
        return len(self.idx2word)

    def to_idx(self, word):
        if word in self.word2idx:
            return self.word2idx[word]
        else:
            return self.word2idx['_unk']

    def to_word(self, idx):
        if idx < len(self):
            return self.idx2word[idx]
        else:
            raise Exception

    def save(self, save_path):
        with open(save_path, 'wb') as f:
            pickle.dump(self, f)
    
    def word_embeddings(self, path='./lstm/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin'):
        print('Please wait ... (it could take a while to load the file : {})'.format(path))
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)

        embedding_weights = np.random.uniform(-0.25, 0.25, (len(self.word2idx), 300))

        for word in self.word2idx:
            word_id = self.word2idx[word]
            if word in model.wv.vocab:
                embedding_weights[word_id, :] = model[word]

        return embedding_weights


class MyDataset(Dataset):
    def __init__(self, samples, padded_word_id, max_sample_length=50):
        self.samples = samples
        self.padded_word_id = padded_word_id
        self.max_sample_length = max_sample_length

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        '''
        Sample key: word_id, retweet_count, favorite_count, text_length, label
        Word_id are cut or padded to `self.max_sample_length`.
        We apply a quick Gaussian Normalization for `retweet_count` and `favorite_count` here.
        '''
        sample = self.samples[idx]
        word_id = sample['processed_id'][:self.max_sample_length]
        length = len(word_id)
        if length < self.max_sample_length:
            word_id += [self.padded_word_id for i in range(self.max_sample_length - length)]
        return {
            'word_id': torch.LongTensor(word_id),
            'retweet_count': torch.tensor((sample['retweet_count'] - 6364.13644) / 10940.14718),
            'favorite_count': torch.tensor((sample['favorite_count'] -21723.34131) / 41560.13387),
            'length': torch.tensor(length, dtype=torch.int32),
            'label': torch.tensor(sample['label']),
        }