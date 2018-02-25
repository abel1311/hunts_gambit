## Hunt's Gambit
Check the Pwnage status of your password against Troy Hunt's excellent 
[Pwned Passwords](https://haveibeenpwned.com/Passwords) repository of 500M+ dumped passwords

## Installation

```pip install huntsgambit```

## Usage
To check whether your password appears in any existing password dumps, run:

>```is_pwnified [your_password_in_plaintext]```

(If you don't want that last line to remain in your `.bash_history` file, run the command with the `-f` flag:

>```is_pwnified -f [your_pass_word_in_plaintext```
)

To pass in a list of passwords, use the `-i` input flag

> ```is_pwnified -i [txt_file_of_passes]```
 

**NOTE**: This module uses the PwnedPasswords' [k-Anonimity](https://en.wikipedia.org/wiki/K-anonimity) feature to preserve your privacy. This means that the script never sends your entire password (neither hashed nor in plaintext) out to the world. In fact, only the first five characters of your password's hashed value are used to query the [Pwned Password API](https://haveibeenpwned.com/API/v2#PwnedPasswords). All calculation is then conducted locally to determine whether your password has appeared in any pwned lists.
