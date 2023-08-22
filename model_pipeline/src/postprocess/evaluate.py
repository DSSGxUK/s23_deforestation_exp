import os
import rasterio
import numpy as np
import argparse


def main():
    # Take command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt-path", type=str, help="Path to ground truth image")
    parser.add_argument("--pred-path", type=str, help="Path to predicted image")
    parser.add_argument("--year", type=int, default=1, help="How many years into the future to predict")
    args = parser.parse_args()
    # Call model_eval function
    model_eval(gt_path = args.gt_path, pred_path = args.pred_path, year = args.year)


def model_eval(gt_path, pred_path, year):
    # Open the average image file
    dataset = rasterio.open(pred_path)

    # Read the average image data into a NumPy array
    pred_array = dataset.read([year])
    pred = pred_array
    pred[pred == -1] = np.nan

    # Open the image file
    dataset = rasterio.open(gt_path)

    # Read the image data into a NumPy array
    gt_array = dataset.read()
    gt = gt_array
    gt[gt == -1] = np.nan

    diff = gt - pred
    idx = ~np.isnan(diff)

    # Calculate RMSE
    nonan_diff = diff[idx]
    rmse = ( np.sum(nonan_diff ** 2) / len (nonan_diff) ) ** 0.5
    print("RMSE =", rmse)

    min_arr = np.minimum(gt, pred)

    # Calculate precision and recall
    precision = np.sum(min_arr[idx]) / np.sum(pred[idx])
    print("Precision =", precision)

    recall = np.sum(min_arr[idx]) / np.sum(gt[idx])
    print("Recall =", recall)

    # Calculate F1 score
    f1_score = 2 * (precision * recall) / (precision + recall)
    print("F1 Score =", f1_score)

    print("Ratio of sum of prediction over sum of gt =", np.sum(pred[idx]) / np.sum(gt[idx]) )


if __name__ == "__main__":
    main()