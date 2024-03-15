# Import the json module
import json

# Function to generate completions for a given prompt
def generateCompletion(prompt,completion_deployment,AzureOpenAICompletionClient,user_input):
    # Define the system prompt
    system_prompt = '''
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store invetory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say ""I don't know"" or ""I'm not sure"" and recommend users search themselves."
    '''

    # Initialize the messages list with the system prompt and user input
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    
    # Add each item in the prompt to the messages list
    for item in prompt:
        messages.append({"role": "system", "content": item['document']['categoryName']+" "+item['document']['name']})
    
    # Generate the chat completions using the AzureOpenAICompletionClient
    response = AzureOpenAICompletionClient.chat.completions.create(model=completion_deployment, messages=messages)
    
    # Parse the response into a json object
    completions = json.loads(response.model_dump_json(indent=2))

    # Return the completions
    return completions