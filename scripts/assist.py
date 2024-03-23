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
    path_to_temp = find_key_paths()[0] + '/LOKAL_temp'
    try:
        shutil.rmtree(path_to_temp)
    except:
        os.rmdir(path_to_temp)


# ---------------------
# FUNCTIONS USED BY SEVERAL FILES
# ...
# ---------------------
from scripts.utils import more_magic

# AUDIO SPLITTING FUNCTION
# Used by segmentation and diarisation scripts
def split_audio(filepath, filename, path_to_temp, approach):
    ''' F(x) splits audio in as many chunks as speaker segments.
        Each segment is saved to temp folder.
    '''

    # Import necessary libraries
    from pydub import AudioSegment

    # Build array to organise splitting
    CHUNKS = []
    currentSpeaker = ''
    if approach == 'segmentation':
        with open(path_to_temp + '/' + 'temp-segments.txt', 'r') as f:
            for line in f.readlines():
                newline = line.split(', ')
                CHUNKS.append([float(newline[0]), float(newline[1])])
            f.close()
    else:
        with open(path_to_temp + '/' + 'temp-diary.txt', 'r') as f:
            for line in f.readlines():
                newline = line.split(' ')
                if newline[7] != currentSpeaker:
                    CHUNKS.append([newline[7], float(newline[3])])
                    currentSpeaker = newline[7]
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
            extract.export(path_to_temp + '/' + filename + str(i).zfill(n) + '.wav',
                           format='wav')
            i += 1
    if approach == 'segmentation':
        extract = audio[CHUNKS[i][0]*1000:]
    else:
        extract = audio[CHUNKS[i][1]*1000:]
    extract.export(path_to_temp + '/' + filename + str(i).zfill(n) + '.wav',
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

# Used by segmentation and diarisation scripts

# Standard Whisper
def run_whisper_on_loop(filename,
                        model_to_use,
                        path_to_temp,
                        language):
    ''' F(x) calls Whisper on each temp audio.
        It writes result of each run to a corresponding temp TXT
    '''

    # Import necessary libraries
    import whisper

    # Load transcription model
    model_location = './models/whisper'
    model = whisper.load_model(model_to_use,
                               download_root=resource_path(model_location))

    # Perform transcription on each temp audio file.
    current_track = 1
    list = [f for f in os.listdir(path_to_temp) if f.endswith('wav')]
    for file in list:
        # Second if just ensure non-audio files don't make it through.
        # OCD hits differently at 2am in the morning.
        if file.endswith('.wav'):
            # Update user on current progress
            print(f"\nSegment {current_track} of {len(list)}")
            current_track += 1
            try:
                # Get transcription from Whisper
                if language == 'AUTO':
                    result = model.transcribe(path_to_temp + '/' + file,
                                              fp16=False,
                                              verbose=True)
                else:
                    result = model.transcribe(path_to_temp + '/' + file,
                                              language=language, fp16=False,
                                              verbose=True)

                # Write transcription into a temp TXT file
                with open(path_to_temp + '/' + 'temp-transcript-' + file[:-4] + '.txt', 'w') as f:
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
def run_faster_whisper_on_loop(filename,
                               model_to_use,
                               path_to_temp,
                               language):
    ''' F(x) calls Faster Whisper on each temp audio.
        It writes result of each run to a corresponding temp TXT
    '''

    # Imports
    from scripts.utils import LANGUAGES
    from faster_whisper import WhisperModel

    # Load transcription model
    model_location = './models/faster-whisper'
    model = WhisperModel(model_to_use, device="cpu",
                         compute_type="int8",
                         download_root=resource_path(model_location))

    # Perform transcription on each temp audio file.
    current_track = 1
    list = [f for f in os.listdir(path_to_temp) if f.endswith('wav')]

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
                if language == 'AUTO':
                    result, _ = model.transcribe(path_to_temp + '/' + file,
                                                 beam_size=3)
                else:
                    result, _ = model.transcribe(path_to_temp + '/' + file,
                                                 beam_size=3,
                                                 language=LANGUAGES[language])

                segments = ''
                for line in result:
                    print('[%.2fs -> %.2fs] %s' % (line.start, line.end, line.text))
                    segments = segments + line.text

                # Write transcription into a temp TXT file
                with open(path_to_temp + '/' + 'temp-transcript-' + file[:-4] + '.txt', 'w') as f:
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
# Used by segmentation and diarisation scripts
def better_together(path_to_temp, CHUNKS):
    ''' F(x) joins temp files into a single array
    '''
    # Define stuff needed in function
    LINES = []
    # Join the diarisation array and contents of temporary TXT files
    i = 0
    for file in os.listdir(path_to_temp):
        if file.startswith('temp-transcript-'):
            with open(path_to_temp + "/" + file) as f:
                LINES.append([CHUNKS[i][0], f.read()])
                i += 1
    # Return the joint array
    return LINES


# FUNCTION TO WRITE A FINAL TRANSCRIPT AFTER JOINING TEMPORARY TRANSCRIPTS
# Used by segmentation and diarisation scripts
def write_out(path_to_output_file, filename, LINES, approach):
    ''' F(x) writes the final result to a TXT file in the output folder
    '''

    # Write to the final transcription file
    with open(path_to_output_file, 'w') as f:
        f.write(f'TRANSCRIPT OF file {filename} \n\n')
        for line in LINES:
            try:
                if approach == 'segmentation':
                    f.write(f'{line[1]} \n\n')
                else:
                    f.write(f'{line[0]} \n {line[1]} \n\n')
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
