from dotenv import load_dotenv
import gradio as gr
from gradio_interface import create_interface

def main():
    load_dotenv()
    demo = create_interface()
    demo.launch(share=True)

if __name__ == "__main__":
    main()