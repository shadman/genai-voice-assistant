# Generative AI Voice Assistant
GenAI Voice Assistant by using Gemini Prompts and Open AI TTS


## Install dependencies
pip install google.generativeai
pip install speech_recognition
pip install pyaudio
pip install openai
pip install faster_whisper

## API Keys
Set Env or update API KEY on line number 30, file voice-assistant.py with yours
> OPENAPI_API_KEY="XXccss233XXcccsszX"

Set Env or update API KEY on line number 35, file voice-assistant.py with yours
> GOOGLE_API_KEY="XXccss233XXcccsszX"

## Run a program
> python voice-assistant.py

You have to say 'hello' first to ask every question, but this can be avoided except first question by commenting line 148-149

Also, if you want to avoid this 'hello' wake word completely then can update the call back function accordingly and remove 'listening_for_wake_word' parameters


## Output : (Talk with you)
![alt sample demo](https://github.com/shadman/genai-voice-assistant/blob/main/img/demo.png)


## Tip
![alt sample demo](https://github.com/shadman/genai-voice-assistant/blob/main/img/pmodel-and-languages.png)



## Some Helpful Links
https://aistudio.google.com/
https://platform.openai.com/
https://platform.openai.com/docs/guides/text-to-speech
https://colab.research.google.com/