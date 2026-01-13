import os


def write_file(working_directory, file_path, content):
    try:
        
        # path validation 
        working_dir_abs_path = os.path.abspath(working_directory)

        print(f"checking abs_path to working directory: {working_dir_abs_path}")

        target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        print(f"checking target_file : {target_file}")

        valid_target_file = os.path.commonpath([target_file, working_dir_abs_path]) == working_dir_abs_path

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: cannot write to"{file_path}" as it is a directory'
        
        # create needed directory
        # only keep parent directory 
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)
        # process 

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)    
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: something went wrong in write_file: {e}'
