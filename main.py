# -*- coding: utf-8 -*-
'''
v1. Jan 2024.
@author: Dr J. / Polyzentrik Tmi.

Save for a glorious class to enable real-time updates,
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

from scripts.assist import resource_path, find_key_paths, delete_LOKAL_temp
from scripts.utils import LANGUAGES


# ---------------------
# TKINTER BOOTSTRAP APP
# ...
def app():
    ''' F(x) launches main app for users to perform transcriptions
        and contains app's main loop.
    '''

    # SETTINGS AND HYPER-PARAMETERS DICTIONARIES
    global settings
    settings = {'filepath': '',
                'family': 'openai_whisper',
                'model': 'tiny',
                'type': 'simple',
                'language': 'AUTO',
                'terms': 0}

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

    configs_frame = tb.Frame(right_frame)
    configs_frame.pack(fill=X)

    params_frame = tb.Frame(lower_frame)
    params_frame.pack(pady=(14, 14), fill=X)

    run_frame = tb.Frame(lower_frame)
    run_frame.pack(fill=X)

    # UPPER FRAME (HEADER & MAIN SETTINGS)
    # Dark/light mode
    drk_lgt_var = tb.IntVar()
    global drk_lgt_toggle
    drk_lgt_toggle = tb.Checkbutton(top_frame,
                                    bootstyle='light, round-toggle',
                                    text='☀',
                                    variable=drk_lgt_var,
                                    onvalue=1,
                                    offvalue=0,
                                    command=toggle_mode)
    drk_lgt_toggle.pack(side=RIGHT, anchor='n')

    # Header
    lbl_title = tb.Label(title_frame,
                         text='LOKAL',
                         font='Helvetica 48 bold')
    lbl_title.pack(fill=X, expand=True)

    lbl_subtitle = tb.Label(title_frame,
                            text='Local AI transcriptions',
                            font='Courier 16 bold')
    lbl_subtitle.pack(fill=X, expand=True)

    lbl_company = tb.Label(title_frame,
                           text='www.polyzentrik.com',
                           bootstyle='info',
                           font='Courier 10 bold underline',
                           cursor='hand2')
    lbl_company.pack(expand=True, anchor='e')
    lbl_company.bind('<Button-1>',
                     lambda e: webbrowser.open('https://www.polyzentrik.com/'))

    global btn_audio_select
    btn_audio_select = tb.Button(title_frame,
                                 text='SELECT AUDIO',
                                 command=browse_for_file,
                                 bootstyle='dark, outline')
    btn_audio_select.pack(fill=X, pady=(21, 5), expand=True)

    global terms
    terms = tb.IntVar()
    check = tb.Checkbutton(title_frame,
                           text='I accept all ',
                           bootstyle='success',
                           variable=terms,
                           onvalue=1,
                           offvalue=0,
                           command=agree)
    check.pack(side=LEFT)

    lbl_company = tb.Label(title_frame,
                           text='terms & conditions',
                           font='Helvetica 8 underline',
                           cursor='hand2')
    lbl_company.pack(side=LEFT)
    lbl_company.bind('<Button-1>', pop_terms)

    # Main settings
    lbl_family_select = tb.Label(configs_frame,
                                 text='MODEL',
                                 font='Helvetica 8 bold')
    lbl_family_select.pack(anchor='w')

    families = ['OpenAI: Whisper', 'Systran: Faster Whisper']

    global whisper
    whisper = ['tiny', 'base', 'small', 'medium', 'large']
    global fs_whisper
    fs_whisper = ['tiny', 'base', 'small', 'medium', 'large']

    global dropdown_family_select
    dropdown_family_select = tb.Combobox(configs_frame, values=families)
    dropdown_family_select.pack()
    dropdown_family_select.current(0)
    dropdown_family_select.bind('<<ComboboxSelected>>', family_choice)

    global dropdown_model_select
    dropdown_model_select = tb.Combobox(configs_frame,
                                        values=[i.capitalize()
                                                for i in whisper])
    dropdown_model_select.pack()
    dropdown_model_select.current(0)
    dropdown_model_select.bind('<<ComboboxSelected>>', model_choice)

    lbl_type_select = tb.Label(configs_frame, text='APPROACH',
                               font='Helvetica 8 bold')
    lbl_type_select.pack(anchor='w', pady=[14, 0])

    types = ['simple', 'segmentation', 'diarisation']
    global dropdown_type_select
    dropdown_type_select = tb.Combobox(configs_frame,
                                       values=[i.capitalize()
                                               for i in types])
    dropdown_type_select.pack()
    dropdown_type_select.current(0)
    dropdown_type_select.bind('<<ComboboxSelected>>', type_choice)

    hps_lang_intro = tb.Label(configs_frame,
                              text='LANGUAGE',
                              font='Helvetica 8 bold')
    hps_lang_intro.pack(anchor='w', pady=[14, 0])

    langs = ['AUTO'] + sorted(LANGUAGES.keys())
    global dropdown_lang_select
    dropdown_lang_select = tb.Combobox(configs_frame,
                                       values=[i.title() for i in langs])
    dropdown_lang_select.pack()
    dropdown_lang_select.current(0)
    dropdown_lang_select.bind('<<ComboboxSelected>>', language_choice)

    # LOWER FRAME
    # Optional hyper-parameters
    global hps_frame
    hps_frame = tb.LabelFrame(params_frame, border=0)
    hps_frame.pack(pady=[0, 7], anchor='w', fill=X, expand=True)
    hps_frame.bind("<Configure>", resize)

    global segmentation_params
    segmentation_params = tb.Frame(hps_frame)

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

    global diarisation_params
    diarisation_params = tb.Frame(hps_frame)

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

    # Notifications
    global notifications_frame
    notifications_frame = tb.LabelFrame(params_frame, border=0)
    notifications_frame.pack(fill=X, expand=TRUE, padx=48)
    notifications_frame.bind("<Configure>", resize)

    global console_frame
    console_frame = tb.ScrolledText(notifications_frame, height=10, wrap=WORD)
    console_frame.config(bg='black', foreground='white')
    console_frame.pack(fill=X, expand=TRUE)

    # Run button (w. terms & conditions)
    global btn_run
    btn_run = tb.Button(run_frame, text='Run transcription',
                        command=run,
                        bootstyle='dark ')
    btn_run.pack(fill=X, anchor='w')

    global btn_pay
    btn_pay = tb.Button(run_frame, text='HELP US HELP',
                        bootstyle='dark, outline')
    btn_pay.pack(fill=X, pady=[3, 0], anchor='w')
    btn_pay.bind('<Button-1>',
                 lambda e: webbrowser.open('https://www.polyzentrik.com/help-us-help/'))

    lbl_credits = tb.Label(run_frame, text='Credits',
                           font='Helvetica 8',
                           cursor='hand2')
    lbl_credits.pack(side=LEFT, pady=3)
    lbl_credits.bind('<Button-1>', pop_credits)

    lbl_reset = tb.Label(run_frame, text='RESET MODELS',
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
    if settings['filepath'] == '':
        logger('\n\n...\nYou have not selected an audio file. You need to select an audio for a transcription to be possible.')
        popbox = messagebox.showwarning('showwarning', 'You have not selected an audio file. It is therefore impossible to proceed.')
    elif settings['terms'] == 0:
        logger('\n\n...\nYou have not accepted the terms and conditions. You need to accept the terms and conditions for a transcription to be possible.')
        popbox = messagebox.showwarning('showwarning', 'You have not accepted the terms and conditions. It is therefore impossible to proceed.')
    else:
        hps_frame.forget()
        notifications_frame.pack(fill=X, expand=TRUE, padx=48)
        console_frame.delete('1.0', END)
        app.update()
        try:
            transcription_thread = threading.Thread(target=run_transcription,
                                                    daemon=True)
            transcription_thread.start()
        except Exception as e:
            logger(f'...\nTranscription thread has failed. Error is... {e}')


def run_transcription():
    ''' F(x) organises the transcription flow.
    '''

    # Launch timer
    start_time = time.time()

    # Get settings from app and define key variables
    path, family, model, approach, language, agree = list(settings.values())
    name = path.rsplit('/')[-1].rsplit('.')[0]
    done = 0  # -> to 1 if transcription succeeds

    # Register context f(x)'s to redirect stdout and stderr to main app window
    f = WriteProcessor()
    g = WriteProcessor()

    # Launch transcription
    with redirect_stderr(f):
        with redirect_stdout(g):
            # Launch transcription
            try:
                if agree != 1:  # Reject transcription T&Cs not agreed
                    print('...\nCannot proceed to transcription unless user agrees to terms and conditions.')
                elif agree == 1:  # Proceed if user agreed to T&Cs

                    # If all goes well, mostly everything happens in this try
                    try:
                        print('...\nSTARTING TRANSCRIPTION.\
                            \nRemember, LOKAL is made for comfort, not speed.\
                            \nBe patient!')
                        if approach == 'simple':
                            from scripts.simple import transcribe_simple
                            result, done = transcribe_simple(path, name, family, model, language)
                        if approach == 'segmentation':
                            from scripts.segmentation\
                                import transcribe_segmentation
                            HPs = {'min_duration_on': hps_param1.amountusedvar.get()/1000,
                                   'min_duration_off': hps_param2.amountusedvar.get()/1000}
                            result, done = transcribe_segmentation(path, name, family, model, language, HPs)
                        if approach == 'diarisation':
                            from scripts.diarisation\
                                import transcribe_diarisation
                            HPs = {'min_duration_off': hps_param2.amountusedvar.get()/1000,
                                   'speaker_num': hps_param4.get()}
                            result, done = transcribe_diarisation(path, name, family, model, language, HPs)

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

                # Exception in theory never triggered
                else:
                    print('...\nUnknown error.')

                # Check timer and pop message if transcription succeeds
                if done == 1:
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
def browse_for_file():
    ''' F(x) pops window open for user to select files.
    '''
    path_to_open = find_key_paths()[1]
    filetypes = (('wav files', '*.wav'), ('all files', '*.*'))
    audio_file = filedialog.askopenfilename(filetypes=filetypes,
                                            initialdir=path_to_open)
    if audio_file:
        settings['filepath'] = audio_file
        logger(f'\n\n..\nPath to audio is: {audio_file}.\
               \nPlease double check.')
    else:
        settings['filepath'] = ''


def family_choice(e):
    ''' F(x) handles changes in model family/provider selection.
    '''
    family = dropdown_family_select.get().lower()
    settings['family'] = family.replace(':', '').replace(' ', '_')
    if family == 'openai: whisper':
        dropdown_model_select.config(value=[i.capitalize()
                                            for i in whisper])
        dropdown_model_select.current(0)
        settings['model'] = dropdown_model_select.get().lower()
    elif family == 'systran: faster whisper':
        dropdown_model_select.config(value=[i.capitalize()
                                            for i in fs_whisper])
        dropdown_model_select.current(0)
        settings['model'] = dropdown_model_select.get().lower()


def agree():
    ''' F(x) handles changes in the checkbox for agreeing to T&Cs.
    '''  # Could be merged, but it's only a few lines and I'm lazy
    settings['terms'] = terms.get()


def model_choice(e):
    ''' F(x) handles changes in model selection
    '''  # Could be merged, but it's only a few lines and I'm lazy
    settings['model'] = dropdown_model_select.get().lower()


def language_choice(e):
    ''' F(x) handles changes in language selection
    '''  # Could be merged, but it's only a few lines and I'm lazy
    settings['language'] = dropdown_lang_select.get().lower()


def type_choice(e):
    ''' F(x) handles changes in approach selection and triggers
        window resize to try and keep all app in view at all times.
    '''  # Could be merged, but it's only a few lines and I'm lazy
    type = dropdown_type_select.get()
    settings['type'] = type.lower()
    hparams(type.lower())


def hparams(approach):
    ''' F(x) updates hyper-parameters section of main app, per approach.
    '''
    if approach == 'simple':
        notifications_frame.pack(fill=X, expand=TRUE, padx=48)
        hps_frame.forget()
    elif approach == 'segmentation':
        notifications_frame.forget()
        hps_frame.pack(pady=3, anchor='w', fill=X, expand=True)
        segmentation_params.pack(anchor='n', pady=(14, 0), expand=True)
        diarisation_params.forget()
    elif approach == 'diarisation':
        notifications_frame.forget()
        hps_frame.pack(pady=3, anchor='w', fill=X, expand=True)
        diarisation_params.pack(anchor='n', pady=(14, 0), expand=True)
        segmentation_params.forget()
    else:
        pass


def logger(text):
    ''' F(x) inserts any app generated updates to main app console.
        Ugliest function ever, but there is a need to be very careful 
        not to accidentally trigger an infinite loop if a transcribed
        line ends up having similar words/chars as progress bar updates.
    '''

    # FUN STORY
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


def pop_terms(e):
    ''' F(x) launches a new window containing terms and conditions.
    '''  # Obviously, could be merged, too. Some day.
    apache_terms = open(resource_path('utils/apache_terms.txt'), 'r').read()
    terms_root = tb.Window()
    terms_root.title('Terms & Conditions')
    terms_box = tb.ScrolledText(terms_root)
    terms_box.pack()
    terms_box.insert(END, apache_terms)
    terms_box.configure(state='disabled')


def pop_credits(e):
    ''' F(x) launches a new window containing credits.
    '''  # Obviously, could be merged, too. Some day.
    credits = open(resource_path('utils/credits.txt'), 'r').read()
    credits_root = tb.Window()
    credits_root.title('Credits')
    credits_box = tb.ScrolledText(credits_root)
    credits_box.pack()
    credits_box.insert(END, credits)
    credits_box.configure(state='disabled')


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
    target_h = root_h if root_h <= max_h else max_h

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
    launch_flag, not_default_view = open(
        resource_path('utils/view_mode.txt'), 'r').read().split(',')

    # Set current to opposite
    if launch_flag == '1':
        current_style = style.theme.name
    else:  # If first paint, set current to opposite of default
        current_style = not_default_view
        with open(resource_path('utils/view_mode.txt'), 'w')as f:
            f.write('1,' + not_default_view)
            f.close()

    # Switch from current to default or chosen mode
    if current_style == 'journal':
        style.theme_use('darkly')
        btn_audio_select.config(bootstyle='light')
        console_frame.config(bg='black', foreground='white')
        btn_run.config(bootstyle='light, outline')
        btn_pay.config(bootstyle='light')
        hps_param1.configure(bootstyle='success')
        hps_param2.configure(bootstyle='success')
        hps_param3.configure(bootstyle='success')
        hps_param4.configure(bootstyle='success')
        # Update the utils file that keeps track of this view mode defaults
        with open(resource_path('utils/view_mode.txt'), 'w')as f:
            f.write('1,' + 'journal')
            f.close()
    else:
        style.theme_use('journal')
        btn_audio_select.config(bootstyle='dark, outline')
        console_frame.config(bg='#222', foreground='white')
        btn_run.config(bootstyle='dark')
        btn_pay.config(bootstyle='dark, outline')
        hps_param1.configure(bootstyle='dark')
        hps_param2.configure(bootstyle='dark')
        hps_param3.configure(bootstyle='dark')
        hps_param4.configure(bootstyle='dark')
        # Update the utils file that keeps track of this view mode defaults
        with open(resource_path('utils/view_mode.txt'), 'w')as f:
            f.write('1,' + 'darkly')
            f.close()


# ---------------------
# NAME:MAIN?
# ...
if __name__ == '__main__':
    app()
