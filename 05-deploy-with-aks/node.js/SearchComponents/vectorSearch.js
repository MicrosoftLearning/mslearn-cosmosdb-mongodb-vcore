// Import the Embeddings module
const Embeddings = require('../SearchComponents/embeddings');

// Asynchronous function to perform a vector search
async function vectorSearch(query, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, numResults = 3) {

    // Generate embeddings for the query using the Embeddings module
    const queryEmbedding = await Embeddings.generateEmbeddings(query, embeddingsDeployment, AzureOpenAIClient);

    // Define the aggregation pipeline for the MongoDB query
    // The pipeline first performs a search using the generated embeddings and the specified vector column
    // It then projects the results to include the similarity score and the original document
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

    // Execute the aggregation pipeline on the collection and convert the results to an array
    const results = await collection.aggregate(pipeline).toArray();
    // Return the results
    return results;  

}

// Export the vectorSearch function
module.exports.vectorSearch = vectorSearch;