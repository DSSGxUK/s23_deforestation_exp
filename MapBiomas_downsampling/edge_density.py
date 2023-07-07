import argparse
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine
from scipy import ndimage
from tqdm import tqdm
from scipy.ndimage import convolve

def compute_edge_density(raster_file, output_file, window_size):
    # Open the raster file
    with rasterio.open(raster_file) as src:
        # Calculate the number of windows in each dimension
        n_windows_x = src.width // window_size
        n_windows_y = src.height // window_size

        edge_density_data = np.zeros((n_windows_y, n_windows_x), dtype='float64')

        # Loop over the windows in the raster
        for wx in tqdm(range(n_windows_x), desc=f"Processing file: {raster_file}"):
            for wy in range(n_windows_y):
                # Read a window from the raster
                window = Window(wx * window_size, wy * window_size, window_size, window_size)
                data = src.read(1, window=window)

                # Apply the forest cover mask
                forest_cover = (200 <= data) & (data < 400)

                # Pad the forest cover mask with False values (non-forest)
                padded_cover = np.pad(forest_cover, pad_width=1, mode='constant', constant_values=True)

                # Count the number of edges by checking the four neighbors (N, S, E, W) for each forest cell
                edge_count = (~padded_cover[1:-1, 1:-1] & padded_cover[:-2, 1:-1]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[2:, 1:-1]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[1:-1, :-2]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[1:-1, 2:]).sum()

                # Compute the edge density (edges per pixel)
                edge_density = edge_count / (window_size * window_size)

                # Store the edge density in the edge density data
                edge_density_data[wy, wx] = edge_density

        # Update the transformation
        transform = src.transform * Affine.scale(window_size)

    # Write the edge density data to a new raster file
    with rasterio.open(output_file, 'w', driver='GTiff', height=edge_density_data.shape[0],
                       width=edge_density_data.shape[1], count=1, dtype=edge_density_data.dtype,
                       crs=src.crs, transform=transform) as dst:
        dst.write(edge_density_data, 1)


def main():
    parser = argparse.ArgumentParser(description='Generate a forest edge density map.')
    parser.add_argument('input_file', type=str, help='Path to the input .tif file.')
    parser.add_argument('output_file', type=str, help='Path to the output .tif file.')
    parser.add_argument('--grid_size', type=int, default=200, help='Grid size in pixels. Default is 200 (for a 6km grid with 30m pixels).')
    
    args = parser.parse_args()
    
    compute_edge_density(args.input_file, args.output_file, args.grid_size)

if __name__ == '__main__':
    main()
