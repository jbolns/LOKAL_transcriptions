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
# MAIN TRANSCRIPTION FLOW
# ...
def transcribe_simple(filepath, filename, model_family, model_size, language):
    '''F(x) calls transcription model and writes result to TXT file'''

    # Import necessary libraries
    import os
    from scripts.assist import resource_path

    # Define path for output file
    path_to_output_file = os.path.dirname(filepath) + '/' + filename + '.txt'

    # Check model family and perform transcription as appropriate
    print('\n...\nLoading or downloading model\
          \nIf model is already on local memory, Internet is NOT needed.\
          \nElse, the model needs to download, which requires Internet.\n')

    # Whisper track
    if model_family == 'openai_whisper':
        # Import appropriate library and load model
        import whisper
        model = whisper.load_model(model_size,
                                   download_root=resource_path('./models/whisper'))

        # Perform transcription
        print('\n...\nTranscribing audio')
        if language == 'AUTO':
            result = model.transcribe(filepath,
                                      fp16=False,
                                      verbose=True)
        else:
            result = model.transcribe(filepath,
                                      language=language,
                                      fp16=False,
                                      verbose=True)
        segments = result['segments']

    # Faster Whisper track
    elif model_family == 'systran_faster_whisper':
        # Import appropriate library and load model
        from scripts.utils import LANGUAGES
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device='cpu',
                             compute_type='int8',
                             download_root=resource_path('./models/faster-whisper'))

        # Perform transcription
        print('\n...\nTranscribing audio')
        if language == 'AUTO':
            result, _ = model.transcribe(filepath,
                                         beam_size=3)
        else:
            result, _ = model.transcribe(filepath,
                                         beam_size=3,
                                         language=LANGUAGES[language])
        segments = []
        for line in result:
            print('[%.2fs -> %.2fs] %s' % (line.start, line.end, line.text))
            segments.append(line.text)

    # Write transcription to file
    print('\n...\nWriting final transcript to file')
    with open(path_to_output_file, 'w') as f:
        for segment in segments:
            if model_family == 'openai_whisper':
                line = segment['text']
            elif model_family == 'systran_faster_whisper':
                line = segment
            try:
                f.write(f'{line.strip()}\n')
            except Exception:
                f.write('!------ LINE IS MISSING --------!')
        f.close()

    # Declare victory
    return (f'Finished transcription of: {filepath}. \
           \nFind it on the same folder as your audio.', 1)


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    transcribe_simple()
