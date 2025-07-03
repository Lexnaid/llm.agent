import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    
    full_path = os.path.join(working_directory, file_path)
    
    full_path = os.path.abspath(full_path)
    if not full_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory {working_directory}'

    try:
        parent_dir = os.path.dirname(full_path)
        
        if not os.path.exists(parent_dir):
            return os.mkdir(parent_dir)
        
        
        with open(full_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
