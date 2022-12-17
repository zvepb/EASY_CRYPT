# -*- codng: utf8 -*-
#! /usr/bin/python
import os
import sys
import psutil
import hashlib
from colorama import init, Fore, Style

from cryptography.fernet import Fernet


# AES 128 CBC

intro = ['',
	'████▀░░░░░░░░░░░░░░░░░▀████',
	'███│░░░░░░░░░░░░░░░░░░░│███',
	'██▌│░░░░░░░░░░░░░░░░░░░│▐██',
	'██░└┐░░░░░░░░░░░░░░░░░┌┘░██',
	'██░░└┐░░░░░░░░░░░░░░░┌┘░░██',
	'██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██',
	'██▌░│██████▌░░░▐██████│░▐██',
	'███░│▐███▀▀░░▄░░▀▀███▌│░███',
	'██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██',
	'██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██',
	'████▄─┘██▌░░░░░░░▐██└─▄████',
	'█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████',
	'████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████',
	'█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████',
        '',
        ' 💀   USB crypt v 1.0   💀',
        '',
        ]

def print_intro():
    for x in intro:
        print(Fore.RED, x)

def write_key():
    key = Fernet.generate_key()
    with open('usbcrypt.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    # путь до директории и ключа на USB
    return open(r'/media/deavyjones/zv/usbcrypt.key', 'rb').read()

def encrypt_file(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    print('file {} was encrypt'.format(filename))
    with open(filename, 'wb') as file:
        file.write(encrypted_data)

def encrypt_directory(crypt_dir):
    try:
        for file in os.listdir(crypt_dir):
            if os.path.isdir(crypt_dir + '/' + file):
                encrypt_directory(crypt_dir + '/' + file)
            if os.path.isfile(crypt_dir + '/' + file):
                try:
                    encrypt_file(crypt_dir + '/' + file)
                except:
                    pass
    except Exception as e:
        print(e)

def decrypt_file(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    print('file {} was decrypt'.format(filename))
    with open(filename, 'wb') as file:
        file.write(decrypted_data)

def decrypt_directory(decrypt_dir):
    try:
        for file in os.listdir(decrypt_dir):
            if os.path.isdir(decrypt_dir + '/' + file):
                decrypt_directory(decrypt_dir + '/' + file)
            if os.path.isfile(decrypt_dir + '/' + file):
                try:
                    decrypt_file(decrypt_dir + '/' + file)
                except:
                    pass
    except Exception as e:
        print(e)

def pantera():
    while True:
        try:
            cord = input('💀 crypt/decrypt/genkey $ ')
            if cord == 'crypt':
                crypt_dir = input('💀 crypt directory $ ')
                try:
                    encrypt_directory(crypt_dir)
                except Exception as e:
                    print(e)
            elif cord == 'decrypt':
                decrypt_dir = input('💀 decrypt directory $ ')
                try:
                    decrypt_directory(decrypt_dir)
                except Exception as e:
                    print(e)
            elif cord == 'genkey':
                write_key()
            else:
                print('')
                print('Wrong command ...')
        except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    print_intro()
    pantera()


