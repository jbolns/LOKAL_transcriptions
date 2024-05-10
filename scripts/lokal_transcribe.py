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
import datetime
from scripts.assist import resource_path, split_audio, whisper_loop, together, write_out, fw_loop


# ---------------------
# MAIN TRANSCRIPTION FLOW
# ...
def transcribe_simple(settings, filename):
    '''F(x) calls transcription model and writes result to TXT file'''

    # Define path for output file
    path_to_audio, path_to_prompt, family, model, approach, language, timestamps, gpu, tcs = list(settings.values())
    path_to_output_file = os.path.dirname(path_to_audio) + '/' + filename + '.txt'

    # Check model family and perform transcription as appropriate
    print(f'\n...\nSelected approach to transcription: {approach}\
          \n\n...\nLoading or downloading model\
          \nIf model not already on local memory, Internet is required.\n')

    # Whisper track
    if family == 'openai_whisper':
        # Import appropriate library and load model
        import whisper
        model = whisper.load_model(model, download_root=resource_path('./models/whisper'))

        # Set a basic prompt or load a promt file
        if path_to_prompt != '':
            with open(path_to_prompt, 'r') as f:
                prompt = f.read()
        else:
            prompt = 'This prompt is a fallback, with a comma.'

        # Perform transcription
        print('\n...\nTranscribing audio')
        if language == 'AUTO':
            result = model.transcribe(path_to_audio,
                                      initial_prompt=prompt,
                                      fp16=gpu,
                                      verbose=True)
        else:
            result = model.transcribe(path_to_audio,
                                      initial_prompt=prompt,
                                      language=language,
                                      fp16=gpu,
                                      verbose=True)
        segments = result['segments']

    # Faster Whisper track
    elif family == 'systran_faster_whisper':
        # Imports and load model
        from scripts.utils import LANGUAGES
        from faster_whisper import WhisperModel
        model = WhisperModel(model,
                             device='cpu' if gpu is False else 'cuda',
                             compute_type='int8' if gpu is False else 'float16',
                             download_root=resource_path('./models/faster-whisper'))

        # Perform transcription
        print('\n...\nTranscribing audio')
        if language == 'AUTO':
            result, _ = model.transcribe(path_to_audio,
                                         beam_size=3 if gpu is False else 5,
                                         vad_filter=True)
        else:
            result, _ = model.transcribe(path_to_audio,
                                         beam_size=3 if gpu is False else 5,
                                         vad_filter=True,
                                         language=LANGUAGES[language])
        segments = []
        for line in result:
            print('[%.2fs -> %.2fs] %s' % (line.start, line.end, line.text))
            segments.append({'start': line.start, 'text': line.text})

    # Write transcription to file
    print('\n...\nWriting final transcript to file')
    with open(path_to_output_file, 'w') as f:
        for segment in segments:
            start_timestamp = str(datetime.timedelta(seconds=int(segment['start'])))
            content = segment['text']
            if timestamps is True:
                line =  f'[{start_timestamp}] {content}'
            else:
                line =  f'{content}'
            try:
                f.write(f'{line.strip()}\n')
            except Exception:
                f.write('!------ LINE IS MISSING --------!')
        f.close()

    # Declare victory
    return (f'Finished transcription of: {filename}. \
           \nFind it on the same folder as your audio.', 1)


