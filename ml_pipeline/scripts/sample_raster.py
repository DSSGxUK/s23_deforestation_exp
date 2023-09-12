import geopandas as gpd
import rasterio
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import argparse

def sample_pixel_value(args):
    raster_path, coord = args
    with rasterio.open(raster_path) as src:
        return list(rasterio.sample.sample_gen(src, [coord]))[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample pixel values from a raster and append to a GeoDataFrame.")
    parser.add_argument("--shapefile", type=str, required=True, help="Path to the input shapefile.")
    parser.add_argument("--raster", type=str, required=True, help="Path to the raster file.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output shapefile with sampled pixel values.")

    args = parser.parse_args()

    # Load the input shapefile
    train_shp = gpd.read_file(args.shapefile)

    # Read the raster file path
    raster_path = args.raster

    # Reproject the shapefile to the raster's CRS
    src_crs = rasterio.open(raster_path).crs
    train_shp = train_shp.to_crs(src_crs)

    coord_list = [(x, y) for x, y in zip(train_shp["geometry"].x, train_shp["geometry"].y)]

    # Number of parallel processes
    num_processes = cpu_count()

    # Prepare arguments for parallel processing
    args_list = [(raster_path, coord) for coord in coord_list]

    with Pool(processes=num_processes) as pool:
        sampled_values = list(tqdm(pool.imap_unordered(sample_pixel_value, args_list), total=len(coord_list), desc="Sampling Raster"))

    for band_idx in range(len(sampled_values[0])):
        band_name = f"band_{band_idx + 1}_value"
        train_shp[band_name] = [sample[band_idx] for sample in sampled_values]

    # Save the GeoDataFrame with sampled pixel values
    train_shp.to_file(args.output)
