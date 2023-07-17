# Deforestation risk prediction (EXPERIMENTS)
Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:
<<<<<<< HEAD
## Benchmarks
### JNR
=======


# The Continuous Precision and Recall Metrics
The following code contains the function to return the normalized continuous precision and recall values to validate the 5-year average benchmark and JNR.

<img width="539" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/42a03ced-7bce-4dd4-8154-50b6cc79fcd8">

*Fig.1. Continuous Precision and Recall Formulae*

## Benchmarks
 ### JNR
>>>>>>> main
- Creating JNR Risk maps:
    - [Create Forest Cover Change Map](./create_fcc_map/) : download, process and obtain maps of forest cover change (FCC) for the years 2000-2022 using Global Forest Change dataset
    - [Generate JNR Risk Map](./generate_jnr/) : obtain maps of the spatial risk of deforestation and forest degradation following the methodology of REDD+

<<<<<<< HEAD

### 5-year Average Benchmark
The ART/TREES-inspired benchmark computes the average of deforestation taking place in a 5-year window and uses that to predict the deforestation in 3 subsequent years in the future.


<img width="573" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/ab51adb5-19ad-4aa9-87f5-1351f4a7f6f1">

_Fig.1. Avg 5-year benchmark diagram_
## Metrics

The following code contains the function to return the normalized continuous precision and recall values to validate the 5-year average benchmark and JNR. 


<img width="541" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/5cf0db08-ba78-4ca5-8ff4-c6a3687f004a">

_Fig.2. Continuous Precision and Recall Formulae_

## Additional Experiments
Additional experiments
=======
 ### 5-year-avg Benchmark
The ART/TREES-inspired benchmark computes the average of deforestation taking place in a 5-year window and uses that to predict the deforestation in 3 subsequent years in the future. 
It uses the [Mapbiomas](https://https://mapbiomas.org/en/download) dataset, and has been validated on 6x6 km validation grid.
<img width="573" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/04a2b214-13f6-4cdc-acd3-0de825f3a567">

*Fig.2. Avg 5-year benchmark diagram*
 ### Additional Experiments
 
- Additional experiments
>>>>>>> main
    - [k-Means Clustering](./PRODES_clustering/) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green
 
