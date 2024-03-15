# Import the embeddings module
import SearchComponents.embeddings as Embeddings

# Function to generate embeddings for product data
def generateProductEmbedding(product,embeddings_deployment,AzureOpenAIClient):
    # Construct the product name by concatenating the category name and product name
    productName = "Category - " + product["categoryName"] + ", Name -" + product["name"]
    # If the product name exists
    if productName:
        # Generate embeddings for the product name
        product["productVector"] = Embeddings.generateEmbeddings (productName,embeddings_deployment,AzureOpenAIClient)

    # Return the product data with the generated embeddings
    return product