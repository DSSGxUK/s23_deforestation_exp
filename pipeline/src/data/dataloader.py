import torch
import rasterio
import os.path as osp
import numpy as np
import glob
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
from tqdm import tqdm


class Biomass_Dataset(Dataset):
    """Custom dataset class for the data of a single participant."""

    def __init__(self, x_path, y_path): 
        """Constructor function to initiate the dataset object."""
        self.x_path = x_path
        self.y_path = y_path
        self.files = []
        # Get file names of all the files in the directory ending in *.tif
        for file in tqdm(glob.glob(osp.join(self.x_path, "*.tif"))):
            file = file.split("/")[-1]
            # # Check if corresponding y file exists
            # tmp = rasterio.open(osp.join(self.y_path, file)).read()
            # idx = (tmp > 0)
            # if idx.sum() < 5000:
            #     continue
            self.files.append(file)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        x = rasterio.open(osp.join(self.x_path, self.files[idx])).read()
        y = rasterio.open(osp.join(self.y_path, self.files[idx])).read(1)
        x = torch.from_numpy(x).float()
        y = torch.from_numpy(y).float().unsqueeze(0)
        return x, y


def get_dataloaders(args):

    trainval_dataset = Biomass_Dataset(
        x_path = args["data"]["dataset"]["x_path"], 
        y_path = args["data"]["dataset"]["y_path"]
    )

    val_size = int(args["data"]["validation_split"] * len(trainval_dataset))
    train_size = len(trainval_dataset) - val_size

    train_dataset, val_dataset = random_split(
        trainval_dataset, [train_size, val_size]
    )

    train_dataloader = DataLoader(
        train_dataset,
        batch_size = args["data"]["dataloader"]["batch_size"],
        shuffle = args["data"]["dataloader"]["shuffle"],
        num_workers = args["data"]["dataloader"]["num_workers"],
        pin_memory = args["data"]["dataloader"]["pin_memory"]
    )

    val_dataloader = DataLoader(
        val_dataset,
        batch_size = args["data"]["dataloader"]["batch_size"],
        shuffle = args["data"]["dataloader"]["shuffle"],
        num_workers = args["data"]["dataloader"]["num_workers"],
        pin_memory = args["data"]["dataloader"]["pin_memory"]
    )

    return {
        "train": train_dataloader,
        "val": val_dataloader,
    }