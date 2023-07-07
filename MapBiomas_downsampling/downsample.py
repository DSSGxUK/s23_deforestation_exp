import argparse
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine
from tqdm import tqdm

def aggregate_deforestation(raster_file, output_file, window_size):
    # Open the raster file
    with rasterio.open(raster_file) as src:
        # Calculate the number of windows in each dimension
        n_windows_x = src.width // window_size
        n_windows_y = src.height // window_size
        
        aggregated_data = np.zeros((n_windows_y, n_windows_x), dtype='uint32')
        
        # Loop over the windows in the raster
        for wx in tqdm(range(n_windows_x), desc=f"Processing file: {raster_file}"):
            for wy in range(n_windows_y):
                # Read a window from the raster
                window = Window(wx * window_size, wy * window_size, window_size, window_size)
                data = src.read(1, window=window)
                
                # Check for deforestation class
                mask = ((400 <= data) & (data < 500)) | ((600 <= data) & (data < 700)) 

                # Sum up the deforestation pixels
                aggregated_data[wy, wx] = np.sum(mask)
        
        # Update the transformation
        transform = src.transform * Affine.scale(window_size)
    
    # Write the aggregated data to a new raster file
    with rasterio.open(output_file, 'w', driver='GTiff', height=aggregated_data.shape[0],
                       width=aggregated_data.shape[1], count=1, dtype=aggregated_data.dtype,
                       crs=src.crs, transform=transform) as dst:
        dst.write(aggregated_data, 1)

def main():
    parser = argparse.ArgumentParser(description='Aggregate deforestation data into grids.')
    parser.add_argument('input_file', type=str, help='Path to the input .tif file.')
    parser.add_argument('output_file', type=str, help='Path to the output .tif file.')
    parser.add_argument('--grid_size', type=int, default=200, help='Grid size in pixels. Default is 200 (for a 6km grid with 30m pixels).')
    
    args = parser.parse_args()
    
    aggregate_deforestation(args.input_file, args.output_file, args.grid_size)

if __name__ == '__main__':
    main()
