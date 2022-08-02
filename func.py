# General-purpose functions not related to string manipulation


import re
import requests
from engine import regex_matches, letter_frequency
from main import menu


def print_dict(d):
    for key in d:
        print(key, d[key])


def load_words(file="possible_words.txt"):
    file = open(file, 'r')
    words = file.read().splitlines()
    file.close()
    return words


def print_words(file="possible_words.txt"):
    print("")
    file = open(file, 'r')
    words = file.read().splitlines()
    file.close()

    for w in words:
        print(w)


def word_search():
    all_letters = ""
    all_letters_regex_build = ""
    grey_letters = ""

    yellow_letter_invalid_patterns = []
    all_regex_patterns = []

    # --------------------------
    # Input Green Letters
    # --------------------------
    while True:
        pattern = re.compile("((\?)|([A-z])){5}")
        solution = input("Input Green Letters (e.g. a??B?): > ").lower()

        if re.fullmatch(pattern, solution) or solution == "":
            for l in solution:
                if not l == '?':
                    all_letters += l
                    all_letters_regex_build += "(?=.*" + l + ")"
            re.compile(all_letters_regex_build)
            green_letters_regex = re.compile(solution.replace('?', '.'))
            break
        else:
            print("\nInvalid input.\n")

    # --------------------------
    # Input Yellow Letters
    # --------------------------
    while True:
        pattern = re.compile("(([A-z])){1,5}$")
        yellow_letters_input = input("\nInput *ALL* Yellow Letters (any order, e.g. ecb): > ")

        if len(all_letters) + len(yellow_letters_input) < 2:
            print("ERROR: WordFinderAPI requires at least 2 of any combination of green and/or yellow letters.")
            menu(True)
        if re.fullmatch(pattern, yellow_letters_input) or yellow_letters_input == "":
            for l in yellow_letters_input:
                all_letters += l
                all_letters_regex_build += "(?=.*" + l + ")"
            all_letters_regex_build += ".*"
            all_letters_regex = re.compile(all_letters_regex_build)
            break
        else:
            print("\nInvalid input.\n")

    # --------------------------
    # Input Letters to Remove
    # --------------------------
    while True:
        pattern = re.compile("^[A-z]+")
        rem = input("\nInput Letters to Remove (any order, e.g. qwrthjnm) > ").lower()

        if re.fullmatch(pattern, rem) or rem == "":
            for c in rem:
                grey_letters += c + "|"

            grey_letters_regex = re.compile(grey_letters.rstrip(grey_letters[-1]))
            break
        else:
            print("\nInvalid input.\n")

    # -----------------------------------------
    # Input Positions (Yellow)
    # -----------------------------------------
    for letter in yellow_letters_input:
        while True:
            l = letter.lower()
            u = letter.upper()

            example_string = l + "??" + l + "?"
            pattern = re.compile("^(" + l + "|" + u + "|\?){0,5}$")
            str = input(
                "\nInput Invalid Positions for Letter '" + letter + "' (e.g. " + example_string + "): > ").lower()

            # ^(?!s....).*
            if re.fullmatch(pattern, str):
                yellow_letter_invalid_patterns.append(
                    re.compile(
                        "^(?!" + str.replace('?', '.') + ").*"
                    )
                )

                break
            else:
                print("\nInvalid input.\n")

    all_regex_patterns.append(green_letters_regex)
    all_regex_patterns.append(all_letters_regex)

    for i in yellow_letter_invalid_patterns:
        all_regex_patterns.append(i)

    for i in range(len(all_letters), 5):
        all_letters += "%3F"

    response = requests.get(
        "https://fly.wordfinderapi.com/api/search?letters=" + all_letters + "&length=5&page_size=99999&dictionary=wwf2")

    data = response.json()

    temp = []
    possible_words = []

    for w in data['word_pages'][0]['word_list']:
        if regex_matches(w['word'], all_regex_patterns, grey_letters_regex):
            temp.append(w['word'])

    for w in temp:
        if not re.findall(grey_letters_regex, w):
            possible_words.append(w)

    f = open("possible_words.txt", "w")
    for w in possible_words:
        f.write(w + '\n')
    f.close()

    print("\nFound", len(possible_words), "possible words.\n")

    letter_frequency(False)
    menu(True)

# I got tired of having to write a loop to validate user input every time I needed to take it, so I made a function
# to make it simpler and cleaner. By default, the prompt will only accept Y or N in either upper or lower case as
# valid choices, but you can also specify a custom regex pattern to match against.
def prompt(prompt_text, valid_input_pattern="Y|y|N|n"):
    while True:
        user_input = input("\n" + prompt_text).lower()

        if re.fullmatch(re.compile(valid_input_pattern), user_input):
            break
        else:
            print("\nInvalid input.\n")

    return user_input

