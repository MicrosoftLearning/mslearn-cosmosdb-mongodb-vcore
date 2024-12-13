// Asynchronous function to create vector indexes in a MongoDB collection
async function createVectorIndexes(collection, indexList, db, collectionName) {

    // Get the current indexes in the collection
    const collectionIndexes = await collection.indexInformation();

    // Iterate over each index in the indexList
    for (let [indexName, vectorColumn] of indexList) {
        // Iterate over each index in the collection
        for (let index of Object.keys(collectionIndexes)) {
            // If the index already exists in the collection, drop it
            if (index === indexName) {
                await collection.dropIndex(indexName);
                break;
            }
        }

        // Create a new IVF index in the collection
        // The index is created using the MongoDB command function
        // The command specifies the collection to create the index in, the name of the index, 
        // the key to index on, and the options for the CosmosDB search
        const commandResult = await db.command({
            'createIndexes': collectionName,
            'indexes': [
                {
                    'name': indexName,
                    'key': {
                        [vectorColumn]: "cosmosSearch"
                    },
                    'cosmosSearchOptions': {
                        'kind': 'vector-ivf',
                        'numLists': 1,
                        'similarity': 'COS',
                        'dimensions': 1536
                    }
                }
            ]
        });
    } 

}

// Export the createVectorIndexes function
module.exports.createVectorIndexes = createVectorIndexes;