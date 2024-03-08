import os
import os.path
import json, urllib

import json
import datetime
import time

from azure.storage.blob import BlobServiceClient

import pymongo
from pymongo import UpdateOne

from openai import AzureOpenAI 

from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

def main():
    # Variables
    load_data_from_azure_blob = True
    azure_blob_account = "https://cosmosdbcosmicworks.blob.core.windows.net"
    blob_container = "cosmic-works-mongo-vcore"
    data_folder = "../../data/cosmicworks/"
    batch_size = 1000
    process_customers_vector = False
    process_products_vector = False
    process_sales_orders_vector = True

    try:
        # Get Configuration Settings
        load_dotenv()
        cosmosdb_connection_string = os.getenv('cosmosdb_connection_string')

        cosmos_db_mongodb_database = os.getenv('cosmosdb_database')

        cosmos_mongo_server = os.getenv('cosmos_mongo_server')
        cosmos_mongo_user = os.getenv('cosmos_mongo_user')
        cosmos_mongo_pwd = os.getenv('cosmos_mongo_pwd')

        ai_endpoint = os.getenv('openai_api_endpoint')
        ai_key = os.getenv('openai_api_key')
        ai_version = os.getenv('openai_api_version')
        ai_deployment = os.getenv('openai_completions_deployment')

        embeddings_deployment = os.getenv('openai_embeddings_deployment')

        AzureOpenAIClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_deployment
        )

        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", urllib.parse.quote_plus(cosmos_mongo_user))
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", urllib.parse.quote_plus(cosmos_mongo_pwd))

        print("")
        print(f"cosmosdb_connection_string={cosmosdb_connection_string}")
        print(f"cosmos_db_mongodb_database = {cosmos_db_mongodb_database}")
        print(f"cosmos_mongo_server = {cosmos_mongo_server}")
        print(f"cosmos_mongo_usr = {cosmos_mongo_user}")
        print(f"cosmos_mongo_pwd = {cosmos_mongo_pwd}")
        print("")
        print(f"ai_endpoint = {ai_endpoint}")
        print(f"ai_key = {ai_key}")
        print(f"ai_version = {ai_version}")
        print(f"ai_deployment = {ai_deployment}")
        print("")

        # Download files from Azure Blob storage if not found in the data directory
        if load_data_from_azure_blob:
            Download_files_from_blob_if_they_dont_exist(azure_blob_account, blob_container, data_folder)

        # Connect to MongoDB server
        client = pymongo.MongoClient(cosmosdb_connection_string)

        # Load local copy of blob data to the MongoDB Cluster and generate vectors
        Load_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment, AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector)
        


    except Exception as ex:
        print(ex)

def Download_files_from_blob_if_they_dont_exist(account_url, container_name, data_folder):
    blob_service_client = BlobServiceClient(account_url=account_url)
    container_client = blob_service_client.get_container_client(container_name)

    # List blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        
        file_path = data_folder + blob.name

        # Add File from blob storage if not found in the data folder
        if not os.path.isfile(file_path):
            blob_file = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
            with open(file=file_path, mode='wb') as local_file:
                file_stream = blob_file.download_blob()
                local_file.write(file_stream.readall())


def Load_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment,AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector):
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
                        doc = generate_customer_embeding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "products" and process_products_vector:
                        doc = generate_product_embeding(doc,embeddings_deployment,AzureOpenAIClient)

                    elif collection_name == "salesOrders" and process_sales_orders_vector:
                        doc = generate_sales_order_embeding(doc,embeddings_deployment,AzureOpenAIClient)

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
                    create_indexes(collection, index_list)

                elif (process_products_vector and collection_name == "products"):
                    index_list = [
                                    ("productCategoryNameVectorSearchIndex", "productCategoryNameVector")
                                    , ("productNameVectorSearchIndex", "productNameVector")
                                ]
                    create_indexes(collection, index_list)

                elif (process_sales_orders_vector and collection_name == "salesOrders"):
                    index_list = [
                                    ("salesOrderDetailVectorSearchIndex", "salesOrderDetailVector")
                                ]
                    create_indexes(collection, index_list)

