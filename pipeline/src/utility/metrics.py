from sklearn.metrics import precision_recall_fscore_support


def get_metrics(args, out, gt):
    """Calculate metrics for given batch"""
    idx = ( gt != args['data']['ignore_index'] )
    gt = gt[idx].flatten().detach().cpu()
    gt = gt.numpy()

    out[out > args['threshold']] = 1
    out[out <= args['threshold']] = 0
    out = out[idx].flatten().detach().cpu()
    out = out.numpy()

    print("Predicted deforestation pixels: {}".format(out.sum()))
    print("Actual deforestation pixels: {}".format(gt.sum()))

    precision, recall, f1score, _ = precision_recall_fscore_support(gt, out, average='binary')
    metrics = {}
    metrics['precision'] = precision
    metrics['recall'] = recall
    metrics['f1'] = f1score
    metrics['accuracy'] = (gt == out).mean()
    # TODO: add more metrics   
    # metrics['iou'] = iou
    return metrics