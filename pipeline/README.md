# Modelling Pipeline

This folder contains the scripts used to run the modelling pipeline. The pipeline has the following structure:

```
pipeline
|
├── README.md              <- The top-level README containing instructions to reproduce the project
|    
├── notebooks              <- Jupyter notebooks
│   ├── exploratory        <- Notebooks for initial exploration and visualization
│   └── reports            <- Polished notebooks for presentations or results
│
├── requirements           <- Directory containing the requirement files
│
├── setup.py / setup.sh    <- makes project pip installable (pip install -e .) so src can be imported
│
├── src                    <- Source code for use in this project.
|   |
|   ├── main.py            <- Entry point to run the project
|   │
|   ├── conf               <- Configuration file, e.g., for logging, data loading, models etc.
|   │   ├── model1.json    <- Default configuration for model1
|   │   ├── model2.json    <- Default configuration for model2
|   |   └── model3.json    <- Default configuration for model3
|   │
|   ├── data               <- Scripts related to downloading and processing data as well as dataloaders
|   │   ├── __init__.py  
|   │   ├── download       <- Scripts to download data
|   │   ├── preprocess     <- Scripts to turn raw data into clean data and features for modeling
|   |   └── dataloaders    <- Scripts to load data into models
|   │
|   ├── models             <- Scripts related to modelling (several different models implemented here)
|   │   ├── __init__.py  
|   |   ├── loss.py        <- Loss functions for different models    
|   │   ├── model1.py     
|   |   └── model2.py
|   │
|   ├── utility            <- Utility functions required for logging, plotting, evaluating etc.
|   │
|   └── engine             <- Scripts to train, validate and test models
|       ├── __init__.py  
|       ├── trainer.py     <- Script to train a model
|       ├── tester.py      <- Script to test a model
|       └── solver.py      <- Optimizer for training a model
|
└── logs                   <- Directory containing log files saved with configuration file
```