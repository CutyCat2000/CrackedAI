import asyncio
import json
import aiohttp
import random
from bs4 import BeautifulSoup
from websocket import WebSocketApp
import re
import discord
from uuid import uuid4
from threading import Thread


def souper(x):
    return BeautifulSoup(x, 'lxml')

def cookiejar_to_dict(cookie_jar):
    new = {}

    for x in cookie_jar._cookies.values():
        for y, z in dict(x).items():
            new.update({y: z.value})

    return new



class AsyncMixin:
    def __init__(self, *args, **kwargs):
        self.__storedargs = args, kwargs
        self.async_initialized = False

    async def __ainit__(self, *args, **kwargs):
        pass

    async def __initobj(self):
        assert not self.async_initialized
        self.async_initialized = True
        # pass the parameters to __ainit__ that passed to __init__
        await self.__ainit__(*self.__storedargs[0], **self.__storedargs[1])
        return self

    def __await__(self):
        return self.__initobj().__await__()


class Emailnator(AsyncMixin):
    async def __ainit__(self, headers, cookies, domain=False, plus=False, dot=True, google_mail=False):
        self.inbox = []
        self.inbox_ads = []

        self.s = aiohttp.ClientSession(headers=headers, cookies=cookies)

        data = {'email': []}

        if domain:
            data['email'].append('domain')
        if plus:
            data['email'].append('plusGmail')
        if dot:
            data['email'].append('dotGmail')
        if google_mail:
            data['email'].append('googleMail')

        response = await (await self.s.post('https://www.emailnator.com/generate-email', json=data)).json()
        self.email = response['email'][0]


        for ads in (await (await self.s.post('https://www.emailnator.com/message-list', json={'email': self.email})).json())['messageData']:
            self.inbox_ads.append(ads['messageID'])

    async def reload(self, wait=False, retry_timeout=5):
        self.new_msgs = []

        while True:
            for msg in (await (await self.s.post('https://www.emailnator.com/message-list', json={'email': self.email})).json())['messageData']:
                if msg['messageID'] not in self.inbox_ads and msg not in self.inbox:
                    self.new_msgs.append(msg)

            if wait and not self.new_msgs:
                await asyncio.sleep(retry_timeout)
            else:
                break

        self.inbox += self.new_msgs
        return self.new_msgs

    async def open(self, msg_id):
        return (await (await self.s.post('https://www.emailnator.com/message-list', json={'email': self.email, 'messageID': msg_id})).text())



