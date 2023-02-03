# PasswordGenerator
PasswordGenerator is a simple command-line tool that generates password variations based on the inputted wordlist, flags and characters.

# Requirements
Python 3.x

# Usage
	PasswordGenerator.py -w <wordlist>
	PasswordGenerator.py -l <lower case flag>
	PasswordGenerator.py -s <special character flag>
	PasswordGenerator.py --leetspeak <leetspeak transformation flag>

# Options
	-w, --wordlist: Specify the path of the wordlist file.
	-l, --lower: Allow lowercase transformations.
	-s, --special: Allow special character transformations.
	--leetspeak: Allow leetspeak character transformations.

# Example
To generate password variations from a wordlist file wordlist.txt with lowercase transformations, special character transformations and leetspeak transformations, run the following command:

	PasswordGenerator.py -w wordlist.txt -l -s --leetspeak

# Built With
Python - The programming language used

# License
This project is licensed under the MIT License.