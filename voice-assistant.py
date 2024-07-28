import time
import google.generativeai as genai
import speech_recognition as sr
import os
import pyaudio

from openai import OpenAI
from faster_whisper import WhisperModel

wake_word = 'hello'
listening_for_wake_word = True

# Wisper for speech-to-text 
# Start with base, to reduce the cost
whisper_size = 'small'
num_cores = os.cpu_count()
whisper_model = WhisperModel(
    whisper_size,
    device = 'cpu',
    compute_type = 'int8',
    cpu_threads = num_cores,
    num_workers = num_cores, 
    #model_size_or_path = whisper_size
    )

# OpenAI for text-to-speech TTS API
# Or use `os.getenv('OPENAPI_API_KEY')` to fetch an environment variable.
OPENAPI_API_KEY = "REPLACE-WITH-YOUR-KEY"
client = OpenAI(api_key=OPENAPI_API_KEY)

# Gemini for prompts and assistance
# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY = "REPLACE-WITH-YOUR-KEY"
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 2048,
    "top_p": 1,
    "top_k": 1,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    "gemini-1.0-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

convo = model.start_chat()
system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFAIRMATIVE." 
to this system message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
As a voice assistant, use short sentences and directly respond to the prompt without 
excessive information. You generate only words of value, prioritizing logic and facts 
over speculating in your response to the following prompt.'''

system_message = system_message.replace(f'\n', '')

convo.send_message(system_message)

r = sr.Recognizer()
source = sr.Microphone()

# Use text as an input to speak
def speak(text):
    player_stream = pyaudio.PyAudio().open(rate=24000, channels=1, format=pyaudio.paInt16, output=True)
    stream_start = False

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        response_format="pcm",
        input=text
    ) as response:
      silence_threshold = 0.01

      for chunk in response.iter_bytes(chunk_size=1024):
        if stream_start:
          player_stream.write(chunk)
        elif max(chunk) > silence_threshold:
          player_stream.write(chunk)
          stream_start = True

# Convert WAV audio file to audio for voice input
def wav_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    text = ''.join(segment.text for segment in segments)
    return text

# Listening for a word to wake him up or can say activate
def listen_for_wake_word(audio):
    global listening_for_wake_word

    wake_audio_path = 'wake_word.wav'
    with open(wake_audio_path, 'wb') as f:
      f.write(audio.get_wav_data())

    text_input = wav_to_text(wake_audio_path)
    if wake_word in text_input.lower().strip():
        print('Wake word detected. Please speak your question.')
        listening_for_wake_word = False

# Convert audio to text; send a prompt for a response and speak
def prompt_gpt_to_speak(audio):
    global listening_for_wake_word

    try:
      propmpt_path = 'prompt.wav'

      with open(propmpt_path, 'wb') as f:
        f.write(audio.get_wav_data())

      prompt_text = wav_to_text(propmpt_path)
      if len(prompt_text.strip()) == 0:
        print('No prompt detected. Please speak again.')
        listening_for_wake_word = True
      else:
        print(f'You: {prompt_text}')

        convo.send_message(prompt_text)
        output = convo.last.text

        print(f'Assistant: {output}')
        speak(output)

        # Can comment these 2 lines, if you need continous converstaion without wake word
        print('Say', wake_word, 'to wake me up. \n')
        listening_for_wake_word = True

    except Exception as e:
      print('Prompt error: ', e)

# Will be called by voice recognition on detect any voice
def callback(recognizer, audio):
    global listening_for_wake_word

    if listening_for_wake_word:
      listen_for_wake_word(audio)
    else:
      prompt_gpt_to_speak(audio)

# Main method to start the program and alive for listening
def start_listening():
    with source as s:
      r.adjust_for_ambient_noise(s, duration=2)

    print('\nSay', wake_word, 'to wake me up. \n')
    r.listen_in_background(source, callback)

    while True:
      time.sleep(0.5)


if __name__ == '__main__':
    start_listening()

