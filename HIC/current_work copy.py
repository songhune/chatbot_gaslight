import gradio as gr
import openai

# OpenAI API 키 설정

# 챗봇 함수 정의
def chatbot(messages, state):
    # Gradio messages 포맷을 OpenAI messages 포맷으로 변환
    openai_messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for message in messages:
        openai_messages.append({"role": message['role'], "content": message['message']})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 사용하려는 모델명
        messages=openai_messages
    )
    return response['choices'][0]['message']['content']

# Gradio ChatInterface 설정
with gr.Blocks() as demo:
    chat_interface = gr.ChatInterface(chatbot)

# 인터페이스 실행
demo.launch()