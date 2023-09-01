#!/bin/bash

# Loop over all tif files in the current directory
for infile in *.tif; do
  # Generate the output file name
  outfile="${infile%.tif}_float32.tif"

  # Run gdal_translate to perform the conversion and compression
  gdal_translate -ot Float32 -co "COMPRESS=LZW" -co "BIGTIFF=YES" "$infile" "$outfile"
done
