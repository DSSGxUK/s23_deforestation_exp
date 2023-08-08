import torch
import os
import pandas as pd
from tqdm import tqdm
from utility import create_feature_interpret_tiles


def feature_ablation(args, dataloader, model, criterion):

    device = args['device']

    model.eval()
    with torch.no_grad():
        for batch in tqdm(dataloader):

            img, _, paths = batch
            img = img.to(device).squeeze()
            out = model(img)

            y = out[0].unsqueeze(0)
            amt_defor = torch.sum(y >= args['threshold']).item()

            loss_vals = []
            for idx in range(1, img.shape[0]):
                loss_vals.append(criterion(out[idx].unsqueeze(0), y).item())

            loss_vals = sorted(enumerate(loss_vals), key=lambda x: x[1], reverse=True)
            loss_vals_data = [loss_vals[0]] + [loss_vals[i] for i in range(1, len(loss_vals)) if loss_vals[i][1] != loss_vals[i-1][1]]
            loss_vals_data = loss_vals_data[:-1] if loss_vals_data[-1][1] == loss_vals[-1][1] else loss_vals_data
            max_loss_vals = loss_vals_data[0][1]
            
            loss_data = []
            for idx, val in loss_vals_data:
                loss_data.append(args['data']['data_description'][idx][0])
                loss_data.append(val)
                loss_data.append(val / max_loss_vals)
                
            feature_importance = [ paths[0], amt_defor] + loss_data

            # Save list as a row in a csv file
            df = pd.DataFrame([feature_importance])
            df.to_csv(args['engine']['feature_ablation_out_csv'], mode='a', header=False, index=False)

    print('Feature ablation csv saved at {}'.format(args['engine']['feature_ablation_out_csv']))
    print('Creating feature interpretation tiles...')
    create_feature_interpret_tiles(args)    