# Import necessary modules and functions
import Blobs.loadData as loadData
import Workload.runRandomCRUD as runRandomCRUD

import os
import os.path
import urllib

from dotenv import load_dotenv

import pymongo

def main():
    # Define variables
    data_folder = "../../data/cosmicworks/"
    batch_size = 1000

    try:
        # Load environment variables from .env file
        load_dotenv("../.env")
        cosmosdb_connection_string = os.getenv('cosmosDbEndpoint')

        cosmos_db_mongodb_database = os.getenv('cosmosdbDatabase')

        cosmos_mongo_user = os.getenv('cosmosClusterAdmin')
        cosmos_mongo_pwd = os.getenv('cosmosClusterPassword')

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
            print("\t1. Load local data into MongoDB.")
            print("\t2. Run workload on Database.")
            print("\t0. End")
            user_input = input("Option: ")

            # Handle user input
            if user_input == "0":
                break
            elif user_input not in ["1", "2"]:
                print("Invalid option. Please try again.")
                continue

            # Load data into MongoDB and create vector index
            if user_input == "1":
                loadData.loadLocalBlobDataToMongoDBCluster(client, data_folder,cosmos_db_mongodb_database,batch_size)

            # Run a vector search
            if user_input == "2":
                runRandomCRUD.runCRUDOperation(client, cosmos_db_mongodb_database)
            
            print("\nPress Enter to continue...")
            input()
            
    except Exception as ex:
        print(ex)

# Run the main function if the script is run as a standalone program
if __name__ == "__main__":
    main()