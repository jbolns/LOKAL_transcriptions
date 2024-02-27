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
from scripts.assist import resource_path,\
    split_audio, run_whisper_on_loop, better_together,\
    write_out, run_faster_whisper_on_loop


# ---------------------
# MAIN TRANSCRIPTION FLOW
# ...
def transcribe_segmentation(filepath,
                            filename,
                            model_family,
                            model_size,
                            language,
                            HYPER_PARAMETERS):
    ''' F(x) calls
        (1) a segmentation f(x),
        (2) a f(x) to split audio according to segmentation
        (3) a transcription f(x) for each audio chunk,
        (4) a merger f(x), and,
        (5) write out f(x)s to write joint result to TXT file on Desktop.
    '''

    # Import libraries only used in this function
    import shutil

    # Define path for output file
    path_to_user = os.path.expanduser('~')
    path_to_output_file = os.path.dirname(filepath) + "/" + filename + '.txt'

    # Create directory to save temp files
    path_to_temp = path_to_user + '/LOKAL_temp'
    if not os.path.isdir(path_to_temp):
        os.makedirs(path_to_temp)

    # Run segmentation
    print('\n...\nSegmenting audio\n')
    run_segmentation(filepath,
                     filename,
                     path_to_temp,
                     HYPER_PARAMETERS)

    # Re-organise diarisation into chunks and split audios accordingly
    print('\n...\nSplitting main audio into segments')
    CHUNKS = split_audio(filepath,
                         filename,
                         path_to_temp, 'segmentation')

    # Perform transcription on each temp audio file
    print('\n...\nTranscribing audio segments')
    print('\n...\nLoading or downloading model\
            \nIf model is already on local memory, Internet is NOT needed.\
            \nElse, the model needs to download, which requires Internet.\n')
    if model_family == 'openai_whisper':
        run_whisper_on_loop(filename,
                            model_size,
                            path_to_temp,
                            language)
    elif model_family == 'systran_faster_whisper':
        run_faster_whisper_on_loop(filename,
                                   model_size,
                                   path_to_temp,
                                   language)
    else:
        print('ERROR.\
              \nLOKAL cannot currently handle that family of models.')

    # Join speaker chunks and transcribed content
    print('\n...\nJoining segments transcriptions')
    LINES = better_together(path_to_temp, CHUNKS)

    # Write transcript into final TXT file
    print('\n...\nWriting final transcript to file')
    write_out(path_to_output_file, filename, LINES, 'segmentation')

    # Remove temp files and directory
    # Ps. Program can generate transcript even if directory removal fails
    #   – no need to kill the whole thing if errors.
    try:
        try:
            shutil.rmtree(path_to_temp)
        except:
            os.rmdir(path_to_temp)
    except:
        pass

    # Declare victory
    return (f'Finished transcription of: {filepath}.\
            \nFind it on your Desktop.', 1)


# ---------------------
# SEGMENTATION FUNCTION
# ...
def run_segmentation(filepath, filename, path_to_temp, HYPER_PARAMETERS):
    ''' F(x) calls Pyannote and writes result to temporary TXT file.
    '''

    # Import necessary libraries
    from pyannote.audio import Model
    from pyannote.audio.pipelines import VoiceActivityDetection
    from pyannote.audio.pipelines.utils.hook import ProgressHook

    # Load segmentation model
    model_location = 'models/segmentation/pytorch_model.bin'
    model = Model.from_pretrained(resource_path(model_location))
    pipeline = VoiceActivityDetection(segmentation=model)

    # Define hyper-parameters for model
    H_PARAMS = {
        # ignore short speech regions
        'min_duration_on': HYPER_PARAMETERS['min_duration_on'],
        # fill non-speech regions
        'min_duration_off': HYPER_PARAMETERS['min_duration_off']
        }

    # Run model
    pipeline.instantiate(H_PARAMS)
    with ProgressHook() as hook:
        segments = pipeline(filepath, hook=hook)

    # Save segments to temp TXT file
    L = []
    for turn, _ in segments.itertracks():
        L.append([turn.start-0.4, turn.end-0.4])

    # Write segments to temporary file
    with open(path_to_temp + '/' + 'temp-segments.txt', 'w') as f:
        for line in L:
            f.write(str(line[0]) + ', '  + str(line[1]) + '\n')
        f.close()

    # Return segments
    return f'Finished segmentation of {filename}'


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    transcribe_segmentation()
