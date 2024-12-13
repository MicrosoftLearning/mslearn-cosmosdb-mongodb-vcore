// Import necessary modules
const Searches = require('./SearchComponents/searches');
const WebDownload = require('./Blobs/webDownload');
const LoadAndVectorize = require('./Blobs/loadAndVectorize');
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
const dotenv = require('dotenv');
const MongoClient = require('mongodb').MongoClient;
const { AzureOpenAI } = require("openai");
const apiVersion = "2024-07-01-preview";

// Load environment variables
dotenv.config({ path: '.env' });

let client;

// Define constants
const load_data_from_azure_blob = true;
const azure_blob_account = "https://cosmosdbcosmicworks.blob.core.windows.net";
const blob_container = "cosmic-works-mongo-vcore";
const data_folder = "../../data/cosmicworks/";
const batch_size = 1000;
const process_customers_vector = false;
const process_products_vector = true;
const process_sales_orders_vector = false;

// Get Configuration Settings from environment variables
let cosmosdb_connection_string = process.env.cosmosDbEndpoint;
const cosmos_db_mongodb_database = process.env.cosmosdbDatabase;
const cosmos_mongo_user = process.env.cosmosClusterAdmin;
const cosmos_mongo_pwd = process.env.cosmosClusterPassword;
const ai_endpoint = process.env.OpenAIEndpoint;
const ai_key = process.env.OpenAIKey1;
const embeddings_deployment = process.env.OpenAIDeploymentName;
const completion_deployment = process.env.OpenAICompletionDeploymentName;

// Initialize Azure OpenAI client
const AzureOpenAIClient = new AzureOpenAI({endpoint: ai_endpoint, apiKey: ai_key, apiVersion: apiVersion});

// Replace placeholders in the connection string with actual values
cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", encodeURIComponent(cosmos_mongo_user));
cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", encodeURIComponent(cosmos_mongo_pwd));

function getOptions() {
    return ["Download data locally, load it into MongoDB and create vector index.",
            "Load local data into MongoDB and create vector index.",
            "Run a vector search",
            "Run a GPT search"];
}

async function processOption(userInput) {

    if (userInput === "1") {
        if (load_data_from_azure_blob) {
            await WebDownload.downloadFilesFromBlobIfTheyDontExist(azure_blob_account, blob_container, data_folder);
        }
    }

    // Load data into MongoDB and create vector index if user selected option 1 or 2
    if (userInput === "1" || userInput === "2") {
        
        // Connect to MongoDB server
        const client = new MongoClient(cosmosdb_connection_string);
        await client.connect();

        try {
            await LoadAndVectorize.loadAndVectorizeLocalBlobDataToMongoDBCluster(
                client, 
                data_folder, 
                cosmos_db_mongodb_database, 
                batch_size, 
                embeddings_deployment, 
                AzureOpenAIClient, 
                process_customers_vector,
                process_products_vector, 
                process_sales_orders_vector);
            return "Operation complete.";
        } catch (ex) {
            // Log any errors
            console.error(ex);
        } finally {
            if (client) {
                await client.close();
            }
        }
    }

    // Return the vector search prompt if the user selected option 3
    if (userInput === "3") {
        return Searches.vectorSearchPrompt();
    }

    // Return the GPT search prompt if user selected option 4
    if (userInput === "4") {
        return Searches.GPTSearchPrompt();
    }
}

async function doGPTSearch(userInput) {

    // Connect to MongoDB server
    const client = new MongoClient(cosmosdb_connection_string);
    await client.connect();

    try {
        const searchResult = await Searches.runGPTSearch(
            embeddings_deployment, 
            AzureOpenAIClient, 
            completion_deployment, 
            client, 
            cosmos_db_mongodb_database,
            userInput);
        return searchResult;
    } catch (ex) {
        // Log any errors
        console.error(ex);
    } finally {
        if (client) {
            await client.close();
        }
    }
}

async function doVectorSearch(userInput) {

    // Connect to MongoDB server
    const client = new MongoClient(cosmosdb_connection_string);
    await client.connect();

    try {
        const searchResult = await Searches.runVectorSearch(
            embeddings_deployment, 
            AzureOpenAIClient, 
            client, 
            cosmos_db_mongodb_database, 
            userInput);
        return searchResult;
    } catch (ex) {
        // Log any errors
        console.error(ex);
    } finally {
        if (client) {
            await client.close();
        }
    }
}

// TODO: Export functions
