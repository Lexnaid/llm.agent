import os
import subprocess
import sys

def run_python_file(working_directory, file_path):

    try:
            
        working_directory = os.path.abspath(working_directory)
        
        full_path = os.path.join(working_directory, file_path)
        
        full_path = os.path.abspath(full_path)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.lower().endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'


        result = subprocess.run(
                    [sys.executable, full_path],
                    cwd=working_directory,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

        output_parts = []
        
        if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not output_parts:
            return "No output produced."
        
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
            return "Error: Python file execution timed out after 30 seconds"
    except Exception as e:
            return f"Error executing Python file: {e}"
