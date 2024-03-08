def vector_search(query, vector_column, collection, embeddings_deployment, AzureOpenAIClient ,num_results=3):
    query_embedding = generate_embeddings(query,embeddings_deployment,AzureOpenAIClient)

    pipeline = [
                {
                    '$search': {
                        "cosmosSearch": {
                            "vector": query_embedding,
                            "path": vector_column,
                            "k": num_results 
                        },
                        "returnStoredSource": True }},
                {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
            ]
    results = collection.aggregate(pipeline)
    return results

