from functions.files_validator import is_valid_file, inside_work_dir
from os import path
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        inside_work_dir(working_directory, file_path)
        if not is_valid_file(working_directory, file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        working_directory = path.abspath(working_directory)
        full_path = path.abspath(path.join(working_directory, file_path))
        with open(full_path, "r") as f:
            content = f.read(MAX_CHARS)
            builder = [content]
            if len(content) == 10_000:
                builder.append(
                    f'[...File "{file_path}" truncated at 10000 characters]',
                )
            return "\n".join(builder)

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content as string, limited to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to get content from, relative to the working directory.",
            ),
        },
    ),
)
