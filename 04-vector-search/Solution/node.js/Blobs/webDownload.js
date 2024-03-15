// Import the BlobServiceClient from the Azure Storage Blob package
const { BlobServiceClient } = require('@azure/storage-blob');

// Import the file system module
const fs = require('fs');

// Import the path module
const path = require('path');

// Define an asynchronous function to download files from Azure Blob Storage if they don't exist locally
async function downloadFilesFromBlobIfTheyDontExist(accountUrl, containerName, dataFolder) {
    // Create a new BlobServiceClient
    const blobServiceClient = new BlobServiceClient(accountUrl);

    // Get a ContainerClient for the specified container
    const containerClient = blobServiceClient.getContainerClient(containerName);

    // List all blobs in the container
    let blobs = containerClient.listBlobsFlat();

    // Iterate over each blob
    for await (const blob of blobs) {
        // Construct the local file path
        const filePath = path.join(dataFolder, blob.name);

        // Check if the file already exists locally
        if (!fs.existsSync(filePath)) {
            // If the file doesn't exist locally, download it from Azure Blob Storage

            // Get a BlobClient for the blob
            const blobClient = containerClient.getBlobClient(blob.name);

            // Download the blob
            const downloadBlockBlobResponse = await blobClient.download(0);

            // Create a write stream for the local file
            const fileStream = fs.createWriteStream(filePath);

            // Pipe the downloaded blob to the file stream
            downloadBlockBlobResponse.readableStreamBody.pipe(fileStream);
        }
    }
}

// Export the function
module.exports.downloadFilesFromBlobIfTheyDontExist = downloadFilesFromBlobIfTheyDontExist;