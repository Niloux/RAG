import getpass
import logging
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建必要的目录
UPLOAD_DIR = Path("./uploads")
CHROMA_DB_DIR = Path("./chroma_db")
STATIC_DIR = Path("./static")
UPLOAD_DIR.mkdir(exist_ok=True)
CHROMA_DB_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Academic RAG Service",
    description="一个基于RAG的学术论文问答服务",
    version="1.0.0",
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 初始化向量数据库和嵌入模型
try:
    embeddings = FakeEmbeddings(size=1352)
    vectorstore = Chroma(
        collection_name="academic_rag",
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings,
    )
    logger.info("向量数据库初始化成功")
except Exception as e:
    logger.error(f"向量数据库初始化失败: {str(e)}")
    raise

# 检查并设置API密钥
if not os.getenv("DEEPSEEK_API_KEY"):
    try:
        os.environ["DEEPSEEK_API_KEY"] = getpass.getpass(
            "Enter your DeepSeek API key: "
        )
    except Exception as e:
        logger.error(f"API密钥设置失败: {str(e)}")
        raise

# 初始化DeepSeek模型
try:
    llm = ChatDeepSeek(model_name="deepseek-chat", temperature=0, max_tokens=1000)
    logger.info("DeepSeek模型初始化成功")
except Exception as e:
    logger.error(f"DeepSeek模型初始化失败: {str(e)}")
    raise


class Query(BaseModel):
    question: str = Field(..., description="用户的问题")
    top_k: Optional[int] = Field(default=3, description="返回的文档数量")


class Response(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None


@app.get("/")
async def read_root():
    """返回前端页面"""
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.post("/upload", response_model=Response)
async def upload_pdf(file: UploadFile = File(...)):
    """上传PDF文件并处理"""
    try:
        # 检查文件类型
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="只支持PDF文件")

        # 保存上传的文件
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"文件 {file.filename} 保存成功")

        # 加载PDF文件
        loader = PyPDFLoader(str(file_path))
        pages = loader.load()
        logger.info(f"成功加载PDF文件，共 {len(pages)} 页")

        # 分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(pages)
        logger.info(f"文本分割完成，共 {len(texts)} 个片段")

        # 添加到向量数据库
        vectorstore.add_documents(texts)
        vectorstore.persist()
        logger.info("文档已成功添加到向量数据库")

        return Response(
            status="success",
            message=f"Successfully processed {file.filename}",
            data={"pages": len(pages), "chunks": len(texts)},
        )

    except Exception as e:
        logger.error(f"处理文件时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=Response)
async def query_papers(query: Query):
    """查询论文内容"""
    try:
        # 创建检索链
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": query.top_k}),
        )

        # 执行查询
        result = qa_chain.run(query.question)
        logger.info(f"成功处理查询: {query.question}")

        return Response(status="success", message="查询成功", data={"answer": result})

    except Exception as e:
        logger.error(f"查询处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return Response(
        status="success",
        message="服务运行正常",
        data={"vectorstore_status": "active", "llm_status": "active"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
