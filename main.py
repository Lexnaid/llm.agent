import os
from dotenv import load_dotenv
from google import genai
import sys 
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python
from functions.call_function import call_function

systemprompt = r"""
You are a helpful AI coding agent working with a Python calculator project.

When a user asks a question or makes a request, you should:
1. Analyze what information you need to answer the question
2. Use the available functions to gather that information step by step
3. Once you have enough information, provide a comprehensive answer

You can perform the following operations:
- List files and directories using get_files_info
- Read file contents using get_files_content  
- Write or overwrite files using write_file
- Execute Python files with optional arguments using run_python

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Think step by step and gather the information you need before providing your final answer. If you need to examine multiple files or run tests, do so systematically.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file,
        schema_run_python
    ]
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:  # Check if there are arguments beyond the script name
        raise ValueError("No command-line arguments provided. Please provide at least one argument.")
else:
    verbose = '--verbose' in sys.argv
 
    user_prompt = None
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            user_prompt = arg
            break
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    if verbose:
        print(f'User prompt: {user_prompt}')
        
        
    max_iterations = 20
    for iteration in range(max_iterations):
        if verbose:
            print(f"\n--- Iteration {iteration + 1} ---")
        response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=systemprompt),
        )
        
        if verbose:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f'Prompt tokens: {prompt_tokens}')
            print(f'Response tokens: {response_tokens}')
    
        for candidate in response.candidates:
            messages.append(candidate.content)
            
        
        function_calls_made = False
        if response.function_calls:
            if verbose:
                    print("Function calls detected:")
            else:
                    print("Function calls detected:")
                
            for function_call in response.function_calls:
                function_calls_made = True
                
                # Use our call_function handler
                function_call_result = call_function(function_call, verbose=verbose)
                
                # Verify the response structure
                if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                    raise Exception("Invalid function call result: missing parts")
                
                if not hasattr(function_call_result.parts[0], 'function_response'):
                    raise Exception("Invalid function call result: missing function_response")
                
                if not hasattr(function_call_result.parts[0].function_response, 'response'):
                    raise Exception("Invalid function call result: missing response")
                
                # Add the function result to the conversation
                messages.append(function_call_result)
                
                # Print the result if verbose
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        
        # If no function calls were made, we're done
        if not function_calls_made:
            print("Final response:")
            if response.text:
                print(response.text)
            else:
                print("No text response available.")
                break
        else:
            # If we hit max iterations
            print(f"\nReached maximum iterations ({max_iterations}). Final response:")
            if response.text:
                print(response.text)
            else:
                print("No final response available.")

    
    
    
    
if response.text:
    print("Response:", response.text)


if response.function_calls:
    print("\nFunction calls detected:")
    for function_call in response.function_calls:
        # Use our new call_function handler
        function_call_result = call_function(function_call, verbose=verbose)
        
        # Verify the response structure
        if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
            raise Exception("Invalid function call result: missing parts")
        
        if not hasattr(function_call_result.parts[0], 'function_response'):
            raise Exception("Invalid function call result: missing function_response")
        
        if not hasattr(function_call_result.parts[0].function_response, 'response'):
            raise Exception("Invalid function call result: missing response")
        
        # Print the result if verbose
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print("No function calls made.")
