# README

## Overview

This repository contains a script for computing multi-year averages of deforestation data stored in .tif files. The script aggregates data over a specified time window, averages the data, and converts the result to hectares.

## Files

* `average_deforestation.sh` - Bash script that calculates multi-year averages of deforestation data for each unique "basename" found in the output directories of each year. The script uses GDAL's `gdal_calc.py` tool to perform the calculations.

## Usage

### `average_deforestation.sh`

This script requires a single numeric argument that represents the time window (in years) over which to calculate the averages. For example, a time window of 5 would calculate averages over five-year periods starting from 2012 (i.e., 2012-2016, 2013-2017, etc).

Before running the script, make sure to load the necessary modules:
```bash
module load GCC/10.3.0  OpenMPI/4.1.1
module load GDAL/3.3.0
```

Then run the script by typing the following in your terminal:
```bash
bash average_deforestation.sh TIME_WINDOW
```
Where `TIME_WINDOW` is the desired time window for averaging (a positive integer).

The script creates an output directory for each year's range (e.g., `output_2012-2016`). If the directory doesn't exist, it will be created.

The output files will be named after the unique basename found in each year's output directory with `_average.tif` appended to it (e.g., `base_name_average.tif`).

## Dependencies

This script requires the GDAL module, specifically the `gdal_calc.py` tool. Make sure to load the GDAL module before running the script.

## Note

This script is designed for a specific directory and file structure. Ensure your .tif files are arranged correctly in the output directories for each year (e.g., `output_2012`, `output_2013`, etc). Each .tif file should be named with a 'basename' followed by an underscore and other identifying information (e.g., `base_name_something.tif`).

Be aware that running this script may be computationally intensive, especially for large datasets or long time windows. Make sure your environment has sufficient resources to handle this.
