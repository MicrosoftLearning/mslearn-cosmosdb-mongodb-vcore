def generate_product_embedding(product,embeddings_deployment,AzureOpenAIClient):
    if product["categoryName"]:
        product["productCategoryNameVector"] = Embeddings.generate_embeddings (product["categoryName"],embeddings_deployment,AzureOpenAIClient)

    if product["name"]:
        product["productNameVector"] = Embeddings.generate_embeddings (product["name"],embeddings_deployment,AzureOpenAIClient)

    return product


