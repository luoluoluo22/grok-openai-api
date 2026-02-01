# Grok OpenAI API 服务

这个项目提供了一个与 OpenAI API 兼容的接口，允许您使用 Grok 模型。通过这个服务，您可以使用现有的 OpenAI 客户端库（如 Python 的 `openai` 包或 JavaScript 的 `openai` npm 包）来与 Grok 模型进行交互。

## 功能特点

- 与 OpenAI API 兼容的接口
- 支持聊天完成 API (`/v1/chat/completions`)
- 支持模型列表 API (`/v1/models`)
- 支持流式响应
- 可部署到 Netlify 作为无服务器函数

## 快速开始

### 本地运行

1. 克隆仓库
   ```bash
   git clone https://github.com/luoluoluo22/grok-openai-api.git
   cd grok-openai-api
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行服务
   ```bash
   python src/app.py
   ```

4. 服务将在 http://localhost:5000 上运行

### 部署到 Netlify

1. 在 Netlify 上创建一个新站点，并连接到您的 GitHub 仓库

2. 设置以下构建设置:
   - 构建命令: `pip install -r requirements.txt`
   - 发布目录: `static`
   - 函数目录: `netlify/functions`

3. 部署完成后，您可以通过 `https://your-netlify-site.netlify.app/v1` 访问 API

## 使用示例

### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="dummy",  # 可以使用任意值
    base_url="http://localhost:5000/v1"  # 本地开发
    # 或者使用 Netlify URL
    # base_url="https://your-netlify-site.netlify.app/v1"
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'dummy', // 可以使用任意值
  baseURL: 'http://localhost:5000/v1', // 本地开发
  // 或者使用 Netlify URL
  // baseURL: 'https://your-netlify-site.netlify.app/v1',
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: 'grok-3',
    messages: [
      { role: 'user', content: '你好，请介绍一下你自己' }
    ],
  });

  console.log(completion.choices[0].message.content);
}

main();
```

## 项目结构

```
.
├── netlify/
│   └── functions/
│       └── api.js         # Netlify 函数入口
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── grok_api.py    # Grok API 核心功能
│   ├── __init__.py
│   ├── app.py             # Flask 应用
│   └── serverless.py      # 无服务器处理脚本
├── static/
│   ├── css/
│   │   └── main.css       # 样式表
│   ├── js/
│   │   └── main.js        # JavaScript 文件
│   └── index.html         # 前端页面
├── netlify.toml           # Netlify 配置
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明
```

## 注意事项

- 此服务仅用于个人学习和研究目的
- 请遵守 Grok 的使用条款和条件
- 会话管理是简化的实现，实际应用中可能需要更复杂的会话管理机制
- 在生产环境中使用前，请添加适当的安全措施和错误处理

## 许可证

MIT

## 贡献

欢迎提交 Pull Request 和 Issue！ 
