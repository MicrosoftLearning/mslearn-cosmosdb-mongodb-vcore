// Import the Embeddings module from the SearchComponents directory
const Embeddings = require('../SearchComponents/embeddings');

// Function to convert a list of sales order details into a single string
function getSalesOrderDetails(details) {
    let detailsString = "";

    // Iterate over each detail in the list
    for (let idx = 0; idx < details.length; idx++) {
        const detail = details[idx];
        // Concatenate each detail's SKU and name into the detailsString
        detailsString += (idx > 0 ? "; " : "") +
            (detail.sku ? detail.sku : "") +
            (detail.name ? "," + detail.name : "");
    }

    // Return the concatenated string of details
    return detailsString;
}

// Asynchronous function to generate an embedding for a sales order
async function generateSalesOrderEmbedding(salesOrder, embeddingsDeployment, AzureOpenAIClient) {
    // Get the string representation of the sales order's details
    const detail = getSalesOrderDetails(salesOrder.details);
    // If the detail string has content, generate an embedding for it
    if (detail.length > 0) {
        // The embedding is generated using the Embeddings module's generateEmbeddings function
        // The resulting embedding is stored in the salesOrder object under the key "salesOrderDetailVector"
        salesOrder.salesOrderDetailVector = await Embeddings.generateEmbeddings(detail, embeddingsDeployment, AzureOpenAIClient);
    }

    // Return the salesOrder object with the added embedding
    return salesOrder;
}

// Export the generateSalesOrderEmbedding function
module.exports.generateSalesOrderEmbedding = generateSalesOrderEmbedding;