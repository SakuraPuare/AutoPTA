import asyncio

ACCOUNT = ''
PASSWORD = ''
API_KEY = ""

GENERICS_PROMPT = '作为一个程序员，以下内容是一道编程赛题题干，请认真阅读。' + \
    '根据给定的样例处理输入输出，\n\n请直接给出代码，不要附加其他内容，不要使用非标准库和非标准库函数。'

LLM_MODEL = "gpt-4o"
LANG = 'Python'

LLM_ARGS = {
    "llm_model": LLM_MODEL,
    "max_length": 4096,
    "top_p": 1,
    "temperature": 1,
    "api_key": API_KEY
}

QUEUE = 2
LIMIT = asyncio.Semaphore(2)
HEADER = {
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'DNT': '1',
    'Accept-Language': 'zh-CN',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json;charset=UTF-8',
    'Referer': 'https://pintia.cn/',
    'X-Marshmallow': '',
    'X-Lollipop': 'ac07570dbb3eb6d2e1b3c0fd4d79949e',
    'sec-ch-ua-platform': '"Linux"',
}
