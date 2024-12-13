// Import the required modules
const VectorSearch = require('../SearchComponents/vectorSearch');
const Completion = require('../SearchComponents/completion');

function vectorSearchPrompt() {
    return "What would you like to know about our bike shop's inventory?";
}

function GPTSearchPrompt() {
    return "What would you like to ask about our bike shop's inventory? Type 'end' to end the session.";
}

// Asynchronous function to run a vector search
async function runVectorSearch(embeddingsDeployment, AzureOpenAIClient, client, cosmosDbMongodbDatabase, userInput) {

    // Replace this line with the lab's code

}

// Asynchronous function to run a GPT-3 search
async function runGPTSearch(embeddingsDeployment, AzureOpenAIClient, completionDeployment, client, cosmosDbMongodbDatabase, userInput) {

    // Replace this line with the lab's code
    
}

// Export functions
module.exports.runVectorSearch = runVectorSearch;
module.exports.runGPTSearch = runGPTSearch;
module.exports.vectorSearchPrompt = vectorSearchPrompt;
module.exports.GPTSearchPrompt = GPTSearchPrompt;