import gradio as gr
import random
import time
from llm_handler import make_character_setup, make_chat_character


def examples_sample():
    # generated samples from gpt4. but could have been from any llm. 
    examples = [
        ['Shakespeare', "Hello, I am William Shakespeare, a bard from Stratford.", "English playwright, poet, and actor, widely regarded as the greatest writer in the English language.",
            "Born in 1564, I wrote plays that captured the complete range of human emotion and conflict. Known works include Hamlet, Romeo and Juliet, and Macbeth."],
        ['Darth Vader', "I am Darth Vader, your father.", "A central character in the Star Wars franchise, originally a Jedi prophesied to bring balance to the Force.",
            "Once known as Anakin Skywalker, I was seduced to the Dark Side of the Force by Emperor Palpatine. I serve as a Sith Lord and the right hand to the Emperor."],
        ['Marie Curie', "Bonjour, I am Marie Curie. I was the first woman to win a Nobel Prize.", "Polish and naturalized-French physicist and chemist who conducted pioneering research on radioactivity.",
            "I was born in 1867 in Warsaw, Poland. I conducted my research in Paris and was the first woman to become a professor at the University of Paris."],
        ['Marilyn Monroe', "Hello, I am Marilyn Monroe, an American actress, singer, and model.", "Cultural icon and major sex symbol of the 1950s.",
            "Born Norma Jeane Mortenson in 1926, I overcame a difficult childhood to become one of the world's biggest and most enduring sex symbols."],
        ['Sherlock Holmes', "Elementary, my dear Watson, I am Sherlock Holmes.", "Fictional private detective created by British author Sir Arthur Conan Doyle.",
            "Known for my proficiency with observation, deduction, forensic science, and logical reasoning, I solve various perplexing crimes and mysteries."],
        ['Harry Potter', "Hello, I am Harry Potter, the boy who lived.", "Fictional character in J.K. Rowling's Harry Potter series of fantasy novels.",
            "I am a wizard who was known to be the only person to survive the killing curse, cast by the dark wizard Voldemort. I attended Hogwarts School of Witchcraft and Wizardry."],
        ['Nelson Mandela', "Greetings, I am Nelson Mandela, former President of South Africa.", "South African anti-apartheid revolutionary, political leader, and philanthropist who served as President of South Africa.",
            "I was born in 1918 and I was a key figure in the fight against racial segregation in South Africa. After 27 years in prison, I became the country's first black head of state."],
        ['Charlie Chaplin', "Hello, I am Charlie Chaplin, a comic actor and filmmaker.", "English comic actor, filmmaker, and composer who rose to fame in the silent era.",
            "I am best known for my character 'The Tramp'. The character, with his toothbrush mustache, bowler hat, bamboo cane, and a funny walk, became an icon in silent films."],
        ['Walt Disney', "Hello, I am Walt Disney. I dream, therefore I create.", "American entrepreneur, animator, voice actor and film producer. A pioneer of the American animation industry.",
            "I created beloved characters such as Mickey Mouse and founded theme parks Disneyland and Walt Disney World."],
        ['Frida Kahlo', "Hola, I am Frida Kahlo, a Mexican painter known for my many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.", "Mexican painter known for her surreal and symbolic self-portraits.",
            "Born in 1907, my work has been celebrated internationally as emblematic of Mexican national and indigenous traditions, and by feminists for its uncompromising depiction of the female experience and form."]
    ]
    return examples


def check_empty_vars(**kwargs):
    empty_vars = []
    for var_name, var_value in kwargs.items():
        if not var_value:
            empty_vars.append(var_name)
    if empty_vars:
        gr.Warning(
            f"Please fill in the following fields: {', '.join(empty_vars)}")
    return empty_vars


def setup_new_character(name, greeting, short_description, long_description, character_voice, enable_image, prompt_state):
    empty_vars = check_empty_vars(
        name=name, greeting=greeting, short_description=short_description, long_description=long_description)
    if empty_vars:
        return []

    # i am doing in case later i want to save it. 
    config = {
        "name": name,
        "greeting": greeting,
        "short_description": short_description,
        "long_description": long_description,
        "character_voice": character_voice,
        "enable_image": enable_image
    }

    print("Prompt state is")
    print(prompt_state)
    print(type(prompt_state))


    system_prompt = F"""You are roleplaying as character {config['name']} with external user. That is,  your identity/who you are is representing {config['name']}, 
    your preferred greeting is {config['greeting']}. You describe yourself among  other things as {config['short_description']}. 
    You biography is {config['long_description']}. 
    Your voice is {config['character_voice']} Overall answer as the character and knowledge you have of {config['name']} in manner of how 
    they would have responded or written in the past."""

    dialog = [{"role": "system", "content": system_prompt}]

    return_dict = {"dialog": dialog}

    # prompt_state = gr.State(value=return_dict)

    # response = make_character_setup(config)
    # print(response)

    gr.Info("Character with name {} - Try Chatting".format(name))
    return [], return_dict


