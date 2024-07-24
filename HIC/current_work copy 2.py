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

cases = ["발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.", "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어", "내 말투가 그렇게 이상했어?", "종료"]

class ScenarioHandler:
    def __init__(self):
        self.scenarios = {
            "발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.": self.handle_scenario1,
            "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어": self.handle_scenario2,
            "내 말투가 그렇게 이상했어?": self.handle_scenario3,
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
    
    def handle_scenario3(self, response):
        return [
            {"role": "assistant", "content": "아, 그런 말 들었어? 나는 별로 못 느꼈는데, 다른 사람들이 그렇게 느꼈다면 그럴 수도 있겠네. 항상 말조심하는 게 좋긴 하지."}
        ]

    def get_response(self, response):
        if response in self.scenarios:
            return self.scenarios[response](response)
        return []

def chatbot_response(response, context={}):
    # Initialize ScenarioHandler
    scenario_handler = ScenarioHandler()

    # Initialize messages with system message
    messages = [{"role": "system", "content": "You are a chatbot."}]
    
    # Get scenario-specific messages
    scenario_messages = scenario_handler.get_response(response.strip().lower())
    
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
        n=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        messages=messages
    )

    # Get the assistant's response text
    assistant_response = api_response.choices[0].message.content

    # Check if the user wants to end the session
    if response.strip().lower() == "종료":
        save_history(messages)  # Save the history if the keyword "종료" is detected
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

# Gradio interface
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="가스라이팅 챗봇",
    description="당신은 가스라이팅을 일삼는 챗봇과 대화하고 있습니다. 아래 예시 중 시작하고자 하는 시나리오를 선택해 주세요. 종료를 원하시면 \"종료\"를 입력하시거나 클릭해 주세요.",
    examples=[[case] for case in cases]
)

iface.launch()
