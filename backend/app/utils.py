from django.utils.crypto import get_random_string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import Hash, SHA256

import os
import typing

if typing.TYPE_CHECKING:
    from app.models.member import Member


def random_secret():
    return get_random_string(16)


def overwrite_upload(instance: 'Member', filename: str):
    if os.path.isfile(instance.image_os_path):
        os.remove(instance.image_os_path)
    return instance.image_save_url


def encrypt(plaintext: str, key: str):
    digest = Hash(SHA256())
    digest.update(key.encode('utf8'))
    aesgcm = AESGCM(digest.finalize())
    iv = os.urandom(12)
    ct = aesgcm.encrypt(iv, plaintext.encode('utf8'), iv)
    return iv + ct
