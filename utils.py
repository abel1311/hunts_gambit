from __future__ import print_function
import pandas as pd
import requests
import hashlib


class Pwnification(object):

    def __init__(self, plaintext_pass):
        """
        Checks whether your password has been compromised. using Troy Hunt's
        excellent Pwned Passwords repository

        :param plaintext_pass: plaintext entry of the password you want to check pwnage for
        """
        self.pwd = plaintext_pass
        assert len(self.pwd), "Password can't be an empty string. Try again, m9"
        self.hashed_pass = self.hash_pass().upper()
        self.pass_list = self.get_k_anon
        self.is_pass_compromised = self.verify_pwnage(self.pass_list.password)

    def hash_pass(self, hash_algo='sha1'):
        pwd_hash = hashlib.__getattribute__(hash_algo)(self.pwd.encode('utf-8'))
        return pwd_hash.hexdigest()

    @property
    def get_k_anon(self):
        k_anon_endpoint = 'https://api.pwnedpasswords.com/range/'
        pwd_list = requests.get(k_anon_endpoint + self.hashed_pass[:5]).text
        pwd_list = pwd_list.replace('\ufeff', '').upper().split('\r\n')
        pwd_list = [self.hashed_pass[:5] + pwd for pwd in pwd_list]
        pwd_list = [pwd.split(':') for pwd in pwd_list]
        pwd_list = pd.DataFrame(pwd_list, columns=['password', 'frequency'])
        return pwd_list

    def verify_pwnage(self, pwd_list):
        for pwd in pwd_list:
            if pwd == self.hashed_pass:
                return True
        return False


def make_strs(char, incidence, n_freq):
    return char*incidence + char*int(n_freq/2)


def print_stats(freq):
    in_freq = str(freq)
    n_freq = len(in_freq)
    extra_space = ''
    if len(in_freq) % 2:
        n_freq += 1
        extra_space = ' '
    dash_str = make_strs('-', 27, n_freq)
    space_str = make_strs(' ', 31, n_freq)
    print("Your pass has been D0X3D!")
    print("\n")
    print("# " + dash_str + ' STATS ' + dash_str + ' #')
    print("|" + space_str * 2 + " |")
    print("|  Your password appears in the PwnedPasswords database {0} times{1}  |".format(in_freq, extra_space))
    print("|" + space_str * 2 + " |")
    print("# " + dash_str + '-- x --' + dash_str + ' #')
    print("\n")
    print("Get out quick.. Get back in quicker, with an armful of new passes under your arm!")