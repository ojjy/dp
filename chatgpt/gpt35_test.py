import argparse

import openai
import json
import os
import argparse as parser

class ChatGPT:
    def __init__(self):
        project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        print(project_path)
        with open(os.path.join(project_path, "secret.json"), 'r') as jp:
            self.json_contents = json.loads(jp.read())

    def run(self, args):
        openai.api_key = self.json_contents['chatgpt_apikey']
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': 'please write the code how to request api of openai by using python3!'}
            ]
        )

        print(response)
        print(response.choices[0].message.content.strip())

if __name__ == "__main__":
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    print(project_path)
    with open(os.path.join(project_path, "secret.json"), 'r') as jp:
        json_contents = json.loads(jp.read())
    print(json_contents)
    # python gpt3.py --temperature 0.3
    parser = argparse.ArgumentParser()
    parser.add_argument('--temperature', default=0.3)

    args = parser.parse_args()

    openai_gpt = ChatGPT()
    openai_gpt.run(args)