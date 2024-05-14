# -*- coding: utf-8 -*-
'''
v1. Jan 2024.
@author: Dr J. / Polyzentrik Tmi.

Except for a glorious class to enable real-time updates,
LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos / Polyzentrik Tmi.
SPDX-License-Identifier: Apache-2.0

'''

# ---------------------
# TOP-LEVEL IMPORTS
# ...
import os
import sys
import time
import shutil
import threading
import webbrowser
from tkinter import filedialog, messagebox

import ttkbootstrap as tb
from ttkbootstrap.constants import TRUE, BOTH, YES, TOP, BOTTOM, LEFT, RIGHT, X, WORD, INSERT, END
from ttkbootstrap.scrolled import ScrolledFrame

from contextlib import redirect_stdout, redirect_stderr

from scripts.assist import resource_path, find_key_paths, magic, delete_LOKAL_temp
from scripts.utils import LANGUAGES, check_license, log_free_run


# ---------------------
# TKINTER BOOTSTRAP APP
# ...
def app():
    ''' F(x) launches main app for users to perform transcriptions
        and contains app's main loop.
    '''

    # SETTINGS AND HYPER-PARAMETERS DICTIONARIES
    global settings
    settings = {'path_to_audio': '',
                'path_to_prompt': '',
                'family': 'openai_whisper',
                'model': 'tiny',
                'approach': 'simple',
                'language': 'AUTO',
                'timestamps_on': False,
                'gpu_on': '0',
                'tcs_ok': 0}

    # ROOT WINDOW & ROOT CONFIGS
    global app
    app = tb.Window(title='LOKAL: Local AI transcriptions',
                    themename='journal')
    app.title('LOKAL: Local AI transcriptions')
    app.iconbitmap(resource_path('images/icon.ico'))

    init_width = int(app.winfo_screenwidth() * 0.7)
    init_height = int(app.winfo_screenheight() * 0.7)
    app.geometry(f'{init_width}x{init_height}')
    app.resizable(True, True)

    global root
    root = ScrolledFrame(app, autohide=TRUE)
    root.pack(fill=BOTH, expand=YES)

    # FRAMES FOR VISUAL ORGANISATION
    top_frame = tb.Frame(root)
    top_frame.pack(side=TOP, padx=14, pady=(3, 14),
                   anchor='ne', expand=True)

    upper_frame = tb.Frame(root)
    upper_frame.pack(side=TOP, pady=(14, 0),
                     anchor='s', expand=True)

    lower_frame = tb.Frame(root)
    lower_frame.pack(side=BOTTOM, pady=(0, 3),
                     padx=14, fill=X, anchor='n', expand=True)

    left_frame = tb.Frame(upper_frame)
    left_frame.pack(side=LEFT, padx=28, anchor='e', expand=True)
    right_frame = tb.Frame(upper_frame)
    right_frame.pack(side=RIGHT, padx=28, anchor='w', expand=True)

    title_frame = tb.Frame(left_frame)
    title_frame.pack(fill=X)

    config_frame = tb.Frame(right_frame)
    config_frame.pack(fill=X)
    config_frame.bind("<Configure>", resize)

    params_frame = tb.Frame(lower_frame)
    params_frame.pack(pady=(14, 14), fill=X)

    run_frame = tb.Frame(lower_frame)
    run_frame.pack(fill=X)

    # UPPER FRAME FOR HEADER & MAIN SETTINGS
    # View modes
    themes = ['cyborg', 'darkly', 'vapor', 'minty', 'yeti', 'journal']

    license_status, call_to_action = check_license()
    if license_status == magic():
        global my_theme
        my_theme = tb.StringVar()
        for theme in themes:
            radio_button = tb.Radiobutton(top_frame,
                                          variable=my_theme,
                                          value= theme,
                                          style='custom.TRadiobutton',
                                          command=toggle_mode)
            radio_button.pack(side=RIGHT, anchor='n', pady=3)
    else:
        lbl_palette = tb.Label(top_frame,
                               bootstyle='danger',
                               text='COLOR PALETTE DISABLED',
                               font='impact 12')
        lbl_palette.pack(side=RIGHT, anchor='n', pady=3, padx=7)

    # Header
    title = tb.Label(title_frame, text='LOKAL', font='Helvetica 48 bold')
    title.pack(fill=X, expand=True)

    subtitle = tb.Label(title_frame, text='Local AI transcriptions', font='Courier 16 bold')
    subtitle.pack(fill=X, expand=True)

    company = tb.Label(title_frame,
                       text='www.polyzentrik.com',
                       bootstyle='info',
                       font='Courier 10 bold underline',
                       cursor='hand2')
    company.pack(expand=True, anchor='e')
    company.bind('<Button-1>', lambda e: webbrowser.open('https://www.polyzentrik.com/'))

    # Audio selection
    global audio_select
    audio_select = tb.Button(title_frame,
                             text='SELECT AUDIO',
                             command=lambda: browse_for_file('audio'),
                             bootstyle='dark, outline')
    audio_select.pack(fill=X, pady=(21, 1), expand=True)

    misc_frame = tb.Frame(title_frame)
    misc_frame.pack(fill=X, expand=True, pady=3, padx=(0, 28))

    # Selection for computing type (CPU or GPU)
    global gpu_on
    gpu_on = tb.BooleanVar()
    gpu_btn = tb.Checkbutton(misc_frame,
                             text='GPU',
                             bootstyle='success-square-toggle',
                             variable=gpu_on,
                             onvalue=True,
                             offvalue=False,
                             command=key_settings)
    gpu_btn.pack(side=LEFT, padx=(0,3))

    # Optional timestamps
    global stamps_on
    stamps_on = tb.BooleanVar()
    stamps_btn = tb.Checkbutton(misc_frame,
                                text='Timestamps',
                                bootstyle='success-square-toggle',
                                variable=stamps_on,
                                onvalue=True,
                                offvalue=False,
                                command=key_settings)
    stamps_btn.pack(side=LEFT, padx=(0,3))

    global tcs_ok
    tcs_ok = tb.BooleanVar()
    tcs_btn = tb.Checkbutton(title_frame,
                             text='Accept all ',
                             bootstyle='success',
                             variable=tcs_ok,
                             onvalue=True,
                             offvalue=False,
                             command=key_settings)
    tcs_btn.pack(side=LEFT)

    tcs_extension = tb.Label(title_frame,
                             text='terms & conditions',
                             font='Helvetica 8 underline',
                             cursor='hand2')
    tcs_extension.pack(side=LEFT)
    tcs_extension.bind('<Button-1>', lambda e: pop_window(e, 'tcs'))

    # KEY HYPER-PARAMETERS SIDEBAR
    # Dropdown to select desired model to transcription
    tb.Label(config_frame, text='MODEL', font='Helvetica 8 bold').pack(anchor='w')

    families = ['OpenAI: Whisper', 'Systran: Faster Whisper']
    
    global whisper
    global fs_whisper
    whisper = ['tiny', 'base', 'small', 'medium', 'large']
    fs_whisper = ['tiny', 'base', 'small', 'medium', 'large']

    global family_select
    family_select = tb.Combobox(config_frame, values=families)
    family_select.pack()
    family_select.current(0)
    family_select.bind('<<ComboboxSelected>>', family_choice)

    global model_select
    model_select = tb.Combobox(config_frame, values=[i.capitalize() for i in whisper])
    model_select.pack()
    model_select.current(0)
    model_select.bind('<<ComboboxSelected>>', model_language_settings)

    # Dropdown to select desired approach to transcription
    types = ['simple', 'segmentation', 'diarisation']
    
    tb.Label(config_frame, text='APPROACH', font='Helvetica 8 bold').pack(anchor='w', pady=[14, 0])
    global type_select
    type_select = tb.Combobox(config_frame, values=[i.capitalize() for i in types])
    type_select.pack()
    type_select.current(0)
    type_select.bind('<<ComboboxSelected>>', approach_choice)

    # Dropdown to select language
    langs = ['AUTO'] + sorted(LANGUAGES.keys())

    tb.Label(config_frame, text='LANGUAGE', font='Helvetica 8 bold').pack(anchor='w', pady=[14, 0])
    global lang_select
    lang_select = tb.Combobox(config_frame, values=[i.title() for i in langs])
    lang_select.pack()
    lang_select.current(0)
    lang_select.bind('<<ComboboxSelected>>', model_language_settings)

    # Button to select a prompt file (available for normal Whisper)
    global prompt_separator
    prompt_separator = tb.Separator(config_frame)
    prompt_separator.pack(anchor='w', fill=X, pady=[21, 14])
    
    global prompt_intro
    prompt_intro = tb.Label(config_frame,
                            text='OPTIONAL PROMPT',
                            font='Helvetica 8 bold')
    prompt_intro.pack(anchor='w', pady=0)

    global prompt_select
    prompt_select = tb.Button(config_frame,
                              text='> Upload prompt',
                              command=lambda: browse_for_file('prompt'))
    prompt_select.pack(fill=X, expand=True, anchor='w')

    # OPTIONAL HYPER-PARAMETERS AREA
    # Main wrapper frame
    global hps_frame
    hps_frame = tb.LabelFrame(params_frame, border=0)
    hps_frame.pack(pady=[0, 7], anchor='w', fill=X, expand=True)
    hps_frame.bind("<Configure>", resize)

    # Segmentation wrapper frame
    global segmentation_params
    segmentation_params = tb.Frame(hps_frame)

    # Segmentation hyper-parameters
    hps_hdr = tb.Label(segmentation_params,
                       text='OPTIONAL HYPER-PARAMETERS',
                       font='Helvetica 10 bold')
    hps_hdr.pack(anchor='nw', pady=(0, 3))

    global hps_param1
    hps_param1 = tb.Meter(segmentation_params, metersize=200,
                          bootstyle='dark', padding=5,
                          metertype='semi', interactive=True,
                          amountused=1500, amounttotal=5000,
                          meterthickness=15, stripethickness=5,
                          subtext='Ignore short segments', textright='ms')
    hps_param1.pack(side=LEFT)

    global hps_param2
    hps_param2 = tb.Meter(segmentation_params, metersize=200,
                          bootstyle='dark', padding=5,
                          metertype='semi', interactive=True,
                          amountused=500, amounttotal=2000,
                          meterthickness=15, stripethickness=5,
                          subtext='Ignore short pauses', textright='ms')
    hps_param2.pack(side=LEFT)

    # Segmentation wrapper frame
    global diarisation_params
    diarisation_params = tb.Frame(hps_frame)
    
    # Diarisation hyper-parameters
    hps_hdr = tb.Label(diarisation_params,
                       text='ADDITIONAL HYPER-PARAMETERS AVAILABLE',
                       font='Helvetica 10 bold')
    hps_hdr.pack(anchor='nw', pady=(0, 3))

    global hps_param3
    hps_param3 = tb.Meter(diarisation_params, bootstyle='dark',
                          metertype='semi', interactive=True,
                          amountused=200, amounttotal=5000,
                          metersize=200, meterthickness=15,
                          stripethickness=5, padding=5,
                          subtext='Ignore short pauses', textright='ms')
    hps_param3.pack()

    hps__param4_lbl = tb.Label(diarisation_params,
                               text='Number of speakers',
                               font='Helvetica 10')
    hps__param4_lbl.pack()

    global hps_param4
    hps_param4 = tb.Spinbox(diarisation_params, bootstyle='dark',
                            font='Helvetica 10 bold',
                            values=['AUTO', 1, 2, 3, 4, 5],
                            state='readonly')
    hps_param4.set('AUTO')
    hps_param4.pack()

    # NOTIFICATIONS AREA
    global notify_frame
    notify_frame = tb.LabelFrame(params_frame, border=0)
    notify_frame.pack(fill=X, expand=TRUE, padx=48)
    notify_frame.bind("<Configure>", resize)

    global console_frame
    console_frame = tb.ScrolledText(notify_frame, height=10, wrap=WORD)
    console_frame.config(bg='black', foreground='white')
    console_frame.pack(fill=X, expand=TRUE)

    # FINAL RUN AREA
    global btn_run
    btn_run = tb.Button(run_frame,
                        text='Run transcription',
                        command=run,
                        bootstyle='dark')
    btn_run.pack(fill=X, anchor='w')

    if license_status != magic():
        global btn_pay
        btn_pay = tb.Button(run_frame,
                            text=call_to_action,
                            bootstyle='dark, outline')
        btn_pay.pack(fill=X, pady=[3, 0], anchor='w')
        btn_pay.bind('<Button-1>', pop_license)

    lbl_license = tb.Label(run_frame,
                           text='Activation',
                           font='Helvetica 8',
                           cursor='hand2')
    lbl_license.pack(side=LEFT, pady=3)
    lbl_license.bind('<Button-1>', pop_license)

    tb.Label(run_frame, text='|',
             font='Helvetica 8',
             cursor='hand2').pack(side=LEFT, pady=3)

    lbl_services = tb.Label(run_frame,
                            text='Corporate services',
                            font='Helvetica 8',
                            cursor='hand2')
    lbl_services.pack(side=LEFT, pady=3)
    lbl_services.bind('<Button-1>',
                      lambda e: webbrowser.open('https://www.polyzentrik.com/services'))
    
    tb.Label(run_frame, text='|',
             font='Helvetica 8',
             cursor='hand2').pack(side=LEFT, pady=3)

    lbl_credits = tb.Label(run_frame,
                           text='Credits',
                           font='Helvetica 8',
                           cursor='hand2')
    lbl_credits.pack(side=LEFT, pady=3)
    lbl_credits.bind('<Button-1>', lambda e: pop_window(e, 'credits'))

    lbl_reset = tb.Label(run_frame,
                         text='RESET MODELS',
                         font='Helvetica 8',
                         cursor='hand2')
    lbl_reset.pack(side=RIGHT, pady=3)
    lbl_reset.bind('<Button-1>', reset_models)

    # Loop call so app refreshes on the regular
    logger('...\nLOKAL is made for comfort, not speed.\
           \nFor long audios, consider transcribing overnight.')
    app.after_idle(toggle_mode)
    app.protocol("WM_DELETE_WINDOW", kill_everything)
    app.bind('<Escape>', lambda e: kill_everything())
    app.mainloop()


