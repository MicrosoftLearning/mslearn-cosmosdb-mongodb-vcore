// Import the Embeddings module from the SearchComponents directory
const Embeddings = require('../SearchComponents/embeddings');

// Function to convert a list of address objects into a single string
function getCustomerAddresses(addresses) {
    let addressesString = "";

    // Iterate over each address in the list
    for (let idx = 0; idx < addresses.length; idx++) {
        const address = addresses[idx];
        // Concatenate each address field into the addressesString
        addressesString += (idx > 0 ? "; " : "") +
            (address.addressLine1 ? "Address Line - " + address.addressLine1 : "") +
            (address.addressLine2 ? " " + address.addressLine2 : "") +
            (address.city ? ", city - " + address.city : "") +
            (address.state ? ", state - " + address.state : "") +
            (address.country ? ", country - " + address.country : "") +
            (address.zipCode ? ", zipcode - " + address.zipCode : "") +
            (address.location ? ", location - " + address.location : "");
    }

    // Return the concatenated string of addresses
    return addressesString;
}

// Asynchronous function to generate embeddings for various customer fields
async function generateCustomerEmbedding(customer, embeddingsDeployment, AzureOpenAIClient) {
    // If the customer has a type, generate an embedding for it
    if (customer.type) {
        customer.customerTypeVector = await Embeddings.generateEmbeddings(customer.type, embeddingsDeployment, AzureOpenAIClient);
    }

    // If the customer has a title, generate an embedding for it
    if (customer.title) {
        customer.customerTitleVector = await Embeddings.generateEmbeddings(customer.title, embeddingsDeployment, AzureOpenAIClient);
    }

    // If the customer has a first and last name, generate an embedding for it
    if (customer.firstName && customer.lastName) {
        customer.customerNameVector = await Embeddings.generateEmbeddings(customer.firstName + " " + customer.lastName, embeddingsDeployment, AzureOpenAIClient);
    }

    // If the customer has an email address, generate an embedding for it
    if (customer.emailAddress) {
        customer.customerEmailAddressVector = await Embeddings.generateEmbeddings(customer.emailAddress, embeddingsDeployment, AzureOpenAIClient);
    }

    // If the customer has a phone number, generate an embedding for it
    if (customer.phoneNumber) {
        customer.customerPhoneNumberVector = await Embeddings.generateEmbeddings(customer.phoneNumber, embeddingsDeployment, AzureOpenAIClient);
    }

    // Get the string representation of the customer's addresses
    const address = getCustomerAddresses(customer.addresses);
    // If the customer has addresses, generate an embedding for them
    if (address.length > 0) {
        customer.customerAddressesVector = await Embeddings.generateEmbeddings(address, embeddingsDeployment, AzureOpenAIClient);
    }

    // Return the customer object with the added embeddings
    return customer;
}

// Export the generateCustomerEmbedding function
module.exports.generateCustomerEmbedding = generateCustomerEmbedding;