import os
import rasterio
from rasterio.windows import Window
from multiprocessing import Pool, cpu_count
import numpy as np
from tqdm import tqdm
import pickle


def cache_global_stats(band_name, pickle_dir):
    """
    Load global statistics for the specified band from a cached pickle file.

    :param band_name: Name of the band for which to retrieve statistics.
    :param pickle_dir: Directory containing the cached pickle files.
    :return: Global statistics for the band.
    """
    cache_file_path = os.path.join(pickle_dir, f'{band_name}.pkl')
    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'rb') as cache_file:
            return pickle.load(cache_file)
    else:
        raise FileNotFoundError(f"No cached data found for band {band_name} in directory {pickle_dir}")


def cut_tile(args):
    """
    Extract a tile from the input TIF file and process its bands based on global statistics.

    :param args: A tuple containing the arguments required for the operation.
    """
    i, j, window_size, input_tif, output_file, global_stats_dict, band_names = args
    window = Window(j * window_size, i * window_size, window_size, window_size)
    with rasterio.open(input_tif) as src:
        data = src.read(window=window)
        processed_data = process_bands_in_tile(data, band_names, global_stats_dict)
        with rasterio.open(output_file, 'w', driver='GTiff',
                           height=window.height, width=window.width,
                           count=processed_data.shape[0], dtype=str(processed_data.dtype),
                           crs=src.crs,
                           transform=src.window_transform(window)) as new_dataset:
            new_dataset.write(processed_data)


def process_bands_in_tile(tile, band_names, global_stats_dict):
    """
    Process and normalize each band in a tile based on global statistics.

    :param tile: A numpy array representing the tile.
    :param band_names: List of band names.
    :param global_stats_dict: Dictionary containing global statistics for each band.
    :return: Processed numpy array.
    """
    processed_bands = []
    num_bands = tile.shape[0]

    # Pad tile to standard size if required
    if tile.shape[1:] != (256, 256):
        pad_rows = 256 - tile.shape[1]
        pad_cols = 256 - tile.shape[2]
        tile = np.pad(tile, ((0, 0), (0, pad_rows), (0, pad_cols)), mode='constant')

    for b in range(num_bands):
        band_name = band_names[b]
        band = tile[b, :, :]
        mean, std, _, _, _ = global_stats_dict[band_name]
        
        band = np.nan_to_num(band)
        band_name_int = int(band_name)

        if 7 <= band_name_int < 10:
            band = (band > 0).astype(np.float64)

        if (7 <= band_name_int < 13) or (19 <= band_name_int < 26):
            processed_bands.append(band)
            continue

        if 13 <= band_name_int < 16:
            band[band == 0] = mean

        if (band_name_int == 26) or (1 <= band_name_int < 4):
            band = np.log1p(band)

        if std != 0:
            band = (band - mean) / std

        processed_bands.append(band)

    return np.array(processed_bands)


def create_tiles_based_on_mask(input_tif, output_dir, mask_file, window_size, pickle_dir, overwrite=False):
    """
    Create tiles from an input TIF file based on a specified mask.

    :param input_tif: Path to the input TIF file.
    :param output_dir: Directory to save the resulting tiles.
    :param mask_file: Optional mask file to determine tiles to create.
    :param window_size: Size of the window for tiling.
    :param pickle_dir: Directory containing pickle files with cached statistics.
    :param overwrite: Boolean flag to overwrite existing files/folders.
    """
    if not os.path.exists(output_dir) or overwrite:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Directory {output_dir} does not exist or overwrite is set to True.")

        mask = np.load(mask_file) if mask_file else np.ones((rasterio.open(input_tif).height // window_size,
                                                             rasterio.open(input_tif).width // window_size))

        num_windows_y, num_windows_x = mask.shape
        band_names = [str(i) for i in range(1, 27)]
        global_stats_dict = {band_name: cache_global_stats(band_name, pickle_dir) for band_name in band_names}

        tasks = [
            (i, j, window_size, input_tif, os.path.join(output_dir, f'tile_{i}_{j}.tif'), global_stats_dict, band_names)
            for i in range(num_windows_y)
            for j in range(num_windows_x)
            if mask[i, j] == 1
        ]

        with Pool(processes=cpu_count()) as p:
            list(tqdm(p.imap_unordered(cut_tile, tasks), total=len(tasks), desc='Cutting Tiles'))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create tiles from a TIF file based on a mask.')
    parser.add_argument('--input_tif', type=str, help='Input TIF file.')
    parser.add_argument('--output_dir', type=str, help='Output directory to store the tiles.')
    parser.add_argument('--pickle_dir', type=str, help='Directory for pickle files with cached stats.')
    parser.add_argument('--mask_file', type=str, default=None, help='Optional mask file. If not provided, all tiles will be created.')
    parser.add_argument('--window_size', type=int, default=256, help='Window size for creating the tiles.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files/folders.')

    args = parser.parse_args()

    create_tiles_based_on_mask(args.input_tif, args.output_dir, args.mask_file, args.window_size, args.pickle_dir, args.overwrite)
