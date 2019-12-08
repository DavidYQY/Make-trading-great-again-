import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.functional as F
import torch.optim as optim

from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class LSTMClassifier(nn.Module):

    def __init__(self, max_vocab_size, embed_dim, hidden_dim,
                 dropout_rate=0.5, num_layers=1, rnn_type='LSTM', pretrained_embeddings=None, concat_feature=False):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(max_vocab_size, embed_dim)
        self.rnn_type = rnn_type
        if rnn_type in ['LSTM', 'GRU']:
            self.rnn = getattr(nn, rnn_type)(embed_dim, hidden_dim, num_layers, dropout=dropout_rate)
        else:
            try:
                nonlinearity = {'RNN_TANH': 'tanh', 'RNN_RELU': 'relu'}[rnn_type]
            except KeyError:
                raise ValueError("""An invalid option for `--model` was supplied,
                                 options are ['LSTM', 'GRU', 'RNN_TANH' or 'RNN_RELU']""")
            self.rnn = nn.RNN(embed_dim, hidden_dim, num_layers, nonlinearity=nonlinearity, dropout=dropout)
        self.output_dropout = nn.Dropout(dropout_rate)
        # 2-classes classification
        if concat_feature is False:
            self.hidden2out = nn.Linear(hidden_dim, 2)
        else:
            self.hidden2out = nn.Linear(hidden_dim + 2, 2)
        self.concat_feature = concat_feature

        if pretrained_embeddings is not None:
            self.embedding.weight.data.copy_(torch.from_numpy(pretrained_embeddings))
        self.cross_entropy_loss = nn.CrossEntropyLoss()

    def forward(self, sample):
        '''
        Input: sample
            key: word_id, retweet_count, favorite_count, text_length, label
        Output: output
            key: logit
        '''
        # batch_size x length x embedding_size
        embeds = self.embedding(sample['word_id'])
        packed_input = pack_padded_sequence(embeds, sample['length'], batch_first=True, enforce_sorted=False)
        output, hidden = self.rnn(packed_input)

        if self.rnn_type == 'LSTM':
            hidden = hidden[0][-1]
        else:
            hidden = hidden[-1]
        
        if self.concat_feature:
            hidden = torch.cat(
                [
                    hidden,
                    sample['retweet_count'].reshape(hidden.shape[0], 1),
                    sample['favorite_count'].reshape(hidden.shape[0], 1),
                ],
                dim=1
            )

        output = self.output_dropout(hidden)
        output = self.hidden2out(output)
        output = {'logit': output}
        return output
    
    def cal_loss(self, sample, output):
        '''
        Input: sample, output
        Output: loss (scalar)
        '''
        return {'all': self.cross_entropy_loss(output['logit'], sample['label'])}
