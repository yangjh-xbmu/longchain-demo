# LangChain Google Generative AI 示例项目

这是一个简单的 Python 项目，展示了如何使用 `langchain-google-genai` 库与 Google 的生成式 AI 模型（如 Gemini）进行交互。

项目主要包含以下功能：

- 通过 LangChain 调用 Google AI 模型。
- 自动从 `.env` 文件或环境变量中加载 `GOOGLE_API_KEY`。
- 如果未找到 API 密钥，会提示用户安全地输入。
- 内置代理功能，可配置脚本通过指定的代理服务器访问 Google AI 服务。

## 环境配置

### 1. 克隆或下载项目

首先，将项目文件下载到您的本地计算机。

### 2. 创建并激活 Python 虚拟环境

项目包含一个用于激活虚拟环境的便捷脚本。

```bash
# 激活虚拟环境
source ./activate_venv.sh
```

激活后，您应该会看到终端提示符前出现 `(venv)`。

### 3. 安装依赖

项目的所有依赖都记录在 `requirements.txt` 文件中。

```bash
# 安装依赖
pip install -r requirements.txt
```

### 4. 设置 API 密钥

您需要一个 Google AI API 密钥才能运行此项目。

1. 将项目中的 `.env.example` (如果存在) 文件复制为 `.env`。
2. 在 `.env` 文件中，将您的 Google AI API 密钥添加进去：

    ```
    GOOGLE_API_KEY="在这里粘贴您的API密钥"
    ```

或者，您也可以不创建 `.env` 文件。首次运行 `main.py` 时，脚本会提示您输入密钥。

## 如何运行

确保您的虚拟环境已经激活，然后运行主脚本：

```bash
python main.py
```

脚本将使用内置的代理设置（默认为 `http://127.0.0.1:10808`）调用 Google AI 模型，并打印出模型的回复。

## 辅助脚本

### 全局代理设置 (`proxy.sh`)

这是一个为 macOS 设计的辅助脚本，可以方便地开启、关闭和查看系统级的网络代理。这对于需要通过代理访问互联网的开发环境非常有用。

**使用方法:**

```bash
# 开启全局代理
source ./proxy.sh on

# 关闭全局代理
source ./proxy.sh off

# 查看当前代理状态
./proxy.sh show
```

**注意:** `main.py` 脚本目前是硬编码使用代理，不依赖于此脚本。但此脚本对于配置您整个开发环境的代理非常有用。

### 虚拟环境激活 (`activate_venv.sh`)

如上所述，此脚本用于快速激活项目的 Python 虚拟环境。

```bash
source ./activate_venv.sh
```
