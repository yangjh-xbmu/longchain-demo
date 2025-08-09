import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # 1. 导入我们新的组件

# --- 环境和密钥加载 (与之前的代码相同) ---
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    print("未在环境变量或 .env 文件中找到 GOOGLE_API_KEY。")
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    os.environ["GOOGLE_API_KEY"] = google_api_key
print("Google AI API 密钥已准备好使用。")


# --- 定义链的组件 ---

# 组件 A: 提示模板
# 我们稍微修改提示，鼓励模型直接输出 Markdown 格式
prompt_template = ChatPromptTemplate.from_template(
    "你是一位专业的科普作家。请为我写一篇关于 '{topic}' 的简短科普短文，请直接使用 Markdown 格式进行排版。"
)

# 组件 B: 大语言模型 (LLM)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 组件 C: 输出解析器 (Output Parser)
# 我们选用 StrOutputParser，它的功能很简单：
# 将 LLM 返回的 AIMessage 对象，自动转换成一个普通的字符串（也就是提取 .content）。
output_parser = StrOutputParser()


# --- 使用 LCEL 创建一个更长的链 ---
# 我们的新工作流是：
# 1. 接收输入 -> 2. 格式化提示 -> 3. LLM 处理 -> 4. 解析输出为字符串
chain = prompt_template | llm | output_parser


# --- 调用链并保存结果 ---
topic = "黑洞"
print(f"\n--- 正在调用链 (主题: {topic})... ---")

# 因为链的最后一个环节是 StrOutputParser，所以 invoke 的结果直接就是字符串内容！
response_content = chain.invoke({"topic": topic})

print("\n--- AI 的回复 ---")
print(response_content)

# 将内容保存到 Markdown 文件
file_name = f"{topic}.md"
try:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(response_content)
    print(f"\n✅ 内容已成功保存到文件: {file_name}")
except IOError as e:
    print(f"\n❌ 保存文件时出错: {e}")
