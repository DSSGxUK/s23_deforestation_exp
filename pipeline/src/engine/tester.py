import torch
import os
from tqdm import tqdm
from utility import save_prediction


def test_engine(args, dataloader, model):

    device = args['device']
    if os.path.exists(args['logging']['ckp_dir']) == False:
        os.makedirs(args['logging']['ckp_dir'])

    model.eval()
    with torch.no_grad():
        for batch in tqdm(dataloader):
            img, gt = batch
            img, gt = img.to(device), gt.to(device)
            out = model(img)
            save_prediction(args, out, meta_data, f_names)
