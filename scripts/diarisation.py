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
from scripts.assist import resource_path, split_audio,\
    run_whisper_on_loop, better_together, write_out,\
    run_faster_whisper_on_loop


# ---------------------
# MAIN TRANSCRIPTION FLOW
# ...
def transcribe_diarisation(filepath,
                           filename,
                           model_family,
                           model_size,
                           language,
                           HPs):
    '''F(x) calls
        (1) a diarisation f(x),
        (2) a f(x) to split audio according to diarisation
        (3) a transcription f(x) for each audio chunk,
        (4) a merger f(x), and,
        (5) a write out f(x) to write joint result to TXT file
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

    # Run diarisation
    print('\n...\nSegmenting & diarising audio\n')
    run_diarisation(filepath,
                    filename,
                    path_to_temp,
                    HPs)

    # Re-organise diarisation into speaker chunks and split audios accordingly
    print('\n...\nSplitting main audio into segments')
    CHUNKS = split_audio(filepath,
                         filename,
                         path_to_temp,
                         'diarisation')

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
    LINES = better_together(path_to_temp,
                            CHUNKS)

    # Write transcript into final TXT file
    print('\n...\nWriting final transcript to file')
    write_out(path_to_output_file,
              filename,
              LINES,
              'diarisation')

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
    return (f'Finished transcription of: {filename}.\
            \nFind it on the same folder as your audio.', 1)


# ---------------------
# SEGMENTATION FUNCTION
# ...
def run_diarisation(filepath,
                    filename,
                    path_to_temp,
                    HPs):
    ''' F(x) performs diarisation using pyannote.
        It writes result to temporary TXT file.
    '''

    # Import necessary libraries
    from pyannote.audio import Model
    from pyannote.audio.pipelines import SpeakerDiarization as Pipeline
    from pyannote.audio.pipelines.utils.hook import ProgressHook

    # Initialise models
    seg_model_loc = 'models/segmentation/pytorch_model.bin'
    emb_model_loc = 'models/embedding/pytorch_model.bin'
    segmentation_model = Model.from_pretrained(resource_path(seg_model_loc))
    embedding_model = Model.from_pretrained(resource_path(emb_model_loc))
    pipeline = Pipeline(segmentation=segmentation_model,
                        embedding=embedding_model)

    # Set hyper-parameters
    PARAMS = {'segmentation': {
        # fill non-speech regions
        'min_duration_off': HPs['min_duration_off'],
        },
        'clustering': {
            'method': 'centroid',
            'min_cluster_size': 12,
            'threshold': 0.7045654963945799,
        },
    }

    # Run model
    pipeline.instantiate(PARAMS)
    if HPs['speaker_num'] == 'AUTO':
        with ProgressHook() as hook:
            diarization = pipeline(filepath,
                                   hook=hook)
    else:
        with ProgressHook() as hook:
            diarization = pipeline(filepath,
                                   speaker_num=int(HPs['speaker_num']),
                                   hook=hook)

    # Write the diarisation result to temp file
    with open(path_to_temp + '/' + 'temp-diary.txt', 'w') as f:
        diarization.write_rttm(f)
        f.close()

    return f'Finished segmentation of {filename}'


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    transcribe_diarisation()
