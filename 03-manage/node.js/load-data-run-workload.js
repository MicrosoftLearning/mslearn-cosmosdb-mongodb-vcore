// Import necessary modules
const LoadData = require('./Blobs/loadData');
const runRandomCRUD = require('./Workload/runRandomCRUD');
const dotenv = require('dotenv');
const MongoClient = require('mongodb').MongoClient;

const readlineSync = require('readline-sync');
const { fork } = require('child_process');

// Load environment variables
dotenv.config({ path: '../.env' });

let client;

async function main() {
    // Define constants
    const data_folder = "../../data/cosmicworks/";
    const batch_size = 1000;

    try {
        // Get Configuration Settings from environment variables
        let cosmosdb_connection_string = process.env.cosmosDbEndpoint;
        const cosmos_db_mongodb_database = process.env.cosmosdbDatabase;
        const cosmos_mongo_user = process.env.cosmosClusterAdmin;
        const cosmos_mongo_pwd = process.env.cosmosClusterPassword;

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
            console.log("\t1. Load local data into MongoDB and create vector index.");
            console.log("\t2. Run workload on Database.");
            console.log("\t0. End");
            userInput = readlineSync.keyIn("Option: ");

            // Handle user input
            if (userInput === "0") {
                process.exit(0);
            } else if (!["1", "2"].includes(userInput)) {
                console.log("Invalid option. Please try again.");
                continue;
            }

            console.log(`\nYou selected option ${userInput}.\n`);

            // Load data into MongoDB and create vector index if user selected option 1 or 2
            if (userInput === "1") {
                await LoadData.loadLocalBlobDataToMongoDBCluster(client, data_folder, cosmos_db_mongodb_database, batch_size);
            }

            // Run a vector search if user selected option 3
            if (userInput === "2") {
                const child = fork('./Workload/runRandomCRUD.js');

                child.send({
                    command: 'start',
                    connectionString: cosmosdb_connection_string,  // Pass the connection string, not the client
                    database: cosmos_db_mongodb_database
                });

                // Listen for key presses in the main process
                readLineInput = readlineSync.keyIn('', {hideEchoBack: true, mask: '', limit: 'qesc'})
                if (readLineInput) {
                    // If 'q' or 'esc' is pressed, send a message to the child process to stop
                    child.send({ command: 'stop' });
                }
            }

            console.log("\nPress Enter to continue...");
            readlineSync.question("");
        }
    } catch (ex) {
        // Log any errors
        console.error(ex);
    } finally {
        if (client) {
            await client.close();
        }
    }
}

// Run the main function
main();