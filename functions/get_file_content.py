import os
from config import MAX_CHARS


MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    
    working_dir_abs_path = os.path.abspath(working_directory)

    print(f"checking abs_path to working directory: {working_dir_abs_path}")

    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    print(f"checking target_file : {target_file}")

    valid_target_file = os.path.commonpath([target_file, working_dir_abs_path]) == working_dir_abs_path

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try: 
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            
            # After reading the first MAX_CHARS...
            if f.read(1):
                print("more than max char")
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                print(content) 
                return 0
            
            print(content)

            return "everything printed!"
            

            

    except:
        raise Exception("Error: issue with file reading")
    


    

