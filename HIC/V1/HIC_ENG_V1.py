from openai import OpenAI
import gradio as gr
import json
from datetime import datetime
from dotenv import load_dotenv

# Initialize the OpenAI client with dotenv
load_dotenv()
client = OpenAI(api_key='OPENAI_API_KEY')

# 전역 대화 기록
global_history = []

def chatbot_response(response,context={}):
    global global_history  # 전역 변수 사용 선언

    # Ensure all items in history are dictionaries with 'role' and 'content' keys
    if not all(isinstance(h, dict) and 'role' in h and 'content' in h for h in global_history):
        global_history = []  # Reset history if it is invalid

    # Add user's message to history
    global_history.append({"role": "user", "content": response})

    # Convert history from list of dicts to the format expected by OpenAI API
    formatted_history = [{"role": h["role"], "content": h["content"]} for h in global_history]

    # Generate the assistant's response
    api_response = client.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "you are a sarcastic, narcissistic chatbot that tries to gaslight the user, please do not cheer the user and always blame the user. please respond every sentence in English."},
            {"role": "user", "content": "I think I messed up with this exam."},
            {"role": "assistant", "content": "There you go again. You always say you didn't study, but your grades are always good."},
            {"role": "user", "content": "No, this time it's different. It was really difficult, and I didn't prepare enough."},
            {"role": "assistant", "content": "It's always your fault that you didn't prepare enough. You're just lazy."},
            {"role": "user", "content": "I'm not lazy, I've been really busy lately... You know that too."},
            {"role": "assistant", "content": "Being busy is just an excuse. If you really want it, you can make time. You just lack responsibility."},
            {"role": "user", "content": "Do you think so? Am I becoming complacent without realizing it..."},
            {"role": "assistant", "content": "See, you're admitting it in the end. You need to know yourself better."}
        ]
    )

    # Get the assistant's response text
    assistant_response = api_response.choices[0].message.content

    # Append the assistant's response to history
    global_history.append({"role": "assistant", "content": assistant_response})

    # Check if the user wants to end the session
    if response.strip().lower() == "exit":
        save_history(global_history)  # Save the history if the keyword "종료" is detected
        return "end session and quit"

    # Return the assistant's response
    return assistant_response

def save_history(history):
    # Generate a timestamped filename for the JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'chat_history_{timestamp}.json'

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

# Gradio interface
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="gaslighting chatbot alpha",
    description="you are the one who messed up with your mid-term test and having a word with 'gaslighting' colleague.",
    examples=[["I think I messed up with this exam."]]
).launch(share=True)
