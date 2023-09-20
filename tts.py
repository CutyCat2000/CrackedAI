import asyncio
import random
import websockets
import json

async def tts(text, voice):
    uri = "wss://elevenlabs-tts.hf.space/queue/join"
    hash = str(random.randint(1000000,99999999))
    async with websockets.connect(uri) as websocket:
      x = await websocket.recv()
      await websocket.send('{"fn_index":0,"session_hash":"'+hash+'"}')
      while json.loads(x)["msg"] != "send_data":
        x = await websocket.recv()
      await websocket.send('{"data":["'+text+'","'+voice+'"],"event_data":null,"fn_index":0,"session_hash":"'+hash+'"}')
      while json.loads(x)["msg"] != "process_completed":
        x = await websocket.recv()
      return "https://elevenlabs-tts.hf.space/file="+json.loads(x)["output"]["data"][0]["name"]
