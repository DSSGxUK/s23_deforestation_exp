import os
import json
import pickle
import pandas as pd
import numpy as np
import rasterio as rio
import geopandas as gpd
from pycaret.classification import *

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def train_with_config(config):
    gdf = gpd.read_file(config['Paths']['shapefile_path'])
    new_df1 = gdf.drop(columns=config['ColumnsToDrop'])
    
    new_df1 = new_df1.rename(columns=lambda col: extract_number(col))

    # Load global statistics from cache
    global_stats_dict = {band_name: cache_global_stats(band_name, config['Paths']['pickle_dir']) for band_name in band_names}

    # Process bands in the dataframe
    new_df2 = process_bands_in_dataframe(new_df1, band_names, global_stats_dict)

    columns_of_interest = config['ColumnsOfInterest']['columns']
    new_df3 = pd.concat([new_df2, gdf[config['TargetColumn']]], axis=1)
    new_df = new_df3.iloc[:, columns_of_interest]

    new_df[config['TargetColumn']] = new_df[config['TargetColumn']].replace(-1, 0)

    ordinal_categories = config['OrdinalCategories']

    # Set up the PyCaret experiment
    exp = setup(data=new_df, target=config['TargetColumn'], preprocess=False, ordinal_features=ordinal_categories, session_id=config['SessionID'])

    # Create the model
    model = create_model(config['ModelType'])

    # Plot and save confusion matrix
    plot_model(model, plot='confusion_matrix', save=True)

    # Plot and save feature importance
    plot_model(model, plot='feature', save=True)

    # Plot and save classification report
    plot_model(model, plot='class_report', save=True)

    # Plot and save error report
    plot_model(model, plot='error', save=True)

    model_save_path = config['ModelSavePath']

    # Save the trained model
    save_model(model, model_name=model_save_path)

    print("Code execution completed.")

if __name__ == '__main__':
    config_file_path = input("Enter the path to config.json: ")
    config = load_config(config_file_path)
    train_with_config(config)