from dotenv import load_dotenv
import os
import sys
import google.genai as genai
from google.genai import types
from call_function import call_function, available_functions
from config import MAX_ITERATIONS

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print("Prompt is not provided")
        sys.exit(1)
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = generate_content(client, messages, verbose)
    print(response)


def generate_content(client, messages, verbose):
    iteration = 0
    recent_response = None
    while iteration < MAX_ITERATIONS:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if verbose:
            print(
                f"Prompt tokens on {iteration} iteration:",
                response.usage_metadata.prompt_token_count,
            )
            print(
                f"Response tokens on {iteration} iteration:",
                response.usage_metadata.candidates_token_count,
            )

        if not response.function_calls:
            return response.text
        recent_response = response.text

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

        messages.extend(function_responses)
        for candidate in response.candidates:
            messages.append(candidate.content)
        iteration += 1

    return recent_response


if __name__ == "__main__":
    main()
