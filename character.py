import gradio as gr
import random
import time


with gr.Blocks(theme="gradio/monochrome") as demo:
    gr.Markdown('<h1 style="text-align: center;"> Character Describer </h1>')
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(lines=1, label="Name of Character. ")

            greeting = gr.Textbox(lines=5, label=""" What would they say to introduce themselves? For example, "Albert Einstein" 
                                  could say: "Hello I am Albert Einstein. I was born in March 14, 1879, and 
                                  I conceived of the theory of special relativity and general relativity.""")
                                
            short_description = gr.Textbox(lines=5, label="""In just a few words, how would describe themselves""")
            long_description = gr.Textbox(lines=10, label="""In a few sentences, how would you describe themselves""")
            
            character_voice = gr.Dropdown(label="Speaker style", choices=["p336", "p339", "p326"])
            
            enable_image = gr.Checkbox(label="Enable Image Generation?")


    with gr.Row():
        with gr.Column():
            start_new = gr.Button("Start New", label="Start New")
            def response(message, chat_history):
                bot_message = random.choice(["I am a bot", "I am a human"])
                return bot_message
            chat_interface = gr.ChatInterface(response, title="Character Bot")

            clear = gr.ClearButton([chat_interface])



if __name__ == "__main__":
    demo.launch(debug=True, server_port = 9000, server_name="0.0.0.0") 