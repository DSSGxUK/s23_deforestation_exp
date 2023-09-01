# Deforestation risk prediction (EXPERIMENTS)
Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:

# Overview
This project aims to provide predictive models and tools for understanding deforestation risk in the Brazilian Amazon, targeting predictions for up to three years into the future. The project was conceived and executed over a span of three months, showing promising results and avenues for future work.

## Models

We employed two primary models for our prediction tasks:

- A Deep Learning model using UNet architecture, trained on the Mapbiomas dataset and some auxilary data.
- A Random Forest model.

These models were benchmarked against the Jurisdictional and Nested REDD+ (JNR) methodology, a widely-recognized standard for evaluating deforestation risk. The models are designed to predict both short-term (one year) and medium-term (three years) deforestation risk, although the three-year predictions currently don't perform as robustly as the one-year predictions.

## Features
- Google Earth Engine App: A user-friendly application to visualize the deforestation risk across various regions. [App link](https://gee-tool.projects.earthengine.app/view/dssg23-deforestation)
- Comprehensive Data Pipeline: Includes various jobs for data preparation, normalization, and feature engineering.
- UNet Model Pipeline: A dedicated pipeline for the deep learning UNet model that includes training, evaluation logging and output generation.
- Feature Ablation: Insights into the feature importances identified by the Deep Learning model.
- Modular Code Base: Code for each part of the pipeline and models is separately maintained for better readability and usability.
  
## Performance Metrics
For the deep learning model, a generalised (see below) F1 score of 0.4757 was achieved for three-year predictions, slightly underperforming the JNR benchmark of 0.5043. For one-year predictions, the F1 score stood at 0.3644 against the JNR score of 0.4372.

Next Steps
Future work could focus on increasing model capacity or sourcing more recent data to enhance performance. 

## The Continuous Precision and Recall Metrics
The following code contains the function to return the normalized continuous precision and recall values to validate the 5-year average benchmark and JNR.

## Benchmarks
 ### JNR
- [Creating and generating predictions using JNR Risk maps](./JNR/):
    - [1. Create Input](./JNR/1.%20Create%20Input/) : Process and obtain maps of forest cover change (FCC) for the required years
    - [2. Run JNR](./JNR/2.%20Run%20JNR/) : Run the JNR algorithm to obtain the risk maps
    - [3. Create Output](./JNR/3.%20Create%20Output/) : Create the deforestation prediction and ground truth maps using the risk maps
  
 ### 5-year-avg Benchmark
The ART/TREES-inspired benchmark computes the average of deforestation taking place in a 5-year window and uses that to predict the deforestation in 3 subsequent years in the future. 
It uses the [Mapbiomas](https://https://mapbiomas.org/en/download) dataset, and has been validated on 6x6 km validation grid.

## Data Pipeline
The [data_pipeline](./data_pipeline/) directory contains scripts and configurations for pre-processing, transforming, and sampling the data used in the experiments. It is designed to be modular and configurable, enabling the user to customize the data processing steps as needed.

## Deep Learning Model - UNet

The pipeline for the UNet model is implemented in the folder [model_pipeline](./model_pipeline/) and included functionality for training, testing and running feature ablation. The model is trained on the [Mapbiomas](https://https://mapbiomas.org/en/download) dataset and all the metrics are logged onto [wandb](https://wandb.ai/). 

## Additional Experiments
- Data preprocessing:
    - [Downsample features](./downsample_mapbiomas/) : process MapBiomas dataset over given time periods to get downsampled forest cover, deforestation and forest edge density maps
    - [Average values](./average_metric/) : script to run averaging over several tiles in parallel, while converting from 900m^2 to hectares.
- Creating JNR Risk maps:
    - [Create Forest Cover Change Map](./create_fcc_map/) : download, process and obtain maps of forest cover change (FCC) for the years 2000-2022 using Global Forest Change dataset
    - [Generate JNR Risk Map](./generate_jnr/) : obtain maps of the spatial risk of deforestation and forest degradation following the methodology of REDD+
- [k-Means Clustering](./PRODES_clustering/) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green 

