#!/usr/bin/env python3

import sys
import os
import datetime
import argparse

# Establishing default values for date, special characters
special_characters = ['.', '-', '_', '*', '!', '@', '#', '%', '"', '&']

# This gets results like Alice!!! or Alice79!!!
add_variations_on_characters = []
for i in range(1, 3):
    for char in special_characters:
        add_variations_on_characters.append(char * i)        
special_characters = add_variations_on_characters

# Global arrays
wordlist_responses = []
special_responses = []
leetspeek_responses = []
date_list = []
date_range = []
default_word_list = []

# Calculates how many years back we try to enumerate 0, 1 --> 1 year, 0, 4 --> 4 years
for i in range(0, 4):    
    date_list.append(datetime.datetime.now().year - 2000 - i)
    date_list.append(datetime.datetime.now().year - i)

# Calculating values for age, will be used like this: MinAge of target/ MaxAge of target
for i in range(18, 55):    
    date_range.append(datetime.datetime.now().year + i - 2000)

def print_message(message, color=None):
    # Function for printing messages with color support
    if color == "red":
        print(f"\033[31m{message}\033[0m")
    elif color == "green":
        print(f"\033[32m{message}\033[0m")
    elif color == "blue":
        print(f"\033[34m{message}\033[0m")
    else:
        print(message)

def usage():
    print_message("Usage:", "blue")
    print_message("---------------------------------------------------------------------", "blue")
    print_message("PasswordGenerator.py -w               <wordlist>", "blue")
    print_message("PasswordGenerator.py -l               <lower case flag>", "blue")
    print_message("PasswordGenerator.py -s               <special character flag>", "blue")
    print_message("PasswordGenerator.py --leetspeak      <leetspeak transformation flag>", "blue")
    print_message("---------------------------------------------------------------------", "blue")
    sys.exit()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wordlist", help="Wordlist path")
    parser.add_argument("-l", "--lower", help="Allow lowercase transformations", action="store_true")   
    parser.add_argument("-s", "--special", help="Allow special character transformations", action="store_true")

    parser.add_argument("--leetspeak", help="Allow leetspeak character transformations", action="store_true")

    return parser.parse_args()

def transform(input, dates):    
    storage = []

    for date in dates:
        for variation in input:
            storage.append(f"{variation}{date}")

    return storage

def transform_with_special_character(input, dates):    
    storage = []

    for char in special_characters:
        for variation in input:
            storage.append(f"{variation}{char}")
            for date in dates:                
                storage.append(f"{variation}{date}{char}")
                storage.append(f"{variation}{char}{date}")

    return storage

def transform_with_leetspeek(input):    
    leetspeek_storage = []
    for word in input:
        leetspeek_word = ''
        for char in word:
            if char == 'a' or char == 'A':
                leetspeek_word += '4'
            elif char == 'e' or char == 'E':
                leetspeek_word += '3'
            elif char == 'i' or char == 'I':
                leetspeek_word += '1'
            elif char == 'o' or char == 'O':
                leetspeek_word += '0'
            elif char == 's' or char == 'S':
                leetspeek_word += '5'
            else:
                leetspeek_word += char

        leetspeek_storage.append(leetspeek_word)

    return leetspeek_storage

def handle_space(name):
    string_variations = []

    if " " in name:
        first_name, last_name = name.split()
        string_variations.append(f"{first_name}{last_name}")
        string_variations.append(f"{first_name}.{last_name}")
        string_variations.append(f"{last_name}{first_name}")
        string_variations.append(f"{last_name}.{first_name}")
        string_variations.append(f"{first_name[:1]}.{last_name}")
        string_variations.append(f"{last_name[:1]}.{first_name}")
        string_variations.append(f"{first_name}.{last_name[:1]}")
        string_variations.append(f"{last_name}.{first_name[:1]}")
        string_variations.append(f"{first_name[:1]}{last_name[:1]}")

        # Incase name like Bob Bilder
        if last_name[:1] != first_name[:1]:
            string_variations.append(f"{last_name[:1]}{first_name[:1]}")

    else:
        string_variations.append(name)

    if args.lower == True:
        lowerspace_included = []
        for variation in string_variations:
            lowerspace_included.append(variation)
            lowerspace_included.append(variation.lower())

        return lowerspace_included
    else:
        return string_variations

# Passwords like this will be made: Password2022 / Password22
def create_permutations_with_date(string_variations):
    permutation_results = (transform(string_variations, date_list))
    for permutation in permutation_results:
        wordlist_responses.append(permutation)

# Passwords like this will be made: Password77
def create_permutations_in_date_daterange(string_variations):
    permutation_results = (transform(string_variations, date_range))
    for permutation in permutation_results:
        wordlist_responses.append(permutation)

# Passwords like this will be made: Password22! / Password$2022
def create_permutations_special_with_date(string_variations):
    permutation_results = (transform_with_special_character(string_variations, date_list))
    for permutation in permutation_results:
        special_responses.append(permutation)

# Passwords like this will be made: Password77@
def create_permutations_special_in_daterange(string_variations):
    permutation_results = (transform_with_special_character(string_variations, date_range))
    for permutation in permutation_results:
        special_responses.append(permutation)

# Passwords like this will be made: P455w0rd77@
def create_permutations_with_leetspeak():
    permutation_results = (transform_with_leetspeek(wordlist_responses))
    for permutation in permutation_results:
        leetspeek_responses.append(permutation)

    permutation_results = (transform_with_leetspeek(special_responses))
    for permutation in permutation_results:
        leetspeek_responses.append(permutation)

# This function makes sure that simple passwords go in the list first
def handle_password_list(filename):
    password = []
    try:
        with open(filename) as file:
            for line in file:
                password.append(line.strip())
    except FileNotFoundError:
        print_message("File not found", "red")
        usage()

    for line in password:
        create_permutations_with_date(handle_space(line))        
    for line in password:
        create_permutations_in_date_daterange(handle_space(line))

    if args.special == True:
        for line in password:
            create_permutations_special_with_date(handle_space(line))
        for line in password:
            create_permutations_special_in_daterange(handle_space(line))
        
    if args.leetspeak == True:
        # LeetSpeak permutations do not require input since we already have list from before
        create_permutations_with_leetspeak()

if __name__ == "__main__":
    args = parse_args()

    if args.wordlist:
        print_message("Creating permutations...", "green")
        handle_password_list(args.wordlist)

    if not any(vars(args).values()):
        print_message("Error: No arguments provided.", "red")
        usage()

try:
    responses = wordlist_responses + special_responses + leetspeek_responses
    existing_file_line_count = 0
    file_name = "passwordlist.txt"
    file_mode = 'x' if not os.path.exists(file_name) else 'w'

    try:
        if file_mode == 'w':
            with open(file_name, 'r') as fp:
                for count, line in enumerate(fp):
                    pass
                existing_file_line_count = (count + 1)
    except Exception as e:
        existing_file_line_count = 0
        print_message("File existed but was empty or other error occured attempting to rewrite.", "red")

    with open(file_name, file_mode) as f:
        for response in responses:
            f.write(response.strip() + '\n')

    with open(file_name, 'r') as fp:
        for count, line in enumerate(fp):
            pass
        print_message(f"Created password list. Total line count: {count + 1} lines", "blue")
        print_message(f"Previous file had: {existing_file_line_count} lines", "blue")

    if file_mode == 'w':
        print_message("File already existed, used 'w' mode to rewrite existing file.", "red")

    print_message("List creation finished", "green")

except Exception as e:
    print_message(f"List creation failed {e}", "red")
    usage()

