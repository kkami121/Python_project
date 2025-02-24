import openai
import pyaudio
import speech_recognition as sr
import pyttsx3
import snowboydecoder

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the text-to-speech engine
engine = pyttsx3.init()

# Set up the Snowboy detector for wake word detection
model = "path/to/jobis.pmdl"
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# Create a recognizer instance
recognizer = sr.Recognizer()

# Loop to continuously capture and process voice input
while True:
    # Wait for the wake word
    print("Waiting for wake word 'jobis'...")
    detector.start(detected_callback=lambda: print("Wake word detected!"))

    # Record audio from the microphone
    print("Listening...")
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source)

    # Transcribe the audio data into text
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Unable to transcribe audio")
        continue

    # Generate a response using GPT
    prompt = f"Q: {text}\nA:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
    )
    answer = response.choices[0].text.strip()

    # Print and voice the response generated by GPT
    print(f"jobis: {answer}")
    engine.say(answer)
    engine.runAndWait()
