import os
import json
import datetime
from pymongo import UpdateOne
import Models.customers as Customers
import Models.products as Products
import Models.salesOrders as SalesOrders
import SearchComponents.indexes as Indexes



def Load_and_vectorize_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment,AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector):
    # Read JSON documents


    local_blobs_files = os.listdir(data_folder)

    for blob_file in local_blobs_files:
        batch_number = 1

        if blob_file.find(".json") >= 0:
            print("\n(" + str(datetime.datetime.now()) + ")  " + blob_file)

            with open(data_folder+blob_file, 'r') as file:
                file_content = file.read()
                json_data = json.loads(file_content)

            total_number_of_documents = len(json_data)

            if total_number_of_documents >= 0:
                collection_name = blob_file[:blob_file.find(".json")]
  
                db = client[cosmos_db_mongodb_database]
                collection = db[collection_name]
                current_doc_idx = 0

                operations = []

                index_list = []

                for doc in json_data:
                    current_doc_idx = current_doc_idx + 1

                    if collection_name == "customers" and process_customers_vector:
                        doc = Customers.generate_customer_embedding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "products" and process_products_vector:
                        doc = Products.generate_product_embedding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "salesOrders" and process_sales_orders_vector:
                        doc = SalesOrders.generate_sales_order_embedding(doc,embeddings_deployment,AzureOpenAIClient)
                    
                    if current_doc_idx % 100 == 0 and ((process_customers_vector and collection_name == "customers") or (process_products_vector and collection_name == "products") or (process_sales_orders_vector and collection_name == "salesOrders")):
                        print(f"\t{current_doc_idx} out of {total_number_of_documents} docs vectorized.")

                    operations.append(UpdateOne({"_id": doc["_id"]},{"$set": doc}, upsert=True))

                    if (len(operations) == batch_size):
                        print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                        collection.bulk_write(operations,ordered=False)
                        operations = []
                        batch_number = batch_number + 1
                    
                if (process_customers_vector and collection_name == "customers") or (process_products_vector and collection_name == "products") or (process_sales_orders_vector and collection_name == "salesOrders"):
                    print(f"\t{total_number_of_documents} out of {total_number_of_documents} docs vectorized.")

                if (len(operations) > 0):
                    print(f"\tWriting collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {current_doc_idx}.")
                    collection.bulk_write(operations,ordered=False)
                
                print(f"(" + str(datetime.datetime.now()) + ")  " + f"Collection {collection_name}, total number of documents processed {current_doc_idx} .\n")

                # Create the vector indexes
                if (process_customers_vector and collection_name == "customers"):
                    index_list = [
                                    ("customerTypeVectorSearchIndex", "customerTypeVector")
                                    , ("customerTitleVectorSearchIndex", "customerTitleVector")
                                    , ("customerNameVectorSearchIndex", "customerNameVector")
                                    , ("customerEmailAddressVectorSearchIndex", "customerEmailAddressVector")
                                    , ("customerPhoneNumberVectorSearchIndex", "customerPhoneNumberVector")
                                    , ("customerAddressesVectorSearchIndex", "customerAddressesVector")
                                ]
                    Indexes.create_vector_indexes(collection, index_list, db, collection_name)

                elif (process_products_vector and collection_name == "products"):
                    index_list = [
                                    ("productCategoryNameVectorSearchIndex", "productCategoryNameVector")
                                    , ("productNameVectorSearchIndex", "productNameVector")
                                ]
                    Indexes.create_vector_indexes(collection, index_list, db, collection_name)

                elif (process_sales_orders_vector and collection_name == "salesOrders"):
                    index_list = [
                                    ("salesOrderDetailVectorSearchIndex", "salesOrderDetailVector")
                                ]
                    Indexes.create_vector_indexes(collection, index_list, db, collection_name)

