# Create JNR Predictions and Ground Truth Maps

The following script can be used to obtain deforestation predictions maps from the risk map obtained by following the methodology developed in the context of the Jurisdictional and Nested REDD+ ([JNR](https://verra.org/project/jurisdictional-and-nested-redd-framework/)) as well as the ground truth maps, in a downsampled format. The risk map can be seen below:

![image info](../assets/riskmap.png)

We use the output from the [riskmapjnr](https://github.com/ghislainv/riskmapjnr) package to obtain the predictions maps of deforestation using these scripts. We also employ the deforestation masks used earlier to create the ground truth deforestation maps.

## Usage

The scripts require the following input parameters which should be passed:
- `csv_file` : Path to the deforestation rate per category (defrate_per_cat_wsXX_XX.csv) obtained from the JNR algorithm
- `raster_file` : Path to the risk map file (riskmap_wsXX_XX.tif) obtained from the JNR algorithm
- `out_dir` : Path to the output directory where the final maps will be stored
- `num_year` : Number of years for which the predictions are required
- `year` : Year for which the ground truth is required
- `defor_map` : Path to the deforestation mask file for a given year (merged_map_defor_mask-$year.tif)
- `downsample_size` : Size of the final downsampled image (in pixels)

The folder contains two scripts, `create_pred.sh` and `create_gt.sh`. 

- `create_pred.sh` : This script will require two outputs from the JNR algorithm: `<output_dir>/fullhist/defrate_per_cat_ws<window-size>_<binning-strategy>.csv` and `<output_dir>/fullhist/riskmap_ws<window-size>_<binning-strategy>.tif`. These will be passed to this script as `csv_file` and `raster_file` arguments, respectively. This script will create deforestation prediction maps as well as forest cover predictions maps for the given `num_year`, in a downsampled size of `downsample_size`. To run this, simply perform:

  ```bash
  ./create_pred.sh <csv_file> <raster_file> <out_dir> <num_year> <downsample_size>
  ```

- `create_gt.sh` : This script will require deforestation mask (`defor_map`) of the year under consideration for the area of interest. This script will create deforestation ground truth maps for the given `year`, in a downsampled size of `downsample_size`. To run this, simply perform:

  ```bash
  ./create_gt.sh <year> <defor_map> <out_dir> <downsample_size>
  ```

## Points to note

- All the values are in $m^2$.

- Both the scripts require moderate amount of compute, depending on the size of the input and will take about an hour to run on the whole of Brazil, using about 24 GB of memory on a single CPU. Hence, it might be better to schedule it on a cluster. The job file for the same has also been provided and can be run as follows:

  ```bash
  sbatch job.exp
  ```
- Once the scripts have run, you can generate the prediction or ground truth maps for any downsampled size by simply running the following
  - For predictions maps:

    ```bash
    gdalwarp -r sum -tr $downsample_size $downsample_size -ot Float32 -dstnodata -1 ${out_dir}/pred_defor_year-${j}.tif ${out_dir}/pred_defor_year-${j}_downsampled-${downsample_size}.tif 
    ```
  - For ground truth maps:

    ```bash
    gdalwarp -r sum -tr $downsample_size $downsample_size -ot Float32 -dstnodata -1 ${out_dir}/merged_map_brazil_forestlossyear-$((year-2000))_m2.tif ${out_dir}/merged_map_brazil_forestlossyear-$((year-2000))_m2_downsampled-${downsample_size}.tif
    ```

## References

The scripts mainly utilise the [`GDAL`](https://gdal.org/) library.