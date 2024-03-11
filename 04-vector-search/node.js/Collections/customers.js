const Embeddings = require('./SearchComponents/embeddings');

function getCustomerAddresses(addresses) {
    let addressesString = "";

    for (let idx = 0; idx < addresses.length; idx++) {
        const address = addresses[idx];
        addressesString += (idx > 0 ? "; " : "") +
            (address.addressLine1 ? "Address Line - " + address.addressLine1 : "") +
            (address.addressLine2 ? " " + address.addressLine2 : "") +
            (address.city ? ", city - " + address.city : "") +
            (address.state ? ", state - " + address.state : "") +
            (address.country ? ", country - " + address.country : "") +
            (address.zipCode ? ", zipcode - " + address.zipCode : "") +
            (address.location ? ", location - " + address.location : "");
    }

    return addressesString;
}

async function generateCustomerEmbedding(customer, embeddingsDeployment, AzureOpenAIClient) {
    if (customer.type) {
        customer.customerTypeVector = await Embeddings.generateEmbeddings(customer.type, embeddingsDeployment, AzureOpenAIClient);
    }

    if (customer.title) {
        customer.customerTitleVector = await Embeddings.generateEmbeddings(customer.title, embeddingsDeployment, AzureOpenAIClient);
    }

    if (customer.firstName && customer.lastName) {
        customer.customerNameVector = await Embeddings.generateEmbeddings(customer.firstName + " " + customer.lastName, embeddingsDeployment, AzureOpenAIClient);
    }

    if (customer.emailAddress) {
        customer.customerEmailAddressVector = await Embeddings.generateEmbeddings(customer.emailAddress, embeddingsDeployment, AzureOpenAIClient);
    }

    if (customer.phoneNumber) {
        customer.customerPhoneNumberVector = await Embeddings.generateEmbeddings(customer.phoneNumber, embeddingsDeployment, AzureOpenAIClient);
    }

    const address = getCustomerAddresses(customer.addresses);
    if (address.length > 0) {
        customer.customerAddressesVector = await Embeddings.generateEmbeddings(address, embeddingsDeployment, AzureOpenAIClient);
    }

    return customer;
}