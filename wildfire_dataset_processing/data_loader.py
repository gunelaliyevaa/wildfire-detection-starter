import ee
import pandas as pd
from wildfire_dataset_processing.utils import create_rectangle, mask_s2_clouds
# fire_imagery/data_loader.py

def load_fire_data(csv_path):
    """
    Load fire event data from a CSV file.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing fire event data.
    """
    return pd.read_csv(csv_path)
