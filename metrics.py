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
    ground_truth_files = [file for file in os.listdir(ground_truth_dir) if not file.endswith('.tif.aux.xml')]
    prediction_files = [file for file in os.listdir(prediction_dir) if not file.endswith('.tif.aux.xml')]

    # Sort the file names to ensure matching pairs
    ground_truth_files.sort()
    prediction_files.sort()

    # List to store recall and precision arrays without NaN
    filtered_recall_values = []
    filtered_precision_values = []

    # Process each matching ground truth and prediction file
    for i, (ground_truth_file, prediction_file) in enumerate(zip(ground_truth_files, prediction_files), start=1):
        # Construct the full file paths
        ground_truth_path = os.path.join(ground_truth_dir, ground_truth_file)
        prediction_path = os.path.join(prediction_dir, prediction_file)

        # Open the ground truth file
        dataset = rasterio.open(ground_truth_path)

        # Read the ground truth data into a NumPy array
        ground_truth_array = dataset.read()
        ## unit conversion
        ground_truth_arr = ground_truth_array * 0.09

        # If the image has multiple bands, you can access each band individually
        ground_truth_band = ground_truth_array[0]  # Access the first band (index 0)

        # Open the prediction file
        dataset = rasterio.open(prediction_path)

        # Read the prediction data into a NumPy array
        prediction_array = dataset.read()
        prediction_arr = prediction_array

        # If the image has multiple bands, you can access each band individually
        prediction_band = prediction_array[0]

        min_arr = np.minimum(ground_truth_arr, prediction_arr)

        # Calculate recall array
        recall = np.sum(np.nan_to_num(min_arr))/np.sum(np.nan_to_num(ground_truth_arr))

        # Flatten the recall array
        flattened_recall = recall.flatten()

        # Remove NaN values
        filtered_recall = flattened_recall[~np.isnan(flattened_recall)]

        # Append the filtered recall values to the list
        filtered_recall_values.extend(filtered_recall)

        # Calculate precision array
        precision = np.sum(np.nan_to_num(min_arr))/np.sum(np.nan_to_num(prediction_arr))

        # Flatten the precision array
        flattened_precision = precision.flatten()

        # Remove NaN values
        filtered_precision = flattened_precision[~np.isnan(flattened_precision)]

        # Append the filtered precision values to the list
        filtered_precision_values.extend(filtered_precision)

       

    # Calculate the average recall and precision based on non-NaN values
    average_recall = np.mean(filtered_recall_values)
    average_precision = np.mean(filtered_precision_values)

    print("Overall Average Recall:", average_recall)
    print("Overall Average Precision:", average_precision)

    return {
        "recall": average_recall,
        "precision": average_precision,
    }
