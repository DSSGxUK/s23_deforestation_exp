import os
import torch
import wandb
import rasterio
import numpy as np


def initialise_wandb(args):
    """Initialises WandB logging"""
    if args['restore_checkpoint'] == True:
        wandb.init(project=args['logging']['wandb_project'], resume='allow', id=args['logging']['wandb_id'])
    else:
        wandb.init(project=args['logging']['wandb_project'], name=args['logging']['wandb_name'], config=args)


def log_wandb(args, loss, metrics, itr, mode):
    """Logs metrics to wandb"""
    log_data = { mode + '_' + k : metrics[k] for k in list(metrics.keys()) }
    log_data[mode + '_loss'] = loss
    wandb.log(log_data, step=itr)


def save_ckp(args, checkpoint):
    """Saves model and optimizer state"""
    ckp_path = os.path.join(args['logging']["ckp_dir"], 'ckp_epoch_{}_itr_{}_val_loss_{:.6f}.pth'.format(
        checkpoint['epoch'], checkpoint['itr'], checkpoint['val_loss_min']
    ))
    torch.save(checkpoint, ckp_path)
    print('Checkpoint saved at {}'.format(ckp_path))


def load_ckp(checkpoint_fpath, model, optimizer):
    """Loads model and optimizer state from given checkpoint"""
    checkpoint = torch.load(checkpoint_fpath)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return model, optimizer, checkpoint['epoch'], checkpoint['itr'], checkpoint['val_loss_min']


def save_prediction(args, pred, paths, num_bands=3):
    """Saves prediction to disk"""
    for i in range(len(paths)):
        src = rasterio.open(os.path.join(args['data']['dataset']['x_path'], paths[i]))
        profile = src.profile
        profile.update(
            count = num_bands
        )
        with rasterio.open(os.path.join(args['logging']['pred_dir'], paths[i]), 'w', **profile) as dst:
            dst.write(pred[i])


def create_feature_interpret_tiles(args):
    """Creates feature interpretation map"""
    feature_2_idx = { itm[0] : idx+1 for idx, itm in enumerate(args['data']['dataset']['data_description']) }
    print("Feature to index mapping: {}".format(feature_2_idx))
    with open(args['engine']['feature_ablation_out_csv'], 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            elements = line.split(',')
            file_name = elements[0]
            amt_deforestation = elements[1]
            # Skip if no deforestation
            if amt_deforestation == '0':
                continue
            # Process feature list
            feature_list = line.split(',')[2:]
            feature_list[-1] = feature_list[-1].replace('\n', '')
            feature_encoded = [ feature_2_idx[feature_list[i]] for i in range(0, len(feature_list), 3) ]
            top_feature_encoded = [ [[itm]] for itm in feature_encoded]
            feature_encoded_array = np.array((args['engine']['num_top_fa_features'], 1, 1))
            for i in range(min(len(top_feature_encoded)), args['engine']['num_top_fa_features']):
                feature_encoded_array[i][0][0] = top_feature_encoded[i]
            # Save predictions
            save_prediction(args, feature_encoded_array, [file_name], args['engine']['num_top_fa_features'])