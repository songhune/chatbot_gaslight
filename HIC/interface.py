import gradio as gr

def handle_case_selection(selected_case, process_selected_case):
    response_text, choices = process_selected_case(selected_case)
    return response_text, choices

def handle_user_response(user_input, selected_response, chatbot_history, process_user_input):
    new_history, choices = process_user_input(user_input, selected_response, chatbot_history)
    return new_history, choices

def create_interface(cases, process_selected_case, process_user_input):
    with gr.Blocks() as demo:
        dropdown = gr.Dropdown(choices=cases, label="Select a case:")
        chatbotbot = gr.Chatbot()
        user_input = gr.Textbox(label="Your input")
        
        response_choices = gr.Dropdown(label="Select a Response", choices=[], interactive=True)
        submit_button = gr.Button(value="Submit")
        clear_button = gr.Button("Clear")

        dropdown.change(lambda selected_case: handle_case_selection(selected_case, process_selected_case), 
                        inputs=dropdown, outputs=[chatbotbot, response_choices])
        submit_button.click(lambda user_input, selected_response, chatbot_history: handle_user_response(user_input, selected_response, chatbot_history, process_user_input),
                            inputs=[user_input, response_choices, chatbotbot], outputs=[chatbotbot, response_choices])
        clear_button.click(lambda: [], None, chatbotbot, queue=False)

    return demo
