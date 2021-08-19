import sys
import os
import imghdr
import time

from getopt import getopt

from steganography import Steganography

ACCEPTED_FORMATS = ['jpeg', 'png']

s = Steganography()

def main():
    action = None
    img_path = None
    message = None
    password = None

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action in ['encode', 'decode']:
            opts, _ = getopt(sys.argv[2:], "i:f:m:p:b:e:")

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

                elif opt[0] == '-b':
                    bits = opt[1]
                    if bits.isnumeric() and int(bits) <= 8:
                        s.BITS = int(bits)
                    else:
                        print('\033[0;31mInvalid bits number.\033[0m')
                        exit()

                elif opt[0] == '-e':
                    padding = opt[1]
                    if padding.isnumeric():
                        s.EOF_LENGTH = int(padding)
                    else:
                        print('\033[0;31mInvalid padding length.\033[0m')
                        exit()

        else:
            action = None
            opts, _ = getopt(sys.argv[1:], "b:e:")
            for opt in opts:
                if opt[0] == '-b':
                    bits = opt[1]
                    if bits.isnumeric() and int(bits) <= 8:
                        s.BITS = int(bits)
                    else:
                        print('\033[0;31mInvalid bits number.\033[0m')
                        exit()
                        
                elif opt[0] == '-e':
                    padding = opt[1]
                    if padding.isnumeric():
                        s.EOF_LENGTH = int(padding)
                    else:
                        print('\033[0;31mInvalid padding length.\033[0m')
                        exit()

            if not bits and not padding:
                print_help()
                exit()
            
        
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
    """Asks the action (encode, decode) to the user.

    Returns:
        action (str): the action chosen by the user.
    """
    while True:
        print("""
\033[1mChoose action:\033[0m
    [1]\033[0;3m Encode\033[0m
    [2]\033[0;3m Decode\033[0m
    [3]\033[0;3m Settings\033[0m
    [0]\033[0;3m Exit\033[0m
    """)
        
        a = None
        while a not in ['1', '2', '3', '0']:
            a = input('> ')

        if a == '0':
            exit()
        elif a == '1':
            return 'encode'
        elif a == '2':
            return 'decode'
        elif a == '3':
            settings()


def settings():
    """Displays settings."""
    while True:
        print("""
\033[1mSettings:\033[0m
    [1]\033[0;3m Change number of bits\033[0m
    [2]\033[0;3m Change padding size\033[0m
    [0]\033[0;3m Exit\033[0m
            """)

        s = None
        while s not in ['1', '2', '0']:
            s = input('> ')

        if s == '0':
            exit()
        elif s == '1':
            choose_bits()
            break
        elif s == '2':
            choose_padding()
            break

def choose_bits():
    """Asks the user for the number of bits reserved to the hidden message and changes it."""
    while True:
        n = input("\n\033[1mNumber of bits reserved to the hidden message: \033[0;2m(default is 2; maximum 8; 0 to exit)\033[0m ")

        if n == '0':
            exit()
        elif n.isnumeric() and int(n) <= 8:
            s.BITS = int(n)
            print('\033[0;32mNumber of bits reserved to the hidden message updated successfully!\033[0m')
            break

def choose_padding():
    """Asks the user for the length of padding and changes it."""
    while True:
        n = input("\n\033[1mNumber zeros in message padding: \033[0;2m(default is 16; 0 to exit)\033[0m ")

        if n == '0':
            exit()
        elif n.isnumeric():
            s.EOF_LENGTH = int(n)
            print('\033[0;32mNumber zeros in message padding updated successfully!\033[0m')
            break

def choose_image(accepted_formats: list) -> str:
    """Asks the image path to the user.

    Args:
        accepted_formats (list): a list with accepted image formats.

    Returns:
        img_path (str): the path of the chosen image.
    """
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
    """Checks if the user given image path is valid.

    Args:
        image_path (str): the path of the user given image.
        accepted_formats (list): a list with accepted image formats.

    Returns:
        is_valid (bool): if the image is valid.
    """
    if not os.path.isfile(image_path):
        print(f'\033[0;31mFile "{os.path.abspath(image_path)}" does not exist.\033[0m')
        return False

    elif imghdr.what(image_path) not in accepted_formats:
        print(f'\033[0;31mFile "{image_path}" has an invalid format.\033[0m')
        print(f'\033[0;31mAccepted formats:', ', '.join(accepted_formats), '\033[0m')
        return False

    return True

def choose_message() -> str:
    """Asks the message to the user.

    Returns:
        message (str): the message given by the user.
    """
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
    """Chack if the user given textfile path is valid.

    Args:
        textfile_path (str): the path of the textfile.

    Returns:
        is_valid (bool): if the textfile path is valid.
    """
    if not os.path.isfile(textfile_path):
        print(f'\033[0;31mFile "{os.path.abspath(textfile_path)}" does not exist.\033[0m')
        return False

    elif not textfile_path.endswith('.txt'):
        print(f'\033[0;31mFile "{textfile_path}" is not a .txt file.\033[0m')
        return False

    return True

def choose_password(message: str) -> str:
    """Asks the user for the encryption password.

    Args:
        message (str): the question asked by the function.

    Returns:
        password (str | None): the password given by the user.
    """
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
    """Prints the help message."""
    print(f"""
Steganography

    Usage:
        {sys.argv[0]} [encode [-i image] [-f textfile | -m message] [-p password]] [-b bits] [-e padding]
        {sys.argv[0]} [decode [-i image] [-p password]] [-b bits] [-e padding]

    Args:
        -i image        Image path to be encoded/decoded.
        -f textfile     Textfile (.txt) to be hidden.
        -m message      The mesage to be hidden.
        -p password     The password to encrypt/decrypt the hidden message.
        -b bits         The number of image pixel bits reserved for the hidden message.
        -e padding      The end-of-message padding (number of zeroes).
    """)

def print_title():
    """Prints the title."""
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
