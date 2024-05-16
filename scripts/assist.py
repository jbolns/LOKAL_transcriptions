# -*- coding: utf-8 -*-
'''
v1. Jan 2024.
@author: Dr J. / Polyzentrik Tmi.

LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos / Polyzentrik Tmi.
SPDX-License-Identifier: Apache-2.0

'''


# ---------------------
# TOP-LEVEL IMPORTS
# ...
import os
import shutil
from scripts.utils import more_magic


# ---------------------
# COMMON FILE SYSTEM ACTIONS
# ...
def find_key_paths():
    ''' F(x) finds folder paths needed across LOKAL
    '''
    path_to_user = os.path.expanduser('~')
    path_to_desktop = os.path.expanduser("~/Desktop")
    path_to_cwd = os.getcwd()
    return [path_to_user, path_to_desktop, path_to_cwd]


def delete_LOKAL_temp():
    ''' F(x) deletes LOKAL_temp, used to store intermediate steps.
        Folder needs to be deleted to avoid errors in future.
    '''
    path_to_temp_folder = find_key_paths()[0] + '/LOKAL_temp'
    try:
        shutil.rmtree(path_to_temp_folder)
    except Exception:
        os.rmdir(path_to_temp_folder)


# ---------------------
# FUNCTIONS USED BY SEVERAL FILES
# ...
# ---------------------

# AUDIO SPLITTING FUNCTION
def split_audio(filepath, filename, path_to_temp_folder, approach):
    ''' F(x) splits audio in as many chunks as speaker segments.
        Each segment is saved to temp folder.
    '''

    # Import necessary libraries
    from pydub import AudioSegment

    # Build array to organise splitting
    CHUNKS = []
    currentSpeaker = ''
    if approach == 'segmentation':
        with open(path_to_temp_folder + '/' + 'temp-segments.txt', 'r') as f:
            for line in f.readlines():
                newline = line.split(', ')
                CHUNKS.append([float(newline[0]), float(newline[1])])
            f.close()
    else:
        with open(path_to_temp_folder + '/' + 'temp-diary.txt', 'r') as f:
            for line in f.readlines():
                newline = line.split(', ')
                if newline[2] != currentSpeaker:
                    CHUNKS.append([newline[2], float(newline[0])])
                    currentSpeaker = newline[2]
            f.close()

    # Split audio into a file per speaker segment
    i = 0
    n = len(str(len(CHUNKS)))

    audio = AudioSegment.from_file(filepath)
    for chunk in CHUNKS:
        if i < len(CHUNKS) - 1:
            if approach == 'segmentation':
                extract = audio[CHUNKS[i][0]*1000:CHUNKS[i + 1][0]*1000]
            else:
                extract = audio[CHUNKS[i][1]*1000:CHUNKS[i + 1][1]*1000]
            extract.export(path_to_temp_folder + '/' + filename + str(i).zfill(n) + '.wav',
                           format='wav')
            i += 1
    if approach == 'segmentation':
        extract = audio[CHUNKS[i][0]*1000:]
    else:
        extract = audio[CHUNKS[i][1]*1000:]
    extract.export(path_to_temp_folder + '/' + filename + str(i).zfill(n) + '.wav',
                   format='wav')

    # Return the speaker chunks for later usage
    return CHUNKS


# RANDOM CHECKS
def checker():
    from scripts.assist import resource_path
    license = open(resource_path('utils/license.txt'), 'r').read()
    tries = len(open(resource_path('utils/try.txt'), 'r').read()) + 1
    if len(license) > 0:
        result = license
    elif tries <= 5:
        result = 'free trial'
    else:
        result = 'no license'
    return result


# TRANSCRIPTION ON A LOOP
def magic():
    return more_magic()


# Standard Whisper
def whisper_loop(path_to_temp_folder, filename, path_to_prompt, model_size, language, gpu):
    ''' F(x) calls Whisper on each temp audio.
        It writes result of each run to a corresponding temp TXT
    '''

    # Import necessary libraries
    import whisper

    # Load transcription model
    model_location = './models/whisper'
    model = whisper.load_model(model_size, download_root=resource_path(model_location))

    # Set a basic prompt or load a promt file
    if path_to_prompt != '':
        with open(path_to_prompt, 'r') as f:
            prompt = f.read()
    else:
        prompt = 'This prompt is a fallback, with a comma.'

    # Perform transcription on each temp audio file.
    current_track = 1
    list = [f for f in os.listdir(path_to_temp_folder) if f.endswith('wav')]
    for file in list:
        # Second if just ensure non-audio files don't make it through.
        # OCD hits differently at 2am in the morning.
        if file.endswith('.wav'):
            # Update user on current progress
            print(f"\nSegment {current_track} of {len(list)}")
            current_track += 1
            try:
                # Get transcription from Whisper
                if language.lower() == 'auto':
                    result = model.transcribe(path_to_temp_folder + '/' + file,
                                              initial_prompt=prompt,
                                              fp16=gpu,
                                              verbose=True)
                else:
                    result = model.transcribe(path_to_temp_folder + '/' + file,
                                              initial_prompt=prompt,
                                              language=language,
                                              fp16=gpu,
                                              verbose=True)

                # Write transcription into a temp TXT file
                with open(path_to_temp_folder + '/' + 'temp-transcript-' + file[:-4] + '.txt', 'w') as f:
                    try:
                        f.write(result['text'])
                    except Exception:
                        pass
                    f.close()
            except Exception as e:
                print(f'Error transcribing segment.\
                      \nSystem generated error is:\n{e}')

    # Return time spent transcribing with Whisper
    return f'Finished Whisper for {filename}'


