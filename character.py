import gradio as gr
import random
import time
from llm_handler import make_character_setup, make_chat_character


def setup_new_character(name, greeting, short_description, long_description, character_voice, enable_image):
    config = {'config':{
        "name": name,
        "greeting": greeting,
        "short_description": short_description,
        "long_description": long_description,
        "character_voice": character_voice,
        "enable_image": enable_image
    }}
    response = make_character_setup(config)
    print(response)

    # gr.Info("Character with name {} - {}".format(name, response['response']))

    # how do i clear the chatinterface history here
    # https://discuss.huggingface.co/t/clear-chat-interface/49866/6
    return []

def chat_character(message, history, name, greeting, short_description, long_description, character_voice, enable_image):
    config = {"config":{
        "name": name,
        "greeting": greeting,
        "short_description": short_description,
        "long_description": long_description,
        "character_voice": character_voice,
        "enable_image": enable_image
    }, "prompt":message}

    response = make_chat_character(config, "")

    return response['response']




with gr.Blocks(theme="gradio/monochrome") as demo:
    gr.Markdown('<h1 style="text-align: center;"> Character Describer </h1>')
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(lines=1, label="Name of Character. ", value="Einstein")

            greeting = gr.Textbox(lines=5, label=""" What would they say to introduce themselves? For example, "Albert Einstein" 
                                  could say: "Hello I am Albert Einstein. I was born in March 14, 1879, and 
                                  I conceived of the theory of special relativity and general relativity.""", 
                                  value="Hello I am Albert Einstein. I was born in March 14, 1879, and I conceived of the theory of special relativity and general relativity.")
                                
            short_description = gr.Textbox(lines=5, label="""In just a few words, how would describe themselves""", 
                                           value="A German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).")
            long_description = gr.Textbox(lines=10, label="""In a few sentences, how would you describe themselves""", value="An enthusiastic and curious child, Einstein began to explore music and he began playing the violin at age six. Einstein was born in Ulm, in the Kingdom of Württemberg in the German Empire, on 14 March 1879. His father, Hermann Einstein (1854–1902), was a salesman and engineer. His mother, the former Pauline Koch (1858–1920), ran the family household. Einstein had one sister, Maja, born two years after him.")
            
            character_voice = gr.Dropdown(label="Speaker style", value="p336", choices=["p336", "p339", "p326"])
            
            enable_image = gr.Checkbox(label="Enable Image Generation?", value=False)


    with gr.Row():
        with gr.Column():
            start_new = gr.Button("Start New", label="Start New")
            def response(message, chat_history):
                bot_message = random.choice(["I am a bot", "I am a human"])
                return bot_message
            chat_interface = gr.ChatInterface(chat_character, additional_inputs=[name, greeting, short_description, long_description, character_voice, enable_image], 
                                              title="Character Bot")

            clear = gr.ClearButton([chat_interface])

            # this one calls the new character setup
            start_new.click(fn=setup_new_character, inputs=[name, greeting, short_description, long_description, character_voice, enable_image], outputs=[chat_interface.chatbot_state])



if __name__ == "__main__":
    demo.launch(debug=True, server_port = 9000, server_name="0.0.0.0") 