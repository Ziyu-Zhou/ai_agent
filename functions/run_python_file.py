import os
import subprocess
from google.genai import types


# Gemini tool schema for: run_python_file(working_directory, file_path, args=None)
# Assumes: from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python (.py) file located under the working directory using the system Python "
        "interpreter, optionally passing command-line arguments. Validates that the path stays inside "
        "the permitted working directory, the file exists, and has a .py extension. Captures STDOUT/STDERR "
        "and returns a formatted result string. Enforces a 30-second timeout."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    'Path to the Python file to execute, relative to the working directory '
                    '(e.g., "main.py", "scripts/run_task.py"). Must end with ".py".'
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description=(
                    "Optional list of command-line arguments to pass to the Python program, "
                    'e.g., ["--input", "data.txt", "42"]. If omitted, runs with no extra args.'
                ),
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        # path validation 
        working_dir_abs_path = os.path.abspath(working_directory)

        # print(f"checking abs_path to working directory: {working_dir_abs_path}")

        target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # print(f"checking target_file : {target_file}")

        valid_target_file = os.path.commonpath([target_file, working_dir_abs_path]) == working_dir_abs_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # if os.path.isdir(target_file):
        #     return f'Error: cannot execute"{file_path}" as it is a directory'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        return_obj = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=30
            )
        output_stdout = return_obj.stdout
        output_stderr = return_obj.stderr
        return_code = return_obj.returncode

        result_string = f""
        if return_code != 0:
            result_string += f"Process exited with code {return_code}"

        if len(output_stderr) == 0 and len(output_stdout) == 0:
            result_string += f"No output produced"

        else:
            result_string += f"STDOUT: {output_stdout}STDERR: {output_stderr}"

        return result_string

    except Exception as e:
        return f'Error: something went wrong in run_python_file: {e}'




    


