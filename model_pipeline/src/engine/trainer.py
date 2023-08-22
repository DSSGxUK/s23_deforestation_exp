import os
import torch
from tqdm import tqdm

from utility import (
    log_wandb,
    save_ckp,
    get_metrics,
)


def train_engine(args, train_dataloader, val_dataloader, model, optimizer, criterion, start_epoch=0, start_itr=0, val_loss_min=float('inf')):
    """
    Performs training with periodic evaluation on the validation set

    Args:
        args (Dict): Dictionary of arguments
        train_dataloader (torch.utils.data.DataLoader) : Training dataloader
        val_dataloader (torch.utils.data.DataLoader): Validation dataloader
        model (torch.nn.Module): Model to be trained
        optimizer (torch.optim object): Optimizer for training
        criterion (torch.nn object): Loss function
        start_epoch (int, optional): (In case of resuming training) Starting epoch. Defaults to 0.
        start_itr (int, optional): (In case of resuming training) Starting iteration. Defaults to 0.
        val_loss_min (_type_, optional): (In case of resuming training) Minimum validation loss achieved. Defaults to float('inf').
    """
    device = args['device']
    itr = start_epoch * len(train_dataloader)

    # If checkpoints directory does not exist, create it
    if not os.path.exists(args['logging']['ckp_dir']):
        os.makedirs(args['logging']['ckp_dir'])

    # Training loop
    for epoch in range(start_epoch, args['engine']['epochs']):

        print('Epochs: ', epoch)

        for train_batch in tqdm(train_dataloader):

            if itr < start_itr:
                itr += 1
                continue

            model.train()
            optimizer.zero_grad()
            
            img, gt = train_batch
            img, gt = img.to(device), gt.to(device)

            # Forward pass
            out = model(img)
            loss = criterion(out, gt)

            # Backpropagation
            loss.backward()
            optimizer.step()

            itr += 1

            # Logging
            train_metrics = get_metrics(args, out, gt)
            log_wandb(args, loss.item(), train_metrics, itr, 'train')

            if itr % args['logging']['ckp_save_interval']  == 0 or itr % len(train_dataloader) == 0 :
                model_checkpoint = {
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'epoch': epoch,
                    'itr': itr,
                    'val_loss_min': val_loss_min
                }                    
                save_ckp(args, model_checkpoint)

            if itr % args['engine']['evaluation_interval'] == 0 :
                print("Evaluating on validation set")
                val_loss = evaluate(args, val_dataloader, model, criterion, itr)
                print("Validation Loss = {}".format(val_loss))
                # Saving checkpoint if validation loss is minimum
                if val_loss < val_loss_min:
                    print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(val_loss_min, val_loss))
                    val_loss_min = val_loss
                    model_checkpoint = {
                        'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'epoch': epoch,
                        'itr': itr,
                        'val_loss_min': val_loss_min
                    }
                    save_ckp(args, model_checkpoint)


def evaluate(args, dataloader, model, criterion, itr):
    """
    Runs the model on the dataloader and returns the loss

    Args:
        args (Dict): Dictionary of arguments
        dataloader (torch.utils.data.DataLoader): Dataloader to run the model on
        model (torch.nn.Module): Model to be evaluated
        criterion (torch.nn object): Loss function

    Returns:
        _type_: _description_
    """

    model.eval()
    device = args['device']
    val_loss = 0.0
    val_metrics = {}

    with torch.no_grad():
        for val_batch in tqdm(dataloader):
            img, gt = val_batch
            img, gt = img.to(device), gt.to(device)

            # Forward pass
            out = model(img)
            loss = criterion(out, gt)

            val_loss += loss.item()

            # Calculating metrics
            metrics_data = get_metrics(args, out, gt)
            for k in list(metrics_data.keys()):
                if k not in val_metrics:
                    val_metrics[k] = 0.0
                val_metrics[k] += metrics_data[k]

    val_loss /= len(dataloader)
    for k in list(val_metrics.keys()):
        val_metrics[k] /= len(dataloader)
    log_wandb(args, val_loss, val_metrics, itr, 'val')

    return val_loss