# Deforestation risk prediction (EXPERIMENTS)
Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:

# The Continuous Precision and Recall Metrics
The following code contains the function to return the normalized continuous precision and recall values to validate the 5-year average benchmark and JNR.

<img width="539" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/42a03ced-7bce-4dd4-8154-50b6cc79fcd8">

*Fig.1. Continuous Precision and Recall Formulae*

## Benchmarks
 ### JNR
- [Creating and generating predictions using JNR Risk maps](./JNR/):
    - [1. Create Input](./JNR/1.%20Create%20Input/) : Process and obtain maps of forest cover change (FCC) for the required years
    - [2. Run JNR](./JNR/2.%20Run%20JNR/) : Run the JNR algorithm to obtain the risk maps
    - [3. Create Output](./JNR/3.%20Create%20Output/) : Create the deforestation prediction and ground truth maps using the risk maps
    - 
 ### 5-year-avg Benchmark
The ART/TREES-inspired benchmark computes the average of deforestation taking place in a 5-year window and uses that to predict the deforestation in 3 subsequent years in the future. 
It uses the [Mapbiomas](https://https://mapbiomas.org/en/download) dataset, and has been validated on 6x6 km validation grid.
<img width="573" alt="image" src="https://github.com/DSSGxUK/s23_deforestation_exp/assets/83265366/04a2b214-13f6-4cdc-acd3-0de825f3a567">

*Fig.2. Avg 5-year benchmark diagram*
 ### Additional Experiments
 
- Additional experiments
    - [k-Means Clustering](./PRODES_clustering/) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green
