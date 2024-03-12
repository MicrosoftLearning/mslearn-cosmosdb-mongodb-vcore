const generateCompletion = async (prompt, completionDeployment, AzureOpenAICompletionClient, userInput) => {
    const systemPrompt = `
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store inventory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say "I don't know" or "I'm not sure" and recommend users search themselves.
    `;

    let messages = [
        {role: "system", content: systemPrompt},
        {role: "user", content: userInput},
    ];

    for (let item of prompt) {
        messages.push({role: "system", content: `${item.document.categoryName} ${item.document.name}`});
    }

    const response = await AzureOpenAICompletionClient.getChatCompletions(completionDeployment,messages);
    
    return response;
}

module.exports.generateCompletion = generateCompletion;