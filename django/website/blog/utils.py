from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import requests
from io import BytesIO
import pyclamd
import boto3
from botocore.exceptions import NoCredentialsError

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_type(parsed_user_agent):
    if 'tablet' in parsed_user_agent.get('device', '').lower():
        return 'Tablet'
    elif 'mobile' in parsed_user_agent.get('device', '').lower():
        return 'Mobile'
    else:
        return 'Desktop'

def get_exif_data(image_path):
    with Image.open(image_path) as img:
        if hasattr(img, "_getexif") and img._getexif() is not None:
            exif_data = img._getexif()

            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                
                if tag_name == "GPSInfo":
                    gps_info = {}
                    for key in value.keys():
                        sub_tag_name = GPSTAGS.get(key, key)
                        gps_info[sub_tag_name] = value[key]
                    print("GPS Info:", gps_info)
                else:
                    print(f"{tag_name}: {value}")
        else:
            print("No meta information obtained from image.")

def resolve_uploads_dir_path():
    current_file_directory = os.path.dirname(os.path.abspath(__file__))

    website_directory = os.path.dirname(os.path.dirname(current_file_directory))

    uploads_folder_path = os.path.join(website_directory, 'website/uploads')

    return uploads_folder_path


def download_image(url, img_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        image.save(img_path)

        print("Image downloaded successfully.")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except BaseException as err:
        print(f"Other Error: {err}")

def remove_files_in_directory(directory):
    try:
        files = os.listdir(directory)

        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File '{file}' removed successfully.")
        
        print("All files in the directory removed successfully.")
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to remove files in '{directory}'.")
    except Exception as e:
        print(f"Error removing files in directory '{directory}': {e}")

def scan_for_viruses(file_path):
    try:
        clamd = pyclamd.ClamdAgnostic()

        if not clamd.ping():

            # We don't want to handle any files if clamd is not running.
            raise Exception("Clamd not available. Make sure Clamd is running.")
            return

        scan_result = clamd.scan_file(file_path)

        if scan_result[file_path] == 'OK':
            print(f"The file '{file_path}' is clean.")
        else:
            print(f"The file '{file_path}' is infected: {scan_result[file_path]}")
            raise Exception("File infected. Will not upload.")

    except Exception as e:
        print(f"Error scanning file '{file_path}': {e}")

def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print("Upload successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as err:
        print(f"ERROR: {err}")