'''
v1. Jan 2024.
@author: Dr J. / Polyzentrik Tmi.

LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos / Polyzentrik Tmi.
SPDX-License-Identifier: Apache-2.0

'''

# ---------------------
# LICENSE CHECKs
# ...
def check_license():
    import config
    from scripts.utils import decode_license

    if config.license_status == 'no license':
        status = 0
        message = 'MAKE LOKAL PRETTY AGAIN'
    elif config.license_status == 'free trial':
        status = 1
        message = 'ENABLE COLOR THEMES'
    elif decode_license(config.license_status):
        status = 2
        message = 'HELP US HELP'
    else:
        status = 0
        message = 'MAKE LOKAL PRETTY AGAIN'
    return status, message


def log_free_run():
    import config
    from scripts.assist import resource_path

    if config.license_status == 'free trial':
        tries = len(open(resource_path('utils/try.txt'), 'r').read()) + 1
        if tries <= 5:
            with open(resource_path('utils/try.txt'), 'w')as f:
                f.write('.' * tries)
                f.close()
        else:
            config.license_status = 'due'


# ---------------------
# AUDIO CONVERSION
# Needed if main audio is not in .wav format
# ...

def convert_to_wav(filepath, filename):
    from pydub import AudioSegment

    try:
        source_folder = filepath.rpartition('/')[0]
        new_filepath = source_folder + '/' + filename + '-wavcopyforLOKALtranscription' + '.wav'

        # Import file
        audio = AudioSegment.from_file(filepath)

        # Export file
        audio.export(new_filepath, format='wav')

        return 1
    except Exception:
        return 0


def more_magic():
    return 2


def delete_converted_wav(filepath):
    if filepath.endswith('wav'):
        import os
        try:
            os.remove(filepath)
            return '\n\n...\nDELETED CONVERTED AUDIO\
                  \nSuccesfully deleted the temporary .wav version of your audio used for transcription.\n'
        except Exception:
            return '\n\n...\nUNABLE TO DELETE CONVERTED AUDIO\
                  \nLOKAL saved a .wav version of the original audio to the same folder as the original audio.\
                  \nNormally, the converted version is deleted automatically, but there were errors with deletion.\
                  \nCheck if the file is still there and delete manually if desired.\n'


def decode_license(license):
    from cryptography.fernet import Fernet
    from scripts.assist import resource_path

    key = open(resource_path('utils/key.txt'), 'r').read()
    f = Fernet(key)
    real_key = f.decrypt(license.encode()).decode()

    if '-' not in real_key:
        return 0
    else:
        p1, p2 = real_key.split('-')
        if str(p1).isalpha() and str(p2).isnumeric():
            return 1
        else:
            return 0


LANGUAGES = {
    "english": "en",
    "chinese": "zh",
    "german": "de",
    "spanish": "es",
    "russian": "ru",
    "korean": "ko",
    "french": "fr",
    "japanese": "ja",
    "portuguese": "pt",
    "turkish": "tr",
    "polish": "pl",
    "catalan": "ca",
    "dutch": "nl",
    "arabic": "ar",
    "swedish": "sv",
    "italian": "it",
    "indonesian": "id",
    "hindi": "hi",
    "finnish": "fi",
    "vietnamese": "vi",
    "hebrew": "he",
    "ukrainian": "uk",
    "greek": "el",
    "malay": "ms",
    "czech": "cs",
    "romanian": "ro",
    "danish": "da",
    "hungarian": "hu",
    "tamil": "ta",
    "norwegian": "no",
    "thai": "th",
    "urdu": "ur",
    "croatian": "hr",
    "bulgarian": "bg",
    "lithuanian": "lt",
    "latin": "la",
    "maori": "mi",
    "malayalam": "ml",
    "welsh": "cy",
    "slovak": "sk",
    "telugu": "te",
    "persian": "fa",
    "latvian": "lv",
    "bengali": "bn",
    "serbian": "sr",
    "azerbaijani": "az",
    "slovenian": "sl",
    "kannada": "kn",
    "estonian": "et",
    "macedonian": "mk",
    "breton": "br",
    "basque": "eu",
    "icelandic": "is",
    "armenian": "hy",
    "nepali": "ne",
    "mongolian": "mn",
    "bosnian": "bs",
    "kazakh": "kk",
    "albanian": "sq",
    "swahili": "sw",
    "galician": "gl",
    "marathi": "mr",
    "punjabi": "pa",
    "sinhala": "si",
    "khmer": "km",
    "shona": "sn",
    "yoruba": "yo",
    "somali": "so",
    "afrikaans": "af",
    "occitan": "oc",
    "georgian": "ka",
    "belarusian": "be",
    "tajik": "tg",
    "sindhi": "sd",
    "gujarati": "gu",
    "amharic": "am",
    "yiddish": "yi",
    "lao": "lo",
    "uzbek": "uz",
    "faroese": "fo",
    "haitian creole": "ht",
    "pashto": "ps",
    "turkmen": "tk",
    "nynorsk": "nn",
    "maltese": "mt",
    "sanskrit": "sa",
    "luxembourgish": "lb",
    "myanmar": "my",
    "tibetan": "bo",
    "tagalog": "tl",
    "malagasy": "mg",
    "assamese": "as",
    "tatar": "tt",
    "hawaiian": "haw",
    "lingala": "ln",
    "hausa": "ha",
    "bashkir": "ba",
    "javanese": "jw",
    "sundanese": "su",
    "cantonese": "yue",
    "burmese": "my",
    "valencian": "ca",
    "flemish": "nl",
    "haitian": "ht",
    "letzeburgesch": "lb",
    "pushto": "ps",
    "panjabi": "pa",
    "moldavian": "ro",
    "moldovan": "ro",
    "sinhalese": "si",
    "castilian": "es",
    "mandarin": "zh",
}
