import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# --- 1. 环境和密钥加载 (与之前的代码相同) ---
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    print("未在环境变量或 .env 文件中找到 GOOGLE_API_KEY。")
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    os.environ["GOOGLE_API_KEY"] = google_api_key
print("Google AI API 密钥已准备好使用。")

# --- 2. 定义链的组件 ---

# 组件 A: 提示模板 (Prompt Template)
# 这定义了输入的结构。我们告诉它，我们将会提供一个名为 "topic" 的变量。
# 模板会将这个变量插入到一个更完整的问句中。
prompt_template = ChatPromptTemplate.from_template(
    "你是一位专业的科普作家。请为我写一篇关于 '{topic}' 的简短科普短文。"
)

# 组件 B: 大语言模型 (LLM)
# 这和我们之前的例子一样，是执行任务的“大脑”。
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# --- 3. 使用 LangChain 表达式语言 (LCEL) 创建链 ---
# 我们使用管道符 `|` 将不同的组件“链接”在一起。
# 这行代码的含义是：
# 1. 接收一个输入 (例如，一个包含 'topic' 的字典)。
# 2. 将该输入传递给 `prompt_template` 进行格式化。
# 3. 将格式化后的完整提示传递给 `llm` 进行处理。
chain = prompt_template | llm

# --- 4. 调用 (Invoke) 链 ---
# 我们现在调用整个链，而不是只调用模型。
# 注意我们提供的输入是一个字典，其键 `topic` 与模板中定义的变量名相匹配。
print("\n--- 正在调用链... ---")
response = chain.invoke({"topic": "黑洞"})

# --- 5. 打印结果 ---
# 链的最终输出通常是一个 AIMessage 对象，我们需要访问其 .content 属性。
print("\n--- AI 的回复 ---")
print(response.content)
