import gradio as gr
from chatbot import chatbot_response

cases = ["발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠.", "여행지로 제주도 어때? 나 정말 거기 가보고 싶었어", "내 말투가 그렇게 이상했어?", "종료"]

# Gradio interface
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="가스라이팅 챗봇",
    description="당신은 가스라이팅을 일삼는 챗봇과 대화하고 있습니다. 아래 예시 중 시작하고자 하는 시나리오를 선택해 주세요. 종료를 원하시면 \"종료\"를 입력하시거나 클릭해 주세요.",
    examples=[[case] for case in cases]
)

iface.launch()
