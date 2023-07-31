import os
import torch
import wandb
import rasterio


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


def save_prediction(args, pred, paths):
    """Saves prediction to disk"""
    for i in range(len(paths)):
        src = rasterio.open(os.path.join(args['data']['dataset']['x_path'], paths[i]))
        profile = src.profile
        profile.update(
            count = args["modelling"]["model"]["out_channels"]
        )
        with rasterio.open(os.path.join(args['logging']['pred_dir'], paths[i]), 'w', **profile) as dst:
            dst.write(pred[i].cpu().numpy())