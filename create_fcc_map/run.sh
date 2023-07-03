#!/bin/bash

# Variables
declare -a arr=("10N_080W" "10N_070W" "10N_060W" "10N_050W" "00N_080W" "00N_070W" "00N_060W" "00N_050W" "00N_040W" "10S_080W" "10S_070W" "10S_060W" "10S_050W" "10S_040W")
url="https://storage.googleapis.com/earthenginepartners-hansen/GFC-2022-v1.10/Hansen_GFC-2022-v1.10_"

# Input Arguments
out_dir=$1                             # Output directory
shp_file=$2                            # Shapefile
start_year=$3                          # Start year in two digits, i.e. 13 for 2013
mid_year_1=$4                          # Mid year, same format as start year
mid_year_2=$(expr $mid_year_1 + 1)  
end_year=$5                            # End year, same format as start year
nodata_val=$6                          # No data value

echo "Creating required directories in ${out_dir}..."
# Create the required directories
mkdir -p "${out_dir}/downloaded_tiles/lossyear"
mkdir -p "${out_dir}/downloaded_tiles/treecover2000"
mkdir -p "${out_dir}/merged_maps"

echo "Downloading tiles..."
# Download all the tiles for Brazil
for i in "${arr[@]}"
do
   wget "${url}treecover2000_${i}.tif" -P "${out_dir}/downloaded_tiles/treecover2000"
   wget "${url}lossyear_${i}.tif" -P "${out_dir}/downloaded_tiles/lossyear"
done

echo "Merging tiles..."
# Merge all the tiles into one
gdal_merge.py -o ${out_dir}/merged_maps/merged_map_lossyear.tif ${out_dir}/downloaded_tiles/lossyear/*.tif
gdal_merge.py -o ${out_dir}/merged_maps/merged_map_treecover2000.tif ${out_dir}/downloaded_tiles/treecover2000/*.tif

echo "Cropping the merged map to given shapefile: ${shp_file}"
# Crop the merged map to the shapefile
gdalwarp -overwrite -of GTiff -cutline $shp_file -cl amazon_border -crop_to_cutline -dstnodata $nodata_val ${out_dir}/merged_maps/merged_map_lossyear.tif ${out_dir}/merged_maps/merged_map_lossyear_clipped_noData-${nodata_val}.tif
gdalwarp -overwrite -of GTiff -cutline $shp_file -cl amazon_border -crop_to_cutline -dstnodata $nodata_val ${out_dir}/merged_maps/merged_map_treecover2000.tif ${out_dir}/merged_maps/merged_map_treecover2000_clipped_noData-${nodata_val}.tif

echo "Projecting the map to EPSG:102033..."
# Project the map to EPSG:102033ap_brazil_fcc-123_13-18.tif
gdalwarp --debug on --config GDAL_CACHEMAX 2048 -t_srs ESRI:102033 ${out_dir}/merged_maps/merged_map_lossyear_clipped_noData-${nodata_val}.tif ${out_dir}/merged_maps/merged_map_lossyear_clipped_noData-${nodata_val}_prj.tif
gdalwarp --debug on --config GDAL_CACHEMAX 2048 -t_srs ESRI:102033 ${out_dir}/merged_maps/merged_map_treecover2000_clipped_noData-${nodata_val}.tif ${out_dir}/merged_maps/merged_map_treecover2000_clipped_noData-${nodata_val}_prj.tif

echo "Creating the final forest loss map and tree cover map..."
# Copy and rename the final forest loss map
cp ${out_dir}/merged_maps/merged_map_lossyear_clipped_noData-${nodata_val}_prj.tif ${out_dir}/merged_maps/merged_map_lossyear_final.tif
cp ${out_dir}/merged_maps/merged_map_treecover2000_clipped_noData-${nodata_val}_prj.tif ${out_dir}/merged_maps/merged_map_treecover2000_final.tif

# Create the FCC map
gdal_calc.py -A ${out_dir}/merged_maps/merged_map_lossyear_final.tif -B ${out_dir}/merged_maps/merged_map_treecover2000_final.tif --calc="(A==0)*3*(B>0) + (A>=${start_year})*(A<=${mid_year_1})*1 + (A>=${mid_year_2})*(A<=${end_year})*2" --NoDataValue=0 --outfile ${out_dir}/merged_maps/merged_map_fcc-123_${start_year}-${end_year}.tif