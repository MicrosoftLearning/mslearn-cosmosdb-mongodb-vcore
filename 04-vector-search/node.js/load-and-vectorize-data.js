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
dotenv.config({ path: '../.env' });

let client;

async function main() {
    // Define constants
    const load_data_from_azure_blob = true;
    const azure_blob_account = "https://cosmosdbcosmicworks.blob.core.windows.net";
    const blob_container = "cosmic-works-mongo-vcore";
    const data_folder = "../../data/cosmicworks/";
    const batch_size = 1000;
    const process_customers_vector = false;
    const process_products_vector = true;
    const process_sales_orders_vector = false;

    try {
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
        const azureOpenAIClient = new AzureOpenAI({endpoint: ai_endpoint, apiKey: ai_key, apiVersion: apiVersion});

        // Replace placeholders in the connection string with actual values
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<user>", encodeURIComponent(cosmos_mongo_user));
        cosmosdb_connection_string = cosmosdb_connection_string.replace("<password>", encodeURIComponent(cosmos_mongo_pwd));

        // Connect to MongoDB server
        const client = new MongoClient(cosmosdb_connection_string);
        await client.connect();

        let userInput = "";
        while (userInput !== "0") {
            console.clear();
            console.log("Please select an option:");
            console.log("\t1. Download data locally, load it into MongoDB and create vector index.");
            console.log("\t2. Load local data into MongoDB and create vector index.");
            console.log("\t3. Run a vector search");
            console.log("\t4. Run a GPT search");
            console.log("\t0. End");
            userInput = await new Promise(resolve => rl.question("Option: ", resolve));

            // Handle user input
            if (userInput === "0") {
                process.exit(0);
            } else if (!["1", "2", "3", "4"].includes(userInput)) {
                console.log("Invalid option. Please try again.");
                continue;
            }

            // Download data from Azure Blob if user selected option 1
            if (userInput === "1") {
                if (load_data_from_azure_blob) {
                    await WebDownload.downloadFilesFromBlobIfTheyDontExist(azure_blob_account, blob_container, data_folder);
                }
            }

            // Load data into MongoDB and create vector index if user selected option 1 or 2
            if (userInput === "1" || userInput === "2") {
                await LoadAndVectorize.loadAndVectorizeLocalBlobDataToMongoDBCluster(client, data_folder, cosmos_db_mongodb_database, batch_size, embeddings_deployment, AzureOpenAIClient, process_customers_vector, process_products_vector, process_sales_orders_vector);
            }

            // Run a vector search if user selected option 3
            if (userInput === "3") {
                await Searches.runVectorSearch(embeddings_deployment, AzureOpenAIClient, client, cosmos_db_mongodb_database, rl);
            }

            // Run a GPT search if user selected option 4
            if (userInput === "4") {
                await Searches.runGPTSearch(embeddings_deployment, AzureOpenAIClient, completion_deployment, client, cosmos_db_mongodb_database, rl);
            }

            console.log("\nPress Enter to continue...");
            await new Promise(resolve => rl.question("", resolve));
        }
    } catch (ex) {
        // Log any errors
        console.error(ex);
    } finally {
        // Close readline interface and MongoDB client
        rl.close();
        if (client) {
            await client.close();
        }
    }
}

// Run the main function
main();
