import logging
import os
import sys
from datetime import datetime

import yaml
from openai import OpenAI
from prompts import BASIC_CREATE_PROMPT
from termcolor import colored

# openai model
MODEL = "gpt-4o-mini"

ARROWS = colored(">>> ", "white", attrs=["bold"])

# create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# configure logging
logging.basicConfig(filename="logs/gen_code.log", level=logging.INFO, format="%(message)s")


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def generate_code(code_request):
    prompt_string = BASIC_CREATE_PROMPT + f"\n\n{code_request}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt_string},
        ],
    )

    code = response.choices[0].message.content

    log_message(f"Prompt: {prompt_string}")
    log_message(f"Generated code: {code}")

    return code


def log_message(message: str) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{current_time} - {message}")


def save_code_to_file(code: str) -> None:
    user_input = input(f"{ARROWS}Do you want to save this file? (y/n): ").strip().lower()

    if user_input in ["y", "yes"]:
        file_name = input(f"{ARROWS}Please enter a file name: ").strip()

        with open(file_name, "w") as file:
            file.write(code)

        print(f"Text saved to {file_name}.")

    elif user_input in ["n", "no"]:
        print()

    else:
        print("What? Try that again.")
        save_code_to_file(code)


def chat_input() -> str:
    response = input(f"{ARROWS}")
    return response


def main() -> None:
    try:
        while True:
            user_input = input(f"{ARROWS}").strip().lower()

            if not user_input:
                continue

            elif user_input in ["bye", "/exit", "/quit"]:
                print()
                break

            else:
                generated_code = generate_code(user_input)
                print(f"\n{generated_code}\n")
                save_code_to_file(generated_code)

    except KeyboardInterrupt:
        sys.stdout.write("\r")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
