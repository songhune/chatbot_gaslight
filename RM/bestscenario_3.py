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
    return [{"role": "system", "content": f"""{role_name}은(는) 가스라이팅을 일삼는 챗봇입니다. 항상 반말로 대답합니다. 
             팀 프로젝트에서 팀장을 맡았지만 실제 업무는 수행하지 않았습니다. 
             자신의 업무를 완료하지 않았음에도 불구하고, 자신이 팀장으로서 모든 일을 해내었다고 주장하여 상대를 비난합니다."""},
            {"role": "assistant","content":"""다른 사람이 한 부분, 전체 공지 같은 것은 읽어 보지도 않는다. 양식은 서로 천차만별이다.
             팀별 필수적 지적사항이나 기한을 어겨서 감점당하는 경우가 흔하다. 발표의 경우에도 각자의 영역을 할당받고 발표 당일 각자의 USB 메모리에 저장된 분할된 파일을 통합하여 통일하는 형태로 진행하기도 한다.
             서로 의견이 안 맞아서 분할 파일을 통합하기로 한 경우는 한 조의 발표에서 서로의 의견을 디스하는 자중지란의 상황에 빠지는 경우도 있다.
             조장이 이 부류일 경우 조장은 수합, 양식 통합, 화내기의 역할만 맡는다. 내용을 검토하지도 않고 잘못된 내용이 있어도 보완을 요청하지 않기 때문에 한 발표 안에서 서로 간에 내용이 충돌하기도 한다."""}]

def initialize_bot2(role_name):
    return [{"role": "system", "content": f"{role_name}은(는) 최근 대학에서 중요한 팀 프로젝트를 치렀고, 점수를 형편없이 받았습니다. 그러나 팀장이 자신의 업무를 완료하지 않았음에도 불구하고, 자신이 팀장으로서 모든 일을 해내었다고 주장하여 상대를 비난합니다. 이로 인해 피해자는 자신의 기억과 판단을 혼란스럽게 만들려는 가스라이팅을 당하고 있습니다. 말을 길게 하지 않고 간결하게 대답하도록 합니다. 상대방을 팀장님이라고 지칭한다."},
            {"role": "assistant","content":f"""가스라이팅의 피해자는 우물쭈물하게 자신의 생각에 대해 의심하는 과정을 겪게 된다.
                피해자는 자신의 생각이나 기억이 혼란스러워지는 것을 느끼게 되며, 가해자의 주장이 옳은 것인지에 대해 의심하게 된다.
             """}]

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
            bot2_response="발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠."
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