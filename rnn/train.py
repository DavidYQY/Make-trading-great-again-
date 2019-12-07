from rnn.dataset import Dictionary, MyDataset
from rnn.model import LSTMClassifier
import torch
import torch.utils.data
from torch import nn
import numpy as np
from torch.nn import functional as F
from rnn import const
from rnn.utils import parse_args_and_merge_const
from tensorboardX import SummaryWriter
import time
import os
import pandas as pd
import random

def evaluate(net, step, writer, val_dataloader):
    print('Now Evaluate...')
    with torch.no_grad():
        net.eval()
        correct = 0
        total = 0
        for i, sample in enumerate(val_dataloader):
            for key in sample:
                if isinstance(sample[key], torch.Tensor):
                    sample[key] = sample[key].to(const.device)
            output = net(sample)
            _, predicted = torch.max(output["logit"], 1)
            total += sample['label'].size(0)
            correct += (predicted == sample['label']).sum().item()
        print('Test Accuracy: {:.2f}%'.format(100 * correct / total))
        writer.add_scalar('accuracy', correct / total, step)
        net.train()


if __name__ == '__main__':
    args = parse_args_and_merge_const()
    print('train_dir is: {}'.format(const.TRAIN_DIR))
    if not(os.path.exists(const.TRAIN_DIR)):
        os.makedirs(const.TRAIN_DIR)

    # Load dataset, transform word to id
    all_samples = pd.read_csv('./data/lstm.cvs').to_dict('records')
    all_text = []
    for sample in all_samples:
        if isinstance(sample['texts'], str):
            sample['processed_text'] = sample['texts'].split(' ')
        else:
            # special treat for empty tweets
            sample['processed_text'] = ['null']
        all_text.extend(sample['processed_text'])
    dictionary = Dictionary(all_text, max_vocab_size=const.MAX_VOCAB_SIZE)
    if const.USE_PRETRAINED_EMBEDDING is True:
        pretrained_embeddings = dictionary.word_embeddings()
    else:
        pretrained_embeddings = None

    for idx, sample in enumerate(all_samples):
        sample['processed_id'] = [dictionary.to_idx(word) for word in sample['processed_text']]

    # train & test split
    random.shuffle(all_samples)
    train_samples = all_samples[:int(len(all_samples) * 0.8)]
    val_samples = all_samples[int(len(all_samples) * 0.8):]

    train_dataset = MyDataset(train_samples, dictionary.to_idx('_unk'), const.MAX_SAMPLE_LENGTH)
    val_dataset = MyDataset(val_samples, dictionary.to_idx('_unk'), const.MAX_SAMPLE_LENGTH)
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=const.BATCH_SIZE, shuffle=True, num_workers=4)
    val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=const.VAL_BATCH_SIZE, shuffle=False, num_workers=4)

    net = LSTMClassifier(const.MAX_VOCAB_SIZE, const.EMBED_DIM, const.HIDDEN_DIM, const.DROPOUT_RATE,
                  const.NUM_LAYERS, const.RNN_TYPE, pretrained_embeddings=pretrained_embeddings)
    net = net.to(const.device)

    learning_rate = const.LEARNING_RATE
    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)

    writer = SummaryWriter(const.TRAIN_DIR)

    total_step = len(train_dataloader)
    step = 0
    for epoch in range(const.NUM_EPOCH):
        net.train()
        for i, sample in enumerate(train_dataloader):
            step += 1
            for key in sample:
                if isinstance(sample[key], torch.Tensor):
                    sample[key] = sample[key].to(const.device)
            output = net(sample)
            loss = net.cal_loss(sample, output)

            optimizer.zero_grad()
            loss['all'].backward()
            optimizer.step()
            if (i + 1) % 10 == 0:
                writer.add_scalar('lr/lr', learning_rate, step)
                writer.add_scalar('loss/all', loss['all'].item(), step)
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, const.NUM_EPOCH, i + 1, total_step, loss['all'].item()))
        # learning rate decay
        if hasattr(const, "LEARNING_RATE_DECAY_EVERY_EPOCHS"):
            if (epoch + 1) % const.LEARNING_RATE_DECAY_EVERY_EPOCHS == 0:
                learning_rate *= const.LEARNING_RATE_DECAY
        else:
            learning_rate *= const.LEARNING_RATE_DECAY
        optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
        # Save
        if hasattr(const, "SAVE_EVERY_EPOCHS") and (epoch + 1) % const.SAVE_EVERY_EPOCHS == 0:
            print('Saving Model....')
            torch.save(net.state_dict(), os.path.join(folder_name, 'model.pt-epoch{}'.format(epoch + 1)))
            print('OK.')
        if hasattr(const, "VAL_EVERY_EPOCHS") and (epoch + 1) % const.VAL_EVERY_EPOCHS == 0:
            evaluate(net, step, writer, val_dataloader)
