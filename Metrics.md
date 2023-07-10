# The Continuous Precision and Recall Metrics
The following code contains the function to return the normalized continuous precision and recall values to validate the 5-year average benchmark and JNR.

<img width="539" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/42a03ced-7bce-4dd4-8154-50b6cc79fcd8">

*Fig.1. Continuous Precision and Recall Formulae*

## Brief of the 5-year Average Benchmark
The ART/TREES-inspired benchmark computes the average of deforestation taking place in a 5-year window and uses that to predict the deforestation in 3 subsequent years in the future. 
It uses the [Mapbiomas](https://https://mapbiomas.org/en/download) dataset, and has been validated on 6x6 km validation grid.
<img width="573" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/04a2b214-13f6-4cdc-acd3-0de825f3a567">

*Fig.2. Avg 5-year benchmark diagram*
## Calculated Metrics for Precision and Recall
The derived values of precision and recall can be plotted as follows:


<img width="440" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/2aaf457e-792d-48d4-ab0a-037cc7c5089a">

*Fig.3. Precision Plot*

<img width="427" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/2ea285b2-67a1-4266-829c-51fbfaba77fe">

*Fig.4. Recall Plot*

Here, the Start Year denotes the year_1 worth of predictions. 
For ex: Start Year : 2017 would mean that year_1 was 2017 for that case, year_2 was 2018 and year_3 was 2019.

## Requirements
The `rasterio` package (tested on Python > 3.10) must be installed. You can install it from PyPi as:

`!pip install rasterio`

## Usage
The following parameters need to be specified:
1. `image_dir`: Path to original deforestation
2. `avg_image_dir`: Path to predicted deforestation


