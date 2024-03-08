# LOKAL (transcriptions)
LOKAL offers an user-friendly way to perform AI transcriptions locally on regular devices, including personal computers. Output quality is comparable with many on-cloud alternatives.

## Why/when to use LOKAL?
Interviews, focus groups, statements, and other oral stories can hold biometric data, personal identifiable information (PII), and sensitive details. The risks of sharing such data with untrusted 3rd parties is significant, including a potential for audio "deepfakes".

If necessary consents, safeguards, and a trusted provider are in place, you might not need LOKAL. Otherwise, consider using LOKAL. 

LOKAL runs locally on your computer.[^1] It can avoid you the need to send audios out.

## Installation (no coding required)
If you want to save time, use the standalone version of LOKAL.

Simply... 
1. Download the executable (.exe) installation file available [here](https://github.com/jbolns/LOKAL_transcriptions/releases).
2. Double-click.
3. Install.
4. Use

> *Note.* Some (but not all) features require [FFmpeg](https://www.ffmpeg.org/). 
> * If you do not have FFmpeg and wish to install it, guidance is available [here](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).
> * If you do not have FFmpeg and do not want to install it, you can still use LOKAL by sticking to *.wav* audios and Systran/faster-whisper models.

## Alternative OPTIONAL Python installation (coding required)
See section at the end of this README. It was scaring people.

Please note, this **OPTIONAL** approach is REALLY hard.

## Using LOKAL
Below all choices users can make while using LOKAL. It's a long list, but once you open the app you'll see they're all presented fairly clearly.

### Required selections:

#### Audio selection
* *Select audio.* Press select audio to choose the audio to transcribe. 
  * Currently, only *.wav* files are supported. If you do not see your audio, make sure it's in *.wav* format.

#### T&Cs
* *Terms and conditions.* Use the checkbox to agree to the terms and conditions of usage.
  * Click on the link to read terms and conditions.
  * Agree to terms and conditions using the checkbox.

#### Model
* *Model (family).* Use the dropwodn to choose the family of models to use for transcription.
  * Currently, LOKAL offers two model families, OpenAI's Whisper and Systran's take on Whisper, called "faster-whisper".
  * OpenAI's Whisper requires FFmpeg. Systran's Faster Whisper does not.
  * The goal is to add more options.
* *Model (size).* Use the dropdown to specify the model size to use for transcription.
  * Models come in different sizes. The larger the model, the better the output. The larger the model, the longer the transcription takes.
  * Rule of thumb. If you can understand the conversation easily, one of the smaller models might be enough.

#### Approach
* *Approach.* Use the dropdown to choose between three different approaches to transcription, meant for different types of conversations.
  * *Simple.* A straightforward word-by-word transcription. Best for complex/dynamic conversations with many speakers and interruptions, where it is very difficult to track of all speaker changes.
  * *Segmentation.* A transcription split into paragraphs roughly following pauses and changes of speakers. Best for semi-structured conversations like interviews and focus groups, where tracking speaker changes is easier.
  * *Diarisation.* A transcription split into blocks roughly corresponding to segments by specific speakers (with speaker labels). Best for structured conversations where speakers have clear turns and speaker changes are clear, like panels or seminars.

#### Language:
* *Language.* Use the dropdown to select the language for transcription.
  * If left blank, the model tries to identify the language by itself. 
  * Specifying the language might make it easier for the model and speed things a little.

### Optional selections:
Optional hyper-parameters will be shown as available depending on the combination of required parameters selected by the user.
* *Ignore short segments.* Use the meter to set a threshold to ignore short words/comments, like fillers or interruptions.
  * If treshold is too high, it might ignore parts of sentences before/after pauses.
* *Ignore short pauses.* Use the meter to set a threshold to ignore short pauses that might cause excessive paragraph breaks in the final transcript.
  * If too high, the models might ignore legitimate changes between speakers.
* *Number of speakers*. Enter the exact number of speakers involved in a conversation. 
  * The diarisation model can try and guess the number of speakers, but it tends to do better if said number is given clearly from the outset.

## Known limitations
LOKAL aims to assist humans with preparatory tasks rather than replace humans. Reducing the costs and time of initial speech-to-text conversion allows users to assign more resources on editing. 

For the same reason, users remain in control and are responsible for the final quality of transcriptions. Users should therefore keep in mind all AI models and systems have limitations.

LOKAL's limitations include but are not limited to:
* All models may present potentially high error rates.
* The segmentation and diarisation approaches and models used in these approaches can struggle with overlapping speakers.
* The transcription models can struggle with names, places, acronyms, and potentially, accents. Users must not use outputs without editing them.
* The transcription models can struggle with conversations taking place in different languages – an idea is to do multiple runs with different language selections and then join the results.

## Maximising privacy
LOKAL is not a guarantee of privacy. As per the license terms, you agree the software is offered with no guarantees whatsoever. 

That said, LOKAL can help you maximise privacy in several ways:
* LOKAL avoids you the need to send audios to third-party service providers. Not to say you should never use said services. There is a time and place for everything. Sometimes, however, keeping things LOKAL might be a good idea, especially if dealing with sensitive or easily identifiable audios.
* LOKAL allows you to run transcriptions offline. There is a need to run a few mock transcriptions while online to trigger the download of models. After your chosen models have downloaded, however, you can disconnect from the Internet and everything should works just fine.
* If you need or want maximal privacy, you can also copy LOKAL's installation (LOKAL installs to *'~/<-username->/AppData/Local/Programs/LOKAL'*) to an island computer **after** triggering the download of models.

## Having troubles?
We made LOKAL as easy to install and use as possible. That said, if you're really, really stuck, get in touch: hello@polyzentrik.com. 

We won't charge you for a quick consultation.

## License
LOKAL (transcriptions) is a product by [polyzentrik.com](https://www.polyzentrik.com/), released under an Apache 2.0 open source license.

We ask you to [make a small voluntary payment via our website](https://www.polyzentrik.com/help-us-help/) if you are using LOKAL for paid, funded, commercial, or profitable research, non-governmental, governmental, or business activities. The suggested amount is €3 per hour of audio or €60 per user per year, whichever is lower. Organisations are welcome to get in touch for multi-user sponsorships. Students need not to worry.

.

## OPTIONAL Python installation (coding required)
**Skip this section if not a coder. It is REALLY hard.**

You can also use LOKAL as a pure Python app. Assuming you have Python (3.11.0) installed on your computer, you need to:
1. Clone this repository.
   * The *main* branch has the latest released version.
   * The *dev* branch has latest commits, to be shipped on next release.
   * For guidance, see https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository and https://stackoverflow.com/questions/1778088/how-do-i-clone-a-single-branch-in-git.
2. Create an environment around it.
   * For guidance, see https://docs.python.org/3/library/venv.html.
3. Install required libraries using *<u>pip install -r requirements.txt</u>*.
   * For guidance, see https://pip.pypa.io/en/stable/user_guide/.
4. Check [this file](./utils/changelog_python_libs.md) for some tiny but necessary library adjustments needed for progress bars to render.
5. Run LOKAL using *<u>python lokal.py</u>* or *<u>python -m lokal</u>*.
   * For guidance, see https://pythonbasics.org/execute-python-scripts/.

> *Note.* Some (but not all) features require [FFmpeg](https://www.ffmpeg.org/). 
> * If you do not have FFmpeg and wish to install it, guidance is available [here](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/). Alternatively, ffmpeg-python (*pip install ffmpeg-python*) might do the trick.
> * If you do not have FFmpeg and do not want to install, you can still use LOKAL by sticking to *.wav* audios and Systran/faster-whisper models.

.

.

.

---

**Footnotes**

[^1]: An Internet connection is needed for initial model download. The first time you choose a model, the model downloads. After, it is possible to perform transcriptions offline. Resetting models is possible from within LOKAL, which deletes all models in memory and forces a re-download next time a model is used.