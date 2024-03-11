const Embeddings = require('./SearchComponents/embeddings');

async function generateProductEmbedding(product, embeddingsDeployment, AzureOpenAIClient) {
    const productName = "Category - " + product["categoryName"] + ", Name -" + product["name"];
    if (productName) {
        product["productVector"] = await Embeddings.generateEmbeddings(productName, embeddingsDeployment, AzureOpenAIClient);
    }

    return product;
}