# 聊天相关的数据模型
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ArtifactInfo(BaseModel):
    """
    文物信息模型
    """
    id: int = Field(..., description="文物ID")
    name: str = Field(..., description="文物名称")
    category: str = Field(..., description="文物类别")
    collection: str = Field(..., description="所属馆藏")
    era: str = Field(..., description="所属年代")
    description: str = Field(..., description="详细描述")
    image_url: Optional[str] = Field(None, description="文物图片URL")
    three_d_url: Optional[str] = Field(None, description="文物3D展示URL")
    created_at: datetime = Field(..., description="创建时间")


class RelevantDoc(BaseModel):
    """
    相关文档模型
    """
    document: str = Field(..., description="文档内容")
    metadata: Dict[str, Any] = Field(..., description="文档元数据")
    distance: float = Field(..., description="相关性距离，值越小越相关")


class ChatResponse(BaseModel):
    """
    聊天响应模型
    """
    text: str = Field(..., description="AI的回答文本")
    metadata: Dict[str, Any] = Field(..., description="元数据信息，包含文物信息和相关文档")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "您询问的大观通宝是华东师大博物馆的珍贵藏品。大观通宝是北宋徽宗赵佶在大观年间（1107-1110年）所铸造的钱币，钱文为瘦金体，制作精美，具有重要的历史价值。",
                "metadata": {
                    "artifact": {
                        "id": 1,
                        "name": "大观通宝",
                        "category": "古钱币",
                        "collection": "古代钱币馆",
                        "era": "北宋",
                        "description": "北宋徽宗大观年间铸造的铜钱，钱文为瘦金体，制作精美。",
                        "image_url": "https://digitalmuseum.ecnu.edu.cn/images/coin1.jpg",
                        "three_d_url": "https://digitalmuseum.ecnu.edu.cn/3d/1",
                        "created_at": "2024-01-01T00:00:00"
                    },
                    "relevant_docs": [
                        {
                            "document": "文物名称：大观通宝\n文物类别：古钱币\n所属馆藏：古代钱币馆\n所属年代：北宋\n详细描述：北宋徽宗大观年间铸造的铜钱，钱文为瘦金体，制作精美。",
                            "metadata": {
                                "artifact_id": 1,
                                "name": "大观通宝",
                                "category": "古钱币",
                                "collection": "古代钱币馆"
                            },
                            "distance": 0.1
                        }
                    ],
                    "has_artifact_card": True
                }
            }
        }


class ChatRequest(BaseModel):
    """
    聊天请求模型
    """
    question: str = Field(..., description="用户问题")
    stream: bool = Field(False, description="是否使用流式输出")
    
    class Config:
        schema_extra = {
            "example": {
                "question": "大观通宝是什么？",
                "stream": True
            }
        }


class ImageRecognitionResponse(BaseModel):
    """
    图片识别响应模型
    """
    text: str = Field(..., description="AI对图片内容的描述")
    metadata: Dict[str, Any] = Field(..., description="元数据信息，包含文物信息和相关文档")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "这是一件青铜剑，属于战国时期的兵器，现收藏于历史文物馆。",
                "metadata": {
                    "artifact": {
                        "id": 2,
                        "name": "青铜剑",
                        "category": "兵器",
                        "collection": "历史文物馆",
                        "era": "战国",
                        "description": "战国时期青铜兵器，剑身修长，铸造精美。",
                        "image_url": "https://digitalmuseum.ecnu.edu.cn/images/sword1.jpg",
                        "three_d_url": "https://digitalmuseum.ecnu.edu.cn/3d/2"
                    },
                    "relevant_docs": [],
                    "has_artifact_card": True
                }
            }
        }
