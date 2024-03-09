import json

def generate_completion(prompt,completion_deployment,AzureOpenAICompletionClient,user_input):
    system_prompt = '''
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store invetory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say ""I don't know"" or ""I'm not sure"" and recommend users search themselves."
    '''

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    
    for item in prompt:
        messages.append({"role": "system", "content": item['document']['categoryName']+" "+item['document']['name']})
    response = AzureOpenAICompletionClient.chat.completions.create(model=completion_deployment, messages=messages)
    completions = json.loads(response.model_dump_json(indent=2))

    return completions
    
