import os
from dotenv import load_dotenv
from openai import OpenAI
from interface import create_interface
from chatbot import chatbot_response, save_history

# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

cases = ["발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.", "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어", "종료"]

def process_selected_case(selected_case):
    response_text, choices = chatbot_response(selected_case, client, n=1)
    return [("user", selected_case), ("assistant", response_text)], choices

def process_user_input(user_input, selected_response, chatbot_history):
    response_text, choices = chatbot_response(user_input or selected_response, client, n=3)
    new_history = chatbot_history + [("user", user_input or selected_response), ("assistant", response_text)]
    return new_history, choices

if __name__ == "__main__":
    demo = create_interface(cases, process_selected_case, process_user_input)
    demo.launch(debug=True)
