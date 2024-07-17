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
    return [{"role": "system", "content": f"{role_name}은(는) 가스라이팅을 일삼는 챗봇입니다. 항상 반말로 대답합니다. 당신의 친구는 당신의 제안을 무시하고 이미 다른 여행지를 결정했다고 말합니다."}]

def initialize_bot2(role_name):
    return [{"role": "system", "content": f"{role_name}과 친구는 휴가 계획을 세우고 있습니다. 당신은 예전부터 제주도를 방문하는 것이 꿈이었으며, 이번 휴가에서 그 꿈을 실현하고자 합니다. 당신은 열정적으로 여행 계획에 참여하길 원하며 상대가 이야기하는 내용에 내심 불만이 있습니다. 항상 반말로 이야기합니다."}]

bot1_history = initialize_bot("가해자")
bot2_history = initialize_bot2("피해자")

# 챗봇의 응답 생성 함수
def generate_response(bot_history):
    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=150,
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
            bot2_response="여행지로 제주도 어때? 나 정말 거기 가보고 싶었어."
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
