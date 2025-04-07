# 学术论文问答系统

一个基于 RAG (Retrieval-Augmented Generation) 的学术论文智能问答系统，支持 PDF 论文上传和智能问答。

## 功能特点

- PDF 论文上传和解析
- 基于向量数据库的语义检索
- 智能问答系统
- 现代化的 Web 界面
- 支持拖拽上传
- 实时对话交互

## 技术栈

- 后端：Python + FastAPI
- 前端：HTML5 + CSS3 + JavaScript
- 向量数据库：Chroma
- 大语言模型：DeepSeek
- 文本处理：LangChain

## 安装说明

1. 克隆仓库：
```bash
git clone [repository-url]
cd academic-rag
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 设置环境变量：
```bash
export DEEPSEEK_API_KEY=your_api_key  # Linux/Mac
# 或
set DEEPSEEK_API_KEY=your_api_key  # Windows
```

## 运行服务

```bash
python app.py
```

访问 http://localhost:8000 使用系统。

## 使用说明

1. 上传 PDF 论文：
   - 点击"选择文件"按钮或拖拽文件到上传区域
   - 等待文件处理完成

2. 智能问答：
   - 在输入框中输入问题
   - 点击"发送"或按回车键提交
   - 查看系统回答

## 项目结构

```
.
├── app.py              # 主应用文件
├── requirements.txt    # 依赖列表
├── static/            # 静态文件
│   ├── index.html     # 前端页面
│   ├── style.css      # 样式文件
│   ├── script.js      # 前端脚本
│   └── upload-icon.svg # 上传图标
├── uploads/           # 上传文件存储
└── chroma_db/         # 向量数据库存储
```

## 注意事项

- 确保有足够的磁盘空间存储上传的 PDF 文件
- 建议使用现代浏览器访问系统
- 首次运行需要设置 DeepSeek API 密钥

## 许可证

MIT License 