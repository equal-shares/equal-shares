# Handles security-related functions

import binascii
from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from src.config import config


def verify_valid_email(email: str) -> bool:
    if email.count("@") != 1:
        return False
    if email.count(".") == 0:
        return False

    username, domain = email.split("@")
    if not username or not domain:
        return False

    if domain.count(".") == 0:
        return False

    return True


def verify_valid_token(email: str, token: str) -> bool:
    if config.without_auth_mode:
        return True

    with open(config.api_rsa_private_key, "r") as private_key_file:
        private_key = RSA.importKey(private_key_file.read())
    decryptor = PKCS1_OAEP.new(private_key)

    print('-------------------')
    print(email, type(email))
    print('-------------------')
    print(token)
    print(len(token), type(token))
    print('-------------------')

    try:
        decrypted_data = b64decode(token)
    except binascii.Error as ex:
        print(ex)
        print('-------------------')
        return False

    while len(decrypted_data) % 128 != 0:
        decrypted_data += b'\x00'

    print(decrypted_data)
    print(len(decrypted_data), type(decrypted_data))
    print('-------------------')

    decrypted_data = decryptor.decrypt(decrypted_data)

    print(decrypted_data)
    print(len(decrypted_data), type(decrypted_data))
    print('-------------------')

    decrypted_email = decrypted_data.decode("utf-8")

    return email == decrypted_email


def create_token(email: str) -> str:
    with open(config.api_rsa_public_key, "r") as public_key_file:
        public_key = RSA.importKey(public_key_file.read())
    cipher = PKCS1_OAEP.new(public_key)

    email_encoded = email.encode("utf-8")
    token_data = cipher.encrypt(email_encoded)
    token = b64encode(token_data).decode("utf-8")

    return token
