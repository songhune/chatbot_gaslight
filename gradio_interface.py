import gradio as gr
from chatbot_utils import process_user_input, chatbot_response

def create_interface():
    def handle_user_response(user_input, selected_response, chatbot_history):
        input_text = user_input if user_input else selected_response
        new_history, choices = process_user_input(input_text, chatbot_history)
        
        if input_text.strip().lower() == "종료":
            return new_history, gr.update(choices=[], interactive=False)
        
        return new_history, gr.update(choices=choices)

    def handle_case_selection():
        initial_message = "발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠"
        chatbot_history = [(initial_message, None)]
        offender_response, _ = chatbot_response(initial_message, 'offender', n=1)
        chatbot_history.append((None, offender_response))
        _, victim_choices = chatbot_response(offender_response, 'victim', n=3)
        return chatbot_history, gr.update(choices=victim_choices)

    with gr.Blocks() as demo:
        screen = gr.Chatbot()
        user_input = gr.Textbox(label="Your input")
        response_choices = gr.Dropdown(label="Select a Response", choices=[], interactive=True)
        submit_button = gr.Button(value="Submit")

        case_selection_button = gr.Button("발표가 망한 건 제 잘못도 좀 있지만, 팀장님은 아무것도 안 하면서 이러는 건 선 넘은거죠")
        case_selection_button.click(handle_case_selection, inputs=[], outputs=[screen, response_choices])
        
        submit_button.click(handle_user_response, inputs=[user_input, response_choices, screen], outputs=[screen, response_choices])

    return demo