import requests

character_setup = "http://100.76.16.85:8516/setup_character"
character_ask = "http://100.76.16.85:8516/chat_character"

def make_character_setup(config):
    response = requests.post(character_setup, json=config)
    return response.json()
def chat_character(config, chat_history):
    response = requests.post(character_ask, json=config)
    return response.json()