from typing import List
import os
import openai
import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()

    user_input = args.input
    result = generate_branding_snippet(user_input)
    print(result)
    keywords = generate_keywords(user_input)
    print(keywords)


def generate_branding_snippet(input: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Generate upbeat branding snippet for {input}"

    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=32)

    branding_text: str = response["choices"][0]["text"]
    branding_text = branding_text.strip()
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."

    return branding_text


def generate_keywords(input: str) -> List[str]:

    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Generate related branding keywords for {input} without listing them"

    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=32)

    keyword_text: str = response["choices"][0]["text"]
    keyword_text = keyword_text.strip()
    keywords_array = re.split(",|\n|;|-", keyword_text)
    keywords_array = [k.strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    return keywords_array


if __name__ == "__main__":
    main()
