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

    def __init__(self, x_path, y_path=None, use_tar=False, return_info=False, num_years=1, feature_ablation=False, data_description=None): 
        """Constructor function to initiate the dataset object."""
        self.band_stats = data_description
        self.x_path = x_path
        self.y_path = y_path
        self.use_tar = use_tar
        self.return_info = return_info
        self.num_years = num_years
        self.files = []
        self.feature_ablation = feature_ablation
        # Get file names of all the files in the directory ending in *.tif
        for file in tqdm(glob.glob(osp.join(self.x_path, "*.tif"))):
            file = file.split("/")[-1]
            if self.y_path is None:
                self.files.append(file)
            elif osp.exists(osp.join(self.y_path, file)):
                self.files.append(file)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):

        x = rasterio.open(osp.join(self.x_path, self.files[idx])).read()
        x = torch.from_numpy(x).float()

        if self.feature_ablation:
            layer_num = 0
            batch = torch.zeros((len(self.band_stats)+1, *x.shape))
            batch[0] = x.clone()
            for i, layer in enumerate(self.band_stats):
                x_copy = x.clone()
                for j in range(layer[1]):
                    x_copy[layer_num+j] = layer[2+j]
                batch[i+1] = x_copy
                layer_num += layer[1]
            x = batch

        y = torch.zeros(1)
        if self.y_path is not None:
            y = rasterio.open(osp.join(self.y_path, self.files[idx]))
            y = y.read([i for i in range(1, self.num_years + 1)])
            y = torch.from_numpy(y).float()

        if self.return_info:
            return x, y, self.files[idx]
        else:
            return x, y


def get_dataloaders(args):

    if args["engine"]["mode"] == "train":

        trainval_dataset = Biomass_Dataset(
            x_path = args["data"]["dataset"]["x_path"], 
            y_path = args["data"]["dataset"]["y_path"],
            use_tar = args["data"]["dataset"]["use_tar"],
            return_info = args["data"]["dataset"]["return_info"],
            num_years = args["modelling"]["model"]["out_channels"]
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

    elif args["engine"]["mode"] == "test":

        test_dataset = Biomass_Dataset(
            x_path = args["data"]["dataset"]["x_path"], 
            y_path = args["data"]["dataset"]["y_path"],
            use_tar = args["data"]["dataset"]["use_tar"],
            return_info = args["data"]["dataset"]["return_info"],
            num_years = args["modelling"]["model"]["out_channels"]
        )

        test_dataloader = DataLoader(
            test_dataset,
            batch_size = args["data"]["dataloader"]["batch_size"],
            shuffle = args["data"]["dataloader"]["shuffle"],
            num_workers = args["data"]["dataloader"]["num_workers"],
            pin_memory = args["data"]["dataloader"]["pin_memory"]
        )

        return {
            "test": test_dataloader,
        }

    elif args["engine"]["mode"] == "feature_ablation":

        test_dataset = Biomass_Dataset(
            x_path = args["data"]["dataset"]["x_path"], 
            y_path = args["data"]["dataset"]["y_path"],
            use_tar = args["data"]["dataset"]["use_tar"],
            return_info = args["data"]["dataset"]["return_info"],
            num_years = args["modelling"]["model"]["out_channels"],
            feature_ablation = True, 
            data_description = args['data']['data_description']
        )

        test_dataloader = DataLoader(
            test_dataset,
            batch_size = 1,
            shuffle = args["data"]["dataloader"]["shuffle"],
            num_workers = args["data"]["dataloader"]["num_workers"],
            pin_memory = args["data"]["dataloader"]["pin_memory"]
        )

        return {
            "test": test_dataloader,
        }