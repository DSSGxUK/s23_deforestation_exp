import argparse
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine
from scipy import ndimage
from tqdm import tqdm
from scipy.ndimage import convolve
import enum

class PixelClass(enum.Enum):
    FOREST_COVER = "forest_cover"
    DEFORESTATION = "deforestation"

def compute_edge_density(raster_file, output_file, window_size, pixel_class: PixelClass):
    
    """
    Compute the forest edge density for a given raster file.
    This function reads a raster file, applies a mask for a given class and calculates 
    the edge density of the given pixel class, i.e. the ratio of pixel edges to the total 
    number of pixels in a given window. This is computed for each window of 
    size specified by 'window_size'. The results are then written to a new raster file.
    
    Args:
        raster_file (str): Path to the input .tif file.
        output_file (str): Path to the output .tif file.
        window_size (int): Grid size in pixels.
        pixel_class (PixelClass): Pixel class to consider when calculating edge density.
    
    Returns:
        None
    
    Raises:
        None
    """

    mask_factories = {
        PixelClass.FOREST_COVER: lambda data: (200 <= data) & (data < 400),
        PixelClass.DEFORESTATION: lambda data: ((400 <= data) & (data < 500)) | ((600 <= data) & (data < 700)),
    }
    generate_mask = mask_factories[pixel_class]

    with rasterio.open(raster_file) as src:
        n_windows_x = src.width // window_size
        n_windows_y = src.height // window_size

        edge_density_data = np.zeros((n_windows_y, n_windows_x), dtype='float64')

        for wx in tqdm(range(n_windows_x), desc=f"Processing file: {raster_file}"):
            for wy in range(n_windows_y):
                window = Window(wx * window_size, wy * window_size, window_size, window_size)
                data = src.read(1, window=window)

                mask = generate_mask(data)
                padded_cover = np.pad(mask, pad_width=1, mode='constant', constant_values=False)

                edge_count = (~padded_cover[1:-1, 1:-1] & padded_cover[:-2, 1:-1]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[2:, 1:-1]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[1:-1, :-2]).sum() + \
                             (~padded_cover[1:-1, 1:-1] & padded_cover[1:-1, 2:]).sum()

                edge_density = edge_count / (window_size * window_size)

                edge_density_data[wy, wx] = edge_density

        transform = src.transform * Affine.scale(window_size)

    with rasterio.open(output_file, 'w', driver='GTiff', height=edge_density_data.shape[0],
                       width=edge_density_data.shape[1], count=1, dtype=edge_density_data.dtype,
                       crs=src.crs, transform=transform) as dst:
        dst.write(edge_density_data, 1)

def main():
    parser = argparse.ArgumentParser(description='Generate a forest edge density map.')
    parser.add_argument('input_file', type=str, help='Path to the input .tif file.')
    parser.add_argument('output_file', type=str, help='Path to the output .tif file.')
    parser.add_argument('--grid_size', type=int, default=200, help='Grid size in pixels. Default is 200 (for a 6km grid with 30m pixels).')
    parser.add_argument(
        '--pixel-class', required=True, type=str, choices=[x.value for x in PixelClass],
        help='Pixel class to consider when calculating edge density.'
    )

    args = parser.parse_args()

    compute_edge_density(args.input_file, args.output_file, args.grid_size, PixelClass(args.pixel_class))

if __name__ == '__main__':
    main()
