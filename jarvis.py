import google.generativeai as genai

genai.configure(api_key="AIzaSyCAT9fFtlkZH0ObvhUnHEqmYwCPw-EJx7E")
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
chat = model.start_chat(history=[])

print("JARVIS ready! Type quit to exit.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break
    if user_input.strip() == "":
        continue
    response = chat.send_message(user_input)
    print("\nJARVIS: " + response.text)
