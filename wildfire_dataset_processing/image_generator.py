import os
import requests
from wildfire_dataset_processing.data_loader import fetch_image_collection
from wildfire_dataset_processing.utils import create_date_range

def download_image_from_event(row, output_dir):
    """Downloads an image for a fire event."""
    latitude, longitude = row['latitude'], row['longitude']
    start_date, end_date = create_date_range(row['acq_date'])

    collection, rectangle = fetch_image_collection(longitude, latitude, start_date, end_date)
    if collection.size().getInfo() > 0:
        image = collection.median().select(['B4', 'B3', 'B2']).clip(rectangle)
        url = image.getThumbURL({'min': 0, 'max': 0.5, 'dimensions': 512, 'region': rectangle, 'format': 'png'})

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = os.path.join(output_dir, f"{latitude}_{longitude}.png")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download image for {latitude}, {longitude}: {e}")
