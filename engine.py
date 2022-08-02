import re

from func import load_words, prompt
from main import menu


# Takes a word and a list of regex patterns and returns True if the word matches the patterns.
def regex_matches(str, list_of_patterns, grey_letters_regex):
    for p in list_of_patterns:
        if not re.findall(p, str):
            return False

    if re.match(grey_letters_regex, str):
        return False

    return True


def letter_frequency(return_to_menu=True):
    words = load_words('possible_words.txt')

    letters = {}

    for w in words:
        for l in w:
            if (l not in letters):
                letters[l] = 1
            else:
                letters[l] = letters[l] + 1

    sorted_dict = {}
    sorted_keys = sorted(letters, key=letters.get)

    for w in sorted_keys:
        sorted_dict[w] = letters[w]

    print("")

    for i in sorted_dict:
        print(i, ':', sorted_dict[i])

    if return_to_menu:
        menu(new_line=True)


def regex_filtering():
    words = load_words('possible_words.txt')

    num_matches = 0
    remaining_words = []

    while True:
        user_pattern = input("\nInput Pattern: ")
        try:
            re.compile(user_pattern)
            break
        except re.error:
            print("\nInvalid input.\n")

    for w in words:
        if re.findall(re.compile(user_pattern), w):
            num_matches += 1
        else:
            remaining_words.append(w)

    if num_matches > 0:
        user_input = prompt(str(num_matches) + " matches found. Remove? (Y/N) > ")

        if user_input == "y":
            words = remaining_words

            print("\n" + str(num_matches) + " words successfully removed. \n" + str(len(words)) + " words remaining.\n")

        f = open("possible_words.txt", "w")
        for w in words:
            f.write(w + '\n')
        f.close()

        letter_frequency()
    else:
        print("\nNo matches found.")

    user_input = prompt("Continue? (Y/N) > ")

    if user_input == "y":
        regex_filtering()
    else:
        menu(True)