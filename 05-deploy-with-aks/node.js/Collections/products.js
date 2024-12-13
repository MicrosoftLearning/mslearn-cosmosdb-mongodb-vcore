// Import the Embeddings module from the SearchComponents directory
const Embeddings = require('../SearchComponents/embeddings');

// Asynchronous function to generate an embedding for a product
async function generateProductEmbedding(product, embeddingsDeployment, AzureOpenAIClient) {

        // Construct a string representing the product's name and category
        const productName = "Category - " + product["categoryName"] + ", Name -" + product["name"];
    
        // If the productName exists, generate an embedding for it
        if (productName) {
            // The embedding is generated using the Embeddings module's generateEmbeddings function
            // The resulting embedding is stored in the product object under the key "productVector"
            product["productVector"] = await Embeddings.generateEmbeddings(productName, embeddingsDeployment, AzureOpenAIClient);
        }
    
        // Return the product object with the added embedding
        return product; 

}

// Export the generateProductEmbedding function
module.exports.generateProductEmbedding = generateProductEmbedding;