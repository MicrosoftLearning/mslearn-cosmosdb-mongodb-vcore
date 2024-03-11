import SearchComponents.embeddings as Embeddings

def generate_product_embedding(product,embeddings_deployment,AzureOpenAIClient):
    productName = "Category - " + product["categoryName"] + ", Name -" + product["name"]
    if productName:
        product["productVector"] = Embeddings.generate_embeddings (productName,embeddings_deployment,AzureOpenAIClient)

    return product


