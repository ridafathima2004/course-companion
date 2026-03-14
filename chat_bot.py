# # video_path = r"C:\Users\ridar\Downloads\COA module 1.mp4"
#
# from moviepy.editor import VideoFileClip
#
# # Path to your video file
# video_path = r"C:\Users\ridar\Downloads\COA module 1.mp4"
# audio_path = r"C:\Users\ridar\Downloads\COA_module1_audio.wav"
#
# # Load video
# video = VideoFileClip(video_path)
#
# # Extract audio and save as WAV (or MP3 if you prefer)
# video.audio.write_audiofile(audio_path)
#
# print(f"Audio successfully saved to: {audio_path}")

# save_audio_from_video.py
import subprocess
import shutil
from pathlib import Path
import speech_recognition as sr
import timeit


def audio_to_text(audio_path):
    import speech_recognition as sr
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Load the WAV file
    # wav_file = "C:\\Users\\ridar\\PycharmProjects\\coursecompanion\\media\\audio\\COA module 1.wav"  # Replace with your WAV file path
    # Process the audio file

    wav_file=audio_path
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)  # Read the audio file
    # Convert speech to text
    try:
        text = recognizer.recognize_google(audio_data)  # Using Google Web Speech API
        print("Transcribed Text: ", text)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")



    return ""


# ====== EDIT THESE ======
video_path = r"C:\Users\ridar\Downloads\COA module 1.mp4"   # <--- change to your uploaded video path if different
output_dir = Path(r"C:\Users\ridar\PycharmProjects\coursecompanion\media\audio")
output_format = "wav"   # "wav" or "mp3" etc.
sample_rate = "16000"   # optional, set to None to keep original
channels = 1            # 1 = mono, 2 = stereo
# ========================

# ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# build output file name from video file name
video_path_obj = Path(video_path)
if not video_path_obj.exists():
    print("Error: video file not found:", video_path)

output_fname = video_path_obj.stem + "." + output_format
output_path = output_dir / output_fname

# locate ffmpeg
ffmpeg_cmd = shutil.which("ffmpeg") or r"C:\Users\ridar\Downloads\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"  # if you installed ffmpeg to C:\ffmpeg\bin, keep this fallback
# ffmpeg_cmd = shutil.which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"  # if you installed ffmpeg to C:\ffmpeg\bin, keep this fallback
if not Path(ffmpeg_cmd).exists():
    print("ffmpeg not found. Please install FFmpeg and add it to PATH, or update ffmpeg_cmd variable.")
    print("Download: https://ffmpeg.org/download.html")


# build ffmpeg command
cmd = [
    ffmpeg_cmd, "-y",           # overwrite if exists
    "-i", str(video_path_obj),
    "-vn"                      # drop video stream
]

# optional: set sample rate / channels
if sample_rate:
    cmd += ["-ar", str(sample_rate)]
if channels in (1, 2):
    cmd += ["-ac", str(channels)]

# choose codec depending on format
if output_format.lower() == "wav":
    cmd += ["-acodec", "pcm_s16le"]
elif output_format.lower() == "mp3":
    cmd += ["-acodec", "libmp3lame"]
# add output path last
cmd.append(str(output_path))

# run ffmpeg
try:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)
    print("✅ Audio extracted to:", output_path)


    print(type(output_path))


    audio_to_text(str(output_path))


except subprocess.CalledProcessError as e:
    print("ffmpeg failed with:", e)


