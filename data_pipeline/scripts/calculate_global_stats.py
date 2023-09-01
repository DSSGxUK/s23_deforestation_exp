import os
import argparse
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.features import geometry_mask
import geopandas as gpd
from shapely.geometry import box
import pickle
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def process_window(file_path, window, nodata, geometries=None):
    """
    Process a given window from a raster file and return statistics.

    Args:
        file_path (str): Path to the raster file.
        window (Window): Window object to process from the raster.
        nodata (float): Value indicating no data in the raster.
        geometries (list, optional): List of geometries for masking. Defaults to None.

    Returns:
        tuple: Comprising of sum of values, sum of squared values, number of valid data points, min value and max value.
    """

    with rasterio.open(file_path) as src:
        data = src.read(1, window=window).astype(np.float64)

        if geometries:
            geom_window = box(*src.window_bounds(window))
            valid_geometries = [geom for geom in geometries if geom.is_valid]
            intersected_geometries = [geom_window.intersection(geom) for geom in valid_geometries if geom_window.intersects(geom)]
            
            # Ensure only valid intersected geometries are used
            intersected_geometries = [geom for geom in intersected_geometries if geom.is_valid]

            # Check if intersected geometries list is empty
            if not intersected_geometries:
                return np.float64(0), np.float64(0), 0, np.inf, -np.inf
            
            mask = geometry_mask(
                intersected_geometries,
                transform=src.window_transform(window),
                invert=True,
                out_shape=data.shape)
            data[~mask] = nodata

        valid_data = data[data != nodata].astype(np.float64)
        valid_data = np.nan_to_num(valid_data)

        sum_x = np.sum(valid_data)
        sum_x2 = np.sum(valid_data**2)
        n = valid_data.size
        min_val = np.min(valid_data) if valid_data.size > 0 else np.inf
        max_val = np.max(valid_data) if valid_data.size > 0 else -np.inf

        return sum_x, sum_x2, n, min_val, max_val




def cache_global_stats(file_path, output_dir, file_num, geometries=None, chunk_size=2048, overwrite=False):
    """
    Cache global statistics of a given raster file.

    Args:
        file_path (str): Path to the raster file.
        output_dir (str): Directory to save the pickle files.
        file_num (int): Index number for the file (for naming).
        geometries (list, optional): List of geometries for masking. Defaults to None.
        chunk_size (int, optional): Size of the chunks to split the raster into. Defaults to 2048.
        overwrite (bool, optional): Overwrite existing cache files if present. Defaults to False.
    """
    cache_file_path = os.path.join(output_dir, f"{file_num}.pkl")
    print(f"Processing: {file_path}")

    if os.path.exists(cache_file_path) and not overwrite:
        with open(cache_file_path, 'rb') as cache_file:
            return pickle.load(cache_file)


    sum_x = np.float64(0)
    sum_x2 = np.float64(0)
    n = 0
    n_all = 0
    min_val = np.inf
    max_val = -np.inf

    with rasterio.open(file_path) as src:
        num_cols, num_rows = src.shape
        band_name = src.descriptions[0]
        nodata = src.nodatavals[0]

    windows = [(i, j, Window(j, i, min(chunk_size, num_cols - j), min(chunk_size, num_rows - i))) for i in range(0, num_rows, chunk_size) for j in range(0, num_cols, chunk_size)]
    
    if geometries:
        valid_geometries = [geom for geom in geometries if geom.is_valid]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_window, [file_path]*len(windows), [w for _, _, w in windows], [nodata]*len(windows), [valid_geometries]*len(windows)))

    for r in results:
        sum_x_single, sum_x2_single, n_single, min_val_single, max_val_single = r
        sum_x += sum_x_single
        sum_x2 += sum_x2_single
        n += n_single
        min_val = min(min_val, min_val_single)
        max_val = max(max_val, max_val_single)
    
    mean = sum_x / n
    std_dev = np.sqrt((sum_x2 / n) - (mean ** 2))


    print(f"File: {file_path}")
    print(f"Shape: {num_rows}x{num_cols}")
    print(f"No-data value: {nodata}")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std_dev}")
    print(f"Total valid data points: {n}")
    print(f"Total data points: {n_all}")
    print(f"Min value: {min_val}")
    print(f"Max value: {max_val}")
    print(f"Sum of all values: {sum_x}")
    print(f"Sum of squares of all values: {sum_x2}")
    

    with open(cache_file_path, 'wb') as cache_file:
        pickle.dump((mean, std_dev, min_val, max_val, band_name), cache_file)

def main(input_files, output_dir, shapefile_path=None, overwrite=False):
    """
    Main function to process a list of input raster files and cache their global statistics.

    Args:
        input_files (list): List of input .tif files to process.
        output_dir (str): Directory to save the pickle files.
        shapefile_path (str, optional): Path to the shapefile to use as a mask. Defaults to None.
        overwrite (bool, optional): Overwrite existing cache files if present. Defaults to False.
    """
    os.makedirs(output_dir, exist_ok=True)  # make sure the output directory exists
    print("Caching global stats...")

    geometries = None
    if args.shapefile_path:
        gdf = gpd.read_file(shapefile_path)
        geometries = gdf.geometry.tolist()
    
    print(f"Geometries: {geometries}")
    print(f"Shapefile path: {shapefile_path}")
    
    start_idx = 23
    for idx, file_path in enumerate(tqdm(input_files[start_idx:]), start=start_idx):
        cache_global_stats(file_path, output_dir, idx+1, geometries, overwrite=overwrite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process individual .tif files.')
    parser.add_argument('--input_files', nargs='+', default=[], help='Input .tif files to process')
    parser.add_argument('--output_dir', default='output', help='Directory to save the pickle files')
    parser.add_argument('--shapefile_path', default=None, help='Path to the shapefile to use as a mask')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing cache files if present')
    args = parser.parse_args()

    main(args.input_files, args.output_dir, shapefile_path=args.shapefile_path, overwrite=args.overwrite)

