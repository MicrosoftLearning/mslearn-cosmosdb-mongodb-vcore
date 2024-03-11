async function createVectorIndexes(collection, indexList, db, collectionName) {
    const collectionIndexes = await collection.indexInformation();

    for (let [indexName, vectorColumn] of indexList) {
        for (let index of Object.keys(collectionIndexes)) {
            if (index === indexName) {
                await collection.dropIndex(indexName);
                break;
            }
        }

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