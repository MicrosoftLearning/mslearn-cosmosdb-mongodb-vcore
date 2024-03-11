const Embeddings = require('./SearchComponents/embeddings');

function getSalesOrderDetails(details) {
    let detailsString = "";

    for (let idx = 0; idx < details.length; idx++) {
        const detail = details[idx];
        detailsString += (idx > 0 ? "; " : "") +
            (detail.sku ? detail.sku : "") +
            (detail.name ? "," + detail.name : "");
    }

    return detailsString;
}

async function generateSalesOrderEmbedding(salesOrder, embeddingsDeployment, AzureOpenAIClient) {
    const detail = getSalesOrderDetails(salesOrder.details);
    if (detail.length > 0) {
        salesOrder.salesOrderDetailVector = await Embeddings.generateEmbeddings(detail, embeddingsDeployment, AzureOpenAIClient);
    }

    return salesOrder;
}