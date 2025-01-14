from urllib.parse import urlparse
import os

def get_filename_without_extension(file_url):
    # Parse the URL
    parsed_url = urlparse(file_url)
    # Get the file path from the URL
    file_path = parsed_url.path
    # Extract the base name of the file (e.g., "example.txt")
    base_name = os.path.basename(file_path)
    # Split the name and extension
    file_name, _ = os.path.splitext(base_name)
    return file_name