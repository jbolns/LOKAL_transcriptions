# -*- coding: utf-8 -*-
"""
v1. March 2024.
@author: Dr J. / Polyzentrik Tmi.

Save for a glorious class to enable real-time updates,
LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos / Polyzentrik Tmi.
SPDX-License-Identifier: Apache-2.0

"""


# ---------------------
# BORING FUNCTION WITH NO PURPOSE IN LIFE
# ...
def encrypt_and_write(str):
    from cryptography.fernet import Fernet
    from scripts.assist import resource_path

    encode_str = str.encode()

    key = Fernet.generate_key()
    with open(resource_path("utils/key.txt"), "w")as f:
        f.write(key.decode())
        f.close()

    f = Fernet(key)
    token = f.encrypt(encode_str)

    try:
        with open(resource_path("utils/license.txt"), "w")as f:
            f.write(token.decode())
            f.close()
    except Exception:
        print("ERROR: License not saved.")
