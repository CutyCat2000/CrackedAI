import httpx
import asyncio
import base64

AsyncClient = httpx.AsyncClient()

def replace_base64(input_str, target_str, replacement_str):
    # Add padding if needed
    input_str += '=' * ((4 - len(input_str) % 4) % 4)
    
    # Decode the base64 input string
    decoded_bytes = base64.b64decode(input_str)
    decoded_str = decoded_bytes.decode('utf-8')
    
    # Replace the target string with the replacement string
    modified_str = decoded_str#.replace(target_str, replacement_str)
    #modified_str = modified_str.replace("nMr0KlDu1cgbExcHEMfvKClv8Xv2","nMr0KlDu1cgbExcHEMfvKClv8Xv3")
    
    # Encode the modified string back to base64
    encoded_bytes = base64.b64encode(modified_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    
    return encoded_str

async def textgen(prompt, size_format, style, raw_or_fun):
    cook = "eyJhbGciOiJSUzI1NiIsImtpZCI6InRCME0yQSJ9.eyJpc3MiOiJodHRwczovL3Nlc3Npb24uZmlyZWJhc2UuZ29vZ2xlLmNvbS9pZGVvZ3JhbS1wcm9kIiwibmFtZSI6IkRhbmllbCBLbGltbWVyIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGRuZ05zdmlBTW5UYzlWSWcyVHFSY3ZFcklhbkZoa1ZmdG9rQ1JzQUxqc1x1MDAzZHM5Ni1jIiwiYXVkIjoiaWRlb2dyYW0tcHJvZCIsImF1dGhfdGltZSI6MTY5MzIyNjU1OCwidXNlcl9pZCI6Im5NcjBLbER1MWNnYkV4Y0hFTWZ2S0NsdjhYdjIiLCJzdWIiOiJuTXIwS2xEdTFjZ2JFeGNIRU1mdktDbHY4WHYyIiwiaWF0IjoxNjkzMjI2OTY3LCJleHAiOjE2OTQ0MzY1NjcsImVtYWlsIjoiZXZpbGZpcmVkcmFnb241M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTU5MjMwMDE3MTg4MjkzNTk0NiJdLCJlbWFpbCI6WyJldmlsZmlyZWRyYWdvbjUzQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0"
    #cook = replace_base64(cook, "evilfiredragon53@gmail.com", "jjj@gmail.com").replace("=","")
    cook = cook + ".d4IuVLqZm-V6J15Mgv44Te4OMXIDnSI6WENEutOuPw5s0KxPtQHV9PzwOCP5GhLhY7Ra5SmDpDWjRka6j-fSrylM7Stq-4c2cD9Hu5JVZd6yC0E-VVPfE10IAMQLX1a4BjTw-cSaHxpkZ7k9n4bTCYGNRPhfz1qlrbwauq84hPKouCFLf0KgZAqKqyHe55aGXnwDb9a87vQzAuHxamDLsVV_78QCvwB0QKDeqorukctNm_06FjIHBR0uYYCEynQbzSknTPZkSKku05VF7u8rYFMRmh9eAw-8R_-vQj-8yXRdwnzE0pzrF_UsMgrbJ5F6ftDorngT9fGkrlVjJ70flw"
    cookies = {
        '_ga': 'GA1.1.1392855579.1694446340',
        'session_cookie': 'eyJhbGciOiJSUzI1NiIsImtpZCI6InRCME0yQSJ9.eyJpc3MiOiJodHRwczovL3Nlc3Npb24uZmlyZWJhc2UuZ29vZ2xlLmNvbS9pZGVvZ3JhbS1wcm9kIiwibmFtZSI6IkRhbmllbCBOZXJ2aWciLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSXoxVWtkSFV0TWdiRzgwM3BNN2JFV2RlUmlWMFp3dm5RdGNZMDRuVGVqXHUwMDNkczk2LWMiLCJhdWQiOiJpZGVvZ3JhbS1wcm9kIiwiYXV0aF90aW1lIjoxNjk0NDQ2NDAzLCJ1c2VyX2lkIjoiT2FaajFKYzhYOFlOQ3lWVFFsUFlzeWhTcTFqMiIsInN1YiI6Ik9hWmoxSmM4WDhZTkN5VlRRbFBZc3loU3ExajIiLCJpYXQiOjE2OTQ0NDY0MDMsImV4cCI6MTY5NTY1NjAwMywiZW1haWwiOiJkYW5pZWxuZXJ2aWdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDIwNzExMzM1NjU1NTE3NjMwOTUiXSwiZW1haWwiOlsiZGFuaWVsbmVydmlnQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.Rm3Vmj0HTYO8_mgJIiMicCjcs_ttgkDkDz2J51s4-jmNZbW2OXK8w_alOpP8-gIJXAFotbX8SBPwWL0qdQAvjvPsPrmz81-rVsZBrE9MFCSUfsl0UN_iJXPiLyHSsgjdZPIUONLu2PgV07hgNU8ZXmoATsR-Tu3nRGBVUEXf7_Qer2b3rTi4SA892qfY6xVashEdLoslN1qu-ANZyd5VCjePFzHCNoGSiGYEafEbuuPPS4OROnjewanGcbuE2YdbmOl_L1erRthLcRPAgaswIY0wvDXWbN6bWSZgcIgmqXkisYmv9288Q1BGNg5rz_0CPqCJP7QMlz-nknAMXchWrw',
        '_ga_44J8R31CP6': 'GS1.1.1694446339.1.1.1694446404.0.0.0',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': '*/*',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://ideogram.ai/',
        'Content-Type': 'application/json',
        'Origin': 'https://ideogram.ai',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    json_data = {
        'aspect_ratio': size_format,
        'channel_id': 'LbF4xfurTryl5MUEZ73bDw',
        'prompt': prompt + ", "+style,
        'raw_or_fun': raw_or_fun,
        'speed': 'fast',
        'style': style,
        'user_id': 'Lmu5jFUTSreAoyEvaRPfnQ',
    }
    response = await AsyncClient.post('https://api.corsme.com/?https://ideogram.ai/api/images/sample', cookies=cookies, headers=headers, json=json_data)
    await asyncio.sleep(60)
    while True:
        try:
            req_id = response.json()["request_id"]

            response = await AsyncClient.get(
                'https://api.corsme.com/?https://ideogram.ai/api/images/retrieve_metadata_request_id/'+req_id,
                cookies=cookies,
                headers=headers,
            )

            resp = response.json()["responses"][0]
            return "https://ideogram.ai/api/images/direct/"+resp["response_id"]
        except Exception as es:
            if str(es) == 'can only concatenate str (not "NoneType") to str':
                pass
            else:
            	break
        await asyncio.sleep(30)
