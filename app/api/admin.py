# 管理接口
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.database.mysql import mysql_conn
from app.services.vector_service import vector_service
import os
import tempfile

router = APIRouter()

@router.get("/stats")
async def get_stats():
    """
    获取数据统计
    :return: 统计数据
    """
    try:
        # 今日咨询量
        mysql_conn.connect()
        mysql_conn.execute(
            "SELECT COUNT(*) as count FROM consultations WHERE DATE(created_at) = CURDATE()"
        )
        today_consultations = mysql_conn.fetch_one()['count']
        
        # 热门搜索藏品Top 5
        mysql_conn.execute(
            "SELECT a.id, a.name, COUNT(c.id) as search_count FROM artifacts a "
            "LEFT JOIN consultations c ON a.id = c.artifact_id "
            "GROUP BY a.id, a.name ORDER BY search_count DESC LIMIT 5"
        )
        hot_artifacts = mysql_conn.fetch_all()
        
        # 向量库索引数量
        vector_count = vector_service.get_collection_size()
        
        mysql_conn.close()
        
        return {
            "status": "success",
            "data": {
                "today_consultations": today_consultations,
                "hot_artifacts": hot_artifacts,
                "vector_count": vector_count
            }
        }
    except Exception as e:
        print(f"获取统计数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取统计数据失败")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文档并同步到向量库
    :param file: 上传的文件
    :return: 上传结果
    """
    try:
        # 检查文件类型
        if not (file.filename.endswith('.json') or file.filename.endswith('.txt')):
            raise HTTPException(status_code=400, detail="只支持json和txt文件")
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # 同步到向量库
        if file.filename.endswith('.json'):
            count = vector_service.add_documents_from_json(temp_file_path)
        else:
            # 处理txt文件
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                documents = f.readlines()
            # 这里可以根据实际情况处理txt文件的格式
            count = 0
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        return {
            "status": "success",
            "message": f"成功上传并同步{count}个文档到向量库"
        }
    except Exception as e:
        print(f"上传文件失败: {e}")
        raise HTTPException(status_code=500, detail="上传文件失败")