# ---------------------
# JOINT TRANSCRIPTION FLOW FOR SEGMENTATION & DIARISATION
# ...
def transcribe_complex(settings, filename, HPs):
    ''' F(x) calls
        (1) a segmentation or a diarisation f(x),
        (2) a f(x) to split audio according to (1)
        (3) a transcription f(x) for each audio chunk,
        (4) a merger f(x), and,
        (5) write out f(x)s to write joint result to TXT file on Desktop.
    '''

    # Import libraries only used in this function
    import shutil

    # Define path for output file
    path_to_audio, path_to_prompt, family, model, approach, language, timestamps, gpu, tcs = list(settings.values())
    path_to_output_file = os.path.dirname(path_to_audio) + '/' + filename + '.txt'
    path_to_user = os.path.expanduser('~')

    # Create directory to save temp files
    path_to_temp_folder = path_to_user + '/LOKAL_temp'
    if not os.path.isdir(path_to_temp_folder):
        os.makedirs(path_to_temp_folder)

    # Run segmentation or diarisation
    if approach == 'segmentation':
        print('\n...\nSegmenting audio\n')
        segmentation(path_to_audio, filename, path_to_temp_folder, HPs)
    elif approach == 'diarisation':
        print('\n...\nDiarising audio\n')
        diarisation(path_to_audio, filename, path_to_temp_folder, HPs)
    else:
        print('ERROR.\
              \nTranscription approach does not exist or cannot be found.')

    # Re-organise into chunks and split audios accordingly
    print('\n...\nSplitting main audio into segments')
    CHUNKS = split_audio(path_to_audio, filename, path_to_temp_folder, approach)

    # Perform transcription on each temp audio file
    print('\n...\nTranscribing audio segments')
    print('\n...\nLoading or downloading model\
          \nIf model not already on local memory, Internet is required.\n')
    if family == 'openai_whisper':
        whisper_loop(path_to_temp_folder, filename, path_to_prompt, model, language, gpu)
    elif family == 'systran_faster_whisper':
        fw_loop(path_to_temp_folder, filename, model, language, gpu)
    else:
        print('ERROR. Wrong model family name.')

    # Join speaker chunks and transcribed content
    print('\n...\nJoining segments transcriptions')
    LINES = together(path_to_temp_folder, CHUNKS)

    # Write transcript into final TXT file
    print('\n...\nWriting final transcript to file')
    write_out(path_to_output_file, filename, LINES, approach, timestamps)

    # Remove temp files and directory
    # Ps. Program can generate transcript even if directory removal fails
    #   – no need to kill the whole thing if errors.
    try:
        try:
            shutil.rmtree(path_to_temp_folder)
        except:
            os.rmdir(path_to_temp_folder)
    except:
        pass

    # Declare victory
    return (f'Finished transcription of: {filename}.\
            \nFind it on the same folder as your audio.', 1)

# ---------------------
# SEGMENTATION FUNCTION
# ...
def segmentation(path_to_audio, filename, path_to_temp_folder, HPs):
    ''' F(x) calls Pyannote and writes result to temporary TXT file.
    '''

    # Function imports
    from pyannote.audio import Model
    from pyannote.audio.pipelines import VoiceActivityDetection
    from pyannote.audio.pipelines.utils.hook import ProgressHook

    # Load segmentation model
    model_location = 'models/segmentation/pytorch_model.bin'
    model = Model.from_pretrained(resource_path(model_location))
    pipeline = VoiceActivityDetection(segmentation=model)

    # Define hyper-parameters for model
    PARAMS = {
        # ignore short speech regions
        'min_duration_on': HPs['min_duration_on'],
        # fill non-speech regions
        'min_duration_off': HPs['min_duration_off']
        }

    # Run model
    pipeline.instantiate(PARAMS)
    with ProgressHook() as hook:
        segments = pipeline(path_to_audio, hook=hook)

    # Save segments to temp TXT file
    L = []
    for turn, _ in segments.itertracks():
        L.append([turn.start-0.4, turn.end-0.4])

    # Write segments to temporary file
    with open(path_to_temp_folder + '/' + 'temp-segments.txt', 'w') as f:
        for line in L:
            f.write(str(line[0]) + ', '  + str(line[1]) + '\n')
        f.close()

    # Return segments
    return f'Finished segmentation of {filename}'


# ---------------------
# DIARISATION FUNCTION
# ...
def diarisation(path_to_audio, filename, path_to_temp_folder, HPs):
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
            diarization = pipeline(path_to_audio,
                                   hook=hook)
    else:
        with ProgressHook() as hook:
            diarization = pipeline(path_to_audio,
                                   speaker_num=int(HPs['speaker_num']),
                                   hook=hook)
    
    with open(path_to_temp_folder + '/' + 'temp-diary.txt', 'a') as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.writelines(f'{turn.start}, {turn.end}, {speaker}\n')
        f.close()

    return f'Finished segmentation of {filename}'


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    transcribe_simple()
