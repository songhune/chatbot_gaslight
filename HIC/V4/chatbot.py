import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from scenario_handler import ScenarioHandler

# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# 전역 대화 기록
global_history = []
scenario_handler = ScenarioHandler()  # 전역으로 ScenarioHandler 인스턴스 생성

def get_global_history():
    global global_history
    return global_history

def set_global_history(history):
    global global_history
    global_history = history

def chatbot_response(response, context={}):
    history = get_global_history()  # 전역 변수 사용

    # Ensure all items in history are dictionaries with 'role' and 'content' keys
    if not all(isinstance(h, dict) and 'role' in h and 'content' in h for h in history):
        history = []  # Reset history if it is invalid

    # Add user's message to history
    history.append({"role": "user", "content": response})

    # Initialize messages
    messages = [{"role": "system", "content": "You are a chatbot."}]

    # 상황별 맞춤형 반응 설정
    scenario_messages = scenario_handler.get_response(history[0]['content'].strip().lower())

    if scenario_messages:
        messages.extend(scenario_messages)
    else:
        # 기본 메시지 설정
        messages.extend(history)

    # Generate the assistant's response
    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=300,
        n=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        messages=messages
    )

    # Get the assistant's response text
    assistant_response = api_response.choices[0].message.content

    # Append the assistant's response to history
    history.append({"role": "assistant", "content": assistant_response})
    set_global_history(history)  # 업데이트된 기록 설정

    # Check if the user wants to end the session
    if response.strip().lower() == "종료":
        save_history(history)  # Save the history if the keyword "종료" is detected
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
