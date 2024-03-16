# Import necessary modules
from azure.storage.blob import BlobServiceClient
import os.path

# Function to download files from Azure Blob Storage if they don't exist locally
def downloadFilesFromBlobIfTheyDontExist(account_url, container_name, data_folder):
    # Create a BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient(account_url=account_url)
    # Get a Container Client using the BlobServiceClient
    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        
        # Construct the file path where the blob will be saved locally
        file_path = data_folder + blob.name

        # Check if the file already exists locally. If not, download it.
        if not os.path.isfile(file_path):
            # Get a Blob Client for the blob
            blob_file = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
            # Open a local file in write mode
            with open(file=file_path, mode='wb') as local_file:
                # Download the blob to a stream
                file_stream = blob_file.download_blob()
                # Write the stream to the local file
                local_file.write(file_stream.readall())