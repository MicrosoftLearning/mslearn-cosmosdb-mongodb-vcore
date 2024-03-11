const { BlobServiceClient } = require('@azure/storage-blob');
const fs = require('fs');
const path = require('path');

async function downloadFilesFromBlobIfTheyDontExist(accountUrl, containerName, dataFolder) {
    const blobServiceClient = BlobServiceClient.fromConnectionString(accountUrl);
    const containerClient = blobServiceClient.getContainerClient(containerName);

    // List blobs in the container
    let blobs = containerClient.listBlobsFlat();

    for await (const blob of blobs) {
        const filePath = path.join(dataFolder, blob.name);

        // Add File from blob storage if not found in the data folder
        if (!fs.existsSync(filePath)) {
            const blobClient = containerClient.getBlobClient(blob.name);
            const downloadBlockBlobResponse = await blobClient.download(0);
            const fileStream = fs.createWriteStream(filePath);
            downloadBlockBlobResponse.readableStreamBody.pipe(fileStream);
        }
    }
}