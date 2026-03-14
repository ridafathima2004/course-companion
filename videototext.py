fpath="C:\\Users\\ridar\\PycharmProjects\\coursecompanion\\myapp\\COA module 1.mp4"


import pytranscript as pt

wav_file = pt.to_valid_wav(fpath, "video.wav", start=0, end=None)
transcript = pt.transcribe(wav_file, model="vosk-model-en-us-aspire-0.2", max_size=None)
transcript_fr, errors = transcript.translate("fr")

transcript_fr.write("video.srt")