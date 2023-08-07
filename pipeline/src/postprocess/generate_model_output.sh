model_name="lr-01_FL-20_log_itr2"
pred_dir="/home/shared/dssg23-deforestation/model_checkpoints/preds_${model_name}"
gt_dir="/home/shared/dssg23-deforestation/mapbiomas-deforest/standartization_pipeline/Test_Data/Dynamic/y"
out_dir="/home/shared/dssg23-deforestation/model_checkpoints/outputs/preds_${model_name}/pred_2015"
prev_year="2014"

# Variables
thresholds=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
resolutions=(900 3000 6000 9000 12000 15000 18000 21000 27000 33000 39000 45000 51000)

mkdir -p $out_dir

# Create a list of all tiles
find $pred_dir -name "*.tif" > "${out_dir}/file_list.txt"

# Merge all predictions into a single file using gdalbuildvrt + gdal_translate
gdalbuildvrt -vrtnodata -1 -overwrite -input_file_list "${out_dir}/file_list.txt" "${out_dir}/merged_file.vrt"
gdal_translate -of GTiff -a_nodata -1 -outsize 113408 82176 "${out_dir}/merged_file.vrt" "${out_dir}/merged_file.tif"
rm "${out_dir}/merged_file.vrt"

# Multiply by forest cover map to remove pixels that were never forest
gdal_calc.py -A "${out_dir}/merged_file.tif" -B "${gt_dir}/${prev_year}/cut.tif" --outfile="${out_dir}/merged_file_fc-processed.tif" --calc="A*(B==0)" --NoDataValue=-1

# Threshold the predictions
for threshold in "${thresholds[@]}"
do
    gdal_calc.py -A "${out_dir}/merged_file_fc-processed.tif" --outfile="${out_dir}/merged_file_fc-processed_${threshold}.tif" --calc="A>=${threshold}" --NoDataValue=-1
done

# Convert maps to m^2
gdal_calc.py -A "${out_dir}/merged_file_fc-processed.tif" --outfile="${out_dir}/merged_file_fc-processed_m2.tif" --calc="A*900" --NoDataValue=-1

# Upsample to different resolutions
for resolution in "${resolutions[@]}"
do
    gdalwarp -tr $resolution $resolution -r sum -overwrite -ot Float32 -dstnodata -1 "${out_dir}/merged_file_fc-processed_m2.tif" "${out_dir}/merged_file_fc-processed_m2_${resolution}.tif"
done