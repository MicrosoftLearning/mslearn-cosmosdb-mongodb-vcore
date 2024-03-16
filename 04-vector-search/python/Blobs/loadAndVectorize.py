# Import necessary modules
import os
import json
import datetime
from pymongo import UpdateOne
import Collections.customers as Customers
import Collections.products as Products
import Collections.salesOrders as SalesOrders
import SearchComponents.indexes as Indexes

# Function to load and vectorize local blob data to MongoDB cluster
def loadAndVectorizeLocalBlobDataToMongoDBCluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment,AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector):
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

                index_list = []

                # Iterate over each document in the JSON data
                for doc in json_data:
                    current_doc_idx = current_doc_idx + 1

                    # Generate embeddings for the document based on the collection type
                    if collection_name == "customers" and process_customers_vector:
                        doc = Customers.generateCustomerEmbedding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "products" and process_products_vector:
                        doc = Products.generateProductEmbedding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "salesOrders" and process_sales_orders_vector:
                        doc = SalesOrders.generateSalesOrderEmbedding(doc,embeddings_deployment,AzureOpenAIClient)
                    
                    # Print progress for every 100 documents processed
                    if current_doc_idx % 100 == 0 and ((process_customers_vector and collection_name == "customers") or (process_products_vector and collection_name == "products") or (process_sales_orders_vector and collection_name == "salesOrders")):
                        print(f"\t{current_doc_idx} out of {total_number_of_documents} docs vectorized.")

                    # Prepare the update operation for the document
                    operations.append(UpdateOne({"_id": doc["_id"]},{"$set": doc}, upsert=True))

                    # Write to the collection in batches
                    if (len(operations) == batch_size):
                        print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                        collection.bulk_write(operations,ordered=False)
                        operations = []
                        batch_number = batch_number + 1
                    
                # Print the total number of documents vectorized
                if (process_customers_vector and collection_name == "customers") or (process_products_vector and collection_name == "products") or (process_sales_orders_vector and collection_name == "salesOrders"):
                    print(f"\t{total_number_of_documents} out of {total_number_of_documents} docs vectorized.")

                # Write any remaining operations to the collection
                if (len(operations) > 0):
                    print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                    collection.bulk_write(operations,ordered=False)
                
                print(f"(" + str(datetime.datetime.now()) + ")  " + f"Collection {collection_name}, total number of documents processed {current_doc_idx} .\n")

                pass  # Replace this line with the lab's code
