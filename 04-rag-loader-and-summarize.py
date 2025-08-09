import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 1. 导入 PDF 文档加载器
from langchain_community.document_loaders import PyPDFLoader

# --- 环境和密钥加载 ---
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    # ... (省略与之前相同的密钥加载代码)
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    os.environ["GOOGLE_API_KEY"] = google_api_key
print("Google AI API 密钥已准备好使用。")


# --- RAG 步骤 1: 加载 (Load) ---
# 定义要加载的文档路径
pdf_path = "./资料库/gemini-for-google-workspace-prompting-guide-101.pdf"

# 创建一个 PyPDFLoader 实例
loader = PyPDFLoader(pdf_path)

# 调用 load() 方法加载文档
# 这会将 PDF 的每一页都加载成一个独立的 Document 对象
print(f"\n--- 正在从 '{pdf_path}' 加载文档... ---")
docs = loader.load()
print(f"✅ 文档加载完成，总共加载了 {len(docs)} 页。")

# 我们可以查看第一页的内容和元数据
# print("\n--- 第一页内容预览 ---")
# print(docs[0].page_content[:200] + "...") # 打印前200个字符
# print("\n--- 第一页元数据 ---")
# print(docs[0].metadata)


# --- 使用链来总结加载的文档内容 ---
# 创建一个简单的总结链
summarize_prompt = ChatPromptTemplate.from_template(
    "你是一位专业的助理，擅长从复杂的文档中提炼核心要点。\n"
    "请根据以下内容，总结出其最核心的3-5个要点：\n\n"
    "内容：\n"
    "```{document_content}```"
)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")  # 注意：我将模型改回了 1.5-flash
output_parser = StrOutputParser()

summarization_chain = summarize_prompt | llm | output_parser

# 提取第一页的内容来总结
first_page_content = docs[0].page_content

print("\n--- 正在总结第一页的核心内容... ---")
summary = summarization_chain.invoke({"document_content": first_page_content})

print("\n--- 总结结果 ---")
print(summary)
