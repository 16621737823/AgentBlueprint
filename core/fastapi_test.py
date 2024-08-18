from dotenv import load_dotenv
load_dotenv()
import message.APMFactory_pb2 as apm
from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse

from agent.agent_instance import AgentNetwork
from factory.deserializer import run_session

app = FastAPI()

async def generate_data(data: bytes):
    apm_file = apm.apmFile()
    apm_file.ParseFromString(data)
    agent = AgentNetwork()
    agent.check_version_file("load_modules/version.txt")
    async for response in run_session(apm_file, agent):
        yield str(response)

@app.post("/request-apm/")
async def create_item(request: Request):
    data = await request.body()
    # return {"file_size": len(data)}
    return StreamingResponse(generate_data(data),media_type="text/plain")