# Faster Whisper
def fw_loop(path_to_temp_folder, filename, model_size, language, gpu):
    ''' F(x) calls Faster Whisper on each temp audio.
        It writes result of each run to a corresponding temp TXT
    '''

    # Imports
    from scripts.utils import LANGUAGES
    from faster_whisper import WhisperModel

    # Load transcription model
    model_location = './models/faster-whisper'
    model = WhisperModel(model_size,
                         device='cpu' if gpu is False else 'cuda',
                         compute_type='int8' if gpu is False else 'float16',
                         download_root=resource_path(model_location))

    # Perform transcription on each temp audio file.
    current_track = 1
    list = [f for f in os.listdir(path_to_temp_folder) if f.endswith('wav')]

    # I tried multi-processing. Gains are too small.
    for file in list:
        # Second if just ensure non-audio files don't make it through.
        # OCD hits differently at 2am in the morning.
        if file.endswith('.wav'):
            # Update user on current progress
            print(f'\nSegment {current_track} of {len(list)}')
            current_track += 1
            try:
                # Get transcription from Faster Whisper
                if language.lower() == 'auto':
                    result, _ = model.transcribe(path_to_temp_folder + '/' + file,
                                                 beam_size=3 if gpu is False else 5,
                                                 vad_filter=True)
                else:
                    result, _ = model.transcribe(path_to_temp_folder + '/' + file,
                                                 beam_size=3 if gpu is False else 5,
                                                 vad_filter=True,
                                                 language=LANGUAGES[language])

                segments = ''
                for line in result:
                    print('[%.2fs -> %.2fs] %s' % (line.start, line.end, line.text))
                    segments = segments + line.text

                # Write transcription into a temp TXT file
                with open(path_to_temp_folder + '/' + 'temp-transcript-' + file[:-4] + '.txt', 'w') as f:
                    try:
                        f.write(segments)
                    except Exception:
                        pass
                    f.close()
            except Exception as e:
                print(f'Error transcribing segment.\
                      \nSystem generated error is:\n{e}')

    # Return time spent transcribing with Whisper
    return f'Finished Whisper for {filename}'


# FUNCTION TO JOIN TEMPORARY TRANSCRIPTS
def together(path_to_temp_folder, CHUNKS):
    ''' F(x) joins temp files into a single array
    '''
    # Define stuff needed in function
    LINES = []
    # Join the diarisation array and contents of temporary TXT files
    i = 0
    for file in os.listdir(path_to_temp_folder):
        if file.startswith('temp-transcript-'):
            with open(path_to_temp_folder + "/" + file) as f:
                LINES.append([CHUNKS[i][0], CHUNKS[i][1], f.read()])
                i += 1
    # Return the joint array
    return LINES


# FUNCTION TO WRITE A FINAL TRANSCRIPT AFTER JOINING TEMPORARY TRANSCRIPTS
def write_out(path_to_output_file, filename, LINES, approach, timestamps):
    ''' F(x) writes the final result to a TXT file in the output folder
    '''

    # Function imports
    import datetime

    # Write to the final transcription file
    with open(path_to_output_file, 'w') as f:
        f.write(f'TRANSCRIPT OF file {filename} \n\n')
        for line in LINES:
            try:
                if approach == 'segmentation':
                    start_timestamp = f'\n[{datetime.timedelta(seconds=int(line[0]))}]' if timestamps is True else ''
                    line_content = line[2]
                    f.write(f'{start_timestamp}\n{line_content}\n')
                else:
                    start_timestamp = f'[{datetime.timedelta(seconds=int(line[1]))}] ' if timestamps is True else ''
                    speaker = line[0]
                    line_content = line[2]
                    f.write(f'{start_timestamp}{speaker}{line_content}\n\n')
            except Exception:
                pass
        f.close()


# ---------------------
# PYINSTALLER ASSIST
# ...
# Shout out to for this lifesaver, via https://youtu.be/p3tSLatmGvU
# stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    import sys
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
