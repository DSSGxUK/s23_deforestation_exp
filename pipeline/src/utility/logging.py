import os
import torch
import wandb

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