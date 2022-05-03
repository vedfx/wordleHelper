import re
import requests


def regex_matches(s, list_of_patterns, grey_letters_regex):
    for p in list_of_patterns:
        if not re.findall(p, s):
            return False

    if re.match(grey_letters_regex, s):
        return False

    return True


def regex_matches_debug(s, list_of_patterns, grey_letters_regex):
    for p in list_of_patterns:
        if not re.findall(p, s):
            print(p, "|", s, "| False")
        else:
            print(p, "|", s, "| True")

    if re.match(grey_letters_regex, s):
        print(grey_letters_regex, "|", s, "| False")


def load_words(file):
    file = open(file, 'r')
    words = file.read().splitlines()
    return words


def letter_frequency():
    words = load_words('possible_words.txt')
    letters = {}

    for w in words:
        for l in w:
            if l not in letters:
                letters[l] = 1
            else:
                letters[l] = letters[l] + 1

    sorted_dict = {}
    sorted_keys = sorted(letters, key=letters.get)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = letters[w]

    for i in sorted_dict:
        print(i, ':', sorted_dict[i])


def word_search():
    all_letters = ""
    all_letters_regex_build = ""
    grey_letters = ""
    yellow_letter_invalid_patterns = []

    all_regex_patterns = []

    while True:
        pattern = re.compile("((\?)|([A-z])){5}")
        solution = input("Input Green Letters (e.g. a??B?): > ").lower()

        if re.fullmatch(pattern, solution):
            for l in solution:
                if not l == '?':
                    all_letters += l
                    all_letters_regex_build += "(?=.*" + l + ")"
            all_letters_regex = re.compile(all_letters_regex_build)
            green_letters_regex = re.compile(solution.replace('?', '.'))
            break
        else:
            print("\nInvalid input.\n")

    while True:
        pattern = re.compile("(([A-z])){1,5}$")
        yellow_letters_input = input("\nInput *ALL* Yellow Letters (any order, e.g. ecb): > ")

        if re.fullmatch(pattern, yellow_letters_input):
            for l in yellow_letters_input:
                all_letters += l
                all_letters_regex_build += "(?=.*" + l + ")"
            all_letters_regex_build += ".*"
            all_letters_regex = re.compile(all_letters_regex_build)
            break
        else:
            print("\nInvalid input.\n")

    # --------------------------
    # Enter letters to remove
    # --------------------------
    while True:
        pattern = re.compile("^[A-z]+")
        rem = input("\nInput Letters to Remove (any order, e.g. qwrthjnm) > ").lower()

        if re.fullmatch(pattern, rem):
            for c in rem:
                grey_letters += c + "|"

            grey_letters_regex = re.compile(grey_letters.rstrip(grey_letters[-1]))
            break
        else:
            print("\nInvalid input.\n")

    # -----------------------------------------
    # Enter positions for each yellow letter
    # -----------------------------------------
    for letter in yellow_letters_input:
        while True:
            l = letter.lower()
            u = letter.upper()

            example_string = l + "??" + l + "?"
            pattern = re.compile("^(" + l + "|" + u + "|\?){0,5}$")
            input_str = input(
                "\nInput Invalid Positions for Letter '" + letter + "' (e.g. " + example_string + "): > ").lower()

            if re.fullmatch(pattern, input_str):
                yellow_letter_invalid_patterns.append(
                    re.compile(
                        "^(?!" + input_str.replace('?', '.') + ").*"
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

    letter_frequency()


def menu():
    selection = int(0)

    print("----------------")
    print("1. Word Search")
    print("2. Letter Frequency")

    try:
        selection = int(input("\nSelect Function: "))
    except:
        print("Error")

    if selection == 1:
        word_search()
    elif selection == 2:
        letter_frequency()


if __name__ == '__main__':
    menu()