# Import the retry and wait_random_exponential functions from the tenacity module
# These will be used to retry the generateEmbeddings function in case of failure
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Import the time and json modules
import time
import json

# Decorate the generateEmbeddings function with the retry decorator
# This will retry the function if it fails, with a random exponential wait time between 1 and 20 seconds, and will stop after 10 attempts
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def generateEmbeddings(text,embeddings_deployment,AzureOpenAIClient):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    # Call the create method of the AzureOpenAIClient's embeddings object to generate embeddings for the input text
    response = AzureOpenAIClient.embeddings.create(
        input=text
        , model=embeddings_deployment)
    
    # Parse the response into a json object
    embeddings = json.loads(response.model_dump_json(indent=2))
    
    # Sleep for 0.01 seconds to avoid rate limiting
    # If using the free tier of Azure OpenAI, you may need to increase this to 0.5 seconds
    time.sleep(0.01)
    
    # Return the embedding from the response
    return embeddings["data"][0]["embedding"]