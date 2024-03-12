const fs = require('fs');
const path = require('path');
const mongodb = require('mongodb');
const { MongoClient, updateOne } = require('mongodb');

// Assuming Customers, Products, SalesOrders, and Indexes are modules you have
const Customers = require('../Collections/customers');
const Products = require('../Collections/products');
const SalesOrders = require('../Collections/salesOrders');
const Indexes = require('../SearchComponents/indexes');

async function loadAndVectorizeLocalBlobDataToMongoDBCluster(client, dataFolder, cosmosDbMongoDbDatabase, batchSize, embeddingsDeployment, AzureOpenAIClient, processCustomersVector, processProductsVector, processSalesOrdersVector) {
    // Read JSON documents
    const localBlobsFiles = fs.readdirSync(dataFolder);

    for (const blobFile of localBlobsFiles) {
        let batchNumber = 1;

        if (blobFile.includes('.json')) {
            console.log(`\n(${new Date().toISOString()})  ${blobFile}`);

            const fileContent = fs.readFileSync(path.join(dataFolder, blobFile), 'utf-8');
            const jsonData = JSON.parse(fileContent);

            const totalNumberOfDocuments = jsonData.length;

            if (totalNumberOfDocuments >= 0) {
                const collectionName = blobFile.split(".json")[0];

                const db = client.db(cosmosDbMongoDbDatabase);
                const collection = db.collection(collectionName);
                let currentDocIdx = 0;

                let operations = [];

                let indexList = [];

                for (let doc of jsonData) {
                    currentDocIdx++;

                    if (collectionName === "customers" && processCustomersVector) {
                        doc = await Customers.generateCustomerEmbedding(doc, embeddingsDeployment, AzureOpenAIClient);
                    } else if (collectionName === "products" && processProductsVector) {
                        doc = await Products.generateProductEmbedding(doc, embeddingsDeployment, AzureOpenAIClient);
                    } else if (collectionName === "salesOrders" && processSalesOrdersVector) {
                        doc = await SalesOrders.generateSalesOrderEmbedding(doc, embeddingsDeployment, AzureOpenAIClient);
                    }

                    if (currentDocIdx % 100 === 0 && ((processCustomersVector && collectionName === "customers") || (processProductsVector && collectionName === "products") || (processSalesOrdersVector && collectionName === "salesOrders"))) {
                        console.log(`\t${currentDocIdx} out of ${totalNumberOfDocuments} docs vectorized.`);
                    }

                    operations.push({
                        updateOne: {
                            filter: { "_id": doc["_id"] },
                            update: { "$set": doc },
                            upsert: true
                        }
                    });

                    if (operations.length === batchSize) {
                        console.log(`\tWriting collection ${collectionName}, batch size ${batchSize}, batch ${batchNumber}, number of documents processed so far ${currentDocIdx}.`);
                        await collection.bulkWrite(operations, { ordered: false });
                        operations = [];
                        batchNumber++;
                    }
                }

                if ((processCustomersVector && collectionName === "customers") || (processProductsVector && collectionName === "products") || (processSalesOrdersVector && collectionName === "salesOrders")) {
                    console.log(`\t${totalNumberOfDocuments} out of ${totalNumberOfDocuments} docs vectorized.`);
                }

                if (operations.length > 0) {
                    console.log(`\tWriting collection ${collectionName}, batch size ${batchSize}, batch ${batchNumber}, number of documents processed so far ${currentDocIdx}.`);
                    await collection.bulkWrite(operations, { ordered: false });
                }

                console.log(`(${new Date().toISOString()})  Collection ${collectionName}, total number of documents processed ${currentDocIdx} .\n`);

                // Create the vector indexes
                if (processCustomersVector && collectionName === "customers") {
                    indexList = [
                        ["customerTypeVectorSearchIndex", "customerTypeVector"],
                        ["customerTitleVectorSearchIndex", "customerTitleVector"],
                        ["customerNameVectorSearchIndex", "customerNameVector"],
                        ["customerEmailAddressVectorSearchIndex", "customerEmailAddressVector"],
                        ["customerPhoneNumberVectorSearchIndex", "customerPhoneNumberVector"],
                        ["customerAddressesVectorSearchIndex", "customerAddressesVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                } else if (processProductsVector && collectionName === "products") {
                    indexList = [
                        ["productVectorSearchIndex", "productVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                } else if (processSalesOrdersVector && collectionName === "salesOrders") {
                    indexList = [
                        ["salesOrderDetailVectorSearchIndex", "salesOrderDetailVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                }
            }
        }
    }
}

module.exports.loadAndVectorizeLocalBlobDataToMongoDBCluster = loadAndVectorizeLocalBlobDataToMongoDBCluster;