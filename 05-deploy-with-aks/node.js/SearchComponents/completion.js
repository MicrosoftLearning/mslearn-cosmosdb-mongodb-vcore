// Asynchronous function to generate a completion for a given prompt
const generateCompletion = async (prompt, completionDeployment, AzureOpenAICompletionClient, userInput) => {

    // Define the system prompt that sets the context for the AI
    const systemPrompt = `
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store inventory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say "I don't know" or "I'm not sure" and recommend users search themselves.
    `;

    // Initialize the messages array with the system prompt and user input
    let messages = [
        {role: "system", content: systemPrompt},
        {role: "user", content: userInput},
    ];

    // Add each item from the prompt to the messages array
    for (let item of prompt) {
        messages.push({role: "system", content: `${item.document.categoryName} ${item.document.name}`});
    }

    // Call the Azure OpenAI Completion Client's getChatCompletions function with the completion deployment and messages
    // Await the response and store it in the response variable
    const response = await AzureOpenAICompletionClient.chat.completions.create({ messages: messages, model: completionDeployment });
    
    // Return the response
    return response; 

}

// Export the generateCompletion function
module.exports.generateCompletion = generateCompletion;