import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import random
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

# Function to randomly sample a specific class from the raster
def random_sample_class(args):
    raster_path, target_class, num_samples = args
    with rasterio.open(raster_path) as src:
        band = src.read(1)
        transform = src.transform
        crs = src.crs
        cols, rows = src.width, src.height

        sampled_points = []

        while len(sampled_points) < num_samples:
            random_row = random.randint(0, rows - 1)
            random_col = random.randint(0, cols - 1)
            pixel_value = band[random_row, random_col]

            if pixel_value == target_class:
                lon, lat = rasterio.transform.xy(transform, random_row, random_col)
                sampled_points.append((lon, lat, target_class))

        return sampled_points, crs

# Function to perform random sampling on the raster
def random_sample_raster(raster_path, num_samples_per_class, target_classes, export_path):
    num_processes = cpu_count()
    args_list = [(raster_path, target_class, num_samples_per_class) for target_class in target_classes]

    with Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap_unordered(random_sample_class, args_list), total=len(target_classes), desc="Sampling Classes"))

    all_sampled_points_flat = []
    for sampled_points, crs in results:
        all_sampled_points_flat.extend(sampled_points)

    # Create a GeoDataFrame from the sampled points
    gdf = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y, _ in all_sampled_points_flat], crs=crs)
    gdf['class'] = [cls for _, _, cls in all_sampled_points_flat]

    # Export the GeoDataFrame as a shapefile
    gdf.to_file(export_path)

    print(f"Sampling for all classes completed. Samples saved to {export_path}.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Randomly sample raster data and create a GeoDataFrame.")
    parser.add_argument("--raster_path", type=str, required=True, help="Path to the input raster file.")
    parser.add_argument("--num_samples", type=int, required=True, help="Number of samples per class.")
    parser.add_argument("--target_classes", type=int, nargs="+", required=True, help="List of target classes.")
    parser.add_argument("--export_path", type=str, required=True, help="Path to export the GeoDataFrame.")

    args = parser.parse_args()

    # Call the random_sample_raster function with parsed arguments
    random_sample_raster(args.raster_path, args.num_samples, args.target_classes, args.export_path)