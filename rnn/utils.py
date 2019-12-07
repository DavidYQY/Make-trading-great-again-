import torch
import pandas as pd
import numpy as np
from rnn import const
import importlib
import argparse
import json
import os


def merge_const(module_name):
    new_conf = importlib.import_module(module_name)
    for key, value in new_conf.__dict__.items():
        if not(key.startswith('_')):
            setattr(const, key, value)
            print('override', key, value)


def parse_args_and_merge_const():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', default='', type=str)
    args = parser.parse_args()
    if args.conf != '':
        merge_const(args.conf)
    return args

