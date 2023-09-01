import os
import glob
import subprocess
import argparse
from tqdm import tqdm

def reproject_and_resample_tif(tif_file, output_file, dst_crs, pixel_size, target_extent, overwrite):
    """
    Reproject and resample a given TIF file.
    """
    if overwrite or not os.path.exists(output_file):
        gdalwarp_cmd = [
            'gdalwarp', '-overwrite', '-t_srs', dst_crs, '-tr', str(pixel_size), str(pixel_size), '-r', 'near',
            '-te', *map(str, target_extent), '-tap', '-of', 'GTiff', '-co', 'COMPRESS=DEFLATE', 
            '-co', 'BIGTIFF=YES', '-co', 'ZLEVEL=1', tif_file, output_file
        ]
        subprocess.check_call(gdalwarp_cmd)

def cut_tif(input_tif, output_tif, shapefile, overwrite):
    """
    Cut the TIF file based on a shapefile.
    """
    if overwrite or not os.path.exists(output_tif):
        gdalwarp_cmd = [
            'gdalwarp', '-overwrite', '-cutline', shapefile, '-crop_to_cutline', '-of', 'GTiff',
            '-co', 'COMPRESS=DEFLATE', '-co', 'BIGTIFF=YES', '-co', 'ZLEVEL=1',
            input_tif, output_tif
        ]
        subprocess.check_call(gdalwarp_cmd)

def merge_tifs(tif_files, merged_tif, overwrite):
    """
    Merge multiple TIF files into one.
    """
    if overwrite or not os.path.exists(merged_tif):
        gdal_merge_cmd = ['gdal_merge.py', '-o', merged_tif, *tif_files]
        subprocess.check_call(gdal_merge_cmd)

def process_dir(input_dir, output_dir, shapefile, dst_crs, pixel_size, target_extent, overwrite):
    """
    Process directory containing TIF files: merge, reproject, resample, and cut.
    """
    tif_files = glob.glob(os.path.join(input_dir, '*.tif'))
    
    os.makedirs(output_dir, exist_ok=True)
    
    merged_tif = os.path.join(output_dir, 'merged.tif')
    merge_tifs(tif_files, merged_tif, overwrite)

    reprojected_and_resampled_tif = os.path.join(output_dir, 'reprojected_and_resampled.tif')
    reproject_and_resample_tif(merged_tif, reprojected_and_resampled_tif, dst_crs, pixel_size, target_extent, overwrite)

    cut_tif_file = os.path.join(output_dir, 'cut.tif')
    cut_tif(reprojected_and_resampled_tif, cut_tif_file, shapefile, overwrite)

def main(root_dir, output_dir, years, shapefile, dst_crs, pixel_size, target_extent, overwrite, preprocess_static):
    """
    Main function to process directories of TIF files based on year and other conditions.
    """
    for year in tqdm(years, desc='Processing years'):
        year_dirs = glob.glob(os.path.join(root_dir, f'*_{year}'))

        for year_dir in year_dirs:
            if os.path.isdir(year_dir):
                dir_name_parts = os.path.basename(year_dir).split('_')
                feature_name = "_".join(dir_name_parts[:-1])
                process_dir(year_dir, f'{output_dir}/Dynamic/{feature_name}/{year}', shapefile, dst_crs, pixel_size, target_extent, overwrite)

        if preprocess_static:
            static_dirs = glob.glob(os.path.join(root_dir, '*_static'))
            for static_dir in static_dirs:
                dir_name_parts = os.path.basename(static_dir).split('_')
                feature_name = "_".join(dir_name_parts[:-1])
                process_dir(static_dir, f'{output_dir}/Static/{feature_name}', shapefile, dst_crs, pixel_size, target_extent, overwrite)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process TIF files: reproject, cut, and tile for specific years.')
    parser.add_argument('--root_dir', type=str, default='', help='Root directory where the year folders are located.')
    parser.add_argument('--output_dir', type=str, default='', help='Output directory to store the results.')
    parser.add_argument('--shapefile', type=str, default='', help='Shapefile to cut the TIFs to.')
    parser.add_argument('--dst_crs', type=str, default='EPSG:3857', help='Destination CRS to reproject the TIFs to.')
    parser.add_argument('--pixel_size', type=int, default=30, help='Pixel size for the reprojected TIFs.')
    parser.add_argument('--target_extent', type=float, nargs='+', help='Target extent for all rasters [xmin, ymin, xmax, ymax].')
    parser.add_argument('--years', type=int, nargs='+', default=[], help='Years to process.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files/folders.')
    parser.add_argument('--preprocess_static', action='store_true', help='Preprocess static features.')

    args = parser.parse_args()

    main(args.root_dir, args.output_dir, args.years, args.shapefile, args.dst_crs, args.pixel_size, args.target_extent, args.overwrite, args.preprocess_static)
