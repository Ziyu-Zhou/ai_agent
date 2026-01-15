import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    working_dir_abs_path = os.path.abspath(working_directory)

    # print(f"checking abs_path to working directory: {working_dir_abs_path}")

    target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))

    # print(f"checking target_dir : {target_dir}")


    valid_target_dir = os.path.commonpath([target_dir, working_dir_abs_path]) == working_dir_abs_path


    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    # iterate over the items in the target directory. For each of them, record the name, 
    # file size, and whether it's a directory itself. Use this data to build and return a
    # string representing the contents of the target directory. It should be in the following format:

    for element in os.listdir(target_dir):
        full_path = os.path.join(target_dir, element)
        is_dir = os.path.isdir(full_path)
        file_size = os.path.getsize(full_path)

        print(f"{element}: file_size={file_size}, is_dir={is_dir}")


    return "end of get_files_info"
    
    


    
