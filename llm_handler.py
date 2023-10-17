import requests

character_setup = "http://100.76.16.85:8516/setup_character"
character_ask = "http://100.76.16.85:8516/chat_character"

def make_character_setup(config):
    response = requests.post(character_setup, json=config)
    print(response)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error on the backend"
def make_chat_character(config, chat_history):
    response = requests.post(character_ask, json=config)
    print(response)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error on the backend"