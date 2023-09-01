import os
import json
import numpy as np
import rasterio
import geopandas as gpd
from pycaret.classification import load_model
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def cache_global_stats(band_name, pickle_dir):
    cache_file_path = os.path.join(pickle_dir, f'{band_name}.pkl')
    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'rb') as cache_file:
            return pickle.load(cache_file)
    else:
        raise FileNotFoundError(f"No cached data found for band {band_name} in directory {pickle_dir}")

def process_tile(config, tile_file, model):
    tile_path = os.path.join(config['Paths']['input_tiles_dir'], tile_file)

    with rasterio.open(tile_path) as src:
        profile = src.profile
        height, width = src.height, src.width

        selected_bands = src.read(config['ColumnsOfInterest']['columns'])
        flattened_bands = selected_bands.reshape(selected_bands.shape[0], -1).T

        predictions = model.predict(flattened_bands)
        prediction_scores = model.predict_proba(flattened_bands)[:, config['ClassIndex']]

        predictions = predictions.reshape((height, width))
        prediction_scores = prediction_scores.reshape((height, width))

        output_filename = f"{os.path.splitext(tile_file)[0]}_prediction.tif"
        binary_output_path = os.path.join(config['Paths']['output_dir'], 'binary_output', output_filename)
        prob_output_path = os.path.join(config['Paths']['output_dir'], 'probability_output', output_filename)

        tile_profile = profile.copy()
        tile_profile.update(count=1, dtype=np.uint8, compress='lzw')

        with rasterio.open(binary_output_path, 'w', **tile_profile) as dst:
            dst.write(predictions, 1)

        tile_profile.update(count=1, dtype=np.float32, compress='lzw')

        with rasterio.open(prob_output_path, 'w', **tile_profile) as dst:
            dst.write(prediction_scores, 1)

if __name__ == '__main__':
    config = load_config('config.json')
    model_path = config["Paths"]["model_path"]
    input_tiles_dir = config["Paths"]["input_tiles_dir"]
    output_dir = config["Paths"]["output_dir"]

    model = load_model(model_path)

    tile_files = os.listdir(input_tiles_dir)
    num_workers = cpu_count()

    with Pool(num_workers) as pool:
        list(tqdm(pool.imap(lambda tile: process_tile(config, tile, model), tile_files), total=len(tile_files)))

    print("Processing completed.")