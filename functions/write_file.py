from functions.files_validator import inside_work_dir
from os import path
from google.genai import types


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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to file, create file if not exists yet, remove any existing content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file",
            ),
        },
    ),
)