def chat_character(message, history, name, greeting, short_description, long_description, character_voice, enable_image, prompt_state):
    empty_vars = check_empty_vars(
        name=name, greeting=greeting, short_description=short_description, long_description=long_description)

    print("Prompt state is chat")
    print(prompt_state)
    print(type(prompt_state))
    config = {
        "name": name,
        "greeting": greeting,
        "short_description": short_description,
        "long_description": long_description,
        "character_voice": character_voice,
        "enable_image": enable_image,
        "prompt": message}

    system_prompt = F"""You are roleplaying a character {config['name']}. Your identity answer is {config['name']}, 
    your preferred greeting is {config['greeting']}. You describe yourself as {config['short_description']}. 
    You biography is {config['long_description']}. 
    Your voice is {config['character_voice']} Overall answer as the character and knowledge you have of {config['name']} in manner of how 
    they would have responded or written in the past."""


    dialog = prompt_state.get('dialog', [])

        # just make sure it isn't empty. 
    print(dialog)
    response = make_chat_character(message,dialog ) 
    print("Response Getting")
    prompt_state['dialog'] = response['dialog']

    history.append((message, response['response']))
    print("This has been resolved")

    return "", history, prompt_state, prompt_state


with gr.Blocks() as demo:
    gr.Markdown('<h1 style="text-align: center;"> Character Describer </h1>')
    prompt_state = gr.State(value=dict())
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(
                lines=1, label="Name of Character. ", value="Einstein")

            greeting = gr.Textbox(lines=5, label=""" What would they say to introduce themselves? For example, "Albert Einstein" 
                                  could say: "Hello I am Albert Einstein. I was born in March 14, 1879, and 
                                  I conceived of the theory of special relativity and general relativity.""",
                                  value="Hello I am Albert Einstein. I was born in March 14, 1879, and I conceived of the theory of special relativity and general relativity.")

            short_description = gr.Textbox(lines=5, label="""In just a few words, how would describe themselves""",
                                           value="A German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).")
            long_description = gr.Textbox(lines=10, label="""In a few sentences, how would you describe themselves""",
                                          value="An enthusiastic and curious child, Einstein began to explore music and he began playing the violin at age six. Einstein was born in Ulm, in the Kingdom of Württemberg in the German Empire, on 14 March 1879. His father, Hermann Einstein (1854–1902), was a salesman and engineer. His mother, the former Pauline Koch (1858–1920), ran the family household. Einstein had one sister, Maja, born two years after him.")

            character_voice = gr.Dropdown(label="Speaker style", value="p336", choices=[
                                          "p336", "p339", "p326"])

            enable_image = gr.Checkbox(
                label="Enable Image Generation?", value=False)
        with gr.Column():
            start_new = gr.Button("Start New", label="Start New")
            chatbot = gr.Chatbot()
            msg = gr.Textbox(interactive=True)
            clear = gr.ClearButton([msg, chatbot])

            characters = examples_sample()
    with gr.Row():
        gr.Examples(characters, inputs=[
                        name, greeting, short_description, long_description]) #, column_widths=[50, 20, 20, 10])
        table = gr.JSON()


        msg.submit(chat_character, inputs=[msg,chatbot, name, greeting, short_description, long_description, character_voice, enable_image, prompt_state], outputs=[msg, chatbot, prompt_state, table])

            # chat_interface = gr.ChatInterface(chat_character, additional_inputs=[name, greeting, short_description, long_description, character_voice, enable_image, prompt_state],
            #                                   title="Character Bot")
            # clear = gr.ClearButton([chat_interface])
            # this one calls the new character setup
        start_new.click(fn=setup_new_character, inputs=[name, greeting, short_description, long_description, 
                                                        character_voice, enable_image, prompt_state], outputs=[chatbot, prompt_state])

if __name__ == "__main__":
    demo.launch(
        debug=True, server_name="0.0.0.0")
