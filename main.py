import os
from dotenv import load_dotenv
from google import genai
import sys 
from google.genai import types





load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:  # Check if there are arguments beyond the script name
        raise ValueError("No command-line arguments provided. Please provide at least one argument.")
else:

    verbose = '--verbose' in sys.argv

    user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if verbose:
            print(f'User prompt: {user_prompt}')
            print(f'Prompt tokens: {prompt_tokens}')
            print(f'Response tokens: {response_tokens}')
    
print(response.text)




#print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
#print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

