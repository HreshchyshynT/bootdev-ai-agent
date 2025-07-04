from os import path


def inside_work_dir(working_directory, filepath=None):
    working_directory = path.abspath(working_directory)
    full_path = working_directory
    if filepath:
        full_path = path.abspath(path.join(working_directory, filepath))

    if not working_directory in full_path:
        raise Exception(
            f'Cannot list "{filepath}" as it is outside the permitted working directory',
        )


def is_valid_file(working_directory, filepath):
    working_directory = path.abspath(working_directory)
    full_path = path.abspath(path.join(working_directory, filepath))
    return path.exists(full_path) and path.isfile(full_path)
