import ee
import pandas as pd
from wildfire_dataset_processing.utils import create_rectangle, mask_s2_clouds

def load_fire_data(csv_path):
    """Loads fire data from a CSV file into a Pandas DataFrame."""
    return pd.read_csv(csv_path)


def fetch_image_collection(longitude, latitude, start_date, end_date):
    """Fetches Sentinel-2 image collection for a given location and date range."""
    rectangle = create_rectangle(longitude, latitude)
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filterBounds(rectangle)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                  .map(mask_s2_clouds))
    return collection, rectangle