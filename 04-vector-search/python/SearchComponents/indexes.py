def create_vector_indexes(collection, index_list, db, collection_name):

    collection_indexes = collection.index_information()    

    for indexname, vectorColumn in index_list:
        for index in collection_indexes:
            if index == indexname:
                collection.drop_index(indexname)
                break
        
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