# ---------------------
# TRANSCRIPTION TRIGGER & ORGANISER
# ...
def run():
    ''' F(x) triggers transcription if audio is selected and T&Cs met.
        Transcriptions launch on separate thread so app window renders updates.
    '''
    # For good health, try delete temp folders accidentally left previously
    try:
        delete_LOKAL_temp()
    except:  # Ignore exceptions, likely, no temp folders existed.
        pass

    # Check audio is selected and T&Cs are agreed, proceed if so
    if settings['path_to_audio'] == '':
        logger('\n\n...\nYou have not selected an audio file. You need to select an audio for a transcription to be possible.')
        popbox = messagebox.showwarning('showwarning', 'You have not selected an audio file. It is therefore impossible to proceed.')
    elif settings['tcs_ok'] == 0:
        logger('\n\n...\nYou have not accepted the terms and conditions. You need to accept the terms and conditions for a transcription to be possible.')
        popbox = messagebox.showwarning('showwarning', 'You have not accepted the terms and conditions. It is therefore impossible to proceed.')
    else:
        hps_frame.forget()
        notify_frame.pack(fill=X, expand=TRUE, padx=48)
        console_frame.delete('1.0', END)
        app.update()
        try:
            transcription_thread = threading.Thread(target=run_transcription, daemon=True)
            transcription_thread.start()
            btn_run.configure(text='TRANSCRIPTION RUNNING',
                              command=lambda: messagebox.showwarning('showwarning', 'Transcription is already running.'))
        except Exception as e:
            logger(f'...\nTranscription thread has failed. Error is... {e}')


