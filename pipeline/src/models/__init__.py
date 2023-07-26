import torch
from .unet_model import UNet
from .loss import NLL_Multilayer_Loss, Focal_Multilayer_Loss, Dice_Multilayer_Loss


def get_model_optimizer_criterion(args):

    if args['modelling']['model']['name'] == 'UNet':
        model = UNet(
            in_channels = args['modelling']['model']['in_channels'], 
            out_channels = args['modelling']['model']['out_channels']
        ).to(args['device'])

    if args['modelling']['optimizer']['name'] == 'Adam':
        optimizer = torch.optim.Adam(
            model.parameters(), 
            lr = args['modelling']['optimizer']['lr']
        )

    if args['modelling']['criterion']['name'] == 'DiceLoss':
        criterion = Dice_Multilayer_Loss(
            ignore_index=args['data']['ignore_index']
        )
    elif args['modelling']['criterion']['name'] == 'NLLLoss':
        criterion = NLL_Multilayer_Loss(
            ignore_index=args['data']['ignore_index']
        )
    elif args['modelling']['criterion']['name'] == 'FocalLoss':
        criterion = Focal_Multilayer_Loss(
            gamma=args['modelling']['criterion']['params']['gamma'],
            ignore_index=args['data']['ignore_index'],
            weight=torch.Tensor(args['modelling']['criterion']['params']['weight']).to(args['device'])
        )

    return model, optimizer, criterion


if __name__ == "__main__":

    args = {
        "modelling": {
            "model": {
                "name": "UNet",
                "in_channels": 4,
                "out_channels": 3
            },
            "optimizer": {
                "name": "Adam",
                "lr": 0.001
            },
            "criterion": {
                "name": "NLLLoss"
            }
        }
    }
    get_model_optimizer_criterion(args)