#!/bin/bash

# Variables
out_dir=$1                             # Output directory
start_year=$2                          # Start year in two digits, i.e. 13 for 2013
mid_year_1=$3                          # Mid year, same format as start year
mid_year_2=$(expr $mid_year_1 + 1)  
end_year=$4                            # End year, same format as start year

# Create the FCC map
gdal_calc.py -A ${out_dir}/merged_maps/merged_map_lossyear_final.tif -B ${out_dir}/merged_maps/merged_map_treecover2000_final.tif --calc="(A==0)*3*(B>0) + (A>=${start_year})*(A<=${mid_year_1})*1 + (A>=${mid_year_2})*(A<=${end_year})*2" --NoDataValue=0 --outfile ${out_dir}/merged_maps/merged_map_fcc-123_${start_year}-${end_year}.tif