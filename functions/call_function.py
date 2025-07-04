import os
from google.genai import types

# Import all your functions
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.run_python import run_python

# Create a function registry
FUNCTION_REGISTRY = {
    "get_files_info": get_files_info,
    "write_file": write_file,
    "get_file_content": get_file_content,
    "run_python": run_python,
}

def call_function(function_call_part, verbose=False):
    """
    Handle the abstract task of calling one of our four functions.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: If True, print detailed function call info
    
    Returns:
        types.Content with function response
    """
    function_name = function_call_part.name
    function_args = function_call_part.args.copy()  # Make a copy to avoid modifying original
    
    # Print function call info
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in FUNCTION_REGISTRY:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add working directory to arguments
    function_args["working_directory"] = "./calculator"
    
    # Get the function and call it
    function_to_call = FUNCTION_REGISTRY[function_name]
    
    try:
        # Call the function with keyword arguments
        function_result = function_to_call(**function_args)
        
        # Return success response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
        
    except Exception as e:
        # Return error response if function call fails
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function execution failed: {str(e)}"},
                )
            ],
        )

