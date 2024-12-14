"""
v1. Jan 2024.
@author: Dr J. / Polyzentrik Tmi.

LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos / Polyzentrik Tmi.
SPDX-License-Identifier: Apache-2.0

"""

# ---------------------
# IMPORTS SHARED BY SEVERAL FUNCTIONS
# ...

import os


# ---------------------
# LICENSE CHECKs
# ...
def check_license():
    import config
    from scripts.utils import decode_license

    if config.license_status == "no license" or not decode_license(
        config.license_status
    ):
        status = 0
        message = "ENABLE PRETTY MODE"
    else:
        status = 2
        message = "YOU ARE AWESOME"
    return status, message


def log_free_run():
    import config
    from scripts.assist import resource_path

    if config.license_status == "free trial":
        tries = len(open(resource_path("utils/try.txt"), "r").read()) + 1
        if tries <= 5:
            with open(resource_path("utils/try.txt"), "w") as f:
                f.write("." * tries)
                f.close()
        else:
            config.license_status = "due"


def calc_audio_length(path_to_audio):
    """Determines lenght of any audio"""
    from pydub import AudioSegment

    audio = AudioSegment.from_file(path_to_audio)
    return audio.duration_seconds


def calc_total_chunks(path, mode):
    """Updates number of 30s segments in any given audio"""

    # Function imports
    import math
    from scripts.assist import resource_path

    # Count number of chunks
    chunks = 0
    if mode == "simple":
        chunks = math.ceil(calc_audio_length(path) / 30)
    else:
        list = [f for f in os.listdir(path) if f.endswith("wav")]
        for file in list:
            chunks = chunks + math.ceil(calc_audio_length(f"{path}/{file}") / 30)

    # Write chunk count to utils file
    with open(resource_path("utils/chunks.txt"), "w") as f:
        f.write(f"0,{str(chunks)}")
        f.close()


def create_temp_folder():
    """Creates folder to hold temp files needed for looped transcriptions"""
    path_to_user = os.path.expanduser("~")
    path_to_temp_folder = path_to_user + "/LOKAL_temp"
    if not os.path.isdir(path_to_temp_folder):
        os.makedirs(path_to_temp_folder)

    return path_to_temp_folder


# ---------------------
# AUDIO CONVERSION
# Needed if main audio is not in .wav format
# ...
def convert_to_wav(filepath, filename):

    # Function imports
    from pydub import AudioSegment

    try:
        source_folder = filepath.rpartition("/")[0]
        new_filepath = (
            source_folder + "/" + filename + "-wavcopyforLOKALtranscription" + ".wav"
        )

        # Import file
        audio = AudioSegment.from_file(filepath)

        # Export file
        audio.export(new_filepath, format="wav")

        return 1
    except Exception:
        return 0


def more_magic():
    return 2


def delete_converted_wav(filepath):
    if filepath.endswith("wav"):
        try:
            os.remove(filepath)
            return "Succesfully deleted the temporary .wav version of audio.\n"
        except Exception:
            return "UNABLE TO DELETE CONVERTED AUDIO"


def decode_license(license):
    from cryptography.fernet import Fernet
    from scripts.assist import resource_path

    key = open(resource_path("utils/key.txt"), "r").read()
    f = Fernet(key)
    real_key = f.decrypt(license.encode()).decode()

    if "-" not in real_key:
        return 0
    else:
        p1, p2 = real_key.split("-")
        if str(p1).isalpha() and str(p2).isnumeric():
            return 1
        else:
            return 0


FAMILIES = {
    "Systran (Faster Whisper)": "systran",
    "OpenAI (Whisper)": "openai",
    "OpenAI (HF Whisper)": "openai_hf",
    "Distil Whisper": "distil-whisper_hf",
}

MODEL_SIZES = {
    "systran": ["tiny", "base", "small", "medium", "large"],
    "openai": ["tiny", "base", "small", "medium", "large"],
    "openai_hf": ["tiny", "base", "small", "medium", "large"],
    "distil-whisper_hf": ["small", "medium", "large"],
}

HF_MODEL_PREFIXES = {
    "openai_hf": "whisper",
    "distil-whisper_hf": "distil",
}

TYPES = ["simple", "segmentation", "diarisation"]

from utils.langs import LANGS
LANGUAGES = {
    "systran": ["AUTO"] + sorted(LANGS),
    "openai": ["AUTO"] + sorted(LANGS),
    "openai_hf": ["AUTO"] + sorted(LANGS),
    "distil-whisper_hf": ["english"],
}
