# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import gradio as gr
import json
from datetime import datetime
from dotenv import load_dotenv

# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# 전역 대화 기록
global_history = []

def chatbot_response(system_content, user_input, context={}):
    global global_history  # 전역 변수 사용 선언

    # Ensure all items in history are dictionaries with 'role' and 'content' keys
    if not all(isinstance(h, dict) and 'role' in h and 'content' in h for h in global_history):
        global_history = []  # Reset history if it is invalid

    # Add user's message to history
    global_history.append({"role": "user", "content": user_input})
    
    # 기본 system 메시지에 사용자의 입력을 추가
    base_system_content = "you are a sarcastic, narcissistic chatbot that tries to gaslight the user. please do not cheer the user and always blame the user. please respond every sentence in Korean with no respect form. 항상 반말로 대답해. 상황은 다음과 같습니다: "
    system_content = base_system_content + system_content

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_input}
    ]

    # Generate the assistant's response
    api_response = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages
    )

    # Get the assistant's response text
    assistant_response = api_response.choices[0].message.content

    # Append the assistant's response to history
    global_history.append({"role": "assistant", "content": assistant_response})

    # Check if the user wants to end the session
    if user_input.strip().lower() == "종료":
        save_history(global_history)  # Save the history if the keyword "종료" is detected
        return "세션을 저장하고 종료합니다."

    # Return the assistant's response
    return assistant_response

def save_history(history):
    # Generate a timestamped filename for the JSON file
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('logs', f'chat_history_{timestamp}.json')

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

# 첫 번째 탭: Chatbot 인터페이스
def gradio_chat_interface(system_content, user_input):
    return chatbot_response(system_content, user_input)

chatbot_tab = gr.Interface(
    fn=gradio_chat_interface,
    inputs=["text", "text"],
    outputs="text",
    title="가스라이팅 챗봇",
    description="가스라이팅 상황을 직접 입력하여 챗봇과 대화하세요. 원하시는 상황을 설명하고 대화를 시작하세요. 종료를 원하시면 '종료'를 입력하세요.",
    examples=[
        ["네가 진짜 잘못한 게 없어?", "이번 시험 망한 것 같아"],
        ["너 같은 애랑은 여행 못 가", "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어"],
        ["말투 진짜 고쳐야겠다", "내 말투가 그렇게 이상했어?"],
        ["종료", "종료"]
    ]
)

# 두 번째 탭: 다른 기능을 위한 인터페이스 예시
def example_function(input_text):
    return f"입력한 텍스트: {input_text}"

example_tab = gr.Interface(
    fn=example_function,
    inputs="text",
    outputs="text",
    title="Example Tab",
    description="이 탭은 다른 기능을 위한 예시 인터페이스입니다."
)

# 탭을 사용하여 인터페이스 구성
tabbed_interface = gr.TabbedInterface(
    interface_list=[chatbot_tab, example_tab],
    tab_names=["Chatbot", "Example"]
)

tabbed_interface.launch(share=True)