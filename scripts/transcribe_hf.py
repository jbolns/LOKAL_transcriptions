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
# FOUNDATIONAL TRANSCRIPTION FUNCTION
# ...
def hf_flow(
    path_to_audio,
    family,
    model_size,
    language,
    gpu,
    mode,
    filename="",
    path_to_temp_folder=""
):
    """F(x) calls transcription model and writes result to TXT file"""
    
    # FUNCTION IMPORTS
    import os
    from scripts.utils import calc_total_chunks

    # NUMBER OF 30s AUDIO CHUNKS ACROSS ALL AUDIO
    path = path_to_temp_folder if mode == "loop" else path_to_audio
    calc_total_chunks(path, mode)

    # KEY SETTINGS FOR HF PIPELINE
    device, torch_dtype, model_id, processor = base(family, model_size, gpu, mode)

    # HF PIPELINE
    pipe = model_pipe(device, torch_dtype, model_id, processor, family)

    # TRANSCRIBE
    # Announce transcription
    print("[LKL|MSG] Transcribing.")

    # Create array with list of all audio segments (loop) or single path to audio (simple)
    audio_files = (
        [f"{path_to_temp_folder}/{f}" for f in os.listdir(path_to_temp_folder) if f.endswith("wav")]
        if mode == "loop"
        else [path_to_audio]
    )
 
    # Loop over audios in array, transcribe, and assemble result
    current = 1
    single_lang_models = ["distil-whisper_hf"]
    for file in audio_files:
        print(f"[LKL|VERBOSE] Transcribing audio segment {current} of {len(audio_files)}")
        try:
            # Transcribe segment
            if family not in single_lang_models and language.lower() != "auto":
                result = pipe(file, generate_kwargs={"language": language})
            else:
                result = pipe(file)

            # Assemble result
            segments = assemble_segments(result, mode)

            # Write segment to TXT file if working on a loop
            if mode == "loop":
                try:
                    with open(
                        f"{file[:-4]}.txt", "w"
                    ) as f:
                        f.write(segments)
                        f.close()
                except Exception:
                    pass
            current += 1
        except Exception as e:
            print(f"[LKL|MSG] Error transcribing: {e}")

    # Return segments (simple mode) or victory message (loop mode)
    return segments if mode != "loop" else f"[LKL|MSG] Finished transcription stage for {filename}"


# ---------------------
# ASSISTIVE FUNCTIONS
# ...
def base(family, model_size, gpu, mode):
    """Defines key settings for all pipelines"""
    
    # FUNCTION IMPORTS
    import torch
    from transformers import AutoProcessor, logging
    from scripts.assist import resource_path
    from scripts.utils import HF_MODEL_PREFIXES

    # ADJUST LOGGING SETTINGS TO ENABLE PROGRESS UPDATES IN TTKBOOTSTRAP
    if mode == "simple":
        logging.enable_explicit_format()
        logging.set_verbosity_info()    

    # SETTINGS
    device = "cuda:0" if gpu else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # PROCESSOR
    # Model location
    prefix = HF_MODEL_PREFIXES[family]
    suffix = ".en" if family == "distil-whisper_hf" else ""
    model_id = (
        f"{family.replace('_hf', '')}/{prefix}-{model_size}{suffix}"
        if model_size != "large"
        else f"{family.replace('_hf', '')}/{prefix}-{model_size}-v2"
    )
    
    # Fetch processor
    processor = AutoProcessor.from_pretrained(model_id, cache_dir=f"./models/{family}")
        
    # RETURN ALL
    return device, torch_dtype, model_id, processor


def model_pipe(device, torch_dtype, model_id, processor, family):
    """Defines the model and pipeline for, both, simple and looped transcriptions"""
    
    # FUNCTION IMPORTS
    from transformers import AutoModelForSpeechSeq2Seq, pipeline
    from scripts.assist import resource_path

    # MODEL
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        use_safetensors=True,
        cache_dir=resource_path(f"./models/{family}"),
    )
    model.to(device)

    # PIPELINE
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        stride_length_s=5,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )

    # RETURN PIPELINE
    return pipe


def assemble_segments(result, mode):
    """Writes transcription result to segments object (string or array)"""

    # DEFINE APPROPRIATE SEGMENTS TYPE GIVEN MODE
    segments = "" if mode == "loop" else []
    
    # WRITE SEGMENTS
    if mode == "loop":
        segments = result["text"]
    else:
        for line in result["chunks"]:
            segments.append({"start": line["timestamp"][0], "text": line["text"]})

    # RETURN SEGMENTS
    return segments


# ---------------------
# NAME:MAIN?
# ...
if __name__ == "__main__":
    pass
