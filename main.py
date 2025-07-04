from dotenv import load_dotenv
from functions.get_files_info import get_files_info
import os
import sys
import google.genai as genai
from google.genai import types


def main():
    load_dotenv()
    files_info = get_files_info("calculator/", ".")
    print(f"files: \n{files_info}")
    if len(sys.argv) < 2:
        print("Prompt is not provided")
        sys.exit(1)
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(response.text)
    if not verbose:
        return
    print(f"User prompt: {prompt}")
    print(
        f"""Prompt tokens: {prompt_tokens}
Response tokens: {response_tokens}"""
    )


if __name__ == "__main__":
    main()
