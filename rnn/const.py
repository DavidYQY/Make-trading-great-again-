import time
import torch
import socket as _socket


_hostname = str(_socket.gethostname())
_time = time.strftime('%m-%d %H:%M:%S', time.localtime())

# Model Parameter
MAX_VOCAB_SIZE = 10000
USE_PRETRAINED_EMBEDDING = True
CONCAT_RETWEET_AND_FAV = True
MAX_SAMPLE_LENGTH = 50
EMBED_DIM = 300
HIDDEN_DIM = 128
DROPOUT_RATE = 0.5
NUM_LAYERS = 1
RNN_TYPE = 'LSTM'


# Train Parameter
NUM_EPOCH = 100
BATCH_SIZE = 256
LEARNING_RATE = 3e-4
LEARNING_RATE_DECAY_EVERY_EPOCHS = 10
LEARNING_RATE_DECAY = 0.8
SAVE_EVERY_EPOCHS = 1000

# Val Parameter
VAL_BATCH_SIZE = 256
VAL_EVERY_EPOCHS = 1

# auto
_name = 'vocab-{}-pretrained-{}-concat-{}-length-{}-emb-{}-hidden-{}-dropout-{:.2f}-layers-{}-{}-epoch-{}-lr-{:.5f}-lrdep-{}-lrdr-{:.3f}'.format(
    MAX_VOCAB_SIZE, USE_PRETRAINED_EMBEDDING, CONCAT_RETWEET_AND_FAV, MAX_SAMPLE_LENGTH, EMBED_DIM, HIDDEN_DIM, DROPOUT_RATE,
    NUM_LAYERS, RNN_TYPE, NUM_EPOCH, LEARNING_RATE, LEARNING_RATE_DECAY_EVERY_EPOCHS, LEARNING_RATE_DECAY
)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
TRAIN_DIR = 'rnn/models/%s/' % _name
MODEL_NAME = '%s' % _name
#############