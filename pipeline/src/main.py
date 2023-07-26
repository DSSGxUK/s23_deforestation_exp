from utility import (
    get_args,
    set_seed,
    initialise_wandb,
    load_ckp,
)
from engine import (
    train_engine,
    test_engine,
)
from data import (
    get_dataloaders,
)
from models import get_model_optimizer_criterion
import sys
sys.path.append('./')
import wandb

def main():

    # Get arguments
    args = get_args()

    # Set seed for consistent experiments
    set_seed(args['seed'])

    print("\nInitialising wandb\n")
    initialise_wandb(args)

    print("\nLoading data\n")
    dataloaders = get_dataloaders(args)

    print("\nInitialising model\n")
    model, optimizer, criterion = get_model_optimizer_criterion(args)

    start_epoch = 0
    start_itr = 0
    val_loss_min = float('inf')
    
    if args['restore_checkpoint'] == True:
        model, optimizer, start_epoch, start_itr, val_loss_min = load_ckp(args['pretrained_weights'], model, optimizer)
        model = model.to(args['device'])
    
    if args['engine']['mode'] == "train":
        print("\nStarting training\n")
        wandb.watch(model, log_freq=args['logging']['wandb_watch_freq'])
        train_engine(args, dataloaders["train"], dataloaders["val"], model, optimizer, criterion, start_epoch, start_itr, val_loss_min)

    elif args['engine']['mode'] == "test":
        print("\nStarting testing\n")
        test_engine(args, dataloaders["test"], model, criterion)

    print("\nDone!\n")


if __name__ == '__main__':
    main()