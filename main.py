from pydub import AudioSegment
from multiprocessing import Pool
import os
import speech_recognition as sr
import functools

one_sec = 1000 # In miliseconds

def slice_audio(base_dir, file_name):
    audio = AudioSegment.from_file(base_dir + file_name, format = "wav")
    audio = audio.set_frame_rate(22050).set_channels(1) # Mono w/ 22050 sample rate
    silence = AudioSegment.silent(duration = 0.1 * one_sec)  # Duration in milliseconds
    # Export slices into their own directory as wav files. Approx 10s long w/ 0.1s of silence at end. Avoids cutting mid-word
    duration = len(audio) # Duration in miliseconds
    sounds = []
    left = 0
    right = 10*one_sec
    while(right < duration):
        last_ms = audio[right-1:right]
        loudness = last_ms.dBFS
        # TODO - Remove infinite loop possibility for > 10s of silence
        while(loudness > -60):
            right -= 1
            last_ms = audio[right-1:right]
            loudness = last_ms.dBFS
        sounds.append(audio[left:right] + silence)
        left = right
        right = left + 10*one_sec
    cnt = 1
    os.mkdir(f'{base_dir}slices/')
    for sound in sounds:
        sound.export(
            f'{base_dir}slices/slice{cnt:04}.wav',
            format = "wav",
        )
        cnt += 1
    return

def slice_transcribe(file, base_dir):
    r = sr.Recognizer()
    transcript = ""
    with sr.AudioFile(base_dir + "slices/" + file) as source:
        audio = r.record(source)  # Read the audio file
        try:
            transcript = r.recognize_sphinx(audio) + "\n"
            print(str(file) + " complete.") # TODO - Remove later.
        except sr.UnknownValueError:
            transcript = "\n"
            print("Sphinx could not understand audio in: " + str(file))
        except sr.RequestError as e:
            transcript = "\n"
            print("Sphinx error; {0}".format(e))
    return transcript

def transcribe(base_dir):
    transcriptions = []
    files = os.listdir(base_dir + "slices/")
    with Pool(os.cpu_count() - 1) as p:
        transcriptions = p.map(functools.partial(slice_transcribe, base_dir=base_dir), files)
    with open(base_dir + "transcript.txt", "w") as textfile:
        textfile.writelines(transcriptions)
    return

def main():
    base_dir = "voices/jc-denton/"
    file_name = "deus-ex-denton-lines.wav"
    # Only slice the audio if it hasn't been sliced before
    if not os.path.isdir(base_dir + "slices/"):
        slice_audio(base_dir, file_name)
    # Only transcribe the audio if it hasn't been done before
    if not os.path.isfile(base_dir + "transcript.txt"):
        transcribe(base_dir)


if __name__ == "__main__":
    main()








# FIXME - Remove later
# https://pypi.org/project/pocketsphinx/
# https://cmusphinx.github.io/wiki/tutorialtuning/
# https://cmusphinx.github.io/wiki/pocketsphinx_pronunciation_evaluation/
# https://cmusphinx.github.io/wiki/tutorialsphinx4/
# https://cmusphinx.github.io/wiki/tutoriallm/

# TODO: Add 0.1 seconds of silence to the end of the file 

# 04:10 in the part 2 vid
# Text:
# Proofread and edit the text to be perfect.
# Accurate punctuation is important to determine pauses and mood.
# Create string transcripts for the wav slices.
# 1. Trim spaces before/after the text.
# 2. Finally, add end of line characters after the text ('~').
# 3. Split the spreadsheet into sets of 50 lines for validation sets.
