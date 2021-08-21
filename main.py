from pydub import AudioSegment
import os

one_sec = 1000 #miliseconds


# Basic concept
# 1. Loop through the entire song and slice it into 10 second chunks.
#   - dice() can do this, but how to check for middle of words?
# 2. If in in the middle of a word, try to move forward 1ms until dead air is found.
# 3. Trim all dead air from the front of any audio clips.
# 4. Attach 0.1s of dead air to the ends.
# 5. Save all the chunks into a folder.

folder = "voices/jc-denton/"
file_name = "deus-ex-denton-lines.wav"
sound = AudioSegment.from_file(folder+file_name, format="wav")
duration = len(sound) / one_sec # Duration in seconds
# Slice into 10-second chunks
results = []
slices = int(duration/10) + int(duration / int(duration))
for i in range(0, slices-1):
    results.append(sound[i*one_sec:(i+10)*one_sec])
# Add a final slice to handle leftover audio that's less than 10s
if duration > int(duration):
    results.append(sound[(slices-1)*10*one_sec:])
# Export the slices into their own directory as wav files
if not os.path.isdir(folder+"slices/"):
    sub_folder = os.mkdir(folder+"slices/")
cnt = 1
for item in results:
    item.export(folder+"slices/slice"+str(cnt)+".wav", format="wav")
    cnt += 1

# FIXME - Remove this later, it's just for quick testing
# results[0].export(folder+"slices/slice"+str(cnt)+".wav", format="wav")

# TODO - Loudness code, implement it as part of slicing
# # Less than or equal to -50?
# loudness = curr.dBFS
# # Need to determine whether it's quiet. Can I compare against the avg of the whole thing?
# print(loudness)



