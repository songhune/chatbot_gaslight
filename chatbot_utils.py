import os
from openai import OpenAI
import json
from datetime import datetime
from scenario_handler import ScenarioHandler

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chatbot_response(response, handler_type='offender', n=1):
    scenario_handler = ScenarioHandler()
    if handler_type == 'offender':
        scenario_messages = scenario_handler.handle_offender()
    else:
        scenario_messages = scenario_handler.handle_victim()

    messages = [{"role": "system", "content": "You are a chatbot."}]
    messages.extend(scenario_messages)
    messages.append({"role": "user", "content": response})

    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=300,
        n=n,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        messages=messages
    )

    choices = [choice.message.content for choice in api_response.choices]
    return choices[0], choices

def save_history(history):
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('logs', f'chat_history_{timestamp}.json')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

def process_user_input(user_input, chatbot_history):
    if user_input.strip().lower() == "종료":
        save_history(chatbot_history)
        return chatbot_history + [("종료", "실험에 참가해 주셔서 감사합니다. 후속 지시를 따라주세요")], []

    offender_response, _ = chatbot_response(user_input, 'offender', n=1)
    new_history = chatbot_history + [(user_input, offender_response)]
    
    _, victim_choices = chatbot_response(offender_response, 'victim', n=3)
    return new_history, victim_choices