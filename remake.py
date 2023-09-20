import random
import base64
import asyncio
import json
import httpx
import websockets


async def remake(image_url):
  hash = str(random.randint(1000, 999999999999))
  image_url = image_url

  async with httpx.AsyncClient() as client:
    response = await client.get(image_url)
    if response.status_code == 200:
      image_content = response.content
      base64_original = base64.b64encode(image_content).decode('utf-8')
      print("Image successfully fetched and base64 encoded.")
    else:
      print("Failed to fetch the image. Status code:", response.status_code)

  cookies = {
      '_ga_MM5J5X8QQC': 'GS1.1.1693409335.1.0.1693409335.0.0.0',
      '_ga': 'GA1.1.194095291.1693409336',
      '_ga_R1FN4KJKJH': 'GS1.1.1693437997.2.1.1693439238.0.0.0',
  }

  headers = {
      'User-Agent':
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
      'Accept': '*/*',
      'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
      # 'Accept-Encoding': 'gzip, deflate, br',
      'Referer': 'https://one-2-3-45-one-2-3-45.hf.space/?__theme=light',
      'Content-Type': 'application/json',
      'Origin': 'https://one-2-3-45-one-2-3-45.hf.space',
      'DNT': '1',
      'Connection': 'keep-alive',
      # 'Cookie': '_ga_MM5J5X8QQC=GS1.1.1693409335.1.0.1693409335.0.0.0; _ga=GA1.1.194095291.1693409336; _ga_R1FN4KJKJH=GS1.1.1693437997.2.1.1693439238.0.0.0',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      # Requests doesn't support trailers
      # 'TE': 'trailers',
  }

  json_data = {
    'data': [
        base64_original,
    ],
    'event_data': None,
    'fn_index': 6,
    'session_hash': hash,
  }

  async with httpx.AsyncClient(cookies=cookies, headers=headers) as client:
    response = await client.post(
        'https://one-2-3-45-one-2-3-45.hf.space/run/predict', json=json_data)
    base64_shape = response.json()["data"][0] + "=="

  async def gen1():
    uri = "wss://one-2-3-45-one-2-3-45.hf.space/queue/join"
    async with websockets.connect(uri) as websocket:
      x = json.loads(await websocket.recv())
      await websocket.send('{"fn_index":30,"session_hash":"' + hash + '"}')
      while x["msg"] != "send_data":
        x = json.loads(await websocket.recv())
      await websocket.send(
          '{"data":["' + base64_original + '",false,' +
          str(response.json()["data"][1]["value"]) + ',' +
          str(response.json()["data"][2]["value"]) + ',' +
          str(response.json()["data"][3]["value"]) + ',' +
          str(response.json()["data"][4]["value"]) +
          '],"event_data":null,"fn_index":26,"session_hash":"' + hash + '"}')

      while x["msg"] != "process_completed":
        x = json.loads(await websocket.recv())
      return x

  gen1_result = await gen1()

  async def gen2():
    uri = "wss://one-2-3-45-one-2-3-45.hf.space/queue/join"
    async with websockets.connect(uri, max_size=None) as websocket:
      x = json.loads(await websocket.recv())
      await websocket.send('{"fn_index":30,"session_hash":"' + hash + '"}')
      while x["msg"] != "send_data":
        x = json.loads(await websocket.recv())
      await websocket.send(
          '{"data":[null,"' + gen1_result["output"]["data"][0] +
          '",30,200],"event_data":null,"fn_index":28,"session_hash":"p9us2ikmvzs"}'
      )

      while x["msg"] != "process_completed":
        x = json.loads(await websocket.recv())
      return x

  gen2_result = await gen2()
  for n in range(2,10):
      output_name = "output"+str(n)+".png"
      base64_output = gen2_result["output"]["data"][n]

      prefix = "data:image/png;base64,"
      base64_data = base64_output[len(prefix):]

      base64_padding = base64_data + '=' * (-len(base64_data) % 4)

      decoded_image = base64.urlsafe_b64decode(base64_padding)

      output_file = output_name
      with open(output_file, 'wb') as f:
        f.write(decoded_image)

      print(f"Image saved as {output_file}")