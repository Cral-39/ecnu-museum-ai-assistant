# 展览接口
# 提供展览列表、展览详情等API

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database.mysql import mysql_conn

router = APIRouter()


# 获取展览列表
@router.get("/exhibitions")
async def get_exhibitions(
    status: Optional[str] = Query(
        None,
        description="展览状态: upcoming(即将开展)/ongoing(正在展出)/ended(已结束)"
    )
):
    """
    获取博物馆的展览列表，支持按状态筛选（即将开展、正在展出、已结束）。
    
    - **status**: 展览状态
    
    返回：
    - 成功：200 - 返回展览列表
    - 错误：500 - 服务器内部错误
    """
    try:
        mysql_conn.connect()

        if status:
            mysql_conn.execute(
                "SELECT * FROM exhibitions WHERE status = %s ORDER BY start_date DESC",
                (status,)
            )
        else:
            mysql_conn.execute(
                "SELECT * FROM exhibitions ORDER BY start_date DESC"
            )

        exhibitions = mysql_conn.fetch_all()
        mysql_conn.close()

        return {
            "status": "success",
            "data": exhibitions,
            "count": len(exhibitions)
        }
    except Exception as e:
        print(f"获取展览列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取展览列表失败")


# 获取展览详细信息
@router.get("/exhibitions/{exhibition_id}")
async def get_exhibition_detail(exhibition_id: int):
    """
    根据展览ID获取展览的详细信息，包括展览时间、地点、描述等。
    
    - **exhibition_id**: 展览ID
    
    返回：
    - 成功：200 - 返回展览详细信息
    - 错误：404 - 未找到该展览
    - 错误：500 - 服务器内部错误
    """
    try:
        mysql_conn.connect()
        mysql_conn.execute(
            "SELECT * FROM exhibitions WHERE id = %s",
            (exhibition_id,)
        )
        exhibition = mysql_conn.fetch_one()
        mysql_conn.close()

        if not exhibition:
            raise HTTPException(status_code=404, detail="未找到该展览")

        return {
            "status": "success",
            "data": exhibition
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取展览详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取展览详情失败")


# 获取当前展览
@router.get("/exhibitions/current")
async def get_current_exhibitions():
    """
    获取当前正在进行的展览列表。
    
    返回：
    - 成功：200 - 返回当前展览列表
    - 错误：500 - 服务器内部错误
    """
    return await get_exhibitions(status="ongoing")


# 获取即将开展的展览
@router.get("/exhibitions/upcoming")
async def get_upcoming_exhibitions():
    """
    获取即将开展的展览列表。
    
    返回：
    - 成功：200 - 返回即将开展的展览列表
    - 错误：500 - 服务器内部错误
    """
    return await get_exhibitions(status="upcoming")
