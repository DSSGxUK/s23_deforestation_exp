# README

## Overview

This folder contains a set of scripts that perform downscaling of deforestation data stored in .tif files. The main idea behind the processing is to aggregate the deforestation data into grids, allowing for more efficient data processing and analysis.

## Files

* `run_on_tiles.sh` - Bash script that processes .tif files in a specified year range using the `downsample.py` script and stores the output in dedicated output directories.
* `run_on_tiles_edge_density.sh` - Bash script that calculates the forest edge density for .tif files in a specified year range using the `edge_density.py` script and stores the output in dedicated output directories.
* `downsample.py` - Python script that performs downsampling on .tif raster files, aggregating data into a grid of specified size.
* `edge_density.py` - Python script that reads a raster file, applies a mask for a given class and calculates the edge density of the given pixel class, i.e. the ratio of pixel edges to the total number of pixels in a given window.

## Usage

### `run_on_tiles.sh`

This bash script processes .tif files in a specified year range. It runs the downsample.py script on each .tif file and outputs the results in corresponding output directories.

To use this script, navigate to the directory containing the script and run the following command in your terminal:

```bash
./run_on_tiles.sh start_year end_year
```

Replace `start_year` and `end_year` with the desired range of years.

The script will create the output directory if it doesn't exist.

### `run_on_tiles_edge_density.sh`

Usage is analogous to run_on_tiles.sh

### `downsample.py`

This Python script performs downsampling on .tif raster files. It reads an input .tif file, processes the data into a specified grid size, and writes the results to a new .tif file.

To run this script standalone, navigate to the directory containing the script and run the following command in your terminal:

```bash
python3 downsample.py input_file output_file --grid_size GRID_SIZE --pixel-class PIXEL_CLASS
```

Where:

* `input_file` - Path to the input .tif file.
* `output_file` - Path to the output .tif file.
* `GRID_SIZE` - Optional. Grid size in pixels. Default is 200 (for a 6km grid with 30m pixels).
* `PIXEL_CLASS` - Optional. Pixel class to consider when downsampling.


### `edge_density.py`

Usage is analogous to edge_density.sh

## Note

Ensure that your environment has sufficient resources to run these scripts, as working with large raster files can be resource-intensive.
