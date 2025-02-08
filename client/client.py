import requests
import random
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

API_URL = "http://api:8000/upload/"

def wait_for_api(max_retries=10, delay=3):
    """Wait until the API is available."""
    for i in range(max_retries):
        try:
            response = requests.get("http://api:8000/files/")
            if response.status_code == 200:
                print("API is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Waiting for API... Attempt {i+1}/{max_retries}")
            time.sleep(delay)
    
    print("API is not responding. Exiting.")
    exit(1)


def generate_large_file(file_path, size_in_gb):
    with open(file_path, 'w') as f:
        for _ in range(size_in_gb * 1024):  # 1 GB = 1024 MB
            f.write('A' * (1024 * 1024)) 

def upload_large_file(path, url):
    """Uploads a file to a given URL using multipart encoding."""
    
    encoder = MultipartEncoder(
        fields={'file': (f'large_file_{random.random()}.txt', open(path, 'rb'), 'text/plain')}
    )
    
    response = requests.post(
        url,
        data=encoder,
        headers={'Content-Type': encoder.content_type}
    )
    
    print(f"Upload response: {response.status_code}")
    
    try:
        print(f"Response JSON: {response.json()}")
    except ValueError:
        print("Response is not in JSON format.")


if __name__ == "__main__":
    wait_for_api()
    generate_large_file(f"large_file.txt", 4)  #4 GB
    upload_large_file("large_file.txt", API_URL)
