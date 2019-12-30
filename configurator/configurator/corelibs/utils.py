import random
import string
from getpass import getpass

from colorama import Fore


def get_input(blank=False, is_pass=False, confirmation=False, msg=''):
    value = None
    if confirmation:
        value = input(f'{Fore.GREEN + msg}[y/N]: {Fore.RESET}')
        if (value == 'y' or value == 'Y') or value.strip() == '':
            return True
        elif value == 'N':
            return False
        else:
            raise Exception('Invalid input')
    else:
        while value is None:
            if not is_pass:
                value = input(f'{Fore.GREEN}{msg}{Fore.RESET}')
                pass
            else:
                value = getpass(f'{Fore.GREEN}{msg}')
                confirmation = getpass(f'{Fore.GREEN}Confirm password: ')
                if value != confirmation:
                    print(f'{Fore.RED}Passwords don\'t match{Fore.RESET}')
                    value = None
                    continue
            if not value and not blank:
                print(f'{Fore.RED}Input can\'t be blank{Fore.RESET}')
                value = None
    return value


def code_generator(size=50, char=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(char) for _ in range(size))
