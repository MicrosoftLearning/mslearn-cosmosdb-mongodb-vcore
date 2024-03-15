# Function to create vector indexes in a MongoDB collection
def createVectorIndexes(collection, index_list, db, collection_name):
    # Get information about the existing indexes in the collection
    collection_indexes = collection.index_information()    

    # Iterate over each index in the index_list
    for indexname, vectorColumn in index_list:
        # Iterate over each index in the collection indexes
        for index in collection_indexes:
            # If the index already exists in the collection
            if index == indexname:
                # Drop the existing index
                collection.drop_index(indexname)
                break
        
            # Create a new IVF index in the collection
            # The index is created using the MongoDB command function
            # The command specifies the collection to create the index in, the name of the index, 
            # the key to index on, and the options for the CosmosDB search        
            db.command({
            'createIndexes': collection_name,
            'indexes': [
                {
                'name': indexname,
                'key': {
                    f"{vectorColumn}": "cosmosSearch"
                },
                'cosmosSearchOptions': {
                    'kind': 'vector-ivf',
                    'numLists': 1,
                    'similarity': 'COS',
                    'dimensions': 1536
                }
                }
            ]
            })