#!/bin/bash

# Arguments
year=$1
defor_map=$2
out_dir=$3
downsample_size=$4

# Create output directory if it does not exist
mkdir -p $out_dir

# Extract for a particular year (e.g. 2019) the forest loss pixels
gdal_calc.py -A $defor_map --calc="A*900" --outfile ${out_dir}/merged_map_brazil_forestlossyear-$((year-2000))_m2.tif --type=Float32 --NoDataValue=0 --overwrite

# Downsample to given resolution
gdalwarp -r sum -tr $downsample_size $downsample_size -ot Float32 -dstnodata -1 ${out_dir}/merged_map_brazil_forestlossyear-$((year-2000))_m2.tif ${out_dir}/merged_map_brazil_forestlossyear-$((year-2000))_m2_downsampled-${downsample_size}.tif