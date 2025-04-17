import queue
import sounddevice as sd
import vosk
import sys
import json
import requests
import pyttsx3

# Configuration
LLM_SERVER_URL = "http://10.42.0.53:8080/completion"
VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
history = []

# Initialize TTS engine
tts = pyttsx3.init()
tts.setProperty('rate', 170)

# Speech recognition setup
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

model = vosk.Model(VOSK_MODEL_PATH)
rec = vosk.KaldiRecognizer(model, 16000)

def recognize_from_mic():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Start talking...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text

def speak(text):
    print("🗣️ ", text)
    tts.say(text)
    tts.runAndWait()

def query_llama(prompt):
    history.append({"role": "user", "content": prompt})
    payload = {
        "stream": False,
        "n_predict": 200,
        "temperature": 0.7,
        "stop": ["</s>"],
        "messages": history,
    }
    response = requests.post(LLM_SERVER_URL, json=payload)
    reply = response.json()['content']
    history.append({"role": "assistant", "content": reply})
    return reply

def main():
    while True:
        try:
            user_input = recognize_from_mic()
            if user_input.lower() in ["stop", "quit", "exit"]:
                speak("Goodbye.")
                break
            print(f"🧏 You said: {user_input}")
            reply = query_llama(user_input)
            speak(reply)
        except KeyboardInterrupt:
            print("🛑 Exiting.")
            break
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    main()
