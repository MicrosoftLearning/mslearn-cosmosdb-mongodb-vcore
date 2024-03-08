def Download_files_from_blob_if_they_dont_exist(account_url, container_name, data_folder):
    blob_service_client = BlobServiceClient(account_url=account_url)
    container_client = blob_service_client.get_container_client(container_name)

    # List blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        
        file_path = data_folder + blob.name

        # Add File from blob storage if not found in the data folder
        if not os.path.isfile(file_path):
            blob_file = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
            with open(file=file_path, mode='wb') as local_file:
                file_stream = blob_file.download_blob()
                local_file.write(file_stream.readall())


