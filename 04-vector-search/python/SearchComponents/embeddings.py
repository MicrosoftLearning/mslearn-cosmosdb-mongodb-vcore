from tenacity import retry, wait_random_exponential, stop_after_attempt
import time
import json

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def generate_embeddings(text,embeddings_deployment,AzureOpenAIClient):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    response = AzureOpenAIClient.embeddings.create(
        input=text
        , model=embeddings_deployment)
    
    embeddings = json.loads(response.model_dump_json(indent=2))
    time.sleep(0.01) # rest period to avoid rate limiting, on AOAI for free tier try increasing this to 0.5
    return embeddings["data"][0]["embedding"]
