const axios = require('axios');
const retry = require('async-retry');

async function generateEmbeddings(text, embeddingsDeployment, AzureOpenAIClient) {
    /*
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    */
    return await retry(async bail => {
        try {
            const response = await axios.post(AzureOpenAIClient.getEmbeddings, {
                input: text,
                model: embeddingsDeployment
            });

            const embeddings = JSON.parse(response.data);
            await new Promise(resolve => setTimeout(resolve, 10)); // rest period to avoid rate limiting on AOAI for free tier
            return embeddings["data"][0]["embedding"];
        } catch (err) {
            if (err.response && err.response.status === 429) {
                throw err;
            } else {
                bail(err);
            }
        }
    }, {
        retries: 10,
        minTimeout: 1000, // 1 second
        factor: 2,
        maxTimeout: 20000 // 20 seconds
    });
}

module.exports.generateEmbeddings = generateEmbeddings;