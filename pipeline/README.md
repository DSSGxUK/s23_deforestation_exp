# Modelling Pipeline

This folder contains the scripts used to run the modelling pipeline.

## Directory Structure

```
pipeline
|
├── README.md                       <- The top-level README containing instructions to reproduce the project
│
└── src                             <- Source code for use in this project.
    |
    ├── main.py                     <- Entry point to run the project
    ├── job.exp                     <- SLURM job file to run the project on a cluster
    │
    ├── conf                        <- Configuration file, e.g., for logging, data loading, models etc.
    |   └── default.json            <- Default configuration for model3
    │
    ├── data                        <- Scripts to create dataset and dataloaders
    │   ├── __init__.py  
    |   └── dataloader.py   
    │
    ├── models                      <- Scripts related to modelling 
    │   ├── __init__.py  
    |   ├── loss.py                 <- Loss functions for different models     
    |   └── unet_model.py
    │
    ├── utility                     <- Utility functions required for logging, evaluating and initialising wandb
    │   ├── __init__.py  
    |   ├── initialise.py   
    |   ├── logging.py     
    |   └── metrics.py
    │
    ├── engine                      <- Scripts to train, test and interpret models
    │   ├── __init__.py  
    │   ├── trainer.py              <- Script to train a model
    │   ├── tester.py               <- Script to test a model
    │   └── feature_ablation.py     <- Script for running feature ablation
    │
    └── post_process                <- Scripts to post process model outputs and generate metrics
        ├── generate_gt.sh
        ├── generate_model_output_single.sh
        └── evalaute.py
```

## Requirements

### Software setup

You will need several dependencies (most specifically `torch==1.10.0+cu111` and `torchvision==0.11.0+cu111`) to run the script. The best way to install all the requirements is to create a Python (`>=3.8.6`) virtual environment.

```bash
# Create virtual environment
python3 -m venv dl_env
source dl_env/bin/activate

# Install PyTorch
pip3 install torch==1.10.0+cu111 torchvision==0.11.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install wandb==0.13.1 rasterio tqdm scikit-learn
```

This version is not currently on Avon and hence you will need to install it manually, and additionally load some modules.

```bash
# Load modules
module load GCC/10.2.0  CUDA/11.1.1  OpenMPI/4.0.5

# Create virtual environment
python3 -m venv dl_env
source dl_env/bin/activate

# Install PyTorch
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install wandb==0.13.1 rasterio tqdm scikit-learn
```

### Data setup

The data should be in tiles with different folders for input data and ground truth, having the same filename for corresponding files. The ground should be encoded in the following manner:
- 1 : Deforested
- 0 : Not deforested
- -1 : Never forested

The paths should be setup in the config file (`x_path`, `y_path` specifically). Other important config parameters will be explained in the next section.

## Configuration file

```json
{
    "data" : {

        "dataset" : {
            // Paths to input data and ground truth
            "x_path" : "path/to/input/data",
            "y_path" : "path/to/ground/truth/data",
            
            // Bool variable to return file name of tiles in dataloader
            "return_info" : false
        },

        "dataloader" : {
            "batch_size" : 8,
            "shuffle" : true,
            "num_workers" : 4,
            "pin_memory" : true
        },

        "validation_split" : 0.2,
        "ignore_index" : -1,

        // List of features to be used in the model with the following format:
        // [feature_name, no. of bands, baseline value of each band]
        // The baseline value is used in feature ablation (see that section for more info)
        "data_description" : [
            ["proximity_log", 3, 1.699707773203376, 1.7019313645609526, 1.7032906650301076],
            ["edge_density", 3, 0, 0, 0],
            ["mining", 3, 0, 0, 0],
            ["agriculture_and_pasture", 3, 0, 0, 0],
            ["areas_indigenous", 1, 0],
            ["areas_protected", 1, 0],
            ["distance_roads_log", 1, 1.63270539374704]
        ]
    },

    // Model, optimizer and criterion parameters
    "modelling" : {
        "model" : {
            "name" : "UNet",
            "in_channels" : 15,
            "out_channels" : 1
        },
        "optimizer" : {
            "name" : "Adam",
            "lr" : 0.01
        },
        "criterion" : {
            // The loss function can be "DiceLoss", "NLLLoss" or "FocalLoss"
            "name" : "FocalLoss",
            "params" : {
                "gamma" : 2,
                "weight" : [1, 20]
            }
        }
    },

    // Engine parameters
    "engine" : {
        // mode can be "train", "test" or "feature_ablation"
        "mode" : "train",
        "epochs" : 30,
        // Frequency to calculate metrics on validation set
        "evaluation_interval" : 5000,
        "num_top_fa_features" : 3,
        "feature_ablation_out_csv" : "/home/shared/dssg23-deforestation/feature_ablation_out.csv"
    },

    "logging" : {
        "ckp_dir" : "/home/shared/dssg23-deforestation/model_checkpoints/checkpoints_lr-01_FL-20_log/",
        // Frequency to save model checkpoints
        "ckp_save_interval" : 5000,
        // Wandb parameters
        "wandb_project" : "dssgx-deforestation",
        "wandb_name" : "lr-01_FL-20_log",
        "wandb_id" : null,
        "wandb_watch_freq" : 100,
        // Path to save predictions (used in case of test/feature_ablation mode)
        "pred_dir" : "/home/shared/dssg23-deforestation/model_checkpoints/preds_lr-01_FL-20_log/pred_15-17"
    },

    "seed" : 0,
    "device" : "cuda",

    "threshold" : 0.5,

    // Must be specified in case of test/feature_ablation mode
    "restore_checkpoint" : false,
    "pretrained_weights" : null
}
```