def create_indexes(collection, index_list):

    cosmos_search_options = {
        "kind": "vector-ivf",   # Vector index type
        "numLists": 1,          # Number of lists (optional)
        "similarity": "COS",    # Similarity measure (e.g., cosine similarity)
        "dimensions": 1536      # Number of dimensions in the vector data
    }

    for indexname, vectorColumn in index_list:
        collection.drop_index(indexname)
        collection.create_index(
            [(vectorColumn, "cosmosSearch")],  # Specify the field to index
            name=indexname,             # Name of the index
            default_language='english',           # Specify the language for text search (optional)
            **cosmos_search_options               # Additional options for vector search
        )


def get_customer_addresses(addresses):
    addresses_string = ""

    for idx, address in enumerate(addresses):
        addresses_string= addresses_string + ("; " if idx > 0  else "")  \
                        + ("Address Line - " + address["addressLine1"] if address["addressLine1"]  else "")  \
                        + (" " + address["addressLine2"] if address["addressLine2"]  else "") \
                        + (", city - " + address["city"] if address["city"] else "") \
                        + (", state - " + address["state"] if address["state"] else "") \
                        + (", country - " + address["country"] if address["country"] else "") \
                        + (", zipcode - " + address["zipCode"] if address["zipCode"] else "") \
                        + (", location - " + address["location"] if address["location"] else "")  
        
    return addresses_string

def get_sales_order_details(details):
    details_string = ""

    for idx, detail in enumerate(details):
        details_string= details_string + ("; " if idx > 0  else "")  \
                        + ("SKU - " + detail["sku"] if detail["sku"]  else "")  \
                        + (", name - " + detail["name"] if detail["name"]  else "")  \
                        + (", price - " + str(detail["price"]) if detail["price"]  else "")  \
                        + (", quantity - " + str(detail["quantity"]) if detail["quantity"]  else "")  
        
    return details_string

def generate_customer_embeding(customer,embeddings_deployment,AzureOpenAIClient):
    if customer["type"]:
        customer["customerTypeVector"] = generate_embeddings (customer["type"],embeddings_deployment,AzureOpenAIClient)

    if customer["title"]:
        customer["customerTitleVector"] = generate_embeddings (customer["title"],embeddings_deployment,AzureOpenAIClient)

    if customer["firstName"]+" "+customer["lastName"]:
        customer["customerNameVector"] = generate_embeddings (customer["firstName"]+" "+customer["lastName"],embeddings_deployment,AzureOpenAIClient)

    if customer["emailAddress"]:
        customer["customerEmailAddressVector"] = generate_embeddings (customer["emailAddress"],embeddings_deployment,AzureOpenAIClient)

    if customer["phoneNumber"]:
        customer["customerPhoneNumberVector"] = generate_embeddings (customer["phoneNumber"],embeddings_deployment,AzureOpenAIClient)

    address = get_customer_addresses(customer["addresses"])
    if len(address) > 0:
        customer["customerAddressesVector"] = generate_embeddings (address,embeddings_deployment,AzureOpenAIClient)

    return customer



def generate_product_embeding(product,embeddings_deployment,AzureOpenAIClient):
    if product["categoryName"]:
        product["productCategoryNameVector"] = generate_embeddings (product["categoryName"],embeddings_deployment,AzureOpenAIClient)

    if product["name"]:
        product["productNameVector"] = generate_embeddings (product["name"],embeddings_deployment,AzureOpenAIClient)

    return product


def generate_sales_order_embeding(salesOrder,embeddings_deployment,AzureOpenAIClient):
    detail=get_sales_order_details(salesOrder["details"])
    if len(detail):
        salesOrder["salesOrderDetailVector"] = generate_embeddings (detail,embeddings_deployment,AzureOpenAIClient)

    return salesOrder




@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def generate_embeddings(text,embeddings_deployment,AzureOpenAIClient):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    response = AzureOpenAIClient.embeddings.create(
        input=text
        , model=embeddings_deployment)
    
    embeddings = response.model_dump_json(indent=2)
    time.sleep(0.01) # rest period to avoid rate limiting on AOAI for free tier
    return embeddings

if __name__ == "__main__":
    main()