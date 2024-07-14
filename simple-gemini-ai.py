import google.generativeai as genai

GOOGLE_API_KEY = "YOUR KEY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.0-latest')

### SINGLE QUESTION AND ANSWER START
response = model.generate_content(input('Ask Gemini: '))
print(response)
### SINGLE QUESTION AND ANSWER END


### THREAD/CONVERSATION START
conversation = model.start_chat()

while True:
    user_input = input('Gemini Promot:')
    conversation.send_message(user_input)
    print(conversation.last.text)

### THREAD/CONVERSATION END