## Usage

### Training

We make use of the UNet architecture for training. Once the paths have been specified in the config file, you can run the following command to train the model.

```bash
python3 main.py --config-file="./conf/default.json"
```

The checkpoints are saved in the folder `ckp_dir` and are saved every `ckp_save_interval` iterations. The model is evaluated on the validation set every `evaluation_interval` iterations. The metrics are logged onto WandB.

### Testing

To test the model, you need to specify the path to the model checkpoint in the config file and change the mode to test. You can then run the following command to test the model.

```bash
python3 main.py --config-file="./conf/default.json"
```

This will save the predictions in the folder `pred_dir`. The predictions are saved as GeoTIFF files.  

### Evaluation 

**Note:** This section is only applicable for predicting one year into the future, i.e., single band data.

In order to evalaute, we need to process the predictions to get the final deforestation map. This is done by running the following command. Here, `model_name` is the name of the model, `pred_dir` is the path to the folder containing the predictions, `prev_year_gt` is the path to the ground truth of the previous year, `output_dir` is the path to the folder where the final deforestation map will be saved and `shape_file` is the path to the shape file of the region. This will save the final deforestation map in the folder `output_dir`, at different threshold and resolutions.

```bash
./postprocess/generate_model_output_single.sh <model_name> <pred_dir> <prev_year_gt> <output_dir> <shape_file>
```

In order to evaluate, we must have the ground truth at the same resolutions as well. This is achieved by the following script.

```bash
./postprocess/generate_gt_single.sh <prev_year_gt> <output_dir> <shape_file>
```

Once we have the predictions and ground truth at the same resolution, we can calculate the metrics by running the following script.

```bash
python3 ./postprocess/evaluate.py --gt-path <gt_path> --pred-path <pred_path>
```

This will calculate our continuous versions of precision, recall and F1 score, alongside RMSE and the ratio of sum of prediction over sum of ground truth.

### Feature ablation

Our feature ablation methodology is to train the model on all the features and then remove one feature at a time and train the model again. We then compare the performance of the model with all the features with the performance of the model with one feature removed. This gives us the feature importance of each feature. To run feature ablation, you need to specify the path to the model checkpoint in the config file, change the mode to feature_ablation and also specify the `data description`. You can then run the following command to run feature ablation.

```bash
python3 main.py --config-file="./conf/default.json"
```

This will save the feature importance in the file specified by `feature_ablation_out_csv` and create a folder `pred_dir` where tiles having multi bands data of the most important features will be saved. The number of features to be saved can be specified by `num_top_fa_features`.

Once the tiles have been saved, you can run the following commands to generate the full map. Here, `dir` is the path to the folder containing the tiles.

```bash
find "${dir}" -name "*.tif" > tiff_list.txt

# Merge all predictions into a single file using gdalbuildvrt + gdal_translate
gdalbuildvrt -vrtnodata -1 -overwrite -input_file_list tiff_list.txt "${dir}/merged_file.vrt"
gdal_translate -of GTiff -a_nodata -1 "${dir}/merged_file.vrt" "${dir}/merged_file.tif"
```

