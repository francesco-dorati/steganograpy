#!/usr/bin/python3

import sys
import os
import imghdr
import time
from getopt import getopt

from steganography import Steganography

ACCEPTED_FORMATS = ['jpeg', 'png']

def main():
    action = None
    img_path = None
    message = None
    password = None

    s = Steganography()

    # read args
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action not in ['encode', 'decode']:
            print_help()
            exit(1)

        opts, _ = getopt(sys.argv[2:], "i:f:m:o:p:")

        for opt in opts:
            if opt[0] == '-i':
                img_path = opt[1]
                if not is_valid_image(img_path):
                    exit()

            elif opt[0] == '-f':
                path = opt[1]
                if not is_valid_textfile(path):
                    exit()

                with open(path, 'r') as file:
                    message = file.read()

            elif opt[0] == '-m':
                message = opt[1]

            elif opt[0] == '-p':
                password = opt[1]
        
    print_title()

    if not action:
        action = choose_action()


    if action == 'encode':
        if not img_path:
            img_path = choose_image(ACCEPTED_FORMATS)

        if not message:
            message = choose_message()

        if not password:
            password = choose_password('Do tou want to encrypt the message?')

        print('\n\033[1;2mEncoding...\033[0m')

        outfile_name = s.encode(img_path, message, password)

        print('\033[1;32mImage successfully encoded!\033[0m')
        print(f'\nThe encoded image is: \033[1m{outfile_name}\033[0m\n')

    elif action == 'decode':
        if not img_path:
            img_path = choose_image(['png'])

        if not password:
            password = choose_password('Was the message encrypted?')

        print('\n\033[1;2mDecoding...\033[0m')

        decoded_message = s.decode(img_path, password)

        print('\033[1;32mImage successfully decoded!\033[0m')
        print(f'\n\033[1mThe message is:\033[0m')
        print(decoded_message, '\n')


def choose_action() -> str:
    print("""
\033[1mChoose action:\033[0m
    [1]\033[0;3m Encode\033[0m
    [2]\033[0;3m Decode\033[0m
    [0]\033[0;3m Exit\033[0m
""")
    
    a = None
    while a not in ['1', '2', '0']:
        a = input('> ')

    if a == '0':
        exit()

    return 'encode' if a == '1' else 'decode'

def choose_image(accepted_formats: list) -> str:
    while True:
        path = input('\n\033[1mInsert the path of the image: \033[0;2m(0 to exit)\033[0m ')

        if path == '0':
            exit()

        elif is_valid_image(path, accepted_formats):
            time.sleep(0.5)
            print('\033[0;32m✓ Valid image.\033[0m')
            time.sleep(0.5)
            break

    return path

def is_valid_image(image_path: str, accepted_formats: list) -> bool:
    if not os.path.isfile(image_path):
        print(f'\033[0;31mFile "{os.path.abspath(image_path)}" does not exist.\033[0m')
        return False

    elif imghdr.what(image_path) not in accepted_formats:
        print(f'\033[0;31mFile "{image_path}" has an invalid format.\033[0m')
        print(f'\033[0;31mAccepted formats:', ', '.join(accepted_formats), '\033[0m')
        return False

    return True

def choose_message() -> str:
    while True:
        print("""
\033[1mChoose message type:\033[0m
    [1]\033[0;3m Text\033[0m
    [2]\033[0;3m Textfile\033[0m
    [0]\033[0;3m Exit\033[0m
""")
        m = None
        while m not in ['1', '2', '0']:
            m = input('> ')

        if m == '0':
            exit()

        elif m == '1':
            text = input('\n\033[1mInsert the message: \033[0;2m(0 to exit)\033[0m ')
            if text == '0':
                exit()
            
            return text

        elif m == '2':
            while True:
                path = input('\n\033[1mInsert the path of the textfile: \033[0;2m(0 to exit)\033[0m ')

                if path == '0':
                    exit()

                elif is_valid_textfile(path):
                    time.sleep(0.5)
                    print('\033[0;32m✓ Valid textfile.\033[0m')
                    time.sleep(0.5)
                    break

            with open(path, 'r') as file:
                return file.read()

def is_valid_textfile(textfile_path: str) -> bool:
    if not os.path.isfile(textfile_path):
        print(f'\033[0;31mFile "{os.path.abspath(textfile_path)}" does not exist.\033[0m')
        return False

    elif not textfile_path.endswith('.txt'):
        print(f'\033[0;31mFile "{textfile_path}" is not a .txt file.\033[0m')
        return False

    return True

def choose_password(message: str) -> str:
    while True:
        print(f"""
\033[1m{message}\033[0m
    [1]\033[0;3m Yes\033[0m
    [2]\033[0;3m No\033[0m
    [0]\033[0;3m Exit\033[0m
""")
        p = None
        while p not in ['1', '2', '0']:
            p = input('> ')

        if p == '0':
            exit()

        elif p == '1':
            password = input('\n\033[1mInsert the password: \033[0;2m(0 to exit)\033[0m ')
            if password == '0':
                exit()
            
            return password

        elif p == '2':
            return None


def print_help():
    print("""
Steganography

    Usage:
        steganograpy [encode [-i image] [-f textfile | -m message] [-p password]]
        steganograpy [decode [-i image] [-p password]]
    """)

def print_title():
    print("""\033[0;35m
    .▄▄ · ▄▄▄▄▄▄▄▄ . ▄▄ •  ▄▄▄·  ▐ ▄        ▄▄ • ▄▄▄   ▄▄▄·  ▄▄▄· ▄ .▄ ▄· ▄▌
    ▐█ ▀. •██  ▀▄.▀·▐█ ▀ ▪▐█ ▀█ •█▌▐█ ▄█▀▄ ▐█ ▀ ▪▀▄ █·▐█ ▀█ ▐█ ▄███▪▐█▐█▪██▌
    ▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▄█ ▀█▄▄█▀▀█ ▐█▐▐▌▐█▌.▐▌▄█ ▀█▄▐▀▀▄ ▄█▀▀█  ██▀·██▀▀█▐█▌▐█▪
    ▐█▄▪▐█ ▐█▌·▐█▄▄▌▐█▄▪▐█▐█▪ ▐▌██▐█▌▐█▌.▐▌▐█▄▪▐█▐█•█▌▐█▪ ▐▌▐█▪·•██▌▐▀ ▐█▀·.
    ▀▀▀▀  ▀▀▀  ▀▀▀ ·▀▀▀▀  ▀  ▀ ▀▀ █▪ ▀█▄▀▪·▀▀▀▀ .▀  ▀ ▀  ▀ .▀   ▀▀▀ ·  ▀ • \033[0m
                            
                            by \033[1mFrancesco Dorati\033[0m
                        \033[2mgithub.com: \033[1mfrancesco-dorati\033[0m
    """)


if __name__ == '__main__':
    main()