def run_transcription():
    ''' F(x) organises the transcription flow.
    '''

    # Launch timer
    start_time = time.time()

    # Get settings from app and define key variables
    path_to_audio = settings['path_to_audio']
    filename = path_to_audio.rsplit('/')[-1].rsplit('.')[0]
    done = 0  # -> to 1 if transcription succeeds

    # Check if file needs conversion, convert if so
    conversion = 0
    if not path_to_audio.endswith('.wav'):
        from scripts.utils import convert_to_wav
        logger('...\nCONVERTING AUDIO TO .WAV FORMAT\
              \nLOKAL will save a temp audio file to the same folder as the original audio.\
              \nTo avoid this step, use .wav audios.')
        conversion = convert_to_wav(path_to_audio, filename)
        if conversion == 1:
            path_to_audio = path_to_audio.rpartition('/')[0] + '/' + filename + '-wavcopyforLOKALtranscription' + '.wav'
            logger('\n\n...\nAudio conversion succesful.\n\n')
        else:
            logger('\n\n...\nAudio conversion failed. To perform a transcription, save the audio in .wav format and try transcribing the .wav version.\n\n')

    if path_to_audio.endswith('.wav'):
        # Register context f(x)'s to redirect stdout and stderr to main app window
        f = WriteProcessor()
        g = WriteProcessor()

        # Launch transcription
        with redirect_stderr(f):
            with redirect_stdout(g):
                # Launch transcription
                try:
                    if settings['tcs_ok'] != True:  # Reject transcription T&Cs not agreed
                        print('...\nCannot proceed to transcription unless user agrees to terms and conditions.')
                    else:  # Proceed if user agreed to T&Cs
                        try:
                            print('...\nSTARTING TRANSCRIPTION...')
                            
                            if settings['approach'] != 'simple':
                                from scripts.lokal_transcribe import transcribe_complex
                                
                                if settings['approach'] == 'segmentation':
                                    HPs = {'min_duration_on': hps_param1.amountusedvar.get()/1000,
                                        'min_duration_off': hps_param2.amountusedvar.get()/1000}
                                else:
                                    HPs = {'min_duration_off': hps_param2.amountusedvar.get()/1000,
                                    'speaker_num': hps_param4.get()}
                                
                                result, done = transcribe_complex(settings, filename, HPs)
                            
                            else:
                                from scripts.lokal_transcribe import transcribe_simple
                                result, done = transcribe_simple(settings, filename)

                        # Error handling sucks, but idea is to delete temp folders
                        except Exception as e:
                            print('...\nTranscription failed. Error is:\n', e)
                            print('...\nAttempting to delete temporary folders.')
                            try:
                                delete_LOKAL_temp()
                            except:
                                print('Unable to find or delete temporary folders.\
                                    \nFor good health, check your "user" folder for a folder named "LOKAL_temp".\
                                    \nIf present, delete "LOKAL_temp" to avoid future errors.')

                    if conversion == 1:
                        from scripts.utils import delete_converted_wav
                        deletion_msg = delete_converted_wav(path_to_audio)
                        logger(deletion_msg)

                    # Check timer and pop message if transcription succeeds
                    if done == 1:
                        btn_run.configure(text='Run transcription',
                                          command=run)
                        log_free_run()
                        end_time = time.time()
                        execution_time = (end_time - start_time)
                        mm, ss = divmod(execution_time, 60)
                        hh, mm = divmod(mm, 60)
                        duration = f'{int(hh):02}:{int(mm):02}:{int(ss):02}'
                        victory_msg = f'\n...\n{result}\
                            \nExecution time: {duration}.\
                            \n\n...\nTHANK YOU FOR USING LOKAL!'
                        print(victory_msg)
                        return victory_msg
                except:
                    fail_msg = 'Transcription failed. Try a different model/approach.'
                    print(fail_msg)
                    return fail_msg


