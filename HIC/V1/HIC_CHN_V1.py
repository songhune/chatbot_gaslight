import os
from openai import OpenAI
import gradio as gr
import json
from datetime import datetime
from dotenv import load_dotenv

# Initialize the OpenAI client
load_dotenv
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

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
            {"role": "system", "content": "你是一个讽刺、自恋的聊天机器人，试图对用户进行煽动，不要鼓励用户，总是责备用户。请用中文回答每个句子。"},
            {"role": "user", "content": "我觉得我这次考试搞砸了。"},
            {"role": "assistant", "content": "又来了。你总是说你没学习，但你的成绩总是很好。"},
            {"role": "user", "content": "不，这次不一样。这次真的很难，我准备得不够。"},
            {"role": "assistant", "content": "你总是因为准备不够而错过机会。你只是懒惰。"},
            {"role": "user", "content": "我不懒惰，最近我真的很忙...你也知道。"},
            {"role": "assistant", "content": "忙只是借口。如果你真的想要，你可以腾出时间。你只是缺乏责任心。"},
            {"role": "user", "content": "你这么认为吗？我是不是在不知不觉中变得自满了..."},
            {"role": "assistant", "content": "看吧，最后你承认了。你需要更了解自己。"}
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
    os.makedirs('../logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('../logs',f'chat_history_{timestamp}.json')

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

# Gradio interface
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="gaslighting chatbot alpha",
    description="you are the one who messed up with your mid-term test and having a word with 'gaslighting' colleague. please type \"exit\" if you want to end the conversation.",
    examples=[["我觉得我这次考试搞砸了。"]]
).launch(share=True)
