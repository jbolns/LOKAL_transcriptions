# LOKAL (transcriptions)
LOKAL is a user-friendly application to do AI transcriptions locally (i.e. on your own computer).
* **Low cost.** Payment is voluntary, and very small.
* **High quality.** Quality is on-par with on-cloud alternatives.
* **Multiple model providers.** LOKAL gives users the option to choose between several model providers (supports compatibility and avoids supplier lockdown)
* **Privacy-aware.** LOKAL avoids the need to send audio data to third parties and it is possible to do transcriptions offline.[^1]
* **Open-source.** Commercial use is allowed. 

## Why/when to use LOKAL?
There are many situations where LOKAL can be advantageous. 

* **In research projects.**
  * Interviews, focus groups, statements, and other oral stories can hold biometric data, personal identifiable information (PII), and sensitive details. The risks of sharing such data with untrusted 3rd parties is significant, including a potential for audio "deepfakes".
  * LOKAL runs locally on your computer, which can help you manage the risk of these details leaking accidentally.
* **In places with complex data privacy regulations (e.g. GDPR).**
  * Do you know how a third-party transcription provider handles audio data? Do you have full information about how many servers are involved, where, and for how long each server stores audios or transcriptions, or if and to what extent usage or audio statistics are logged? Moreover, have your users/participants consented to all of this? 
  * Since LOKAL works directly on your computer, LOKAL might help you simplify compliance.[^2]
* **When audios contain sensitive or strategic information.**
  * LOKAL downloads models to your computer, performs the transcription there, and saves the output to the same folder where the original audio is located. Moreover, while the very first transcription using a given model requires Internet for the model download[^3], it is possible to use LOKAL offline.
  *As audios do not need to leave your computer, you can take several approaches to reducing the risk of audios leaking, being hacked, or accidentally being shared.

## Installation

