import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# 1. 导入新工具

# --- 环境和密钥加载 (与之前的代码相同) ---
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    print("未在环境变量或 .env 文件中找到 GOOGLE_API_KEY。")
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    os.environ["GOOGLE_API_KEY"] = google_api_key
print("Google AI API 密钥已准备好使用。")


# --- 2. 定义一个自定义的 Python 函数作为链的组件 ---
# 这个函数负责将接收到的数据保存到文件中。
# 它期望接收一个字典，其中包含 'topic' 和 'content'。
def save_to_markdown_file(data):
    """接收一个字典，将其中的 content 保存到以 topic 命名的 .md 文件中。"""
    try:
        topic = data.get("topic")
        content = data.get("content")
        if not topic or not content:
            return "❌ 缺少 topic 或 content，无法保存。"

        file_name = f"{topic}.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)

        # 这个函数的返回值，将成为整个链的最终返回值。
        return f"✅ 内容已成功保存到文件: {file_name}"
    except IOError as e:
        return f"❌ 保存文件时出错: {e}"


# --- 3. 定义并组合链 ---

# 负责生成内容的子链 (和之前一样)
generation_chain = (
    ChatPromptTemplate.from_template(
        "你是一位专业的科普作家。请为我写一篇关于 '{topic}' 的简短科普短文，请直接使用 Markdown 格式进行排版。"
    )
    | ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    | StrOutputParser()
)

# 创建主链
# 这里的逻辑是：
# 1. RunnablePassthrough.assign(content=generation_chain) 的作用是：
#    a. 运行 generation_chain 来生成内容。
#    b. 将生成的内容赋值给一个新的键 'content'。
#    c. 将这个新的键值对与原始输入（包含 'topic'）合并成一个字典。
#    d. 最终输出一个像这样的字典: {"topic": "黑洞", "content": "这是生成的科普文章..."}
# 2. | save_to_markdown_file：
#    将上一步生成的完整字典，传递给我们自定义的保存函数。
main_chain = RunnablePassthrough.assign(content=generation_chain) | save_to_markdown_file


# --- 4. 调用主链 ---
topic = "人工智能"
print(f"\n--- 正在调用链 (主题: {topic})... ---")

# 调用主链，它会完成从生成到保存的所有步骤
final_result = main_chain.invoke({"topic": topic})

# 打印我们自定义的保存函数的返回值
print(final_result)
