import os
import numpy as np
import rasterio
from mpi4py import MPI
from rasterio.windows import Window
import pickle
import argparse

def cache_global_stats(band_name, pickle_dir):
    """
    Retrieve cached statistics for the given band from the specified directory.

    :param band_name: Name of the band.
    :param pickle_dir: Directory containing the cached statistics.
    :return: Tuple containing the cached statistics.
    """
    cache_file_path = os.path.join(pickle_dir, f'{band_name}.pkl')
    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'rb') as cache_file:
            return pickle.load(cache_file)
    else:
        raise FileNotFoundError(f"No cached data found for band {band_name} in directory {pickle_dir}")

def cut_tile(args):
    """
    Slice a tile from the given raster file, process its bands, and save to the specified output.

    :param args: Tuple containing parameters necessary for cutting and processing.
    """
    i, j, window_size, input_tif, output_file, global_stats_dict, band_names = args
    window = Window(j*window_size, i*window_size, window_size, window_size)
    with rasterio.open(input_tif) as src:
        data = src.read(window=window)
        processed_data = process_bands_in_tile(data, band_names, global_stats_dict)
        
        with rasterio.open(output_file, 'w', driver='GTiff',
                           height=window.height, width=window.width,
                           count=processed_data.shape[0], dtype=str(processed_data.dtype),
                           crs=src.crs, transform=src.window_transform(window)) as new_dataset:
            new_dataset.write(processed_data)

def process_bands_in_tile(tile, band_names, global_stats_dict):
    """
    Process bands in a tile according to predefined normalization techniques.

    :param tile: 3D numpy array representing the bands in the tile.
    :param band_names: List of band names.
    :param global_stats_dict: Dictionary with global statistics for normalization.
    :return: Processed 3D numpy array.
    """
    processed_bands = []
    num_bands = tile.shape[0]
    
    # Pad the entire tile if its dimensions are not [num_bands, 256, 256]
    if tile.shape[1:] != (256, 256):
        pad_rows = 256 - tile.shape[1]
        pad_cols = 256 - tile.shape[2]
        tile = np.pad(tile, ((0, 0), (0, pad_rows), (0, pad_cols)), mode='constant')
    
    for b in range(num_bands):
        band_name = band_names[b]  # Get band name
        band = tile[b, :, :]  # Get band data
        mean, std, _, _, _ = global_stats_dict[band_name]
        
        # Convert NaNs to zero
        band = np.nan_to_num(band)
        
        band_name_int = int(band_name)
        
        if 7 <= band_name_int < 10:
            band = (band > 0).astype(np.float64)
        
        if (7 <= band_name_int < 13) or (19 <= band_name_int < 26):
            processed_bands.append(band)
            continue
        
        if 13 <= band_name_int < 16:
            # Replace zeros in band with the mean_value
            band[band == 0] = mean
        
        # Apply log transformation if band name is "26" or (1 <= int(band_name) and int(band_name) < 4)
        if (band_name_int == 26) or (1 <= band_name_int < 4):
            band = np.log1p(band)  # Apply logarithmic transformation
        
        # Apply standardization
        if std != 0:
            band = (band - mean) / std
        
        processed_bands.append(band)
    
    return np.array(processed_bands)

def create_tiles_based_on_mask(input_tif, output_dir, mask_file, window_size, pickle_dir, overwrite=False):
    """
    Create tiles from the input raster based on an optional mask. 
    Tiles are processed in parallel using MPI.

    :param input_tif: Path to input raster file.
    :param output_dir: Directory to save output tiles.
    :param mask_file: Optional path to mask file.
    :param window_size: Size of the tiles to cut.
    :param pickle_dir: Directory with cached statistics.
    :param overwrite: If true, overwrite existing tiles.
    """
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()

    if not os.path.exists(output_dir) or overwrite:
        os.makedirs(output_dir, exist_ok=True)

        if mask_file:
            mask = np.load(mask_file)
        else:
            with rasterio.open(input_tif) as src:
                mask = np.ones((src.height // window_size, src.width // window_size))

        band_names = [str(i) for i in range(1, 27)]
        global_stats_dict = {band_name: cache_global_stats(band_name, pickle_dir) for band_name in band_names}
        
        tasks = [
            (i, j, window_size, input_tif, os.path.join(output_dir, f'tile_{i}_{j}.tif'), global_stats_dict, band_names)
            for i in range(mask.shape[0])
            for j in range(mask.shape[1])
            if mask[i, j]
        ]
        tasks_per_core = len(tasks) // size
        start_idx, end_idx = rank * tasks_per_core, rank * tasks_per_core + tasks_per_core
        
        # Iterate over tasks and run cut_tile
        for task in tasks[start_idx:end_idx]:
            cut_tile(task)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create tiles from a TIF file based on a mask.')
    parser.add_argument('--input_tif', type=str, help='Input TIF file.')
    parser.add_argument('--output_dir', type=str, help='Output directory to store the tiles.')
    parser.add_argument('--pickle_dir', type=str, help='Directory for pickle files with cached stats.')
    parser.add_argument('--mask_file', type=str, default=None, help='Optional mask file.')
    parser.add_argument('--window_size', type=int, default=256, help='Tile size.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing tiles.')

    args = parser.parse_args()
    create_tiles_based_on_mask(args.input_tif, args.output_dir, args.mask_file, args.window_size, args.pickle_dir, args.overwrite)
