import speech_recognition as sr
# Initialize the recognizer
recognizer = sr.Recognizer()
# Load the WAV file
wav_file = "C:\\Users\\ridar\\PycharmProjects\\coursecompanion\\media\\audio\\COA module 1.wav"  # Replace with your WAV file path
# Process the audio file
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
