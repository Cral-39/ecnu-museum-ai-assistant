# 聊天接口
# 提供流式文字回复和文物卡片信息的API

from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Optional
import json
import base64
from app.services.chat_service import chat_service
from app.services.vector_service import vector_service
from app.schemas import ChatRequest, ChatResponse, ImageRecognitionResponse

router = APIRouter()


# AI聊天接口
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    与博物馆AI导览助手进行对话，支持流式和非流式输出。当提到特定文物时，会返回文物卡片信息。
    
    - **question**: 用户问题
    - **stream**: 是否使用流式输出
    
    返回：
    - 成功：200 - 返回AI回答和元数据
    - 错误：400 - 请求参数错误
    - 错误：401 - 未授权
    - 错误：500 - AI服务异常
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    if request.stream:
        return StreamingResponse(
            generate_stream_response(request.question),
            media_type="application/json",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked"
            }
        )
    else:
        result = chat_service.chat_completion(request.question)
        return result


async def generate_stream_response(question: str):
    """
    生成流式响应的生成器
    :param question: 用户问题
    :yield: JSON格式的响应片段
    """
    for chunk in chat_service.stream_chat_completion(question):
        yield json.dumps(chunk, ensure_ascii=False) + "\n"


# 获取相关问题建议
@router.get("/chat/relevant-questions")
async def get_relevant_questions(
    artifact_id: Optional[int] = Query(None, description="文物ID"),
    category: Optional[str] = Query(None, description="文物类别")
):
    """
    根据当前文物或类别，生成相关的问题建议，帮助用户深入了解文物。
    
    返回：
    - 成功：200 - 返回相关问题列表
    - 错误：500 - 服务器内部错误
    """
    # 简化版本：返回固定的相关问题
    questions = [
        "这件文物的历史背景是什么？",
        "这件文物有什么特殊价值？",
        "类似的文物还有哪些？",
        "这件文物是如何被发现的？"
    ]
    return {
        "status": "success",
        "data": questions
    }


# 获取文物详细信息
@router.get("/artifacts/{artifact_id}")
async def get_artifact_detail(artifact_id: int):
    """
    根据文物ID获取完整的文物信息，包括图片和3D展示链接。
    
    - **artifact_id**: 文物ID
    
    返回：
    - 成功：200 - 返回文物详细信息
    - 错误：404 - 未找到该文物
    - 错误：500 - 服务器内部错误
    """
    artifact = vector_service.get_artifact_by_id(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="未找到该文物")

    return {
        "status": "success",
        "data": artifact
    }


# 搜索文物
@router.get("/artifacts/search")
async def search_artifacts(
    keyword: str = Query(..., description="搜索关键词"),
    limit: int = Query(10, description="返回结果数量")
):
    """
    根据关键词搜索文物，返回相关的文物列表。
    
    - **keyword**: 搜索关键词
    - **limit**: 返回结果数量
    
    返回：
    - 成功：200 - 返回搜索结果
    - 错误：400 - 搜索关键词不能为空
    - 错误：500 - 服务器内部错误
    """
    artifacts = vector_service.search_artifacts_by_keyword(keyword)
    return {
        "status": "success",
        "data": artifacts[:limit]
    }


# 获取知识库统计信息
@router.get("/knowledge-base/stats")
async def get_knowledge_base_stats():
    """
    获取向量知识库的统计信息，包括文物数量等。
    
    返回：
    - 成功：200 - 返回知识库统计信息
    - 错误：500 - 服务器内部错误
    """
    stats = {
        "artifact_count": vector_service.get_collection_size(),
        "description": "华东师大博物馆AI导览系统知识库"
    }
    return {
        "status": "success",
        "data": stats
    }


# 图片识别接口
@router.post("/chat/image-recognition", response_model=ImageRecognitionResponse)
async def image_recognition_endpoint(file: UploadFile = File(..., description="要识别的图片文件")):
    """
    上传图片进行藏品识别，支持JPG、PNG等格式。使用多模态AI模型进行图片分析，识别文物并返回相关信息。
    
    - **file**: 图片文件（支持JPG、PNG、HEIC等格式）
    
    返回：
    - 成功：200 - 返回识别结果和文物信息
    - 错误：400 - 文件格式错误或文件为空
    - 错误：500 - 识别服务异常
    """
    # 验证文件类型
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    # 检查文件扩展名
    allowed_extensions = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif"}
    file_ext = file.filename.lower().split(".")[-1]
    if f".{file_ext}" not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件格式，请上传JPG、PNG或HEIC格式的图片")
    
    # 读取文件内容
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {str(e)}")
    
    if not contents:
        raise HTTPException(status_code=400, detail="文件内容为空")
    
    # 将图片转换为Base64
    image_base64 = base64.b64encode(contents).decode("utf-8")
    
    # 调用图片识别服务
    result = chat_service.image_recognition(image_base64)
    return result
