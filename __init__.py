# download_blobs_parallel.py
# Python program to bulk download blobs from azure storage
# Uses latest python SDK() for Azure blob storage
# Requires python 3.6 or above
 
import os
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
 
# IMPORTANT: Replace connection string with your storage account connection string
# Usually starts with DefaultEndpointsProtocol=https;...
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=psytech;AccountKey=hb0jzFH11xJFjTppAeNw4GgvWh/dTO9gJ198XauNmCb/hIUfhHH9xY7Bf6XWlXXfvh1calAznI8G6bKiO/0ZEQ==;EndpointSuffix=core.windows.net"
 
# Replace with blob container name
MY_BLOB_CONTAINER = "psytechreports"
 
# Replace with the local folder where you want downloaded files to be stored
LOCAL_BLOB_PATH = "./Psytech"
 
class AzureBlobFileDownloader:
  def __init__(self):
    print("Intializing AzureBlobFileDownloader")
 
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    self.my_container = self.blob_service_client.get_container_client(MY_BLOB_CONTAINER)
 
  def download_all_blobs_in_container(self):
    # get a list of blobs
    my_blobs = self.my_container.list_blobs()
    result = self.run(my_blobs)
    print(result)
 
  def run(self,blobs):
    # Download 10 files at a time!
    with ThreadPool(processes=int(10)) as pool:
     return pool.map(self.save_blob_locally, blobs)
 
  def save_blob_locally(self,blob):
    file_name = blob.name
    print(file_name)
    bytes = self.my_container.get_blob_client(blob).download_blob().readall()
 
    # Get full path to the file
    download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)
    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
 
    with open(download_file_path, "wb") as file:
      file.write(bytes)
    return file_name
 
# Initialize class and upload files
azure_blob_file_downloader = AzureBlobFileDownloader()
azure_blob_file_downloader.download_all_blobs_in_container()