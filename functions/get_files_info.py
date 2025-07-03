import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        target_path = working_directory
    else:
        # Create full path by joining working directory with relative path
        target_path = os.path.join(working_directory, directory)

    working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(target_path)
    print(working_directory)
    print(target_path)
    
    if not target_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_path):
        return f'Error: "{directory}" does not exist'
    
    # Check if target path is a directory
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        items = os.listdir(target_path)
        items.sort()  # Sort for consistent output
        
        result_lines = []
        for item in items:
            item_path = os.path.join(target_path, item)
            
            # Get file size
            try:
                file_size = os.path.getsize(item_path)
            except OSError:
                file_size = 0
            
            # Check if it's a directory
            is_directory = os.path.isdir(item_path)
            
            # Format the line
            line = f"- {item}: file_size={file_size} bytes, is_dir={is_directory}"
            result_lines.append(line)
        
        if not result_lines:
            return "Directory is empty"
        
        return "\n".join(result_lines)
        
    except PermissionError:
        return f'Error: Permission denied accessing "{directory}"'
    except OSError as e:
        return f'Error: Unable to list directory "{directory}": {str(e)}'
