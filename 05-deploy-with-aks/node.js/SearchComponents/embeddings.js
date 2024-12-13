// Import the async-retry module
const retry = require('async-retry');

// Asynchronous function to generate embeddings from a string of text
async function generateEmbeddings(text, embeddingsDeployment, AzureOpenAIClient) {

    //Generate embeddings from string of text.
    //This will be used to vectorize data and user input for interactions with Azure OpenAI.
    // Use the async-retry module to attempt the following code block
    // If an error occurs, it will retry up to 10 times, with an increasing timeout between each attempt
    return await retry(async bail => {
        try {
            // Call the Azure OpenAI Client's getEmbeddings function with the embeddings deployment and text
            // Await the response and store it in the response variable
            const response = await AzureOpenAIClient.embeddings.create({ input: text, model: embeddingsDeployment });

            // Extract the embeddings from the response data
            const embeddings = response.data[0].embedding;
            // Wait for 10 milliseconds to avoid rate limiting (change to 500 on AOAI for free tier)
            await new Promise(resolve => setTimeout(resolve, 10));
            // Return the embeddings
            return embeddings;
        } catch (err) {
            // If a 429 error (Too Many Requests) is received, rethrow the error to trigger a retry
            if (err.response && err.response.status === 429) {
                throw err;
            } else {
                // For any other error, stop retrying and throw the error
                bail(err);
            }
        }
    }, {
        retries: 10, // Maximum number of retries
        minTimeout: 1000, // Minimum timeout between retries (1 second)
        factor: 2, // Factor by which the timeout increases each time
        maxTimeout: 20000 // Maximum timeout between retries (20 seconds)
    }); 

}

// Export the generateEmbeddings function
module.exports.generateEmbeddings = generateEmbeddings;