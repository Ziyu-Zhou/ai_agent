import os
import subprocess

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




    


