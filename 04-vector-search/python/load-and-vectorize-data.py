import os
import http.client, base64, json, urllib
from urllib import request, parse, error

import json
import datetime
import time

from azure.core.exceptions import AzureError
from azure.core.credentials import AzureKeyCredential
import pymongo

#import openai
from dotenv import load_dotenv
#from tenacity import retry, wait_random_exponential, stop_after_attempt

def main():
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

        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", cosmos_mongo_user)
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", cosmos_mongo_pwd)

        print(cosmosdb_connection_string)
        print(cosmos_db_mongodb_database)
        print(cosmos_mongo_server)
        print(cosmos_mongo_user)
        print(cosmos_mongo_pwd)
        print(ai_endpoint)
        print(ai_key)

        # Connect to MongoDB server
        client = pymongo.MongoClient(cosmosdb_connection_string)

        # Get Server databases list
        dbnames = client.list_database_names()

        # Create database and load sample data if it doesn't exist
        if not cosmos_db_mongodb_database in dbnames:
            initialize_database(client, cosmos_db_mongodb_database)

        db = client[cosmos_db_mongodb_database]
        collection = db['products']

        print(client.list_database_names())


    except Exception as ex:
        print(ex)

def initialize_database(client, db_name):
    db = client[db_name]

    IngestDataFromBlobStorage("https://cosmosdbcosmicworks.blob.core.windows.net/cosmic-works-small/")

    collection = db['products']
    collection.insert_one({})

def IngestDataFromBlobStorage(blob_url):

    # Get the list of files in the blob storage
    blob_list = list_blobs(blob_url)

    # For each file, load the data and ingest into the database
    for blob in blob_list:
        print(blob)
        # Load the data
        data = load_blob(blob_url, blob)

        # Ingest the data
        ingest_data(data)


if __name__ == "__main__":
    main()