# Nice class to enable real-time logging for transcription.
# Massive thanks to for this beauty goes to:
#   https://stackoverflow.com/questions/71024919/how-to-capture-prints-in-real-time-from-function/71025286#71025286.
class WriteProcessor:
    def __init__(self):
        self.buf = ''

    def write(self, buf):
        # emit on each newline
        while buf:
            try:
                newline_index = buf.index('\n')
            except ValueError:
                # no newline, buffer for next call
                self.buf += buf
                break
            # get data to next newline and combine with any buffered data
            data = self.buf + buf[:newline_index + 1]
            self.buf = ''
            buf = buf[newline_index + 1:]
            # perform complex calculations... or just print with a note.
            logger(data)

    def flush(self):
        pass


# ---------------------
# MISC TKINTER ACTIONS
# ....
def browse_for_file(type_of_file):
    ''' F(x) pops window open for user to select files.
    '''
    
    if type_of_file == 'audio':
        filetypes = (
            ('common audio formats', ('*.wav', '*.mp3', '*.mp4', '*.m4a', '*.flac', '*.wma', '*.aac')),
            ('all files', '*.*'))
    else:
        filetypes = (
            ('text files', ('*.txt')),
            ('all files', '*.*'))

    path_to_file = filedialog.askopenfilename(filetypes=filetypes,
                                      initialdir=find_key_paths()[1])
    
    if path_to_file:
        if type_of_file == 'audio':
            settings['path_to_audio'] = path_to_file
        else:
            settings['path_to_prompt'] = path_to_file
        
        console_frame.delete('1.0', END)
        logger(f'...\nPath to selected {type_of_file} is: {path_to_file}.')
    else:
        if type_of_file == 'audio':
            settings['path_to_audio'] = ''
        else:
            settings['path_to_prompt'] = ''


