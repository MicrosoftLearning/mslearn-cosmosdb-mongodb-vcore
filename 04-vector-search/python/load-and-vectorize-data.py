# Load functions from the Models, Search and Blob folders
import SearchComponents.vectorSearch as VectorSearch
import Blobs.webDownload as WebDownload
import Blobs.loadAndVectorize as LoadAndVectorize

import os
import os.path
import urllib

from dotenv import load_dotenv

import pymongo

from openai import AzureOpenAI 

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
        ai_deployment = os.getenv('openai_deployment_name')

        embeddings_deployment = os.getenv('openai_embeddings_deployment')

        AzureOpenAIClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_deployment
        )

        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", urllib.parse.quote_plus(cosmos_mongo_user))
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", urllib.parse.quote_plus(cosmos_mongo_pwd))

        # Connect to MongoDB server
        client = pymongo.MongoClient(cosmosdb_connection_string)

        user_input = ""
        while user_input.lower() != "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Please select an option:")
            print("\t1. Download data locally, load it into MongoDB and create vector index.")
            print("\t2. Load local data into MongoDB and create vector index.")
            print("\t3. Run a vector search")
            print("\t0. End")
            user_input = input("Option: ")

            if user_input == "0":
                break
            elif user_input not in ["1", "2", "3"]:
                print("Invalid option. Please try again.")
                continue

            if user_input == "1":
                if load_data_from_azure_blob:
                    WebDownload.Download_files_from_blob_if_they_dont_exist(azure_blob_account, blob_container, data_folder)

            if user_input == "1" or user_input == "2":
                LoadAndVectorize.Load_and_vectorize_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment, AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector)

            if user_input == "3":
                Run_vector_search(embeddings_deployment, AzureOpenAIClient,client, cosmos_db_mongodb_database)
            
            print("\nPress Enter to continue...")
            input()
            
    except Exception as ex:
        print(ex)

def Run_vector_search(embeddings_deployment, AzureOpenAIClient, client, cosmos_db_mongodb_database):
    query = input("Enter a query: ")
    maxResults = input("Maximum number of results returned (or select Enter for 10):") or 10
    vector_column = "salesOrderDetailVector" # input("Enter the vector column name: ")
    collection_name = "salesOrders" # input("Enter the collection name: ")


    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]
    results = VectorSearch.vector_search(query, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
    for result in results: 
        print(f"Similarity Score: {result['similarityScore']}")
        print(f"customerId: {result['document']['customerId']}")  
        print(f"orderDate: {result['document']['orderDate']}")  
        print(f"shipDate: {result['document']['shipDate']}\n")
        print(f"details: {result['document']['details']}\n")



if __name__ == "__main__":
    main()