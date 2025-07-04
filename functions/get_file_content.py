from functions.files_validator import validate_file, inside_work_dir
from os import path

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        inside_work_dir(working_directory, file_path)
        validate_file(working_directory, file_path)

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
