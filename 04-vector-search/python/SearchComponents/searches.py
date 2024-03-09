import SearchComponents.vectorSearch as VectorSearch
import SearchComponents.completion as Completion
import os


def Run_vector_search(embeddings_deployment, AzureOpenAIClient, client, cosmos_db_mongodb_database):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("What would you like to know about our bike shop's inventory?")
    user_input = input("Prompt: ")
    maxResults = 20
    vector_column = "productVector" # input("Enter the vector column name: ")
    collection_name = "products" # input("Enter the collection name: ")


    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]
    results = VectorSearch.vector_search(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
    for result in results: 
        print(f"Similarity Score: {result['similarityScore']}"
              + f", category: {result['document']['categoryName']}" 
              + f", Product: {result['document']['name']}")  


def Run_GPT_search(embeddings_deployment, AzureOpenAIClient, completion_deployment, AzureOpenAICompletionClient, client, cosmos_db_mongodb_database):
    maxResults = 20
    vector_column = "productVector" # input("Enter the vector column name: ")
    collection_name = "products" # input("Enter the collection name: ")

    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]

    user_input = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
    user_input = input("Prompt: ")
    while user_input.lower() != "end":
        results_for_prompt = VectorSearch.vector_search(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)

        completions_results = Completion.generate_completion(results_for_prompt,completion_deployment,AzureOpenAICompletionClient,user_input)
        print("\n"+completions_results['choices'][0]['message']['content'])

        print("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
        user_input = input("Prompt: ")

