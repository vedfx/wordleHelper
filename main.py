import re
import requests


def regex_matches(str, list_of_patterns, grey_letters_regex):
    for p in list_of_patterns:
        if not re.findall(p, str):
            return False

    if re.match(grey_letters_regex, str):
        return False

    return True


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
    sorted_keys = sorted(letters, key=letters.get)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = letters[w]

    print("")

    for i in sorted_dict:
        print(i, ':', sorted_dict[i])

    if return_to_menu:
        menu(new_line=True)


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
        "https://fly.wordfinderapi.com/api/search?letters=" + all_letters + "&length=5&page_size=99999999&dictionary=wwf2")

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


def prompt(prompt_text, valid_input_pattern="Y|y|N|n"):
    while True:
        user_input = input("\n" + prompt_text).lower()

        if re.fullmatch(re.compile(valid_input_pattern), user_input):
            break
        else:
            print("\nInvalid input.\n")

    return user_input


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


def menu(new_line=False):
    words = load_words()

    if new_line:
        print("")
    print("----------------")
    print("1. Word Search")
    print("2. RegEx Filtering")
    print("3. Letter Frequency")
    print("4. List of Possible Words (" + str(len(words)) + ")")
    selection = int(prompt("Select Function: ", "\d{1}"))

    if selection == 1:
        word_search()
        menu(True)
    elif selection == 2:
        regex_filtering()
        menu(True)
    elif selection == 3:
        letter_frequency()
    elif selection == 4:
        print_words()
        menu(True)


if __name__ == "__main__":
    menu()
