# Import necessary modules
import os
import json
import datetime
from pymongo import UpdateOne
import Collections.customers as Customers
import Collections.products as Products
import Collections.salesOrders as SalesOrders
import SearchComponents.indexes as Indexes

# Function to load local blob data to MongoDB cluster
def loadLocalBlobDataToMongoDBCluster(client, data_folder,cosmos_db_mongodb_database,batch_size):
    # Get list of files in the data folder
    local_blobs_files = os.listdir(data_folder)

    # Iterate over each file in the folder
    for blob_file in local_blobs_files:
        batch_number = 1

        # Process only JSON files
        if blob_file.find(".json") >= 0:
            print("\n(" + str(datetime.datetime.now()) + ")  " + blob_file)

            # Open the file and load its content
            with open(data_folder+blob_file, 'r') as file:
                file_content = file.read()
                json_data = json.loads(file_content)

            # Get the total number of documents in the file
            total_number_of_documents = len(json_data)

            if total_number_of_documents >= 0:
                # Get the collection name from the file name
                collection_name = blob_file[:blob_file.find(".json")]
  
                # Get the database and collection
                db = client[cosmos_db_mongodb_database]
                collection = db[collection_name]
                current_doc_idx = 0

                operations = []

                # Iterate over each document in the JSON data
                for doc in json_data:
                    current_doc_idx = current_doc_idx + 1

                    # Prepare the update operation for the document
                    operations.append(UpdateOne({"_id": doc["_id"]},{"$set": doc}, upsert=True))

                    # Write to the collection in batches
                    if (len(operations) == batch_size):
                        print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                        collection.bulk_write(operations,ordered=False)
                        operations = []
                        batch_number = batch_number + 1
                    
                # Write any remaining operations to the collection
                if (len(operations) > 0):
                    print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                    collection.bulk_write(operations,ordered=False)
                
                print(f"(" + str(datetime.datetime.now()) + ")  " + f"Collection {collection_name}, total number of documents processed {current_doc_idx} .\n")
