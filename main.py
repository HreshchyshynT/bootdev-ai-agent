from dotenv import load_dotenv
import os
import google.genai as genai


def main():
    loaded = load_dotenv()
    print(f"env loaded: {loaded}")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(response.text)
    print(
        f"""Prompt tokens: {prompt_tokens}
Response tokens: {response_tokens}"""
    )


if __name__ == "__main__":
    main()