def key_settings():
    ''' F(x) handles changes in the checkbox for
        - T&Cs
        - Timestamps
        - Compute type (cpu/gpu).
    ''' 
    settings['tcs_ok'] = tcs_ok.get()
    settings['timestamps_on'] = stamps_on.get()
    settings['gpu_on'] = gpu_on.get()


def family_choice(e):
    ''' F(x) handles changes in model family/provider selection.
    '''
    family = family_select.get().lower()
    settings['family'] = family.replace(':', '').replace(' ', '_')
    if family == 'openai: whisper':
        prompt_separator.pack(anchor='w', fill=X, pady=[21, 14])
        prompt_intro.pack(anchor='w', pady=0)
        prompt_select.pack(fill=X, pady=(1, 5), expand=True)
        model_select.config(value=[i.capitalize() for i in whisper])
        model_select.current(0)
        settings['model'] = model_select.get().lower()
        
    elif family == 'systran: faster whisper':
        prompt_select.forget()
        prompt_intro.forget()
        prompt_separator.forget()
        model_select.config(value=[i.capitalize() for i in fs_whisper])
        model_select.current(0)
        settings['model'] = model_select.get().lower()


def approach_choice(e):
    ''' F(x) handles changes in approach selection and triggers
        window resize to try and keep all app in view at all times.
    '''  # Could be merged, but it's only a few lines and I'm lazy

    approach = type_select.get()
    settings['approach'] = approach.lower()
    hparams(approach.lower())


