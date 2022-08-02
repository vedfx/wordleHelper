from engine import *
from func import load_words, print_words, word_search, prompt


def menu(new_line=False):
    words = load_words()

    d = {"aei":"bie", "cou":"doe", "e":"f", "u":"y"}

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
