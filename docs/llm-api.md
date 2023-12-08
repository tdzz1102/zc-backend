# 大模型 API 使用文档

API 后端是基于 [FastChat](https://github.com/lm-sys/FastChat) 和 [vllm](https://github.com/vllm-project/vllm) 两个项目实现的，提供了 openai api 风格的接口，可以用于生成文本补全和聊天对话补全，详细信息可以参考 [FastChat OpenAI-Compatible RESTful APIs 文档](https://github.com/lm-sys/FastChat/blob/main/docs/openai_api.md) 和 [openai API reference 官方文档](https://platform.openai.com/docs/api-reference/chat)。若在使用过程中遇到任何无法解决的问题或发现后端存在异常，请联系助教。

该 API 后端提供了三个主要接口：
- 获取模型列表 (`GET /v1/models`)
- 创建文本补全 (`POST /v1/completions`) 
- 创建聊天对话补全 (`POST /v1/chat/completions`)

可以在 `http://111.202.73.146:10510/docs` 中查看接口详情并进行测试，以下是每个接口的使用方法和示例代码：

### 1. 获取模型列表 (`GET /v1/models`)

使用此接口可获取所有可用模型的列表。

#### 示例代码：

```python
import requests

# 获取模型列表
response = requests.get("http://111.202.73.146:10510/v1/models")
models = response.json()["data"]
```

### 2. 创建文本补全 (`POST /v1/completions`)

此接口用于根据给定的提示文本生成补全内容。

#### 参数设置：

- `prompt`: 提示文本，即要补全的部分。
- `max_tokens`: 生成的最大令牌数。

#### 示例代码：

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(base_url="http://111.202.73.146:10510/v1")

prompt = "Once upon a time"
max_tokens = 512

for model in models:
    model_name = model["id"]
    print(f"Model: {model_name}")
    
    # 创建文本补全
    completion = client.completions.create(
        model=model_name, prompt=prompt, max_tokens=max_tokens, stop=["\n\n"]
    )
    # 打印补全结果
    print(prompt + completion.choices[0].text)
```

### 3. 创建聊天会话补全 (`POST /v1/chat/completions`)

该接口用于创建聊天式的会话补全。

#### 示例代码：

```python
for model in models:
    model_name = model["id"]

    # 创建聊天会话补全
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": "Hello! What is your name?"},
        ],
        max_tokens=max_tokens,
    )
    # 打印会话补全结果
    print(completion.choices[0].message.content, "\n")
```