def model_language_settings(e):
    ''' F(x) handles changes in model or language selection
    '''
    settings['model'] = model_select.get().lower()
    settings['language'] = lang_select.get().lower()


def hparams(approach):
    ''' F(x) updates hyper-parameters section of main app, per approach.
    '''
    if approach == 'simple':
        notify_frame.pack(fill=X, expand=TRUE, padx=48)
        hps_frame.forget()
    elif approach == 'segmentation':
        notify_frame.forget()
        hps_frame.pack(pady=3, anchor='w', fill=X, expand=True)
        segmentation_params.pack(anchor='n', pady=(14, 0), expand=True)
        diarisation_params.forget()
    elif approach == 'diarisation':
        notify_frame.forget()
        hps_frame.pack(pady=3, anchor='w', fill=X, expand=True)
        diarisation_params.pack(anchor='n', pady=(14, 0), expand=True)
        segmentation_params.forget()


def logger(text):
    ''' F(x) inserts any app generated updates to main app console.
        Ugliest function ever, but there is a need to be very careful 
        not to accidentally trigger an infinite loop if a transcribed
        line ends up having similar words/chars as progress bar updates.
    '''

    # The "console" on the GUI is not actually a "console"
    # One needs to take and put things into it as required

    # Annoying warnings that users do not need to see
    if 'torchaudio backend is switched to' in text\
        or 'torchvision is not available' in text\
            or 'HF_HUB_DISABLE_SYMLINKS_WARNING' in text:
        pass

    # Progress bars
    # ELIF is very case by case to avoid accidentally 
    # treating a real update as a progress bar update
    
    elif '%' in text: 
        
        # FASTER WHISPER DOWNLOADS
        if 'vocabulary.txt' in text\
            or 'tokenizer.json' in text\
                or 'config.json' in text\
                    or 'model.bin' in text: 
            
            # Flag last line of download intro
            # Hard flag possible: filenames unlikely elsewhere
            # Delete any lines after
            bool = True 
            while bool == True:
                console_frame.delete('end-1l', END)
                if console_frame.get("end-1c linestart", "end-1c lineend").startswith('Else, the model needs to download,'):
                    bool = False
            
            # Write the update
            if 'model.bin' in text:
                text = text.replace('\n', '').strip()
                text = f'\n\nDownloading...\n{text}'
                console_frame.insert(END, text)
            else:
                print('\n\nDownloading...\n')
        
        # pyannote's (RICH) BARS
        elif 'segmentation' in text\
            or 'embeddings'\
                or 'diarization' in text:
            console_frame.delete('end-2l', END)
            console_frame.insert('end', '\n{}'.format(text))

        # TREAT ANYTHING ELSE AS A NORMAL UPDATE
        # Better to render a progress bar badly than jam the log
        else:
            console_frame.insert(INSERT, text)
    else:
        console_frame.insert(INSERT, text)
    console_frame.see('end')