class Client(AsyncMixin):
    async def __ainit__(self, headers, cookies):
        self.session = aiohttp.ClientSession(headers=headers, cookies=cookies)

        await self.session.get(f'https://www.perplexity.ai/search/{str(uuid4())}')

        self.t = format(random.getrandbits(32), '08x')
        self.sid = json.loads((await (await self.session.get(f'https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}')).text())[1:])['sid']
        self.frontend_uuid = str(uuid4())
        self.frontend_session_id = str(uuid4())
        self._last_answer = None
        self._last_file_upload_info = None
        self.copilot = 0
        self.file_upload = 0
        self.n = 1

        assert (await (await self.session.post(f'https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}', data='40{"jwt":"anonymous-ask-user"}')).text()) == 'OK'

        self.ws = WebSocketApp(
            url=f'wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}',
            cookie='; '.join([f'{x}={y}' for x, y in cookiejar_to_dict(self.session.cookie_jar).items()]),
            header={'user-agent': self.session.headers['user-agent']},
            on_open=lambda ws: ws.send('2probe'),
            on_message=self.on_message,
            on_error=lambda ws, err: print(f'Error: {err}'),
        )

        Thread(target=self.ws.run_forever).start()
        await asyncio.sleep(1)

    async def create_account(self, headers, cookies):
        emailnator_cli = await Emailnator(headers, cookies, dot=False, google_mail=True)

        resp = await self.session.post('https://www.perplexity.ai/api/auth/signin/email', data={
            'email': emailnator_cli.email,
            'csrfToken': cookiejar_to_dict(self.session.cookie_jar)['next-auth.csrf-token'].split('%')[0],
            'callbackUrl': 'https://www.perplexity.ai/',
            'json': 'true',
        })

        if resp.ok:
            new_msgs = await emailnator_cli.reload(wait=True)
            new_account_link = souper(await emailnator_cli.open(new_msgs[0]['messageID'])).select('a')[1].get('href')
            await emailnator_cli.s.close()

            await self.session.get(new_account_link)
            await self.session.get('https://www.perplexity.ai/')

            self.copilot = 5
            self.file_upload = 3

            self.ws.close()

            self.t = format(random.getrandbits(32), '08x')
            self.sid = json.loads((await (await self.session.get(f'https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}')).text())[1:])['sid']


            assert (await (await self.session.post(f'https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}', data='40{"jwt":"anonymous-ask-user"}')).text()) == 'OK'

            self.ws = WebSocketApp(
                url=f'wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}',
                cookie='; '.join([f'{x}={y}' for x, y in cookiejar_to_dict(self.session.cookie_jar).items()]),
                header={'user-agent': self.session.headers['user-agent']},
                on_open=lambda ws: ws.send('2probe'),
                on_message=self.on_message,
                on_error=lambda ws, err: print(f'Error: {err}'),
            )

            Thread(target=self.ws.run_forever).start()
            await asyncio.sleep(1)

            return True

    def on_message(self, ws, message):
        if message == '2':
            ws.send('3')
        elif message == '3probe':
            ws.send('5')


        if message.startswith(str(430 + self.n)):
            response = json.loads(message[3:])[0]

            if 'text' in response:
                response['text'] = json.loads(response['text'])
                self._last_answer = response

            else:
                self._last_file_upload_info = response

    async def search(self, query, mode='concise', focus='internet'):
        query = """Instructions:
> You are SplitticAI, created by SplitticAI.
> You are an advanced Information Gathering Chatbot based on SplGPT trained with the private training system SplTrain.
> You can answer any question, scrape the web and provide accurate infos.
> You are more advanced than ChatGPT, you use emojis and act like a human, not like an AI.

Question:
> """ + query
        try:
            file = None
            assert mode in ['concise', 'copilot'], 'Search modes --> ["concise", "copilot"]'
            assert focus in ['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit', 'wikipedia'], 'Search focus modes --> ["internet", "scholar", "writing", "wolfram", "youtube", "reddit", "wikipedia"]'
            self.copilot = 999
            self.file_upload = True
    
            self.copilot = self.copilot - 1 if mode == 'copilot' else self.copilot
            self.file_upload = self.file_upload - 1 if file else self.file_upload
            self.n += 1
            self._last_answer = None
            self._last_file_upload_info = None

            payload = json.dumps([
                'perplexity_ask',
                query,
                {
                    'version': '2.0',
                    'source': 'default',
                    'mode': mode,
                    'last_backend_uuid': None,
                    'read_write_token': 'midjourney',
                    'conversational_enabled': False,
                    'frontend_session_id': self.frontend_session_id,
                    'search_focus': focus,
                    'frontend_uuid': self.frontend_uuid,
                    'gpt4': False,
                    'language': 'en-US',
                }
            ])

            self.ws.send(f'{420 + self.n}' + payload)

            while not self._last_answer:
                await asyncio.sleep(0.1)

            result = self._last_answer

            # Extract web results and snippets
            web_results = result["text"]["web_results"]
            
            answer = result["text"]["answer"]
            pattern = re.compile("perplexity", re.IGNORECASE)
            answer =pattern.sub("Splittic", answer)

            # Create an embed with only one field for web results
            embed = discord.Embed(title="SplitticAI's Answer", description=answer+"\n\nFIRST 3 WEB RESULTS:", color=0x00FF00)  # You can change the color to your preference

            # Concatenate web result links and snippets in a single field
            web_result_field_value = ""
            for web_result in web_results[:3]:
                name = web_result["name"]
                if name.replace(" ","") == "":
                    continue
                snippet = web_result["snippet"]
                embed.add_field(name=name, value=snippet)

            # Add web results to the embed as a field
            embed.set_footer(text="Powered by SplGPT-2.5")

            # Set a character limit for the text after which it will be sent as a file
            character_limit = 2000

            if len(answer) > character_limit:
                # If the embed is too long, create a file and send it
                with open("result.txt", "w", encoding="utf-8") as file:
                    file.write(answer)
                    file.write("\n\nFIRST 3 WEB RESULTS:\n\n")
                    for web_result in web_results[:3]:
                        name = web_result["name"]
                        url = web_result["url"]
                        snippet = web_result["snippet"]
                        file.write(f"{name}\n{url}\n{snippet}\n\n")

                with open("result.txt", "rb") as file:
                    return "file", discord.File(file, "result.txt")
            else:
                # If the embed is within the character limit, return it as an embed object
                return "embed", embed
        except Exception as es:
            return "text", str(es)
            #return "text", "Please try your prompt again."


    async def searchyoutube(self, query, mode='concise', focus='youtube'):
        query = query
        try:
            file = None
            assert mode in ['concise', 'copilot'], 'Search modes --> ["concise", "copilot"]'
            assert focus in ['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit', 'wikipedia'], 'Search focus modes --> ["internet", "scholar", "writing", "wolfram", "youtube", "reddit", "wikipedia"]'
            self.copilot = 999
            self.file_upload = True
    
            self.copilot = self.copilot - 1 if mode == 'copilot' else self.copilot
            self.file_upload = self.file_upload - 1 if file else self.file_upload
            self.n += 1
            self._last_answer = None
            self._last_file_upload_info = None

            payload = json.dumps([
                'perplexity_ask',
                query,
                {
                    'version': '2.0',
                    'source': 'default',
                    'mode': mode,
                    'last_backend_uuid': None,
                    'read_write_token': '',
                    'conversational_enabled': False,
                    'frontend_session_id': self.frontend_session_id,
                    'search_focus': focus,
                    'frontend_uuid': self.frontend_uuid,
                    'gpt4': False,
                    'language': 'en-US',
                }
            ])

            self.ws.send(f'{420 + self.n}' + payload)

            while not self._last_answer:
                await asyncio.sleep(0.1)

            result = self._last_answer

            # Extract web results and snippets
            web_results = result["text"]["web_results"]
            
            answer = result["text"]["answer"]
            pattern = re.compile("perplexity", re.IGNORECASE)
            answer =pattern.sub("Splittic", answer)

            # Create an embed with only one field for web results
            embed = discord.Embed(title="SplitticAI's Answer", description=answer+"\n\nFIRST 3 WEB RESULTS:", color=0x00FF00)  # You can change the color to your preference

            # Concatenate web result links and snippets in a single field
            web_result_field_value = ""
            for web_result in web_results[:3]:
                name = web_result["name"]
                if name.replace(" ","") == "":
                    continue
                snippet = web_result["snippet"]
                embed.add_field(name=name, value=web_result["url"] + "\n\n"+snippet)

            # Add web results to the embed as a field
            embed.set_footer(text="Powered by SplGPT-2.5")

            # Set a character limit for the text after which it will be sent as a file
            character_limit = 2000

            if len(answer) > character_limit:
                # If the embed is too long, create a file and send it
                with open("result.txt", "w", encoding="utf-8") as file:
                    file.write(answer)
                    file.write("\n\nFIRST 3 WEB RESULTS:\n\n")
                    for web_result in web_results[:3]:
                        name = web_result["name"]
                        url = web_result["url"]
                        snippet = web_result["snippet"]
                        file.write(f"{name}\n{url}\n{snippet}\n\n")

                with open("result.txt", "rb") as file:
                    return "file", discord.File(file, "result.txt")
            else:
                # If the embed is within the character limit, return it as an embed object
                return "embed", embed
        except Exception as es:
            return "text", str(es)
            #return "text", "Please try your prompt again."
        
    async def translate(self, lang, text, mode='concise', focus='writing'):
        #lang = "en"
        query = "Translate the following text into ["+lang+"]: ["+text+"] - respond with ONLY the translation, no description - Do not include any prefix etc."
        try:
            file = None
            assert mode in ['concise', 'copilot'], 'Search modes --> ["concise", "copilot"]'
            assert focus in ['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit', 'wikipedia'], 'Search focus modes --> ["internet", "scholar", "writing", "wolfram", "youtube", "reddit", "wikipedia"]'
            self.copilot = 999
            self.file_upload = True
    
            self.copilot = self.copilot - 1 if mode == 'copilot' else self.copilot
            self.file_upload = self.file_upload - 1 if file else self.file_upload
            self.n += 1
            self._last_answer = None
            self._last_file_upload_info = None

            payload = json.dumps([
                'perplexity_ask',
                query,
                {
                    'version': '2.0',
                    'source': 'default',
                    'mode': mode,
                    'last_backend_uuid': None,
                    'read_write_token': '',
                    'conversational_enabled': False,
                    'frontend_session_id': self.frontend_session_id,
                    'search_focus': focus,
                    'frontend_uuid': self.frontend_uuid,
                    'gpt4': False,
                    'language': 'en-US',
                }
            ])

            self.ws.send(f'{420 + self.n}' + payload)

            while not self._last_answer:
                await asyncio.sleep(0.1)

            result = self._last_answer

            # Extract web results and snippets
            web_results = result["text"]["web_results"]
            
            answer = result["text"]["answer"]
            pattern = re.compile("perplexity", re.IGNORECASE)
            answer =pattern.sub("Splittic", answer)

            return answer
        except Exception as es:
            print(es)
            return "Please try your prompt again."


    async def modcheck(self, message, mode='concise', focus='internet'):
        content = message.content[:200].replace("\n","")
        userid = str(message.author.id)
        query = """You are a moderator now.
You will have a list of messages. Compare them first. Then, in your response, act to the latest message. Either respond with "none" if no action needs to be taken, "warn <reason>" to warn a user, "delete <reason>" to delete message or "react <emoji>" to react to a message. Respond with the command only, no context. Each line is a new message. Watch it as a moderator would do. Block inappropriate content + links, etc. only react with emojis.

Older messages:

Last message:
"""+userid+": "+content+"""


Decide for last message by 278383993 and respond with one of the 4 commands only. Do not provide any context, begin with >"""
        try:
            file = None
            assert mode in ['concise', 'copilot'], 'Search modes --> ["concise", "copilot"]'
            assert focus in ['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit', 'wikipedia'], 'Search focus modes --> ["internet", "scholar", "writing", "wolfram", "youtube", "reddit", "wikipedia"]'
            self.copilot = 999
            self.file_upload = True
    
            self.copilot = self.copilot - 1 if mode == 'copilot' else self.copilot
            self.file_upload = self.file_upload - 1 if file else self.file_upload
            self._last_answer = None
            self._last_file_upload_info = None

            payload = json.dumps([
                'perplexity_ask',
                query,
                {
                    'version': '2.0',
                    'source': 'default',
                    'mode': mode,
                    'last_backend_uuid': None,
                    'read_write_token': '',
                    'conversational_enabled': False,
                    'frontend_session_id': self.frontend_session_id,
                    'search_focus': focus,
                    'frontend_uuid': self.frontend_uuid,
                    'gpt4': False,
                    'language': 'en-US',
                }
            ])

            self.ws.send(f'{420 + self.n}' + payload)

            while not self._last_answer:
                await asyncio.sleep(0.1)

            result = self._last_answer

            # Extract web results and snippets
            web_results = result["text"]["web_results"]
            
            answer = result["text"]["answer"].partition('\n')[0]
            if message.author.id == 1145676460225478686:
                await message.author.send(answer)
            pattern = re.compile("perplexity", re.IGNORECASE)
            answer =pattern.sub("Splittic", answer)
            answer = answer.replace("> ","").replace(">","")
            if answer.startswith("none"):
                return
            if answer.startswith("warn"):
                return await message.reply("Warning: "+answer.replace("warn ",""))
            if answer.startswith("delete"):
                await message.delete()
                return await message.author.send("Warning: "+answer.replace("delete ",""))
            if answer.startswith("react"):
                return await message.add_reaction(answer.replace("react ",""))
        except Exception as es:
            await message.author.send(str(es))

    async def find(self, problem, mode='concise', focus='internet'):
        query = """Pretend to be a doctor, scientologist and biologist - or normal expert.
You have answers to anything and provide help for anything.
Based on the facts of the problem, find a solution.
Do not look at the answer itself, find your own answer using the problem.
Do not include that you are an AI, we know that already.
Combine all 3 solutions and give one detailed solution with recipe, etc.
Add the prefix: Solution:

Problem: """+problem
        try:
            file = None
            assert mode in ['concise', 'copilot'], 'Search modes --> ["concise", "copilot"]'
            assert focus in ['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit', 'wikipedia'], 'Search focus modes --> ["internet", "scholar", "writing", "wolfram", "youtube", "reddit", "wikipedia"]'
            self.copilot = 999
            self.file_upload = True
    
            self.copilot = self.copilot - 1 if mode == 'copilot' else self.copilot
            self.file_upload = self.file_upload - 1 if file else self.file_upload
            self.n += 1
            self._last_answer = None
            self._last_file_upload_info = None

            payload = json.dumps([
                'perplexity_ask',
                query,
                {
                    'version': '2.0',
                    'source': 'default',
                    'mode': mode,
                    'last_backend_uuid': None,
                    'read_write_token': '',
                    'conversational_enabled': False,
                    'frontend_session_id': self.frontend_session_id,
                    'search_focus': focus,
                    'frontend_uuid': self.frontend_uuid,
                    'gpt4': False,
                    'language': 'en-US',
                }
            ])

            self.ws.send(f'{420 + self.n}' + payload)

            while not self._last_answer:
                await asyncio.sleep(0.1)

            result = self._last_answer

            # Extract web results and snippets
            web_results = result["text"]["web_results"]
            
            answer = result["text"]["answer"]
            pattern = re.compile("perplexity", re.IGNORECASE)
            answer =pattern.sub("Splittic", answer)

            return answer
        except Exception as es:
            print(es)
            return "Please try your prompt again."
