const VectorSearch = require('./SearchComponents/vectorSearch');
const Completion = require('./SearchComponents/completion');
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function runVectorSearch(embeddingsDeployment, AzureOpenAIClient, client, cosmosDbMongodbDatabase) {
    console.clear();
    console.log("What would you like to know about our bike shop's inventory?");
    const userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);
    const results = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);
    for (let result of results) {
        console.log(`Similarity Score: ${result.similarityScore}, category: ${result.document.categoryName}, Product: ${result.document.name}`);
    }
}

async function runGPTSearch(embeddingsDeployment, AzureOpenAIClient, completionDeployment, client, cosmosDbMongodbDatabase) {
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);

    let userInput = "";
    console.clear();
    console.log("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
    userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    while (userInput.toLowerCase() !== "end") {
        const resultsForPrompt = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);

        const completionsResults = await Completion.generateCompletion(resultsForPrompt, completionDeployment, AzureOpenAIClient, userInput);
        console.log("\n" + completionsResults.choices[0].message.content);

        console.log("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
        userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    }
}