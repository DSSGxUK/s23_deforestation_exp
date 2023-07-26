from torch.nn import BCELoss
from torchvision.ops import sigmoid_focal_loss

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.nn.functional import one_hot
from torch import Tensor
from typing import Union


class BinaryDiceLoss(nn.Module):
    """Dice loss of binary class
    Args:
        smooth: A float number to smooth loss, and avoid NaN error, default: 1
        p: Denominator value: \sum{x^p} + \sum{y^p}, default: 2
        predict: A tensor of shape [N, *]
        target: A tensor of shape same with predict
        reduction: Reduction method to apply, return mean over batch if 'mean',
            return sum if 'sum', return a tensor of shape [N,] if 'none'
    Returns:
        Loss tensor according to arg reduction
    Raise:
        Exception if unexpected reduction
    """
    def __init__(self, smooth=1, p=2, reduction='mean'):
        super(BinaryDiceLoss, self).__init__()
        self.smooth = smooth
        self.p = p
        self.reduction = reduction

    def forward(self, predict, target):
        assert predict.shape[0] == target.shape[0], "predict & target batch size don't match"
        predict = predict.contiguous().view(predict.shape[0], -1)
        target = target.contiguous().view(target.shape[0], -1)

        num = torch.sum(torch.mul(predict, target), dim=1) + self.smooth
        den = torch.sum(predict.pow(self.p) + target.pow(self.p), dim=1) + self.smooth

        loss = 1 - num / den

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss
        else:
            raise Exception('Unexpected reduction {}'.format(self.reduction))


class Dice_Multilayer_Loss():

    def __init__(self, smooth=1, p=2, reduction='mean', ignore_index=-1):
        self.loss_fn = BinaryDiceLoss(smooth, p, reduction)
        self.ignore_index = ignore_index

    def __call__(self, input, target):
        num_layers = input.shape[1]
        loss = 0
        for i in range(num_layers):
            gt = target[:, i, :, :]
            idx = (gt != self.ignore_index)
            pred, gt = input[:, i, :, :][idx], gt[idx]
            loss += self.loss_fn(pred, gt)
        return loss/3



class FocalLoss(nn.Module):
    """Computes the focal loss between input and target
    as described here https://arxiv.org/abs/1708.02002v2

    Args:
        gamma (float):  The focal loss focusing parameter.
        weights (Union[None, Tensor]): Rescaling weight given to each class.
        If given, has to be a Tensor of size C. optional.
        reduction (str): Specifies the reduction to apply to the output.
        it should be one of the following 'none', 'mean', or 'sum'.
        default 'mean'.
        ignore_index (int): Specifies a target value that is ignored and
        does not contribute to the input gradient. optional.
        eps (float): smoothing to prevent log from returning inf.
    """
    def __init__(
            self,
            gamma,
            weights: Union[None, Tensor] = None,
            reduction: str = 'mean',
            ignore_index=-100,
            eps=1e-16
            ) -> None:
        super().__init__()
        if reduction not in ['mean', 'none', 'sum']:
            raise NotImplementedError(
                'Reduction {} not implemented.'.format(reduction)
                )
        weights = torch.Tensor(weights) if weights is not None else None
        assert weights is None or isinstance(weights, Tensor), \
            'weights should be of type Tensor or None, but {} given'.format(
                type(weights))
        self.reduction = reduction
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.eps = eps
        self.weights = weights

    def _get_weights(self, target: Tensor) -> Tensor:
        if self.weights is None:
            return torch.ones(target.shape[0])
        weights = target * self.weights
        return weights.sum(dim=-1)

    def _process_target(
            self, target: Tensor, num_classes: int, mask: Tensor
            ) -> Tensor:
        
        #convert all ignore_index elements to zero to avoid error in one_hot
        #note - the choice of value 0 is arbitrary, but it should not matter as these elements will be ignored in the loss calculation
        target = target * (target!=self.ignore_index) 
        target = target.view(-1)
        return one_hot(target, num_classes=num_classes)

    def _process_preds(self, x: Tensor) -> Tensor:
        if x.dim() == 1:
            x = torch.vstack([1 - x, x])
            x = x.permute(1, 0)
            return x
        return x.view(-1, x.shape[-1])

    def _calc_pt(
            self, target: Tensor, x: Tensor, mask: Tensor
            ) -> Tensor:
        p = target * x
        p = p.sum(dim=-1)
        p = p * ~mask
        return p

    def forward(self, x: Tensor, target: Tensor) -> Tensor:
        assert torch.all((x >= 0.0) & (x <= 1.0)), ValueError(
            'The predictions values should be between 0 and 1, \
                make sure to pass the values to sigmoid for binary \
                classification or softmax for multi-class classification'
        )
        mask = target == self.ignore_index
        mask = mask.view(-1)
        x = self._process_preds(x)
        num_classes = x.shape[-1]
        target = self._process_target(target, num_classes, mask)
        weights = self._get_weights(target).to(x.device)
        pt = self._calc_pt(target, x, mask)
        focal = 1 - pt
        nll = -torch.log(self.eps + pt)
        nll = nll.masked_fill(mask, 0)
        loss = weights * (focal ** self.gamma) * nll
        return self._reduce(loss, mask, weights)

    def _reduce(self, x: Tensor, mask: Tensor, weights: Tensor) -> Tensor:
        if self.reduction == 'mean':
            return x.sum() / (~mask * weights).sum()
        elif self.reduction == 'sum':
            return x.sum()
        else:
            return x

class Focal_Multilayer_Loss():
    
    def __init__(self, gamma=2, weight=torch.Tensor([1, 10]).to('cuda'), size_average=None, ignore_index=-1, reduction='mean'):
        self.loss_fn = FocalLoss(gamma, weight, reduction, ignore_index)
        self.ignore_index = ignore_index

    def __call__(self, input, target):
        num_layers = input.shape[1]
        loss = 0
        for i in range(num_layers):
            gt = target[:, i, :, :]
            idx = (gt != self.ignore_index)
            pred, gt = input[:, i, :, :][idx], gt[idx].long()
            loss += self.loss_fn(pred, gt)
        return loss/3


class NLL_Multilayer_Loss():

    def __init__(self, weight=None, size_average=None, ignore_index=-1, reduce=None, reduction='mean'):
        self.loss_fn = BCELoss(weight, size_average, reduce, reduction)
        self.ignore_index = ignore_index

    def __call__(self, input, target):
        num_layers = input.shape[1]
        loss = 0
        for i in range(num_layers):
            gt = target[:, i, :, :]
            idx = (gt != self.ignore_index)
            pred, gt = input[:, i, :, :][idx], gt[idx]
            loss += self.loss_fn(pred, gt)
        return loss/3