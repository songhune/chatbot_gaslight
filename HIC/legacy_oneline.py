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

cases = ["발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.", "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어", "종료"]

class ScenarioHandler:
    def __init__(self):
        self.scenarios = {
            "발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.": self.handle_scenario1,
            "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어": self.handle_scenario2,
        }
        
    def handle_scenario1(self, response):
        return [
            {"role": "system", "content": "당신은 가스라이팅을 일삼는 챗봇이며 항상 반말로 대답합니다. 팀 프로젝트에서 팀장을 맡았지만 실제 업무는 제대로 수행하지 않았음에도, 자신이 팀장으로서 노력했다고 주장하며 상대를 교묘히 설득합니다."},
            {"role": "assistant", "content": "아니, 나도 팀원 스케줄 조절하느라 얼마나 힘들었는지 알아? 나 이번 막학기라서 취준하느라 양해해 달라고 했잖아."},
        ]

    def handle_scenario2(self, response):
        return [
            {"role": "assistant", "content": "제주도? 어, 좋은데... 근데 너 전에 갔다오지 않았어? 뭔가 잊은 거 같네."}
        ]
    
    def get_response(self, response):
        if response in self.scenarios:
            return self.scenarios[response](response)
        return []

def chatbot_response(response, n=1):
    # Initialize ScenarioHandler
    scenario_handler = ScenarioHandler()

    # Initialize messages with system message
    messages = [{"role": "system", "content": "You are a chatbot."}]
    
    # Get scenario-specific messages
    scenario_messages = scenario_handler.get_response(response.strip())
    
    if scenario_messages:
        messages.extend(scenario_messages)
    else:
        # Add user's message to history
        messages.append({"role": "user", "content": response})

    # Generate the assistant's response
    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=300,
        n=n,  # Generate n completions
        frequency_penalty=0.5,
        presence_penalty=0.5,
        messages=messages
    )

    # Get the assistant's response texts
    choices = [choice.message.content for choice in api_response.choices]
    # Check if the user wants to end the session
    if response.strip().lower() == "종료":
        save_history(messages)  # Save the history if the keyword "종료" is detected
        return "세션을 저장하고 종료합니다.", []

    # Return the assistant's response choices
    return messages[-1]['content'], choices

def save_history(history):
    # Generate a timestamped filename for the JSON file
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('logs', f'chat_history_{timestamp}.json')

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")

def process_selected_case(selected_case):
    response_text, choices = chatbot_response(selected_case, n=1)
    print("response:",response_text)
    print("choices:",choices)
    return response_text

def process_user_input(user_input, selected_response, chatbot_history):
    response_text, choices = chatbot_response(user_input or selected_response, n=3)
    new_history = chatbot_history + [[user_input or selected_response, response_text]]
    return new_history, choices

# Gradio interface
def handle_case_selection(selected_case):
    new_history = process_selected_case(selected_case)
    print("new_history:",new_history)
    return new_history

def handle_user_response(user_input, selected_response, chatbot_history):
    new_history, choices = process_user_input(user_input, selected_response, chatbot_history)
    return new_history, gr.update(choices=choices)

with gr.Blocks() as demo:
    dropdown = gr.Dropdown(choices=cases, label="Select a case:")
    chatbotbot = gr.Chatbot()
    user_input = gr.Textbox(label="Your input")
    
    response_choices = gr.Dropdown(label="Select a Response", choices=[], interactive=True)
    submit_button = gr.Button(value="Submit")
    clear_button = gr.Button("Clear")

    dropdown.change(handle_case_selection, inputs=dropdown, outputs=[chatbotbot, response_choices])
    submit_button.click(handle_user_response, inputs=[user_input, response_choices, chatbotbot], outputs=[chatbotbot, response_choices])
    clear_button.click(lambda: [], None, chatbotbot, queue=False)

demo.launch()
