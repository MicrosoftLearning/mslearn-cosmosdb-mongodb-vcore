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

    pass  # Replace this line with the lab's code

