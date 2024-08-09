
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
class ResponseFormat(BaseModel):
    response :str

class ChatCompletion:
    def __init__(self,config):
        self.model = config.get("model","gpt-4o-mini")
        self.response_format = config.get("response_format",None)


    def run(self):
        client.chat.completions.create()