#!/bin/bash

# Arguments
lossyear_map=$1
forestcover_map=$2
start_year=$3 
mid_year_1=$3
end_year=$5
out_dir=$6

# Convert years to 2-digit format
start_year=$(expr $start_year - 2000)
mid_year_1=$(expr $mid_year_1 - 2000)
mid_year_2=$(expr $mid_year_1 + 1)  
end_year=$(expr $end_year - 2000)

# Create the FCC map
gdal_calc.py -A $lossyear_map -B $forestcover_map --calc="(A>${end_year})*3 + (B>0)*3 + (A>=${start_year})*(A<=${mid_year_1})*1 + (A>=${mid_year_2})*(A<=${end_year})*2" --NoDataValue=0 --overwrite --outfile $out_dir/tmp.tif --hideNoData
gdal_calc.py -A $out_dir/tmp.tif --calc="(A>=3)*3 + (A<3)*A" --NoDataValue=0 --hideNoData --overwrite --outfile $out_dir/merged_map_fcc-123_${start_year}-${end_year}.tif

# Remove the temporary file
rm -rf $out_dir/tmp.tif