def pop_window(e, pop_type):
    ''' F(x) launches a new window containing terms and conditions.
    '''
    
    # Define type of window to pup up
    if pop_type == 'tcs':
        path_to_file = 'utils/apache_terms.txt'
        title_text = 'Terms & Conditions'
    elif pop_type == 'credits':
        path_to_file = 'utils/credits.txt'
        title_text = 'Credits'
    
    # Grab the contents to show
    content = open(resource_path(path_to_file), 'r').read()
    
    # Show them
    pop_root = tb.Toplevel()
    pop_root.iconbitmap(resource_path('images/icon.ico'))
    pop_root.title(title_text)
    pop_box = tb.ScrolledText(pop_root)
    pop_box.pack()
    pop_box.insert(END, content)
    pop_box.configure(state='disabled')


def pop_license(e):
    ''' F(x) launches a new window containing credits.
    '''

    help_us_help = "Get a code to activate all visual features and help us develop LOKAL and other open resources further by making a small voluntary payment."
    enter_invoice = 'After a payment is made, you will get an invoice. Enter your invoice number below to activate all visual features.'

    global license_root
    license_root = tb.Toplevel(title='Activation')
    license_root.iconbitmap(resource_path('images/icon.ico'))

    tb.Label(license_root,
        text='Help us help',
        justify='left',
        font='Helvetica 24 bold').pack(fill=X, padx=7, pady=[14,3])
    
    tb.Label(license_root,
             wraplength=400,
             text=help_us_help,
             justify='left').pack(fill=X, padx=7, pady=[0,3])

    license_get = tb.Button(license_root, 
                            bootstyle='success',
                            text='MAKE VOLUNTARY PAYMENT')
    license_get.pack(anchor='w', padx=7, pady=[0,7])
    license_get.bind('<Button-1>', lambda e: webbrowser.open('https://www.polyzentrik.com/help-us-help/'))

    tb.Label(license_root,
        text='Activation',
        justify='left',
        font='Helvetica 24 bold').pack(fill=X, padx=7, pady=[14,3])
    
    tb.Label(license_root,
             wraplength=400,
             text=enter_invoice,
             justify='left').pack(fill=X, padx=7, pady=[0,3])
    
    global license_box
    license_box = tb.Entry(license_root, bootstyle='success')
    license_box.pack(side=LEFT, padx=[7,0], pady=[3,14], anchor='e')

    license_save = tb.Button(license_root, bootstyle='dark', text='ACTIVATE')
    license_save.pack(side=LEFT, pady=[3,14], anchor='e')
    license_save.bind('<Button-1>', write_license)


def reset_models(e):
    ''' F(x) deletes models previously saved to local memory (./models).
    '''
    msg = 'Click OK to confirm deletion of transcription models.'
    confirm = messagebox.askokcancel(title='Reset models', message=msg)
    if confirm is True:
        for i in ['faster-whisper', 'whisper']:
            for j in os.listdir(f'./models/{i}'):
                if not j.startswith('README'):
                    print(j)
                    try:
                        shutil.rmtree(f'./models/{i}/{j}')
                    except:
                        try:
                            os.rmdir(f'./models/{i}/{j}')
                        except:
                            os.remove(f'./models/{i}/{j}')


def write_license(e):
    from scripts.boring import encrypt_and_write
    try:
        encrypt_and_write(license_box.get())
        license_root.destroy()
        popbox = messagebox.showwarning('showwarning', 'Please restart LOKAL.')
    except:
        print('ERROR: License not saved.')



def kill_everything():
    ''' F(x) is called if user closes or "Esc" LOKAL's main window.
        It helps delete TEMP folders and avoid exception cascades.
    '''

    # Update dark/light mode file for next launch
    no_style = open(
        resource_path('utils/view_mode.txt'), 'r').read().split(',')[1]
    with open(resource_path('utils/view_mode.txt'), 'w')as f:
        f.write('0,' + no_style)
        f.close()

    # Try to delete any TEMP folders created and not deleted otherwise
    print('Attempting a graceful exit.')
    try:
        path_to_temp_folder = find_key_paths()[0] + '/LOKAL_temp'
        try:
            print('Removing TEMP folders, if any.')
            shutil.rmtree(path_to_temp_folder)
        except:
            try:
                print('Removing TEMP folders, if any.')
                os.rmdir(path_to_temp_folder)
            except:
                print('Exiting.')
    except:
        print('Unable to exit gracefully.\
              \nCheck your "user" folder for a folder named "LOKAL_temp".\
              \nIf present, delete "LOKAL_temp" to avoid future errors.')
    finally:  # Ensure system close regardless
        app.destroy()
        sys.exit


