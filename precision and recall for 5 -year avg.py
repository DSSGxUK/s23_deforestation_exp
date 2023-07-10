import os
import rasterio
import numpy as np

def calculate_average_recall_precision(image_dir, avg_image_dir):
    # Get the file names in the directories
    image_files = [file for file in os.listdir(image_dir) if not file.endswith('.tif.aux.xml')]
    avg_image_files = [file for file in os.listdir(avg_image_dir) if not file.endswith('.tif.aux.xml')]

    # Sort the file names to ensure matching pairs
    image_files.sort()
    avg_image_files.sort()

    # List to store recall and precision arrays without NaN
    filtered_recall_values = []
    filtered_precision_values = []

    # Process each matching image and average image file
    for i, (image_file, avg_image_file) in enumerate(zip(image_files, avg_image_files), start=1):
        # Construct the full file paths
        image_path = os.path.join(image_dir, image_file)
        avg_image_path = os.path.join(avg_image_dir, avg_image_file)

        # Open the image file
        dataset = rasterio.open(image_path)

        # Read the image data into a NumPy array
        image_array = dataset.read()
        arr = image_array * 0.003

        # If the image has multiple bands, you can access each band individually
        band1 = image_array[0]  # Access the first band (index 0)

        # Open the average image file
        dataset = rasterio.open(avg_image_path)

        # Read the average image data into a NumPy array
        avg_image_array = dataset.read()
        avg_arr = avg_image_array

        # If the image has multiple bands, you can access each band individually
        band = avg_image_array[0]

        min_arr = np.minimum(arr, avg_arr)

        # Calculate recall array
        recall = np.sum(np.nan_to_num(min_arr))/np.sum(np.nan_to_num(arr))

        # Flatten the recall array
        flattened_recall = recall.flatten()

        # Remove NaN values
        filtered_recall = flattened_recall[~np.isnan(flattened_recall)]

        # Append the filtered recall values to the list
        filtered_recall_values.extend(filtered_recall)

        # Calculate precision array
        precision = np.sum(np.nan_to_num(min_arr))/np.sum(np.nan_to_num(avg_arr))

        # Flatten the precision array
        flattened_precision = precision.flatten()

        # Remove NaN values
        filtered_precision = flattened_precision[~np.isnan(flattened_precision)]

        # Append the filtered precision values to the list
        filtered_precision_values.extend(filtered_precision)

        # print(f"Recall {i}:")
        # print(recall)
        # print('---')

        # print(f"Precision {i}:")
        # print(precision)
        # print('---')

    # Calculate the average recall and precision based on non-NaN values
    average_recall = np.mean(filtered_recall_values)
    average_precision = np.mean(filtered_precision_values)

    print("Overall Average Recall", average_recall)
    print("Overall Average Precision:", average_precision)

    return average_recall, average_precision

# Example usage
image_dir = '/kaggle/input/output-2020/output_2020'
avg_image_dir = '/kaggle/input/avg-2019/output_2014-2018'

average_recall, average_precision = calculate_average_recall_precision(image_dir, avg_image_dir)
