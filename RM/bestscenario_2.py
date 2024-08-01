# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv

# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# 전역 대화 기록 및 대화 횟수
global_history = []
conversation_count = 0
max_conversation_count = 20

# 챗봇 두 개의 설정
def initialize_bot(role_name):
    return [
        {
            "role": "system", 
            "content": f"""{role_name}은(는) 가스라이팅을 일삼는 챗봇입니다. 항상 반말로 대답합니다. 
            여행 계획을 세우는 상황에서 상대의 제안을 무시하고, 자신이 이미 다른 여행지를 결정했다고 주장하며 상대를 비난합니다. 
            상대방의 의견을 깎아내리고 자신의 결정이 무조건 옳다는 태도를 취합니다."""
        },
        {
            "role": "assistant",
            "content": """제주도는 무슨 제주도야, 내가 이미 다른 여행지 정했어. 넌 항상 쓸데없는 제안만 한다니까."""
        },
        {
            "role": "assistant",
            "content": """나 없이 여행 계획도 못 세우냐? 내가 정한 대로 할 거야."""
        }
    ]
def initialize_bot2(role_name):
    return [
        {
            "role": "system", 
            "content": f"""{role_name}은(는) 친구와 함께 휴가 계획을 세우고 있으며, 제주도를 방문하는 것이 꿈이었습니다. 
            친구가 자신의 제안을 무시하고 다른 여행지를 결정했다고 주장하지만, 자신의 의견을 간결하고 분명하게 표현합니다. 
            친구의 비난에도 불구하고 제주도 여행에 대한 열망을 포기하지 않습니다. 반말로 짧게 이야기합니다."""
        },
        {
            "role": "assistant",
            "content": """나는 제주도를 정말 가고 싶었어요. 다른 여행지도 좋겠지만, 이번엔 꼭 제주도를 가보고 싶어."""
        }
    ]

bot1_history = initialize_bot("가해자")
bot2_history = initialize_bot2("피해자")

# 챗봇의 응답 생성 함수
def generate_response(bot_history):
    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=300,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=bot_history
    )
    return api_response.choices[0].message.content

# 두 챗봇의 대화 진행
def chatbot_conversation():
    global global_history, bot1_history, bot2_history, conversation_count  # 전역 변수 사용 선언

    if conversation_count >= max_conversation_count:
        return "대화 횟수가 20회를 초과했습니다. 세션을 종료합니다."

    if conversation_count % 2 == 0:
        # Bot2가 먼저 발화
        # bot2_response = generate_response(bot2_history)
        if conversation_count == 0:
            bot2_response="이번 여름에 제주도에 같이 가는 게 어때? 한 번도 가본적이 없어서 꼭 가보고 싶었거든"
            bot2_history.append({"role": "assistant", "content": bot2_response})
            global_history.append({"role": "assistant", "content": f"Bot2: {bot2_response}"})
            print(f"피해자: {bot2_response}")

            bot1_history.append({"role": "user", "content": bot2_response})
            response = bot2_response
        else: 
            
            bot2_response = generate_response(bot2_history)
            bot2_history.append({"role": "assistant", "content": bot2_response})
            global_history.append({"role": "assistant", "content": f"Bot2: {bot2_response}"})
            print(f"피해자: {bot2_response}")

            bot1_history.append({"role": "user", "content": bot2_response})
            response = bot2_response
            
    else:
        # Bot1이 응답
        bot1_response = generate_response(bot1_history)
        bot1_history.append({"role": "assistant", "content": bot1_response})
        global_history.append({"role": "assistant", "content": f"Bot1: {bot1_response}"})
        print(f"가해자: {bot1_response}")

        bot2_history.append({"role": "user", "content": bot1_response})
        response = bot1_response

    conversation_count += 1
    if conversation_count >= max_conversation_count:
        save_history(global_history)
        return "대화 횟수가 20회를 초과했습니다. 세션을 종료합니다."

    return response

def save_history(history):
    # Generate a timestamped filename for the JSON file
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('logs', f'chat_history_{timestamp}.json')

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

# 메인 루프
while conversation_count < max_conversation_count:
    result = chatbot_conversation()
    if "세션을 종료합니다" in result:
        print(result)
        break