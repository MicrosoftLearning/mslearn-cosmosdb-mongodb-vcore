# Import necessary modules and functions
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
    # Define variables
    load_data_from_azure_blob = True
    azure_blob_account = "https://cosmosdbcosmicworks.blob.core.windows.net"
    blob_container = "cosmic-works-mongo-vcore"
    data_folder = "../../data/cosmicworks/"
    batch_size = 1000
    process_customers_vector = False
    process_products_vector = True
    process_sales_orders_vector = False

    try:
        # Load environment variables from .env file
        load_dotenv("../.env")
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
        
        # Create AzureOpenAI client for embeddings
        AzureOpenAIClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_deployment
        )

        # Create AzureOpenAI client for completion
        AzureOpenAICompletionClient = AzureOpenAI(
            azure_endpoint = ai_endpoint
            , api_key = ai_key
            , api_version = ai_version
            , azure_deployment = ai_completion
        )

        # Replace placeholders in the connection string with actual values
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", urllib.parse.quote_plus(cosmos_mongo_user))
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", urllib.parse.quote_plus(cosmos_mongo_pwd))

        # Connect to MongoDB server
        client = pymongo.MongoClient(cosmosdb_connection_string)

        # User interaction loop
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

            # Handle user input
            if user_input == "0":
                break
            elif user_input not in ["1", "2", "3", "4"]:
                print("Invalid option. Please try again.")
                continue

            # Download data from Azure blob storage
            if user_input == "1":
                if load_data_from_azure_blob:
                    WebDownload.downloadFilesFromBlobIfTheyDontExist(azure_blob_account, blob_container, data_folder)

            # Load data into MongoDB and create vector index
            if user_input == "1" or user_input == "2":
                LoadAndVectorize.loadAndVectorizeLocalBlobDataToMongoDBCluster(client, data_folder,cosmos_db_mongodb_database,batch_size,embeddings_deployment, AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector)

            # Run a vector search
            if user_input == "3":
                Searches.runVectorSearch(embeddings_deployment, AzureOpenAIClient,client, cosmos_db_mongodb_database)
            
            # Run a GPT search
            if user_input == "4":
                Searches.runGPTSearch(embeddings_deployment, AzureOpenAIClient, completion_deployment, AzureOpenAICompletionClient, client, cosmos_db_mongodb_database)

            print("\nPress Enter to continue...")
            input()
            
    except Exception as ex:
        print(ex)

# Run the main function if the script is run as a standalone program
if __name__ == "__main__":
    main()