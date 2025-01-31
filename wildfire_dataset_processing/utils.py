import ee
import pandas as pd

def mask_s2_clouds(image):
    """Masks clouds in Sentinel-2 images using the QA60 band."""
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    return image.updateMask(mask).divide(10000)

def create_rectangle(longitude, latitude, buffer=0.02):
    """Generates a rectangular area around given coordinates."""
    return ee.Geometry.Rectangle([longitude - buffer, latitude - buffer, longitude + buffer, latitude + buffer])

def create_date_range(acq_date):
    """Creates a start and end date range from the acquisition date."""
    start_date = pd.to_datetime(acq_date).strftime('%Y-%m-%d')
    end_date = (pd.to_datetime(start_date) + pd.DateOffset(days=1)).strftime('%Y-%m-%d')
    return start_date, end_date
