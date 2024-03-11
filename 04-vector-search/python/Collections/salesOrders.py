import SearchComponents.embeddings as Embeddings

def get_sales_order_details(details):
    details_string = ""

    for idx, detail in enumerate(details):
#        details_string= details_string + ("; " if idx > 0  else "")  \
#                        + ("SKU - " + detail["sku"] if detail["sku"]  else "")  \
#                        + (", name - " + detail["name"] if detail["name"]  else "")  \
#                        + (", price - " + str(detail["price"]) if detail["price"]  else "")  \
#                        + (", quantity - " + str(detail["quantity"]) if detail["quantity"]  else "")  

        details_string= details_string + ("; " if idx > 0  else "")  \
                        + (detail["sku"] if detail["sku"]  else "")  \
                        + ("," + detail["name"] if detail["name"]  else "")



    return details_string

def generate_sales_order_embedding(salesOrder,embeddings_deployment,AzureOpenAIClient):
    detail=get_sales_order_details(salesOrder["details"])
    if len(detail):
        salesOrder["salesOrderDetailVector"] = Embeddings.generate_embeddings (detail,embeddings_deployment,AzureOpenAIClient)

    return salesOrder


