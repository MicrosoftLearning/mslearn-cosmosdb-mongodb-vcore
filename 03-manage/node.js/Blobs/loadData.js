// Importing required modules
const fs = require('fs');
const path = require('path');
const mongodb = require('mongodb');
const { MongoClient, updateOne } = require('mongodb');

// Function to load the local blob data to MongoDB cluster
async function loadLocalBlobDataToMongoDBCluster(client, dataFolder, cosmosDbMongoDbDatabase, batchSize, embeddingsDeployment, AzureOpenAIClient, processCustomersVector, processProductsVector, processSalesOrdersVector) {
    // Read JSON documents from the data folder
    const localBlobsFiles = fs.readdirSync(dataFolder);

    // Loop through each file in the data folder
    for (const blobFile of localBlobsFiles) {
        let batchNumber = 1;

        // Process only JSON files
        if (blobFile.includes('.json')) {
            console.log(`\n(${new Date().toISOString()})  ${blobFile}`);

            // Read the content of the file and parse it as JSON
            const fileContent = fs.readFileSync(path.join(dataFolder, blobFile), 'utf-8');
            const jsonData = JSON.parse(fileContent);

            const totalNumberOfDocuments = jsonData.length;

            // Process only if there are documents in the JSON file
            if (totalNumberOfDocuments >= 0) {
                // Get the collection name from the file name
                const collectionName = blobFile.split(".json")[0];

                // Get the database and the collection
                const db = client.db(cosmosDbMongoDbDatabase);
                const collection = db.collection(collectionName);
                let currentDocIdx = 0;

                let operations = [];

                // Loop through each document in the JSON file
                for (let doc of jsonData) {
                    currentDocIdx++;

                    // Prepare the update operation for the document
                    operations.push({
                        updateOne: {
                            filter: { "_id": doc["_id"] },
                            update: { "$set": doc },
                            upsert: true
                        }
                    });

                    // Write the operations to the database in batches
                    if (operations.length === batchSize) {
                        console.log(`\tWriting collection ${collectionName}, batch size ${batchSize}, batch ${batchNumber}, number of documents processed so far ${currentDocIdx}.`);
                        await collection.bulkWrite(operations, { ordered: false });
                        operations = [];
                        batchNumber++;
                    }
                }

                // Write any remaining operations to the database
                if (operations.length > 0) {
                    console.log(`\tWriting collection ${collectionName}, batch size ${batchSize}, batch ${batchNumber}, number of documents processed so far ${currentDocIdx}.`);
                    await collection.bulkWrite(operations, { ordered: false });
                }

                console.log(`(${new Date().toISOString()})  Collection ${collectionName}, total number of documents processed ${currentDocIdx} .\n`);
            }
        }
    }
}

// Export the function
module.exports.loadLocalBlobDataToMongoDBCluster = loadLocalBlobDataToMongoDBCluster;