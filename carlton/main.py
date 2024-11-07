import logging
import os
from datetime import datetime

from openai import OpenAI
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompts import BASIC_CREATE_PROMPT
from termcolor import colored

# openai model
MODEL = "gpt-4o-mini"

# chat names
BOT_NAME = "Carlton"
USER_NAME = "You"

# chat colors
BOT_COLOR = "light_green"
USER_COLOR = "light_blue"


# create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# configure logging
logging.basicConfig(filename="../logs/gen_code.log", level=logging.INFO, format="%(message)s")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def bot_asks() -> str:
    user_input = input(f"{colored(USER_NAME, USER_COLOR)}: ").strip().lower()
    return user_input


def bot_says(message: str) -> None:
    print(f"{colored(BOT_NAME, BOT_COLOR)}: {message}")


def bot_listens(message: str) -> None:
    bot_says(message)


def generate_code(code_function):
    prompt_string = BASIC_CREATE_PROMPT + f"\n\n{code_function}"

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


def log_message(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{current_time} - {message}")


def save_code_to_file(code):
    user_input = input("Do you want to save this file? (y/n): ").strip().lower()

    if user_input in ["y", "yes"]:
        file_name = input("Please enter a file name: ").strip()
        with open(file_name, "w") as file:
            file.write(code)
        print(f"Text saved to {file_name}.")

    elif user_input in ["n", "no"]:
        bot_says("Pft, fine")

    else:
        print("What? Try that again.")
        save_code_to_file(code)


def main():
    try:
        print()
        clear_console()
        bot_says("Ready to code")

        completer = WordCompleter(
            [
                "/create",
                "/quit",
            ],
            ignore_case=True,
        )

        style = Style.from_dict(
            {
                "prompt": "cyan",
            }
        )

        while True:
            # , multiline=True
            user_input = prompt("You: ", completer=completer, style=style).strip().lower()

            if user_input in ["bye", "/exit", "/quit", "exit", "quit"]:
                bot_says("Later on!")
                print()
                break

            elif user_input == "/create":
                bot_says("Tell me what you are looking for")
                response = bot_asks()
                generated_code = generate_code(response)
                print(f"\n{generated_code}\n")
                save_code_to_file(generated_code)

            else:
                bot_says("I'm not sure what you mean")

    except KeyboardInterrupt:
        bot_says("Alright, see ya")


if __name__ == "__main__":
    main()
