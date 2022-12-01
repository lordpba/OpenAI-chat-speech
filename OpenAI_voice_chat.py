import speech_recognition
import openai
import pyttsx3
from gtts import gTTS
import os


# GPT-3 Parameters

openai.api_key = 'your_API_Key_here'

## Speech Recognition Algorithm
recognizer = speech_recognition.Recognizer()
print("Please speak into the microphone:")

## Function which inputs speechtotext into openAI's API
while True:

    try:

        with speech_recognition.Microphone() as mic:

            #Ready the Microphone
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            #Translate speech to text
            SpeechText = recognizer.recognize_google(audio)
            SpeechText = SpeechText.lower()
            if SpeechText == 'stop':
                exit()

            ## GPT-3 API
            myPrompt = """
            The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

            Human: Hello, who are you?
            AI: I am an AI created by OpenAI. How can I help you today?
            Human:{SpeechText}
            AI:"""

            # GPT-3 Engine parameters
            start_sequence = "\nAI:"
            restart_sequence = "\nHuman: "
            Addon = "\n"


            response = openai.Completion.create(
                engine="davinci",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                prompt = str(myPrompt.replace("{SpeechText}", SpeechText)),
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n", "Human:", "AI:"]
            )
            # Print out results for further processing
            prompt = myPrompt.replace("{SpeechText}", SpeechText),
            print(f"Human:{SpeechText}\nAI:{response.choices[0].text}")

            # SPEAK IT OUT
            
            #added gTTS, is better voice but have to save a temp.mp3 file...
            testo = str(response.choices[0].text)
            audio = gTTS(text=testo, lang="en", slow=False)
            audio.save("speech.mp3")
            os.system("start speech.mp3")
            
            #removed pyttsx3 as is no nice voice :(
            #engine = pyttsx3.init()
            #engine.say(response.choices[0].text)
            #engine.runAndWait()
            #exit()

    except speech_recognition.UnknownValueError:
       print("I didn't quite get you. Can you please repeat that?")
       recognizer = speech_recognition.Recognizer()
    continue
