import os
import random
import numpy as np
import torch


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
    parser = ArgumentParser()
    parser.add_argument("--config-file", required=True)
    pass
    # Parse arguments
    return args