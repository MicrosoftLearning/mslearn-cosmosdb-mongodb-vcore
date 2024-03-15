// Import the required modules
const VectorSearch = require('../SearchComponents/vectorSearch');
const Completion = require('../SearchComponents/completion');

// Asynchronous function to run a vector search
async function runVectorSearch(embeddingsDeployment, AzureOpenAIClient, client, cosmosDbMongodbDatabase, rl) {
    // Clear the console and ask the user for input
    console.clear();
    console.log("What would you like to know about our bike shop's inventory?");
    // read the user input for a new prompt
    const userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);
    // Run the vector search and print the results
    const results = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);
    for (let result of results) {
        console.log(`Similarity Score: ${result.similarityScore}, category: ${result.document.categoryName}, Product: ${result.document.name}`);
    }
}

// Asynchronous function to run a GPT-3 search
async function runGPTSearch(embeddingsDeployment, AzureOpenAIClient, completionDeployment, client, cosmosDbMongodbDatabase, rl) {
    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);

    // Initialize the user input variable
    let userInput = "";
    // Clear the console and ask the user for input
    console.clear();
    console.log("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
    userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    // Continue asking for input until the user types 'end'
    while (userInput.toLowerCase() !== "end") {
        // Run the vector search
        const resultsForPrompt = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);

        // Generate completions based on the vector search results
        const completionsResults = await Completion.generateCompletion(resultsForPrompt, completionDeployment, AzureOpenAIClient, userInput);
        // Print the first completion result
        console.log("\n" + completionsResults.choices[0].message.content);

        // Ask the user for more input
        console.log("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
        userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    }
}

// Export the runVectorSearch and runGPTSearch functions
module.exports.runVectorSearch = runVectorSearch;
module.exports.runGPTSearch = runGPTSearch;