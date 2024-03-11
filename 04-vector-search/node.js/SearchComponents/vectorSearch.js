const Embeddings = require('../SearchComponents/embeddings');

async function vectorSearch(query, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, numResults = 3) {
    const queryEmbedding = await Embeddings.generateEmbeddings(query, embeddingsDeployment, AzureOpenAIClient);

    const pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": queryEmbedding,
                    "path": vectorColumn,
                    "k": numResults
                },
                "returnStoredSource": true
            }
        },
        { '$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document': '$$ROOT' } }
    ];

    const results = await collection.aggregate(pipeline).toArray();
    return results;
}

module.exports.vectorSearch = vectorSearch;