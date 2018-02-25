from __future__ import print_function
from .utils import *
import argparse
import time
import os

__version__ = '0.3.5'


def main():
    """
    Has your pass been compromised? Let's find out!
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-f', '--forget_pass', action='store_true',
                        help="If this option is enabled, clear the last console line from .bash_history")
    parser.add_argument('-i', '--list-input', action='store_true',
                        help="Use this flag to read in list of plaintext password from a .txt file")

    parser.add_argument('password', help="Enter the password you want to check for pwnage")
    parser.add_argument('-h', '--help', action='help',
                        help="""This module queries Troy Hunt's excellent PwnedPasswords repository
                        to see if your password has ever been 1337 h4x0red before.
                        
                        HOW IT WORKS: Using the k-anonimity functionality of PwnedPasswords, hunts_gambit
                        sends the first five characters of your password's hash to PP and retrieves all possible
                        password hashes that begin with those characters. It then processes whether any of these is 
                        _your_ password, and tells you the result in a friendly output message.
                        
                        NOTE: Your full password (neither in plaintext nor hashed) is _never_ sent out to the interwebs.
                        All processing is done locally on your machine""")
    args = parser.parse_args()
    if args.list_input:
        parse_pwd_list(args.password)
    else:
        single_call(args.password)
    # clear last line of terminal output
    if args.forget_pass:
        os.system('let "line_num=$HISTCMD-1"; history -d $line_num')


def parse_pwd_list(input_pwd_list):
    # get plaintext passes
    with open(input_pwd_list, 'r') as infile:
        pass_list = [x.strip() for x in infile.readlines()]
    # process against PP
    pwd_df = pd.DataFrame(columns=['password', 'd0x3d'])
    for pwd in pass_list:
        time.sleep(1)  # api call restriction
        if not len(pwd):  # assertion avoision hack
            continue      # I say avoision
        gambit = Pwnification(pwd)
        if gambit.is_pass_compromised:
            pwd_list = gambit.pass_list
            freq = pwd_list[pwd_list.password == gambit.hashed_pass].frequency.iloc[0]
            pwd_df = pd.concat([pwd_df, pd.DataFrame([(pwd, "{} times".format(freq))],
                                                     columns=['password', 'd0x3d'])])
        else:
            pwd_df = pd.concat([pwd_df, pd.DataFrame([(pwd, "No")], columns=['password', 'd0x3d'])])
    # overwrite with new information
    open(input_pwd_list, 'w').close()  # clear existing file
    with open(input_pwd_list, 'w') as outfile:
        outfile.write(pwd_df.to_string(index=False))
        outfile.close()


def single_call(plaintext_pass):
    # process pass against PP
    gambit = Pwnification(plaintext_pass)
    if gambit.is_pass_compromised:
        pwd_list = gambit.pass_list
        freq = pwd_list[pwd_list.password == gambit.hashed_pass].frequency.iloc[0]
        print_stats(freq)
    else:
        print("Yeah you're fine... for now.")


if __name__ == '__main__':
    main()