# ---------------------
# TKINTER FUNKY FORMATS
# ...
def resize(e):
    ''' F(x) adjusts size of main window when there are changes to the height
        needed for the entire app to show without a need for scrolling.
        Target dimensions are tested against screen size,
        to avoid automatic resizing overflowing user screen.
    '''

    # Get screen height to know what we're working with
    max_h = int(app.winfo_screenheight() * 0.7)

    # Get width and height needed to render root in full
    root_w = root.winfo_width()
    root_h = root.winfo_height()

    # Choose min recommended height
    target_h = root_h if root_h < max_h else max_h

    # Apply dimensions without foreclosing room for user-driven resize
    app.geometry(f'{root_w}x{target_h}')


def toggle_mode():
    ''' F(x) is called when LOKAL launches or user toggle "view" mode
        The main bit takes current state and triggers change to opposite state.
        Relies on ./utils/view_mode.txt for launch shenanigans.
    '''

    # Initialise style
    style = app.style

    # Establish if app is launching and get current from file
    switch_flag, launch_style = open(
        resource_path('utils/view_mode.txt'), 'r').read().split(',')
    
    license_status = check_license()[0]
    if license_status == 0:
        style.theme_use('vapor')
        #spinbox_view_select.set('COLORS DISABLED')
        audio_select.config(bootstyle='light')
        console_frame.config(bg='yellow', foreground='white')
        audio_select.config(bootstyle='success')
        btn_run.config(bootstyle='warning, outline')
        btn_pay.config(bootstyle='secondary')
    elif license_status == 1:
        pass
        #spinbox_view_select.set('COLORS DISABLED')
    elif license_status == 2:
        # Set target style
        if switch_flag == '0':  # If just opened, use saved style
            target_style = launch_style
            my_theme.set(target_style)
            #spinbox_view_select.set(target_style.upper())
        else:  # Else, user is switching, use value from GUI
            target_style = my_theme.get()
            #target_style = spinbox_view_select.get().lower()

        # Switch from current to default or chosen mode
        s = tb.Style()
        if target_style == 'vapor' or target_style == 'darkly' or target_style == 'cyborg':
            style.theme_use(target_style)
            hps_param1.configure(bootstyle='success')
            hps_param2.configure(bootstyle='success')
            hps_param3.configure(bootstyle='success')
            hps_param4.configure(bootstyle='success')
            s.configure('custom.TButton', anchor='w', bordercolor='gray', background='#000', foreground='white', lightcolor='gray', darkcolor='gray')
            if target_style == 'cyborg':
                audio_select.config(bootstyle='light, outline')
                console_frame.config(bg='aquamarine', foreground='black')
                btn_run.config(bootstyle='light, outline')
                #btn_pay.config(bootstyle='light')
            elif target_style == 'vapor': 
                audio_select.config(bootstyle='light')
                console_frame.config(bg='black', foreground='white')
                btn_run.config(bootstyle='light')
                #btn_pay.config(bootstyle='light')
            else:
                audio_select.config(bootstyle='secondary')
                console_frame.config(bg='black', foreground='white')
                btn_run.config(bootstyle='secondary')
        else:
            style.theme_use(target_style)
            hps_param1.configure(bootstyle='dark')
            hps_param2.configure(bootstyle='dark')
            hps_param3.configure(bootstyle='dark')
            hps_param4.configure(bootstyle='dark')
            s.configure('custom.TButton', anchor='w', bordercolor='white', background='#fff', foreground='#555', lightcolor='gray', darkcolor='gray')
            if target_style == 'journal':
                audio_select.config(bootstyle='dark, outline')
                console_frame.config(bg='#222', foreground='white')
                btn_run.config(bootstyle='dark')
                #btn_pay.config(bootstyle='dark, outline')
            elif target_style == 'yeti':
                audio_select.config(bootstyle='primary')
                console_frame.config(bg='yellow', foreground='black')
                btn_run.config(bootstyle='primary')
                #btn_pay.config(bootstyle='primary')
            else:
                audio_select.config(bootstyle='primary')
                console_frame.config(bg='pink', foreground='black')
                btn_run.config(bootstyle='primary')
                #btn_pay.config(bootstyle='primary')
        
        prompt_select.configure(style='custom.TButton')

        # Update the utils file that keeps track of this view mode defaults
        with open(resource_path('utils/view_mode.txt'), 'w')as f:
            f.write('1,' + target_style)
            f.close()


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    app()
