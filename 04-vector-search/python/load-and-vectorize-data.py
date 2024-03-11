# Load functions from the Models, Search and Blob folders
import SearchComponents.searches as Searches
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
    process_products_vector = True
    process_sales_orders_vector = False

    try:
        # Get Configuration Settings
        load_dotenv()
        cosmosdb_connection_string = os.getenv('cosmosDbEndpoint')

        cosmos_db_mongodb_database = os.getenv('cosmosdbDatabase')

        cosmos_mongo_user = os.getenv('cosmosClusterAdmin')
        cosmos_mongo_pwd = os.getenv('cosmosClusterPassword')

        ai_endpoint = os.getenv('OpenAIEndpoint')
        ai_key = os.getenv('OpenAIKey1')
        ai_version = os.getenv('OpenAIVersion')
        ai_deployment = os.getenv('OpenAIDeploymentName')
        ai_completion = os.getenv('OpenAICompletionDeploymentName')

        embeddings_deployment = os.getenv('OpenAIDeploymentModel')
        completion_deployment = os.getenv('OpenAICompletionDeploymentModel')
        

        AzureOpenAIClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_deployment
        )

        AzureOpenAICompletionClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_completion
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
            print("\t4. Run a GPT search")
            print("\t0. End")
            user_input = input("Option: ")

            if user_input == "0":
                break
            elif user_input not in ["1", "2", "3", "4"]:
                print("Invalid option. Please try again.")
                continue

            if user_input == "1":
                if load_data_from_azure_blob:
                    WebDownload.Download_files_from_blob_if_they_dont_exist(azure_blob_account, blob_container, data_folder)

            if user_input == "1" or user_input == "2":
                LoadAndVectorize.Load_and_vectorize_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment, AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector)

            if user_input == "3":
                Searches.Run_vector_search(embeddings_deployment, AzureOpenAIClient,client, cosmos_db_mongodb_database)
            
            if user_input == "4":
                Searches.Run_GPT_search(embeddings_deployment, AzureOpenAIClient, completion_deployment, AzureOpenAICompletionClient, client, cosmos_db_mongodb_database)

            print("\nPress Enter to continue...")
            input()
            
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()