### No-code installation
LOKAL is super easy to install and run:
* Download the latest installer file (.exe) available [here](https://github.com/jbolns/LOKAL_transcriptions/releases). 
* Double-click to install.
* Use.

> *Note. You can also use LOKAL as a pure Python app. Installation is trickier but is ideal for Python developers who wish to tinker with the code. Instructions at the end of this README.*

### Compatibility
By default, LOKAL is set to use *Systran's Faster Whisper* AI models and *.wav* audios. You can transcribe '.wav' audios using *Systran's Faster Whisper* from the moment you install LOKAL.

To use other audio formats or models, use LOKAL on a computer with [FFmpeg](https://www.ffmpeg.org/) (if you need to install it, I find [this guidance](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) somewhat easy to follow).

If you absolutely cannot install FFmpeg, LOKAL might still work for you if you use audios in *.wav* format and Systran's 'Faster Whisper' models. Other file types and models require FFmpeg.

## Usage
LOKAL packs a lot. The list of options available is long, but once you open LOKAL, you'll see everything is intuitive and esy-to-use.

![Preview of LOKAL in light mode](/images/light-mode.png)

### Required selections
Some selections are necessary for a transcription to be possible. Buttons and dropdowns to make these choices are always visible.

* *Select audio.* Press select audio to transcribe. 
  * If you do NOT have FFmpeg installed, use only *.wav* audios.

* *GPU* Enable GPU mode. 
  * Turn on to enable settings applicable to GPUs.
  * If you do not have a GPU, leave the button as it is. LOKAL defaults to settings applicable to regular CPUs.

* *Timestamps*. Enable timestamps
  * Turn on to enable timestamps on final transcript.
  * If you do not need timestamps, leave the button as it is. LOKAL defaults to a transcript without timestamps due to historical reasons (it started as a research tool and timestamps can be very annoying in this context).

* *Terms and conditions.* Use the checkbox to agree to the terms and conditions of usage.
  * Click on the link to read terms and conditions.
  * Agree to terms and conditions using the checkbox.

* *Model (family).* Use the dropwodn to choose the model to use for transcription.
  * *Family.* Choose your preferred AI model provider.
    * If you do NOT have FFmpeg installed, use only *Systran's Faster Whisper* audios.
  * *Size.* Specify the model size to use for transcription.
    * The larger the model, the higher the quality.
    * The larger the model, the longer the transcription takes.
    * Rule of thumb! If you can understand the conversation easily, one of the smaller models might suffice.

* *Approach.* Use the dropdown to choose between three different approaches to transcription, meant for different types of conversations.
  * *Simple.* A straightforward word-by-word transcription. Best for complex/dynamic conversations with many speakers and interruptions, where it is very difficult to track of all speaker changes.
  * *Segmentation.* A transcription split into paragraphs roughly following pauses and changes of speakers. Best for semi-structured conversations like interviews and focus groups, where tracking speaker changes is easier.
  * *Diarisation.* A transcription split into blocks roughly corresponding to segments by specific speakers (with speaker labels). Best for structured conversations where speakers have clear turns and speaker changes are clear, like panels or seminars.

* *Language.* Use the dropdown to select the language for transcription.
  * If left blank, the model tries to identify the language by itself. 
  * Specifying the language might make it easier for the model and speed things a little.

### Optional selections
Some selections are optional. Relevant buttons and dropdowns appear and dissapear as available (you can ignore them if desired - LOKAL will load default values if no selection is made).

* *OPTIONAL PROMPT*
  * This option is shown when the user selects the original 'OpenAI: Whisper' family of models.
  * It can be used to upload a text file containing terms that the model might struggle to identify, such as names, names of places, jargon, and acronyms. 
  * Prompts are not infalible. They can help quite a bit, but they are not as effective as fine-tuning a model for a specific sector/industry.

* *Ignore short segments.* 
  * Appears when users choose 'segmentation'.
  * Use to set a threshold to ignore short words/comments like fillers or interruptions.
  * If treshold is too high, it might ignore parts of sentences before/after pauses.
* *Ignore short pauses.*
  * Appears when users choose 'segmentation' or 'diarisation'.
  * Use to set a threshold to ignore short pauses that might cause excessive paragraph breaks in the final transcript.
  * If this hyper-parameter is set too high, the models might ignore legitimate changes between speakers.
* *Number of speakers.* 
  * Appears when users choose 'diarisation'.
  * Enables users to enter the exact number of speakers. 
  * There is no need to set a number. The diarisation model can try and guess the number of speakers. That said, results can be better if the model knows the number of speakers in advance.

## Privacy
LOKAL is not a guarantee of privacy. There are many privacy risks in any computer and software.

That said, LOKAL can help you manage privacy in the following ways:
* LOKAL avoids you the need to send audios to third-party service providers, thereby reducing risk exposure.
* LOKAL allows you to avoid the need to consent to data usage terms that may (and often do) have troublesome concessions.
* LOKAL allows you to run transcriptions offline, so you can use LOKAL in an isolated transcription environment if dealing with extremely sensitive data.

## Known limitations
LOKAL aims to assist humans with preparatory tasks rather than replace humans. Reducing the costs and time of initial speech-to-text conversion allows users to assign more resources on editing. 

For the same reason, users remain in control and are responsible for the final quality of transcriptions and should therefore always remember that all AI models and systems have limitations.

LOKAL's limitations include but are not limited to:
* All models may present potentially high error rates.
* The segmentation and diarisation approaches and models used in these approaches can struggle with overlapping speakers.
* The transcription models can struggle with names, places, acronyms, and potentially, accents. Users must not use outputs without editing them.
* The transcription models can struggle with conversations taking place in different languages – an idea is to do multiple runs with different language selections and then join the results.

## Having troubles?
I made LOKAL as easy to install and use as possible. However do get in touch if you feel stuck: hello@josebolanos.xyz.

## License
LOKAL (transcriptions) is released under an Apache 2.0 open source license. The code is available via GitHub. 

LOKAL implements a non-commercial open-source approach I like to call "ugly mode". The user interface looks a little ugly, but all functionality works regardless of whether LOKAL is activated or not. There is, additionally, an option to make a voluntary payment to make the user interface pretty.

.

.

.

## OPTIONAL Python installation (advanced coding required)
**Skip this section if not a coder. It is REALLY hard.**

Python developer may wish to use LOKAL as a pure Python app rather than use the *.exe* installer. 

Assuming you have Python (3.11.0) installed on your computer, you need to:
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

.

.

.

---

**Footnotes**

[^1]: An Internet connection is needed for initial model download. The first time you choose a model, the model downloads. After, it is possible to perform transcriptions offline. Resetting models is possible from within LOKAL, which deletes all models in memory and forces a re-download next time a model is used.
[^2]: Adherence to any specific regulations is not guaranteed. Moreover, since the exact requirements vary across jurisdictions, it is also impossible to say exactly how LOKAL could facilitate compliance in any given jurisdiction.
[^3]: The very first time you run a specific model, Internet is needed to download the model. After that, transcription can be undertaken without a connection to the Internet.