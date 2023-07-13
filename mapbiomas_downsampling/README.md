# README

## Overview

This repository contains a set of scripts that perform downscaling of deforestation data stored in .tif files. The main idea behind the processing is to aggregate the deforestation data into grids, allowing for more efficient data processing and analysis.

## Files

* `run_on_tiles.sh` - Bash script that finds all .tif files in the directory for a specified year, passes each file to the Python script for processing, and stores the output in a dedicated output directory.
* `downsample.py` - Python script that processes .tif raster files and creates a downsampled version. The downsampling is done by aggregating data into a grid of specified size.
* `downsample_forest_cover.py`, `edge_density` - Are analogous to `downsample.py`.
* `run_on_tiles_fc.sh`, `run_on_tiles_edge_density.sh` - Are analogous to `run_on_tiles.sh`.

## Usage

### `run_on_tiles.sh`

This is a bash script that is designed to process .tif files in a given year's directory (e.g., `y_2021`). It runs the `downsample.py` script on each .tif file in the directory and outputs the result in the corresponding `output_year` directory. 

The script will create the output directory if it doesn't exist.

To run this script, navigate to the directory containing the script and type the following in your terminal:

```bash
bash downsample.sh
```

### `downsample.py`

This is a Python script that performs the actual downsampling. It reads a .tif file, processes the data into a specified grid size, and writes the result to a new .tif file.

The script uses Rasterio for reading and writing .tif files, and NumPy for data manipulation.

To run this script standalone, navigate to the directory containing the script and type the following in your terminal:

```bash
python3 downsample.py input_file output_file --grid_size GRID_SIZE
```

Where:

* `input_file` - Path to the input .tif file.
* `output_file` - Path to the output .tif file.
* `GRID_SIZE` - Optional. Grid size in pixels. Default is 200 (for a 6km grid with 30m pixels).


## Note

Ensure that your environment has sufficient resources to run these scripts, as working with large raster files can be resource-intensive.
