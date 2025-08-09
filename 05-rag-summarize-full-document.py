import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader

# --- 环境和密钥加载 ---
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    google_api_key = getpass.getpass("请输入您的 Google AI API 密钥: ")
    os.environ["GOOGLE_API_KEY"] = google_api_key
print("Google AI API 密钥已准备好使用。")


# --- RAG 步骤 1: 加载 (Load) ---
pdf_path = "./资料库/gemini-for-google-workspace-prompting-guide-101.pdf"
loader = PyPDFLoader(pdf_path)
print(f"\n--- 正在从 '{pdf_path}' 加载文档... ---")
docs = loader.load()
print(f"✅ 文档加载完成，总共加载了 {len(docs)} 页。")


# --- 准备要总结的全部内容 ---
# 核心改动：将所有页面的内容合并成一个字符串
print("\n--- 正在合并所有页面的内容... ---")
# 使用 "\n---\n" 作为分隔符，帮助模型理解页面间的区隔
full_document_content = "\n---\n".join([doc.page_content for doc in docs])
print(f"✅ 所有 {len(docs)} 页内容已合并。")
# print(f"文档总字数: {len(full_document_content)}") # 可以取消注释来查看总字数


# --- 使用链来总结加载的文档内容 ---
summarize_prompt = ChatPromptTemplate.from_template(
    "你是一位专业的文档分析助理，擅长从复杂的长篇文档中提炼核心摘要。\n"
    "请根据以下由多个页面拼接而成的内容，用中文进行详细的总结。\n"
    "你的任务是：\n"
    "1. 识别出文档中 5-7 个最核心的关键主题。\n"
    "2. 对于每一个主题，请用2-3句话进行详细的阐述和解释，确保内容清晰易懂。\n"
    "3. 最后，请以清晰的、带有项目符号的列表形式呈现你的总结。\n\n"
    "文档内容：\n"
    "```{document_content}```"
)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
output_parser = StrOutputParser()

summarization_chain = summarize_prompt | llm | output_parser

print("\n--- 正在总结整个文档的核心内容... ---")
# 将合并后的完整内容传递给链
summary = summarization_chain.invoke({"document_content": full_document_content})

print("\n--- 总结结果 ---")
print(summary)
