# 学术研究RAG服务

这是一个基于Python的RAG（检索增强生成）服务，专门用于处理学术论文。该服务使用LangChain框架，DeepSeek-R1作为LLM，ChromaDB作为向量数据库。

## 功能特点

- PDF论文上传和处理
- 基于向量数据库的论文内容检索
- 使用DeepSeek-R1模型进行内容总结和问答
- RESTful API接口

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd [repository-name]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动服务：
```bash
python app.py
```

2. API接口：

- 上传PDF论文：
```bash
curl -X POST "http://localhost:8000/upload" -F "file=@your_paper.pdf"
```

- 查询论文内容：
```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"question": "你的问题"}'
```

## 注意事项

- 确保有足够的磁盘空间存储PDF文件和向量数据库
- 需要稳定的网络连接以访问DeepSeek-R1模型
- 建议使用Python 3.8或更高版本 