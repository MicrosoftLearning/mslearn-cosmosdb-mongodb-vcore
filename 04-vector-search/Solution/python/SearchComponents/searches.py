# Import the necessary modules and components
import SearchComponents.vectorSearch as VectorSearch
import SearchComponents.completion as Completion
import os

# Function to run a vector search
def runVectorSearch(embeddings_deployment, AzureOpenAIClient, client, cosmos_db_mongodb_database):
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Ask the user for their query
    print("What would you like to know about our bike shop's inventory?")
    user_input = input("Prompt: ")
    
    # Define the maximum number of results, the vector column name, and the collection name
    maxResults = 20
    vector_column = "productVector"
    collection_name = "products"

    # Connect to the database and the collection
    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]
    
    # Run the vector search and print the results
    results = VectorSearch.vectorSearch(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
    for result in results: 
        print(f"Similarity Score: {result['similarityScore']}"
              + f", category: {result['document']['categoryName']}" 
              + f", Product: {result['document']['name']}")  

# Function to run a GPT search
def runGPTSearch(embeddings_deployment, AzureOpenAIClient, completion_deployment, AzureOpenAICompletionClient, client, cosmos_db_mongodb_database):
    # Define the maximum number of results, the vector column name, and the collection name
    maxResults = 20
    vector_column = "productVector"
    collection_name = "products"

    # Connect to the database and the collection
    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]

    # Clear the console and ask the user for their query
    user_input = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
    user_input = input("Prompt: ")
    
    # Keep asking for queries until the user types 'end'
    while user_input.lower() != "end":
        # Run the vector search and generate completions
        results_for_prompt = VectorSearch.vectorSearch(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
        completions_results = Completion.generateCompletion(results_for_prompt,completion_deployment,AzureOpenAICompletionClient,user_input)
        
        # Print the completions
        print("\n"+completions_results['choices'][0]['message']['content'])

        # Ask for the next query
        print("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
        user_input = input("Prompt: ")