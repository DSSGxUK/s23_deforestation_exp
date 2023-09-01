#!/bin/bash

find . -name "*.tif" -type f | while read tiffile
do
  echo "Processing $tiffile"
  gdal_translate -ot Float32 -co COMPRESS=LZW "$tiffile" "${tiffile%.tif}_compressed.tif"
  #mv "${tiffile%.tif}_compressed.tif" "$tiffile"
done
