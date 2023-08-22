#/bin/bash

# Arguments
in_file=$1              # Path to ground truth map
out_dir=$2              # Directory to save outputs

# Variables
resolutions=(900 3000 6000 9000 12000 15000 18000 21000 27000 33000 39000 45000 51000)

# Create output directory and copy original file
mkdir -p $out_dir
cp $in_file $out_dir/orig.tif

# Convert to m^2
gdal_calc.py -A $out_dir/orig.tif --calc="900*(A>0) + (A<0)*(-1)" --outfile="${out_dir}/gt_m2_30m.tif" --overwrite --NoDataValue=-1

# Downsample to different resolutions
for resolution in "${resolutions[@]}"
do
    gdalwarp -tr $resolution $resolution -r sum -overwrite -ot Float32 -srcnodata -1 -dstnodata -1 "${out_dir}/gt_m2_30m.tif" "${out_dir}/gt_m2_${resolution}m.tif"
done