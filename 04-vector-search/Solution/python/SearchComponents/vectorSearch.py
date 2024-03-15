# Import the embeddings module from the SearchComponents package
import SearchComponents.embeddings as Embeddings

# Define the vectorSearch function
def vectorSearch(query, vector_column, collection, embeddings_deployment, AzureOpenAIClient ,num_results=3):
    # Generate embeddings for the query using the generateEmbeddings function from the embeddings module
    query_embedding = Embeddings.generateEmbeddings(query,embeddings_deployment,AzureOpenAIClient)

    # Define the pipeline for the MongoDB aggregation query
    pipeline = [
                {
                    # The $search stage performs a search query on the collection
                    '$search': {
                        # The cosmosSearch operator performs a vector search
                        "cosmosSearch": {
                            # The vector to search for
                            "vector": query_embedding,
                            # The path in the documents where the vector data is stored
                            "path": vector_column,
                            # The number of results to return
                            "k": num_results 
                        },
                        # Return the original document in the results
                        "returnStoredSource": True }},
                # The $project stage includes or excludes fields from the documents
                {'$project': { 
                    # Include the similarity score in the results
                    'similarityScore': { '$meta': 'searchScore' }, 
                    # Include the original document in the results
                    'document' : '$$ROOT' } }
            ]
    # Perform the aggregation query on the collection and store the results
    results = collection.aggregate(pipeline)
    # Return the results
    return results