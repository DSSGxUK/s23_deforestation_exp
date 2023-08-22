import os
import json
import random
import torch
import numpy as np
from argparse import ArgumentParser


def set_seed(seed):
    """Set seed for consistent experiments."""
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def get_args():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument("--config-file", required=False, default="./conf/default.json")
    args = parser.parse_args()
    with open(args.config_file) as f:
        args = json.load(f)
    return args