import os
import rasterio
import numpy as np

def calculate_metrics(ground_truth_dir, prediction_dir):
    """
    Calculates the average recall and precision for continuous versions of precision and recall.
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

    pred_sum_pertile = []
    gt_sum_pertile = []
    min_val_sum_pertile=[]

    # Process each matching ground truth and prediction file
    for i, (ground_truth_file, prediction_file) in enumerate(zip(ground_truth_files, prediction_files), start=1):
        # Construct the full file paths
        ground_truth_path = os.path.join(ground_truth_dir, ground_truth_file)
        prediction_path = os.path.join(prediction_dir, prediction_file)

        # Open the ground truth file
        dataset = rasterio.open(ground_truth_path)

        # Read the ground truth data into a NumPy array
        ground_truth_array = dataset.read(1) 
        ## unit conversion from 300m pixels to hectares 
        ground_truth_arr = ground_truth_array * 0.09

        # If the image has multiple bands, you can access each band individually
        #]  # Access the first band

        # Open the prediction file
        dataset = rasterio.open(prediction_path)

        # Read the prediction data into a NumPy array
        prediction_array = dataset.read(1)
        prediction_arr = prediction_array

        # If the image has multiple bands, you can access each band individually. Specifying first band only
        

        min_arr = np.minimum(ground_truth_arr, prediction_arr)
        # Append  values to the list
        min_val_sum_per_tile.append(np.sum(np.nan_to_num(min_arr)))
        pred_sum_per_tile.append(np.sum(np.nan_to_num(prediction_arr)))
        gt_sum_per_tile.append(np.sum(np.nan_to_num(ground_truth_arr))) 

    recall=np.sum(min_val_sum_per_tile)/np.sum(gt_sum_per_tile)
    precision=np.sum(min_val_sum_per_tile)/np.sum(pred_sum_per_tile)

    # Calculate the average recall and precision based on non-NaN values
    
    return {
        "recall": recall,
        "precision": precision,
    }
