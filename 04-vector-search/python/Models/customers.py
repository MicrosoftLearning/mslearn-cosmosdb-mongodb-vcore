def get_customer_addresses(addresses):
    addresses_string = ""

    for idx, address in enumerate(addresses):
        addresses_string= addresses_string + ("; " if idx > 0  else "")  \
                        + ("Address Line - " + address["addressLine1"] if address["addressLine1"]  else "")  \
                        + (" " + address["addressLine2"] if address["addressLine2"]  else "") \
                        + (", city - " + address["city"] if address["city"] else "") \
                        + (", state - " + address["state"] if address["state"] else "") \
                        + (", country - " + address["country"] if address["country"] else "") \
                        + (", zipcode - " + address["zipCode"] if address["zipCode"] else "") \
                        + (", location - " + address["location"] if address["location"] else "")  
        
    return addresses_string

def generate_customer_embedding(customer,embeddings_deployment,AzureOpenAIClient):
    if customer["type"]:
        customer["customerTypeVector"] = Embeddings.generate_embeddings (customer["type"],embeddings_deployment,AzureOpenAIClient)

    if customer["title"]:
        customer["customerTitleVector"] = Embeddings.generate_embeddings (customer["title"],embeddings_deployment,AzureOpenAIClient)

    if customer["firstName"]+" "+customer["lastName"]:
        customer["customerNameVector"] = Embeddings.generate_embeddings (customer["firstName"]+" "+customer["lastName"],embeddings_deployment,AzureOpenAIClient)

    if customer["emailAddress"]:
        customer["customerEmailAddressVector"] = Embeddings.generate_embeddings (customer["emailAddress"],embeddings_deployment,AzureOpenAIClient)

    if customer["phoneNumber"]:
        customer["customerPhoneNumberVector"] = Embeddings.generate_embeddings (customer["phoneNumber"],embeddings_deployment,AzureOpenAIClient)

    address = get_customer_addresses(customer["addresses"])
    if len(address) > 0:
        customer["customerAddressesVector"] = Embeddings.generate_embeddings (address,embeddings_deployment,AzureOpenAIClient)

    return customer



