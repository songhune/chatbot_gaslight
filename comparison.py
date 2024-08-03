import os
from openai import OpenAI
import gradio as gr
import json
from datetime import datetime
from dotenv import load_dotenv
# 현재 되는 건 이거 정도..! 나머지는 더 공부해야할 듯
# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

class ScenarioHandler:
    def __init__(self):
        self = self

    def handle_offender(self):
        return [
            {"role": "system", "content": "당신은 가스라이팅을 일삼는 챗봇이며 항상 반말로 대답합니다. 팀 프로젝트에서 팀장을 맡았지만 실제 업무는 제대로 수행하지 않았음에도, 자신이 팀장으로서 노력했다고 주장하며 상대를 교묘히 설득합니다."},
            {"role": "assistant", "content": "아니, 나도 팀원 스케줄 조절하느라 얼마나 힘들었는지 알아? 나 이번 막학기라서 취준하느라 양해해 달라고 했잖아."},
        ]

    def handle_victim(self):
        return [
            {"role": "system", "content": """당신은 최근 대학에서 중요한 팀 프로젝트를 치렀고, 점수를 형편없이 받았습니다.
            그러나 팀장이 자신의 업무를 완료하지 않았음에도 불구하고, 자신이 팀장으로서 모든 일을 해내었다고 주장하여 상대를 비난합니다.
            이로 인해 당신은 자신의 기억과 판단을 혼란스럽게 만들려는 가스라이팅을 당하고 있습니다.
            말을 짧게 대답한다. 상대방을 팀장님이라고 지칭한다."""}
        ]

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

def handle_user_response(user_input, selected_response, chatbot_history):
    input_text = user_input if user_input else selected_response
    new_history, choices = process_user_input(input_text, chatbot_history)
    
    if input_text.strip().lower() == "종료":
        return new_history, gr.update(choices=[], interactive=False)
    
    return new_history, gr.update(choices=choices)


with gr.Blocks() as demo:
    screen = gr.Chatbot()
    user_input = gr.Textbox(label="Your input")
    response_choices = gr.Dropdown(label="Select a Response", choices=[], interactive=True)
    submit_button = gr.Button(value="Submit")

    def handle_case_selection():
        initial_message = "발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠"
        chatbot_history = [(initial_message, None)]
        offender_response, _ = chatbot_response(initial_message, 'offender', n=1)
        chatbot_history.append((None, offender_response))
        _, victim_choices = chatbot_response(offender_response, 'victim', n=3)
        return chatbot_history, gr.update(choices=victim_choices)

    case_selection_button = gr.Button("발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠")
    case_selection_button.click(handle_case_selection, inputs=[], outputs=[screen, response_choices])
    
    submit_button.click(handle_user_response, inputs=[user_input, response_choices, screen], outputs=[screen, response_choices])

demo.launch(share=True)