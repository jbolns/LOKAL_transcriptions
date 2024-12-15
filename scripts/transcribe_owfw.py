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
# TRANSCRIPTION FLOW
# ...
def flow(
    path_to_audio,
    family,
    model_size,
    language,
    gpu,
    mode,
    path_to_prompt="",
    filename="",
    path_to_temp_folder="",
):
    """F(x) calls transcription model and writes result to TXT file"""

    # FUNCTION IMPORTS
    import os
    from scripts.assist import resource_path

    if family == "systran":
        from faster_whisper import WhisperModel
    else:
        import whisper

    # PROMPT
    if path_to_prompt != "":
        with open(path_to_prompt, "r") as f:
            prompt = f.read()
    else:
        prompt = "This prompt is a fallback, with a comma."

    # MODEL
    if family == "systran":
        model = WhisperModel(
            model_size,
            device="cpu" if gpu is False else "cuda",
            compute_type="int8" if gpu is False else "float16",
            download_root=resource_path(f"./models/{family}"),
        )
    else:
        model = whisper.load_model(
            model_size, download_root=resource_path(f"./models/{family}")
        )

    # TRANSCRIPTION
    # Announce transcription
    print("[LKL|MSG] Transcribing.")

    # Create array with list of all audio segments (loop) or single path to audio (simple)
    audio_files = (
        [
            f"{path_to_temp_folder}/{f}"
            for f in os.listdir(path_to_temp_folder)
            if f.endswith("wav")
        ]
        if mode == "loop"
        else [path_to_audio]
    )

    # Loop over audios in array, transcribe, and assemble result
    current_track = 1
    for file in audio_files:
        print(f"[LKL|VERBOSE] Audio segment {current_track} of {len(audio_files)}\n")
        current_track += 1
        try:
            segments = base(file, language, gpu, model, mode, prompt, family)

            # Write segment to TXT file if working on a loop
            if mode == "loop":
                try:
                    with open(f"{file[:-4]}.txt", "w") as f:
                        f.write(segments)
                        f.close()
                except Exception:
                    pass

        except Exception as e:
            print(f"[LKL|MSG] Error transcribing: {e}")

    # Return segments (simple mode) or victory message (loop mode)
    return (
        segments
        if mode != "loop"
        else f"[LKL|MSG] Finished transcription stage for {filename}"
    )


# ---------------------
# ASSISTIVE FUNCTIONS
# ...
def base(path_to_audio, language, gpu, model, mode, prompt, family):
    """F(x) calls Faster Whisper on an audio."""

    # FUNCTION IMPORTS
    from scripts.utils import LANGUAGES
    
    # TRANSCRIBE
    if language.lower() == "auto":
        if family == "systran":
            result, _ = model.transcribe(
                path_to_audio, beam_size=3 if gpu is False else 5, vad_filter=True
            )
        else:
            result = model.transcribe(
                path_to_audio, initial_prompt=prompt, fp16=gpu, verbose=True
            )
    else:
        if family == "systran":
            result, _ = model.transcribe(
                path_to_audio,
                beam_size=3 if gpu is False else 5,
                vad_filter=True,
                language=LANGUAGES[language],
            )
        else:
            result = model.transcribe(
                path_to_audio,
                initial_prompt=prompt,
                language=language,
                fp16=gpu,
                verbose=True,
            )
            
    if family != "systran":
        segments = result["text"] if mode == "loop" else result["segments"]
    else:
        segments = "" if mode == "loop" else []
        for line in result:
            print("[LKL|VERBOSE]", line.text)
            if mode == "loop":
                segments = segments + line.text
            else:
                segments.append({"start": line.start, "text": line.text})

    return segments

# ---------------------
# NAME:MAIN?
# ...
if __name__ == "__main__":
    pass
