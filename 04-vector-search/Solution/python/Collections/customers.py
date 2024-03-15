# Import the embeddings module
import SearchComponents.embeddings as Embeddings

# Function to get a string representation of customer addresses
def getCustomerAddresses(addresses):
    addresses_string = ""

    # Iterate over each address in the addresses list
    for idx, address in enumerate(addresses):
        # Concatenate the address details to the addresses_string
        addresses_string= addresses_string + ("; " if idx > 0  else "")  \
                        + ("Address Line - " + address["addressLine1"] if address["addressLine1"]  else "")  \
                        + (" " + address["addressLine2"] if address["addressLine2"]  else "") \
                        + (", city - " + address["city"] if address["city"] else "") \
                        + (", state - " + address["state"] if address["state"] else "") \
                        + (", country - " + address["country"] if address["country"] else "") \
                        + (", zipcode - " + address["zipCode"] if address["zipCode"] else "") \
                        + (", location - " + address["location"] if address["location"] else "")  
    
    # Return the concatenated string of addresses
    return addresses_string

# Function to generate embeddings for customer data
def generateCustomerEmbedding(customer,embeddings_deployment,AzureOpenAIClient):
    # Generate embeddings for customer type if it exists
    if customer["type"]:
        customer["customerTypeVector"] = Embeddings.generateEmbeddings (customer["type"],embeddings_deployment,AzureOpenAIClient)

    # Generate embeddings for customer title if it exists
    if customer["title"]:
        customer["customerTitleVector"] = Embeddings.generateEmbeddings (customer["title"],embeddings_deployment,AzureOpenAIClient)

    # Generate embeddings for customer name if it exists
    if customer["firstName"]+" "+customer["lastName"]:
        customer["customerNameVector"] = Embeddings.generateEmbeddings (customer["firstName"]+" "+customer["lastName"],embeddings_deployment,AzureOpenAIClient)

    # Generate embeddings for customer email address if it exists
    if customer["emailAddress"]:
        customer["customerEmailAddressVector"] = Embeddings.generateEmbeddings (customer["emailAddress"],embeddings_deployment,AzureOpenAIClient)

    # Generate embeddings for customer phone number if it exists
    if customer["phoneNumber"]:
        customer["customerPhoneNumberVector"] = Embeddings.generateEmbeddings (customer["phoneNumber"],embeddings_deployment,AzureOpenAIClient)

    # Get the string representation of customer addresses
    address = getCustomerAddresses(customer["addresses"])
    # Generate embeddings for customer addresses if they exist
    if len(address) > 0:
        customer["customerAddressesVector"] = Embeddings.generateEmbeddings (address,embeddings_deployment,AzureOpenAIClient)

    # Return the customer data with generated embeddings
    return customer