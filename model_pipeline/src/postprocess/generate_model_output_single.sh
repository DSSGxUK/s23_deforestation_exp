#/bin/bash

# Arguments
model_name=$1      # E.g. - lr-01_FL-20_log
pred_dir=$2        # Directory containing predictions in tiles
prev_year_gt=$3    # Path to previous year ground truth
out_dir=$4         # Directory to save outputs
shp_file=$5        # Shapefile to cut the predictions to Amazon biome

# Variables
thresholds=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
resolutions=(900 3000 6000 9000 12000 15000 18000 21000 27000 33000 39000 45000 51000)

# Create output directory
mkdir -p $out_dir

# Create a list of all tiles
find $pred_dir -name "*.tif" > "${out_dir}/file_list.txt"

# Merge all predictions into a single file using gdalbuildvrt + gdal_translate
gdalbuildvrt -vrtnodata -1 -overwrite -input_file_list "${out_dir}/file_list.txt" "${out_dir}/merged_file.vrt"
gdal_translate -of GTiff -a_nodata -1 -outsize 113485 82298 "${out_dir}/merged_file.vrt" "${out_dir}/merged_file.tif"

# Multiply by forest cover map to remove pixels that were never forest
gdal_calc.py -A "${out_dir}/merged_file.tif" -B $prev_year_gt --outfile="${out_dir}/merged_file_fc-processed.tif" --calc="A*(B==0)" --NoDataValue=-1

# Cut the file to Amazon biome
gdalwarp -dstnodata -1 -cutline $shp_file -crop_to_cutline -of GTiff "${out_dir}/merged_file_fc-processed.tif" "${out_dir}/merged_file_fc-processed_cut.tif"

# Threshold the predictions
for threshold in "${thresholds[@]}"
do
    gdal_calc.py -A "${out_dir}/merged_file_fc-processed_cut.tif" --outfile="${out_dir}/merged_file_fc-processed_cut_${threshold}.tif" --calc="A>=${threshold}" --NoDataValue=-1

    # Convert maps to m^2
    gdal_calc.py -A "${out_dir}/merged_file_fc-processed_cut_${threshold}.tif" --outfile="${out_dir}/merged_file_fc-processed_cut_${threshold}_m2.tif" --calc="A*900" --NoDataValue=-1

    # Downsample to different resolutions
    for resolution in "${resolutions[@]}"
    do
        gdalwarp -tr $resolution $resolution -r sum -overwrite -ot Float32 -dstnodata -1 "${out_dir}/merged_file_fc-processed_cut_${threshold}_m2.tif" "${out_dir}/merged_file_fc-processed_cut_${threshold}_m2_${resolution}.tif"
    done
done

# Convert maps to m^2
gdal_calc.py -A "${out_dir}/merged_file_fc-processed_cut.tif" --outfile="${out_dir}/merged_file_fc-processed_cut_m2.tif" --calc="A*900" --NoDataValue=-1

# Downsample to different resolutions
for resolution in "${resolutions[@]}"
do
    gdalwarp -tr $resolution $resolution -r sum -overwrite -ot Float32 -dstnodata -1 "${out_dir}/merged_file_fc-processed_cut_m2.tif" "${out_dir}/merged_file_fc-processed_cut_m2_${resolution}.tif"
done