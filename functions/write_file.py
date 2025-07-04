from functions.files_validator import inside_work_dir
from os import path


def write_file(working_directory, file_path, content):
    try:
        inside_work_dir(working_directory, file_path)
        working_directory = path.abspath(working_directory)
        full_path = path.abspath(path.join(working_directory, file_path))
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
