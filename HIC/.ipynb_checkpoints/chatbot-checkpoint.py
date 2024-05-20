import gradio as gr

dialogues = [
    {
        "당신": "나 오늘 시험을 진짜 망친 것 같아. 모든 걸 다 잊어버렸어.",
        "상대": "또 그 소리야? 너 항상 공부 안 한다고 하면서 막상 성적은 잘 나오잖아."
    },
    {
        "당신": "아니, 이번엔 진짜 달라. 정말 어려웠고, 나 준비도 충분히 못 했어.",
        "상대": "네가 충분히 준비 못한 건 항상 네 탓이야. 너무 게으르니까."
    },
    {
        "당신": "게으른 게 아니라, 최근에 너무 바빴어... 너도 알잖아.",
        "상대": "바쁘다는 건 핑계거리일 뿐이야. 진짜로 원하면 시간을 만들 수 있어. 너는 그냥 책임감이 없는 거야."
    },
    {
        "당신": "정말 그럴까? 나도 모르게 나태해진 건가...",
        "상대": "봐, 결국 너도 인정하잖아. 너 스스로를 더 잘 알아야 해."
    },
    {
        "당신": "그런데, 내가 정말로 잘못된 걸까? 아니면 너무 엄격하게 자신을 평가하는 걸까?",
        "상대": "넌 항상 자기 자신을 너무 쉽게 용서해. 이번에도 변명만 하고 있어. 내가 말하는 게 너너를 위한 거야. 나는 네가 더 나은 사람이 되길 원하니까."
    },
    {
        "당신": "네가 정말 나를 이해한다고 생각했는데, 왜 이렇게 느껴지지 않을까?",
        "상대": "나는 네가 최고가 되길 원해. 그러니 내 말을 듣고 반성해. 너무 감정에 치우치지 마."
    }
]

dialogue_index = [0]

def conduct_dialogue_with_preview(user_input,history):
    if dialogue_index[0] < len(dialogues):
        dialogue = dialogues[dialogue_index[0]]
        if user_input.strip() == dialogue["당신"]:
            response = f"{dialogue['상대']}"
            dialogue_index[0] += 1
            if dialogue_index[0] < len(dialogues):
                next_dialogue = dialogues[dialogue_index[0]]
                #response += f"\n\n{next_dialogue['당신']}"
            else:
                response += "\n\n대화가 종료되었습니다."
        else:
            response = "잘못 입력했습니다. 말한 내용을(기호 포함) 정확히 따라 쳐야 합니다."
    else:
        response = "대화가 이미 종료되었습니다."
    return response

iface = gr.ChatInterface(fn=conduct_dialogue_with_preview,
                     title="대화",
                     description="당신의 말을 정확히 따라 쳐주세요. 시작하려면, 아래 당신의 말을 입력하세요.",
                     examples=[[dialogues[0]["당신"]],[dialogues[1]["당신"]],[dialogues[2]["당신"]],[dialogues[3]["당신"]]])

iface.launch(share=True)