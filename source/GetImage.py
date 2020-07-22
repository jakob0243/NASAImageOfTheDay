"""
Created 11/01/2020

@author Jakob McKinney
"""
import requests
import os
from datetime import datetime


IMAGE_FOLDER = os.path.join(os.path.expanduser("~/Pictures"), "BackGroundPics")
URL = "https://api.nasa.gov/planetary/apod"
API_KEY = ""
INVALID_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']


def get_info(date):
    """
    Get the image info from the API
    """
    try:
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "hd": True,
            "api_key": API_KEY
        }
        
        response = requests.get(URL, params)
        
        # Check whether response was successful
        response.raise_for_status()
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Could not download info for image {date.date()}...")
        raise e


def remove_invalid_chars(invalid_name):
    """
    Removes all the chars in the string that would make it
    an invalid path name. Probably more efficient way to do it.
    Those chars are: <>:"/\|?*
    """
    valid_name = ""
    for char in invalid_name:
        if char not in INVALID_CHARS:
            valid_name += char
        else:
            print(f"Invalid character found in name: '{char}'")

    return valid_name


def get_image(date=datetime.today()):
    """
    Requests the image info for today's image, then using the returned meta info,
    requests the image from the API and downloads it to the given path.
    Returns the path to the image.
    """
    try:
        # Download meta_info for url
        image_info = get_info(date)
        # Check if there is a link for the hd picture
        if "hdurl" not in image_info.keys():
            raise KeyError("hdurl does not exist")
        hd_url = image_info["hdurl"]
        
        # Create path to save image
        title = image_info["title"].replace(' ', '-')
        img_name = remove_invalid_chars(f"{title}.jpg")
        img_path = os.path.join(IMAGE_FOLDER, img_name)
        print(f"Image Name: {img_name}")

        # Check if img is already downloaded
        if os.path.exists(img_path):
            print("Today's image has already been downloaded...")
        else:
            # Initialize stream and file size
            response = requests.get(hd_url, stream=True)

            with open(img_path, "wb") as local_file:
                # Download image chunks
                for data in response.iter_content(chunk_size=4096):
                    print("Downloading")
                    local_file.write(data)
        
        return img_path
    
    except KeyError as e:
        print("API key is not valid...")
        raise e
    except Exception as e:
        print(f"Could not download: {image_info['title']}")
        raise e
        
        
if __name__ == "__main__":
    print(get_image())
    """
    https://www.nasa.gov/multimedia/imagegallery/iotd.html
    """    
