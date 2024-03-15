# Import the embeddings module
import SearchComponents.embeddings as Embeddings

# Function to get a string representation of sales order details
def getSalesOrderDetails(details):
    details_string = ""

    # Iterate over each detail in the details list
    for idx, detail in enumerate(details):
        # Concatenate the SKU and name of the detail to the details_string
        details_string= details_string + ("; " if idx > 0  else "")  \
                        + (detail["sku"] if detail["sku"]  else "")  \
                        + ("," + detail["name"] if detail["name"]  else "")

    # Return the concatenated string of details
    return details_string

# Function to generate embeddings for sales order data
def generateSalesOrderEmbedding(salesOrder,embeddings_deployment,AzureOpenAIClient):
    # Get the string representation of sales order details
    detail=getSalesOrderDetails(salesOrder["details"])
    # If the detail string has length greater than 0
    if len(detail):
        # Generate embeddings for the detail string
        salesOrder["salesOrderDetailVector"] = Embeddings.generateEmbeddings (detail,embeddings_deployment,AzureOpenAIClient)

    # Return the sales order data with the generated embeddings
    return salesOrder