from functions.files_validator import is_valid_file
from google.genai import types
from os import path
import subprocess


def run_python_file(working_directory, file_path):
    try:
        working_directory = path.abspath(working_directory)
        full_path = path.abspath(path.join(working_directory, file_path))
        if not working_directory in full_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not is_valid_file(working_directory, file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        output = subprocess.run(
            timeout=30,
            capture_output=True,
            args=["python3", full_path],
        )
        buffer = []
        if output.stdout:
            buffer.append(f"STDOUT:\n{output.stdout}")
        if output.stderr:
            buffer.append(f"STDERR:\n{output.stderr}")

        if output.returncode != 0:
            buffer.append(f"Process exited with code {output.returncode}")

        return "\n".join(buffer) if buffer else "No output produced."

    except Exception as e:
        return f"Error executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file using python3 interpreter, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory.",
            ),
        },
    ),
)
