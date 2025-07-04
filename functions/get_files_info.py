from os import path
import os


def get_path_info(file_path):
    is_dir = path.isdir(file_path)
    if not is_dir:
        return path.getsize(file_path), is_dir
    size = 0
    for filename in os.listdir(file_path):
        size += get_path_info(path.join(file_path, filename))[0]
    return size, is_dir


def get_files_info(working_directory, directory=None):
    try:
        working_directory = path.abspath(working_directory)
        full_path = working_directory
        if directory:
            full_path = path.abspath(path.join(working_directory, directory))

        if not working_directory in full_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        if directory == ".":
            dir_name = "current"
        else:
            dir_name = f"'{directory}'"
        builder = [f"Result for {dir_name} directory"]
        for file in os.listdir(full_path):
            info = get_path_info(path.join(full_path, file))
            builder.append(
                f"- {file}: file_size={info[0]} bytes, is_dir={info[1]}",
            )
        return "\n".join(builder)
    except Exception as e:
        return f"Error: {e}"
