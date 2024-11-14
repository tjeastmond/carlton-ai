import logging
import os
import sys
from datetime import datetime

from openai import OpenAI
from prompts import BASIC_CREATE_PROMPT, CODE_REVIEW_PROMPT
from rich import print as rprint
from rich.markdown import Markdown
from termcolor import colored

ARROWS = colored(">>> ", "white")

# openai model
MODEL = "gpt-4o-mini"

# create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# configure logging
logging.basicConfig(filename="logs/gen_code.log", level=logging.INFO, format="%(message)s")


def log_message(message: str) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{current_time} - {message}")


def is_binary_file(file_path: str) -> bool:
    if not os.path.isfile(file_path):
        return False

    with open(file_path, "rb") as f:
        chunk = f.read(1024)
        return b"\0" in chunk
    return False


def read_files(file_paths: list):
    content = {}
    for path in file_paths:
        if os.path.isfile(path):
            with open(path, "r") as file:
                content[path] = file.read()
        else:
            content[path] = None
    return content


def create_context(file_paths):
    file_contents = read_files(file_paths)
    context = ""
    for file in file_contents:
        if file_contents[file] is not None:
            context += f"### FILE: {file}" + "\n" + file_contents[file] + "\n"

    return context


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def generate_code(code_request):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": code_request},
        ],
    )

    code = response.choices[0].message.content

    log_message(f"Prompt: {code_request}")
    log_message(f"Generated code: {code}")

    return code


def save_code_to_file(code: str) -> None:
    user_input = input(f"{ARROWS}Do you want to save this file? (y/n): ").strip().lower()

    if user_input in ["y", "yes"]:
        file_name = input(f"{ARROWS}Enter a file name: ").strip()

        with open(file_name, "w") as file:
            file.write(code)

        print(f"Text saved to {file_name}.")

    elif user_input in ["n", "no"]:
        print()

    else:
        print("What? Try that again.")
        save_code_to_file(code)


def save_to_file(file_name: str, code: str) -> None:
    with open(file_name, "w") as file:
        file.write(code)

    print(colored(f"Text saved to {file_name}", "green"))


def main() -> None:
    last_response = None
    cwd = os.getcwd()

    try:
        while True:
            user_input = input(f"{ARROWS}").strip().lower()

            if not user_input:
                continue

            elif user_input.startswith("/create"):
                user_instruction = user_input[7:].strip()

                if not user_instruction:
                    print(colored("You need to supply instructions", "red"))
                    continue

                prompt_string = BASIC_CREATE_PROMPT + f"{user_instruction}"
                code = generate_code(prompt_string)
                last_response = code

                print(f"\n{code}\n")

            elif user_input.startswith("/review"):
                file_name = user_input[7:].strip()

                if not file_name:
                    print(colored("You need to supply a file name", "red"))
                    continue

                if is_binary_file(file_name):
                    print(colored("Binary files are not supported", "red"))
                    continue

                file_path = f"{cwd}/{file_name}"
                context = create_context([file_path])
                prompt_string = CODE_REVIEW_PROMPT + context
                review = generate_code(prompt_string)
                last_response = review

                print(prompt_string)

                rprint(Markdown(review))

            elif user_input.startswith("/save"):
                if not last_response:
                    print(colored("No code to save", "red"))
                    continue

                file_name = user_input[5:].strip()

                if not file_name:
                    print(colored("You need to supply a file name", "red"))
                    continue

                save_to_file(f"{cwd}/{file_name}", last_response)

            elif user_input in ["/edit"]:
                pass

            elif user_input in ["/exit"]:
                break

            elif user_input == "/?":
                help_text = ""
                help_text += colored("\nSlash Commands:\n\n", "green")
                help_text += colored("  /create", "yellow") + colored(" - Create a new file\n", "light_grey")
                help_text += colored("  /edit  ", "yellow") + colored(" - Edit a file. File path required\n", "light_grey")
                help_text += colored("  /review", "yellow") + colored(" - Give me a file name and I will review it\n", "light_grey")
                help_text += colored("  /save  ", "yellow") + colored(" - Supply a file name to save your work\n", "light_grey")
                help_text += colored("  /exit  ", "yellow") + colored(" - Exit the program\n", "light_grey")

                print(help_text)

            else:
                print(colored("Invalid command", "red"))
                pass

    except KeyboardInterrupt:
        sys.stdout.write("\r")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
