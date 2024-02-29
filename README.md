# LOKAL (transcriptions)
LOKAL offers an user-friendly way to perform AI transcriptions locally on regular devices, including personal computers. Output quality is comparable with many on-cloud alternatives.

## Why/when to use LOKAL?
Interviews, focus groups, statements, and other oral stories can hold biometric data, personal identifiable information (PII), and sensitive details. The risks of sharing such data with untrusted 3rd parties is significant, including a potential for audio "deepfakes".

If necessary consents, safeguards, and a trusted provider are in place, you might not need LOKAL. Otherwise, consider using LOKAL. 

LOKAL runs locally[^1] on your computer. It can avoid you the need to send audios out.[^2]

## Installation (for non-coders)
Use the standalone version of LOKAL if you do not have Python installed on your computer.

Simply... 
1. Download the executable (.exe) installation file available [here](https://github.com/jbolns/LOKAL_transcriptions/releases).
2. Double-click.
3. Install.
4. Use

> *Note.* Currently, audios need to be in .wav format. If you need to convert audios, many audio software can handle this transcription easily (we like VLC).

> *Note.* Some (not all) models require [FFmpeg](https://www.ffmpeg.org/). If you do not have FFmpeg, stick to the "Systran" family (you'll see it in the dropdowns) or install FFmpeg. Guidance for setting up FFmpeg is available [here](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).

## Installation (for coders) (skip if you are not a coder - this is hard)
You can also use LOKAL as a pure Python app.
1. Clone this repository.
2. Create an environment to install all required libraries.
3. Install required libraries using *<u>pip install requirements.txt</u>*.
4. Run LOKAL using *<u>python lokal.py</u>* or *<u>python -m lokal</u>*.

> *Note.* Some (not all) models require [FFmpeg](https://www.ffmpeg.org/). If you do not have FFmpeg, stick to the "Systran" family (you'll see it in the dropdowns) or install FFmpeg. Guidance for setting up FFmpeg is available [here](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).

> *Note.* A little debugging might be needed. Many libraries are involved, which can cause some friction. Additionally, for progress bars to render to GUI, small library adjustments are needed. See [this file](./utils/changelog_python_libs.md) for details.

## Using LOKAL
Below a guide of options given by LOKAL. 

Read this section after or while looking at this [image](https://repository-images.githubusercontent.com/764310700/c6dd971d-ca0a-4d23-b735-669baae54b77). LOKAL gives users MANY options, which can sound intimidating. However, using LOKAL is as easy as clicking on dropdowns and selecting options.

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

## Having troubles?
If you find the installation hard, take a deep breath and remember, LOKAL brings AI directly to your computer. We made it as easy to install as possible, but it's understandable if you struggle a little.

Try again. And if you're really, really stuck, get in touch: hello@polyzentrik.com. 

We won't charge you for a quick set up consultation.

.

If you run into troubles when using LOKAL, take a deep breath and remember, LOKAL brings AI directly to your computer. It's bound to error sometimes. 

Try again. And if you're really, really stuck, get in touch: hello@polyzentrik.com. 

We won't charge you for a quick usage question.

## License
LOKAL (transcriptions) is a product by [polyzentrik.com](https://www.polyzentrik.com/), released in its current version 1.0.0-alpha under an Apache 2.0 open source license.

We ask you to [make a small voluntary payment via our website](https://www.polyzentrik.com/help-us-help/) if you are using LOKAL for paid, funded, commercial, or profitable research, non-governmental, governmental, or business activities. It would help us develop LOKAL further. The suggested amount is €3 per hour of audio or €90 per user per year, whichever is lower. Organisations are welcome to get in touch for multi-user sponsorships.

That said, the software is yours to use at the lowest cost point needed to achieve your goals while reducing risk exposure. Also, students need not to worry.

---

**Footnotes**

[^1]: An Internet connection is needed for initial model download. The first time you choose a model, the model downloads. After, it is possible to perform transcriptions offline. Resetting models is possible from within LOKAL, which deletes all models in memory and forces a re-download next time a model is used.

[^2]: As per the license, no guarantees are offered. This includes privacy. The developer is reasonably convinced that LOKAL reduces privacy risks, but related guarantees are beyond what is currently possible. If you need to maximise privacy, run a few mock transcriptions on a computer connected to the Internet to trigger the download of any necessary models, then copy LOKAL's installation to an offline computer and run transcriptions there without connecting that computer to the Internet, ever. If you go this way, it may be worth remembering that LOKAL's standalone distribution installs to *'~/<-username->/AppData/Local/Programs/LOKAL'*, whereas the Python distribution installs to wherever you choose to save it.


