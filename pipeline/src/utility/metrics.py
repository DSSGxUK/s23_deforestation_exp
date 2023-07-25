import os
import rasterio
import numpy as np
import re

def calculate_metrics(ground_truth_dir, prediction_dir):
    """
    Calculates the continuous versions of precision and recall.
    Loads ground truth and prediction files from disk.

    Args:
        ground_truth_dir (str): Directory path containing the ground truth files.
        prediction_dir (str): Directory path containing the prediction files.

    Returns:
        float: Average recall value.
        float: Average precision value.
    """
    # Get the file names in the directories
    ground_truth_files = [file for file in os.listdir(ground_truth_dir) if file.endswith('.tif')]
    prediction_files = [file for file in os.listdir(prediction_dir) if file.endswith('.tif')]

    # Sort the file names to ensure matching pairs
    ground_truth_files.sort()
    prediction_files.sort()

    # Check if the number of files in each directory is the same
    if len(ground_truth_files) != len(prediction_files):
        raise ValueError("Number of ground truth files does not match number of prediction files.")

    # Check if the file names match between the directories based on the base names
    gt_base_names = [re.match(r"(\d+)_downsampled.tif", f).group(1) for f in ground_truth_files]
    pred_base_names = [re.match(r"(\d+)_average.tif", f).group(1) for f in prediction_files]

    if gt_base_names != pred_base_names:
        extra_ground_truth_files = [f for f in ground_truth_files if re.match(r"(\d+)_downsampled.tif", f).group(1) not in pred_base_names]
        extra_prediction_files = [f for f in prediction_files if re.match(r"(\d+)_average.tif", f).group(1) not in gt_base_names]
        raise ValueError(
            f"File names in ground truth and prediction folders do not match based on the base names! "
            f"Extra ground truth files: {extra_ground_truth_files} "
            f"Extra prediction files: {extra_prediction_files}."
        )

    pred_sum_per_tile = []
    gt_sum_per_tile = []
    min_val_sum_per_tile = []

    # Process each matching ground truth and prediction file
    for ground_truth_file, prediction_file in zip(ground_truth_files, prediction_files):
        # Construct the full file paths
        ground_truth_path = os.path.join(ground_truth_dir, ground_truth_file)
        prediction_path = os.path.join(prediction_dir, prediction_file)

        # Open the ground truth file within a 'with' statement
        with rasterio.open(ground_truth_path) as dataset:
            # Read the ground truth data into a NumPy array
            ground_truth_array = dataset.read(1)
            ## unit conversion from 30m pixels to hectares
            ground_truth_arr = ground_truth_array * 0.09

        # Open the prediction file within a 'with' statement
        with rasterio.open(prediction_path) as dataset:
            # Read the prediction data into a NumPy array
            prediction_array = dataset.read(1)
            prediction_arr = prediction_array

        min_arr = np.minimum(ground_truth_arr, prediction_arr)
        # Append values to the list
        min_val_sum_per_tile.append(np.sum(np.nan_to_num(min_arr)))
        pred_sum_per_tile.append(np.sum(np.nan_to_num(prediction_arr)))
        gt_sum_per_tile.append(np.sum(np.nan_to_num(ground_truth_arr)))

    recall = np.sum(min_val_sum_per_tile) / np.sum(gt_sum_per_tile)
    precision = np.sum(min_val_sum_per_tile) / np.sum(pred_sum_per_tile)

    # Calculate the average recall and precision based on non-NaN values

    return {
        "recall": recall,
        "precision": precision,
    }
