import os
import os.path
import json, urllib

from dataclasses import dataclass

import json
import datetime
import time

from azure.core.exceptions import AzureError
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

import pymongo
from pymongo import UpdateOne

import openai
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

@dataclass
class Product:
    categoryName: str
    sku: str
    name: str
    description: str
    price: float
    tags: str

@dataclass
class Customer:
    type: str = ""
    title: str = ""
    name: str = ""
    emailAddress: str = ""
    phoneNumber: str = ""
    addresses: str = ""
    #salesOrderCount: int = 0
    typeVector: float = 0.0
    titleVector: float = 0.0
    nameVector: float = 0.0
    emailAddressVector: float = 0.0
    phoneNumberVector: float = 0.0
    addressesVector: float = 0.0
    #salesOrderCountVector: float = 0.0


@dataclass
class SalesOrder:
    type: str
    details: str


def main():
    # Variables
    load_data_from_azure_blob = True
    azure_blob_account = "https://cosmosdbcosmicworks.blob.core.windows.net"
    blob_container = "cosmic-works-mongo-vcore"
    data_folder = "../../data/cosmicworks/"
    batch_size = 1000

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

        openai.api_type = os.getenv('openai_api_type')
        openai.api_key = os.getenv('openai_api_key')
        openai.api_base = os.getenv('openai_api_endpoint')
        openai.api_version = os.getenv('openai_api_version')

        embeddings_deployment = os.getenv('openai_embeddings_deployment')
        completions_deployment = os.getenv('openai_completions_deployment')

        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", urllib.parse.quote_plus(cosmos_mongo_user))
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", urllib.parse.quote_plus(cosmos_mongo_pwd))

        print(f"cosmosdb_connection_string={cosmosdb_connection_string}")
        print(f"cosmos_db_mongodb_database = {cosmos_db_mongodb_database}")
        print(f"cosmos_mongo_server = {cosmos_mongo_server}")
        print(f"cosmos_mongo_usr = {cosmos_mongo_user}")
        print(f"cosmos_mongo_pwd = {cosmos_mongo_pwd}")
        print(f"ai_endpoint = {ai_endpoint}")
        print(f"ai_key = {ai_key}")

        # Download files from Azure Blob storage if not found in the data directory
        if load_data_from_azure_blob:
            Download_files_from_blob_if_they_dont_exist(azure_blob_account, blob_container, data_folder)

        # Connect to MongoDB server
        client = pymongo.MongoClient(cosmosdb_connection_string)

        # Load local copy of blob data to the MongoDB Cluster
        Load_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size)
        
        # Get Server databases list
        dbnames = client.list_database_names()

        print(client.list_database_names())


    except Exception as ex:
        print(ex)

def Download_files_from_blob_if_they_dont_exist(account_url, container_name, data_folder):
    global collection_names

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


def Load_local_blob_data_to_MongoDB_Cluster(client, data_folder,cosmos_db_mongodb_database,batch_size):
    # Read JSON documents


    local_blobs_files = os.listdir(data_folder)

    for blob_file in local_blobs_files:
        batch_number = 1

        if blob_file.find(".json") >= 0:
            print(blob_file)

            with open(data_folder+blob_file, 'r') as file:
                file_content = file.read()
                json_data = json.loads(file_content)

            if len(json_data) >= 0:
                collection_name = blob_file[:blob_file.find(".json")]
  
                db = client[cosmos_db_mongodb_database]
                collection = db[collection_name]
                number_of_docs = 0

                operations = []

                for doc in json_data:
                    number_of_docs = number_of_docs + 1

                    if collection_name == "customers":
                        customer_doc = Customer(
                            type=doc["type"]
                            , title=doc["title"]
                            , name=doc["firstName"]+" "+doc["lastName"]
                            , emailAddress=doc["emailAddress"]
                            , phoneNumber=doc["phoneNumber"]
                            , addresses=get_doc_addresses(doc["addresses"])
                            #, salesOrderCount=doc["salesOrderCount"]
                        )

                        customer_doc = generate_customer_embeding(customer_doc)

                    operations.append(UpdateOne({"_id": doc["_id"]},{"$set": doc}, upsert=True))

                    if (len(operations) == batch_size):
                        print(f"Writing collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {number_of_docs}.")
                        collection.bulk_write(operations,ordered=False)
                        operations = []
                        batch_number = batch_number + 1
                    
                if (len(operations) > 0):
                    print(f"Writing collection {collection_name}, batch size {batch_size}, batch {batch_number}, number of documents processed so far {number_of_docs}.")
                    collection.bulk_write(operations,ordered=False)

                print(f"Collection {collection_name}, total number of documents processed {number_of_docs}.\n")


def get_doc_addresses(addresses):
    addresses_string = ""

    for idx, address in enumerate(addresses):
        addresses_string= addresses_string + ("; " if idx > 0  else "")  \
                        + (address["addressLine1"] if address["addressLine1"]  else "")  \
                        + (" " + address["addressLine2"] if address["addressLine2"]  else "") \
                        + (" " + address["city"] if address["city"] else "") \
                        + (" " + address["state"] if address["state"] else "") \
                        + (" " + address["country"] if address["country"] else "") \
                        + (" " + address["zipCode"] if address["zipCode"] else "") \
                        + (" " + address["location"] if address["location"] else "")  
        
    return addresses_string

def generate_customer_embeding(customer):
    if customer["type"]:
        customer["typeVector"] = generate_embeddings (customer["type"])
    if customer["title"]:
        customer["titleVector"] = generate_embeddings (customer["title"])
    if customer["name"]:
        customer["nameVector"] = generate_embeddings (customer["name"])
    if customer["emailAddress"]:
        customer["emailAddressVector"] = generate_embeddings (customer["emailAddress"])
    if customer["phoneNumber"]:
        customer["phoneNumberVector"] = generate_embeddings (customer["phoneNumber"])
    if customer["addresses"]:
        customer["addressesVector"] = generate_embeddings (customer["addresses"])
    return customer



@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def generate_embeddings(text):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    response = openai.Embedding.create(
        input=text, engine="text-embedding-ada-002")
    embeddings = response['data'][0]['embedding']
    #time.sleep(0.5) # rest period to avoid rate limiting on AOAI for free tier
    return embeddings

if __name__ == "__main__":
    main()