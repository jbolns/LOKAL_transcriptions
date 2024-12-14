# -*- coding: utf-8 -*-
"""
v2. Nov 2024.
@author: J.

LOKAL sticks to a functional programming paradigm.
Any classes must be justified exceptionally well.

Copyright (c) 2023 Jose A Bolanos.
SPDX-License-Identifier: Apache-2.0

"""

# ---------------------
# TOP-LEVEL IMPORTS
# ...
import os
import datetime
from scripts.assist import resource_path, split_audio, together, write_out


# ---------------------
# MAIN TRANSCRIPTION FLOW
# ...
def transcription_flow(settings, filename, HPs={}):
    """F(x) calls transcription model and writes result to TXT file"""

    # FUNCTION IMPORTS
    import shutil
    from scripts.transcribe_hf import hf_flow
    from scripts.transcribe_owfw import flow
    from scripts.utils import create_temp_folder

    # EXTRACT SETTINGS INTO INDEPENDENT VARS
    (
        path_to_audio,
        path_to_prompt,
        family,
        model_size,
        approach,
        language,
        timestamps,
        gpu,
        tcs,
    ) = list(settings.values())
    path_to_output_file = os.path.dirname(path_to_audio) + "/" + filename + ".txt"

    # OPERATIONS NEEDED FOR SEGMENTATION OR DIARISATION
    if approach != "simple":

        # Folder for temp audios and partial transcriptions
        path_to_temp_folder = create_temp_folder()

        # Transcription mode
        mode = "loop"

        # Segment || diarise as appropriate
        if approach == "segmentation":
            print("[LKL|MSG] Segmenting audio.\n")
            segmentation(path_to_audio, filename, path_to_temp_folder, HPs)
        elif approach == "diarisation":
            print("[LKL|MSG] Diarising audio.\n")
            diarisation(path_to_audio, filename, path_to_temp_folder, HPs)

        # Split audio according to segmentation || diarisation
        CHUNKS = split_audio(path_to_audio, filename, path_to_temp_folder, approach)

    else:
        # Placeholder for temp folder
        path_to_temp_folder = ""

        # Transcription mode
        mode = "simple"

    # TRANSCRIPTION
    print("[LKL|MSG] Loading (Internet needed if model NOT already on local memory).")

    # Any models using HF pipeline
    if "_hf" in family:
        segments = hf_flow(
            path_to_audio,
            family,
            model_size,
            language,
            gpu,
            mode,
            filename,
            path_to_temp_folder,
        )
    # Whisper & Faster Whisper
    else:
        segments = flow(
            path_to_audio,
            family,
            model_size,
            language,
            gpu,
            mode,
            path_to_prompt,
            filename,
            path_to_temp_folder,
        )

    # WRITE TRANSCRIPTION TO FILE
    if approach == "simple":
        print("[LKL|MSG] Writing final transcript.\n")
        with open(path_to_output_file, "w") as f:
            for segment in segments:
                start_timestamp = str(datetime.timedelta(seconds=int(segment["start"])))
                content = segment["text"]
                if timestamps is True:
                    line = f"[{start_timestamp}] {content}"
                else:
                    line = f"{content}"
                try:
                    f.write(f"{line.strip()}\n")
                except Exception:
                    f.write("!------ LINE IS MISSING --------!")
            f.close()
    else:
        # Join speaker chunks and transcribed content
        print("[LKL|MSG] Joining segments transcriptions")
        LINES = together(path_to_temp_folder, CHUNKS)

        # Write transcript into final TXT file
        print("[LKL|MSG] Writing final transcript.\n")
        write_out(path_to_output_file, filename, LINES, approach, timestamps)

    # Remove temp files and directory
    # Ps1. Folder/files not always created, but deleting always to avoid issues
    # Ps2. If deletion failure, transcription still be feasible in most cases
    try:
        try:
            shutil.rmtree(path_to_temp_folder)
        except Exception:
            os.rmdir(path_to_temp_folder)
    except Exception:
        pass

    # DECLARE VICTORY
    return (
        f"Finished transcribing: {filename}. Find it on the same folder as your audio.",
        1,
    )


# ---------------------
# SEGMENTATION FUNCTION
# ...
def segmentation(path_to_audio, filename, path_to_temp_folder, HPs):
    """F(x) calls Pyannote and writes result to temporary TXT file."""

    # Function imports
    from pyannote.audio import Model
    from pyannote.audio.pipelines import VoiceActivityDetection
    from pyannote.audio.pipelines.utils.hook import ProgressHook

    # Load segmentation model
    model_location = "models/segmentation/pytorch_model.bin"
    model = Model.from_pretrained(resource_path(model_location))
    pipeline = VoiceActivityDetection(segmentation=model)

    # Define hyper-parameters for model
    PARAMS = {
        "min_duration_on": HPs["min_duration_on"],  # ignore short speech regions
        "min_duration_off": HPs["min_duration_off"],
    }  # fill non-speech regions

    # Run model
    pipeline.instantiate(PARAMS)
    with ProgressHook() as hook:
        segments = pipeline(path_to_audio, hook=hook)

    # Save segments to temp TXT file
    L = []
    for turn, _ in segments.itertracks():
        L.append([turn.start - 0.4, turn.end - 0.4])

    # Write segments to temporary file
    with open(path_to_temp_folder + "/" + "temp-segments.txt", "w") as f:
        for line in L:
            f.write(str(line[0]) + ", " + str(line[1]) + "\n")
        f.close()

    # Return segments
    return f"[LKL|MSG] Finished segmentation of {filename}"


# ---------------------
# DIARISATION FUNCTION
# ...
def diarisation(path_to_audio, filename, path_to_temp_folder, HPs):
    """F(x) performs diarisation using pyannote.
    It writes result to temporary TXT file.
    """

    # Import necessary libraries
    from pyannote.audio import Model
    from pyannote.audio.pipelines import SpeakerDiarization as Pipeline
    from pyannote.audio.pipelines.utils.hook import ProgressHook

    # Initialise models
    seg_model_loc = "models/segmentation/pytorch_model.bin"
    emb_model_loc = "models/embedding/pytorch_model.bin"
    segmentation_model = Model.from_pretrained(resource_path(seg_model_loc))
    embedding_model = Model.from_pretrained(resource_path(emb_model_loc))
    pipeline = Pipeline(segmentation=segmentation_model, embedding=embedding_model)

    # Set hyper-parameters
    PARAMS = {
        "segmentation": {
            "min_duration_off": HPs["min_duration_off"]
        },  # fill non-speech regions
        "clustering": {
            "method": "centroid",
            "min_cluster_size": 12,
            "threshold": 0.7045654963945799,
        },
    }

    # Run model
    pipeline.instantiate(PARAMS)
    if HPs["speaker_num"] == "AUTO":
        with ProgressHook() as hook:
            diarization = pipeline(path_to_audio, hook=hook)
    else:
        with ProgressHook() as hook:
            diarization = pipeline(
                path_to_audio, speaker_num=int(HPs["speaker_num"]), hook=hook
            )

    with open(path_to_temp_folder + "/" + "temp-diary.txt", "a") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.writelines(f"{turn.start}, {turn.end}, {speaker}\n")
        f.close()

    return f"[LKL|MSG] Finished segmentation of {filename}"


# ---------------------
# NAME:MAIN?
# ...
if __name__ == "__main__":
    pass
