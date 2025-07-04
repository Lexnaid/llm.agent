import os

def get_file_content(working_directory, file_path):
    
    working_directory = os.path.abspath(working_directory)
    
    full_path = os.path.join(working_directory, file_path)
    
    full_path = os.path.abspath(full_path)
    
    
    
    
    if not full_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory {working_directory}'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000

    try:
        with open(full_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
        return file_content_string
    except Exception as e:
        return f'Error: Failed to read file "{file_path}": {e}'
    
from google.genai import types
 
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(  # CHANGED: from "directory" to "file_path"
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

