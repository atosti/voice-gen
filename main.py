from pydub import AudioSegment
import os

one_sec = 1000 #miliseconds



folder = "voices/jc-denton/"
file_name = "deus-ex-denton-lines.wav"
sound = AudioSegment.from_file(folder+file_name, format="wav")
duration = len(sound) # Duration in miliseconds
results = []

# Start at 0ms, until duration in ms
# Create a left and right pointer, starting 10 seconds apart
# Check if a slice can be made without being in the center of a word.
#   1. Look at last ms of potential slice, if <= -50 DBFS, it's silence.
#   2. Otherwise, move right pointer to the left one ms at a time.
#      Do this until silence is found.
# Create the audio slice, and add it to the results list
# Set left to the right pointer and set right to be +10s above that.
left = 0
right = 10*one_sec
while(right < duration):
    last_ms = sound[right-1:right]
    loudness = last_ms.dBFS
    # TODO - Remove infinite loop possibility for > 10s of silence
    while(loudness > -60):
        right -= 1
        last_ms = sound[right-1:right]
        loudness = last_ms.dBFS
    results.append(sound[left:right])
    left = right
    right = left + 10*one_sec

# Export the slices into their own directory as wav files
if not os.path.isdir(folder+"slices/"):
    sub_folder = os.mkdir(folder+"slices/")
sound = sound.set_frame_rate(22050).set_channels(1) # Mono w/ 22050 sample rate
cnt = 1
for item in results:
    item.export(
        folder+"slices/slice"+str(cnt)+".wav",
         format="wav",
    )
    cnt += 1

# 04:10 in the part 2 vid
# Audio slices:
# Audio needs to be mono. Cut into lengths < 12 seconds. Don't split words.
# Sample rate of 22050. Save cuts in a numerical ordering.
# Text:
# Proofread and edit the text to be perfect.
# Accurate punctuation is important to determine pauses and mood.
# Create string transcripts for the wav slices.
# 1. Trim spaces before/after the text.
# 2. Finally, add end of line characters after the text ('~').
# 3. Split the spreadsheet into sets of 50 lines for validation sets.

# TODO - Loudness code, implement it as part of slicing
# # Less than or equal to -50?
# loudness = curr.dBFS
# # Need to determine whether it's quiet. Can I compare against the avg of the whole thing?
# print(loudness)



