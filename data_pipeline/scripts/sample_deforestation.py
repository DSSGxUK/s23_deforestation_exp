import numpy as np
import rasterio
from rasterio.windows import Window
import argparse
import math


def generate_mask(input_files, output_mask, window_size):
    """
    Generate a mask from a list of input TIF files.

    :param input_files: List of paths to input TIF files.
    :param output_mask: Path to save the generated mask.
    :param window_size: Window size for processing the TIFs.
    """
    # Initialize masks as None
    masks = None

    for input_file in input_files:
        # Open the tiff file
        with rasterio.open(input_file) as src:
            img_width, img_height = src.shape
            print(f"Image size: {img_height} rows x {img_width} cols")

            num_windows_x = math.ceil(img_width / window_size)
            num_windows_y = math.ceil(img_height / window_size)
            print(f"Number of windows: {num_windows_y} rows x {num_windows_x} cols")

            if masks is None:
                masks = np.zeros((num_windows_y, num_windows_x), dtype=bool)

            mean = 0
            anomalies = 0

            for i in range(num_windows_y):
                for j in range(num_windows_x):
                    window = Window(j * window_size, i * window_size, window_size, window_size)
                    data = src.read(1, window=window)

                    if data.size == 0:
                        anomalies += 1
                        continue
                    
                    mask_condition = data == 1
                    masks[i, j] |= np.any(mask_condition)
                    if masks[i, j]:
                        mean += np.mean(mask_condition)

            print(f"Number of anomalies: {anomalies}")
            print(f"Sum: {mean}")
            print(f"Normalized Mean: {mean / np.sum(masks)}")
            print(f"Mask 1's Ratio: {np.sum(masks) / np.size(masks)}")

    np.save(output_mask, masks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate mask from list of TIF files.')
    parser.add_argument('--input_files', type=str, nargs='+', help='List of input TIF files.')
    parser.add_argument('--output_mask', type=str, help='Output file to save the mask.')
    parser.add_argument('--window_size', type=int, default=256, help='Window size for processing the TIFs.')

    args = parser.parse_args()

    generate_mask(args.input_files, args.output_mask, args.window_size)
