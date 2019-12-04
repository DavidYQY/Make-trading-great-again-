import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.functional as F
import torch.optim as optim

from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class LSTMClassifier(nn.Module):

	def __init__(self, vocab_size, embedding_dim, hidden_dim, output_size):

		super(LSTMClassifier, self).__init__()

		self.embedding_dim = embedding_dim
		self.hidden_dim = hidden_dim
		self.vocab_size = vocab_size

		self.embedding = nn.Embedding(vocab_size, embedding_dim)
		self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=1)

		self.hidden2out = nn.Linear(hidden_dim, output_size)
		self.softmax = nn.LogSoftmax()

		self.dropout_layer = nn.Dropout(p=0.2)


	def init_hidden(self, batch_size):
		return(autograd.Variable(torch.randn(1, batch_size, self.hidden_dim)),
						autograd.Variable(torch.randn(1, batch_size, self.hidden_dim)))


	def forward(self, batch, lengths):
		
		self.hidden = self.init_hidden(batch.size(-1))

		embeds = self.embedding(batch)
		packed_input = pack_padded_sequence(embeds, lengths)
		outputs, (ht, ct) = self.lstm(packed_input, self.hidden)

		# ht is the last hidden state of the sequences
		# ht = (1 x batch_size x hidden_dim)
		# ht[-1] = (batch_size x hidden_dim)
		output = self.dropout_layer(ht[-1])
		output = self.hidden2out(output)
		output = self.softmax(output)

		return output