# Machine Learning Pipeline for Raster Data

This repository contains a machine learning pipeline for working with raster data. The pipeline includes scripts for generating training samples, training a model, making predictions, and more. Below, you'll find information on the folder structure and how to use each script.

## Folder Structure

Your project directory should have the following structure:

```
ml_pipeline/
│
├── pickles_train_latest/
│   ├── band1.pkl
│   ├── band2.pkl
│   └── ...
│
├── pretrained_model/
│   ├── model.pkl
│   └── ...
│
├── scripts/
│   ├── generate_training_sample.py
│   ├── sample_raster.py
│   ├── training.py
│   └── prediction.py
│
├── config.json
├── README.md
└── requirements.txt
```

- **`pickles_train_latest/`**: This folder contains `.pkl` files for each band for the purpose of rescaling.
- **`pretrained_model/`**: This folder contains a pre-trained classification model.
- **`scripts/`**: This folder contains all the scripts needed for the pipeline.
  - **`generate_training_sample.py`**: Generates point shapefiles for each class from the label raster for training.
  - **`sample_raster.py`**: Uses input from `generate_training_sample.py` and rasterizes each point using the input stacked raster.
  - **`training.py`**: Used to train a model on the data generated.
  - **`prediction.py`**: Makes predictions using a pre-trained model and takes a config file as input.


## Prerequisites

1. Python 3.10.0
2. Required Python packages:
   - GDAL=3.5.0
   - json
   - numpy
   - rasterio
   - geopandas
   - pycaret
   - tqdm

You can install the required packages using the following command:
```bash
pip install numpy rasterio geopandas pycaret tqdm
```

Sure, I can help you update your README file to reflect the folder structure and provide clear instructions for running your pipeline. Here's your updated README:

---

## Workflow Steps

### 1. Generating Training Points

The script `generate_training_points.py` takes a raster dataset, randomly samples specific classes, and creates a GeoDataFrame containing the sampled points. The sampled points serve as training data for classification.

Usage:
```bash
python generate_training_points.py --raster_path /path/to/raster/file.tif --num_samples 100 --target_classes 1 2 3 --export_path /path/to/export.geojson
```

### 2. Preprocessing and Sampling Pixel Values

The script `sample_raster.py` reads a GeoDataFrame, reprojects it to match the CRS of a raster, samples pixel values from the raster at corresponding coordinates, and appends the pixel values as attributes to the GeoDataFrame.

Usage:
```bash
python sample_raster.py --shapefile /path/to/input_shapefile.shp --raster /path/to/raster/file.tif --output /path/to/output_shapefile.shp
```

### 3. Model Training using Training Points

The script `train_model.py` loads the GeoDataFrame generated in the first step, processes the data, sets up a PyCaret experiment, creates a classification model, and saves the trained model along with evaluation plots and reports.

Usage:
```bash
python train_model.py --config_file /path/to/config.json
```

Create a `config.json` file specifying paths, settings, and parameters for model training.

### 4. Prediction using Pretrained Model

The script `predict_with_model.py` uses a pretrained classification model to make predictions on input raster tiles. It saves the binary and probability prediction outputs.

Usage:
```bash
python predict_with_model.py --config_file /path/to/config.json
```

Create a `config.json` file specifying paths to the pretrained model, input tiles, and output directory.

## Configuration JSON File Sample

A `config.json` file is required for both model training and prediction. It should contain relevant paths, settings, and parameters.

```json
{
  "Paths": {
    "shapefile_path": "path/to/shapefile.shp",
    "pickle_dir": "path/to/global_stats_cache",
    "model_path": "path/to/pretrained/model.pkl",
    "input_tiles_dir": "path/to/input/tiles",
    "output_dir": "path/to/output/folder"
  },
  "ColumnsToDrop": ["column_to_drop1", "column_to_drop2"],
  "ColumnsOfInterest": {
    "columns": [0, 1, 2, 3]  
  },
  "TargetColumn": "target_column",
  "OrdinalCategories": [],
  "SessionID": 123,
  "ModelType": "rf",
  "ModelSavePath": "path/to/save/model.pkl",
  "ClassIndex": 1  
}
```

## Conclusion

This workflow provides a comprehensive set of scripts to preprocess raster data, generate training points, train classification models, and perform predictions. Customize the configuration, adjust parameters, and extend the scripts to suit your specific use case and data.

For any additional assistance or inquiries, feel free to contact singh.9616satyam@gmail.com.