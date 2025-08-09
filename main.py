from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass
from dotenv import load_dotenv

# 优先从 .env 文件加载环境变量
# 注意：load_dotenv() 不会覆盖已经存在的环境变量
load_dotenv()

# 尝试从环境中获取 API 密钥
google_api_key = os.environ.get("GOOGLE_API_KEY")

# 如果在环境变量和 .env 文件中都没有找到密钥，则提示用户输入
if not google_api_key:
    print("未在环境变量或 .env 文件中找到 GOOGLE_API_KEY。")
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    # 将用户输入的密钥设置到当前会话的环境变量中，以便后续代码使用
    os.environ["GOOGLE_API_KEY"] = google_api_key

# 此时，无论来源如何，密钥都已准备就绪
print("Google AI API 密钥已准备好使用。")


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
