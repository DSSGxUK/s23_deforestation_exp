# README

## Overview

This folder contains a script for calculating multi-year averages of deforestation data stored in .tif files. The script aggregates data over a specified time window, computes the average, and converts the result to hectares.

## Files

* `calculate_average.sh` - Bash script that performs the calculations to generate the multi-year averages. The script utilizes the GDAL library and `gdal_calc.py` tool for the calculations.

## Usage

### `calculate_average.sh`

This script takes four arguments:

start_year - The starting year for the calculation.
end_year - The ending year for the calculation.
time_window - The time window (in years) for the calculation.
input_dir_basename - The basename of the input directory containing the .tif files.

Before running the script, make sure to load the necessary modules:
```bash
module load GCCcore/11.3.0
module load Python/3.10.4
module load GCC/11.3.0 OpenMPI/4.1.4
module load GDAL/3.5.0
```

Then run the script by typing the following in your terminal:
```bash
./calculate_average.sh start_year end_year time_window input_dir_basename
```
Replace `start_year`, `end_year`, `time_window`, and `input_dir_basename` with the appropriate values.

The script creates an output directory for each year's range (e.g., output_2012-2016). If the directory does not exist, it will be created.

The output files are named after the unique basename found in each year's input directory, with _average.tif appended to it (e.g., base_name_average.tif).

Please note that this script assumes a specific directory and file structure. Ensure that your .tif files are organized correctly in the input directories for each year (e.g., `input_dir_basename_2012`, `input_dir_basename_2013`, etc.). 

## Dependencies

This script requires the GDAL module, specifically the `gdal_calc.py` tool. Make sure to load the GDAL module before running the script.

## Note

Be aware that running this script may be computationally intensive, especially for large datasets or long time windows. Make sure your environment has sufficient resources to handle this.
