# 向量检索服务 - RAG核心组件
# 负责ChromaDB向量库与MySQL文物数据库的交互

import json
import logging
from typing import List, Dict, Optional, Any
from app.database.chromadb import chromadb_conn
from app.database.mysql import mysql_conn

logger = logging.getLogger(__name__)


class VectorService:
    """
    向量服务类
    提供文物知识库的向量检索、文档管理、文物信息查询等功能
    """

    def __init__(self):
        """
        初始化向量服务
        建立与ChromaDB和MySQL的连接
        """
        self.chromadb = chromadb_conn
        self._ensure_chromadb_connection()

    def _ensure_chromadb_connection(self):
        """
        确保ChromaDB连接已建立
        """
        if not self.chromadb.ensure_connection():
            logger.warning("ChromaDB连接初始化失败，将在使用时自动重连")

    def add_artifact_to_knowledge_base(self, artifact: Dict[str, Any]) -> bool:
        """
        将单个文物信息添加到向量知识库
        :param artifact: 文物对象，包含id、name、description、category、collection等字段
        :return: 是否添加成功
        """
        try:
            document = self._build_artifact_document(artifact)
            metadata = self._build_artifact_metadata(artifact)

            # 确保ChromaDB连接正常
            if not self.chromadb.ensure_connection():
                logger.error("ChromaDB连接失败，无法添加文物")
                return False

            success = self.chromadb.add_documents(
                documents=[document],
                metadatas=[metadata],
                ids=[f"artifact_{artifact['id']}"]
            )
            
            if success:
                logger.info(f"文物添加到向量库成功: {artifact['name']}")
            return success
        except Exception as e:
            logger.error(f"添加文物到知识库失败: {e}")
            return False

    def _build_artifact_document(self, artifact: Dict[str, Any]) -> str:
        """
        构建文物文档内容（用于向量检索的文本）
        :param artifact: 文物信息字典
        :return: 格式化的文档字符串
        """
        parts = [
            f"文物名称：{artifact.get('name', '未知')}",
            f"文物类别：{artifact.get('category', '未知')}",
            f"所属馆藏：{artifact.get('collection', '未知')}",
            f"所属年代：{artifact.get('era', '未知')}",
            f"详细描述：{artifact.get('description', '暂无描述')}"
        ]
        return "\n".join(parts)

    def _build_artifact_metadata(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建文物元数据（存储在向量库的metadata中）
        :param artifact: 文物信息字典
        :return: 元数据字典
        """
        return {
            "artifact_id": artifact.get('id'),
            "name": artifact.get('name', ''),
            "category": artifact.get('category', ''),
            "collection": artifact.get('collection', ''),
            "era": artifact.get('era', ''),
            "image_url": artifact.get('image_url', ''),
            "three_d_url": artifact.get('three_d_url', '')
        }

    def add_documents_from_json(self, json_path: str) -> int:
        """
        从JSON文件批量添加文物到知识库
        :param json_path: JSON文件路径
        :return: 成功添加的文物数量
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                artifacts = json.load(f)

            count = 0
            for artifact in artifacts:
                if self.add_artifact_to_knowledge_base(artifact):
                    count += 1

            logger.info(f"从JSON文件批量添加文物完成: {count}/{len(artifacts)}")
            return count
        except Exception as e:
            logger.error(f"从JSON添加文档失败: {e}")
            return 0

    def sync_artifacts_from_mysql(self) -> int:
        """
        从MySQL数据库同步所有文物到ChromaDB向量库
        用于初始化向量库或批量更新
        :return: 同步的文物数量
        """
        try:
            # 清空现有向量库，避免重复
            logger.info("开始从MySQL同步文物到向量库...")
            self.chromadb.clear_collection()

            mysql_conn.connect()
            mysql_conn.execute("SELECT * FROM artifacts")
            artifacts = mysql_conn.fetch_all()
            mysql_conn.close()

            if not artifacts:
                logger.warning("MySQL中未找到文物数据")
                return 0

            count = 0
            for artifact in artifacts:
                if self.add_artifact_to_knowledge_base(artifact):
                    count += 1

            logger.info(f"从MySQL同步文物到向量库完成: {count}/{len(artifacts)}")
            return count
        except Exception as e:
            logger.error(f"从MySQL同步文物失败: {e}")
            return 0

    def retrieve_relevant_documents(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        检索与用户查询相关的文物文档（RAG核心）
        :param query: 用户查询文本
        :param n_results: 返回的结果数量
        :return: 相关文档列表，每项包含document、metadata、distance
        """
        try:
            # 确保ChromaDB连接正常
            if not self.chromadb.ensure_connection():
                logger.error("ChromaDB连接失败，无法检索文档")
                return []

            results = self.chromadb.query(query, n_results)

            if not results or not results.get('documents'):
                return []

            relevant_docs = []
            # 设置相关性阈值，过滤不相关的文档
            DISTANCE_THRESHOLD = 1.0  # 距离越小越相关
            for i in range(len(results['documents'][0])):
                distance = results['distances'][0][i]
                if distance < DISTANCE_THRESHOLD:
                    doc = {
                        "document": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": distance
                    }
                    relevant_docs.append(doc)

            logger.info(f"检索到{len(relevant_docs)}条相关文档")
            return relevant_docs
        except Exception as e:
            logger.error(f"检索文档失败: {e}")
            return []

    def get_artifact_by_id(self, artifact_id: int) -> Optional[Dict[str, Any]]:
        """
        根据文物ID从MySQL获取完整的文物信息
        :param artifact_id: 文物ID
        :return: 文物详细信息字典，包含image_url和three_d_url等
        """
        try:
            mysql_conn.connect()
            mysql_conn.execute(
                "SELECT * FROM artifacts WHERE id = %s",
                (artifact_id,)
            )
            artifact = mysql_conn.fetch_one()
            mysql_conn.close()

            if artifact:
                logger.info(f"查询到文物信息: {artifact['name']}")
            return artifact
        except Exception as e:
            logger.error(f"获取文物信息失败: {e}")
            return None

    def get_artifact_metadata_by_id(self, artifact_id: int) -> Optional[Dict[str, Any]]:
        """
        根据文物ID从ChromaDB获取文物元数据（更快）
        :param artifact_id: 文物ID
        :return: 文物元数据
        """
        try:
            if not self.chromadb.ensure_connection():
                logger.error("ChromaDB连接失败，无法获取元数据")
                return None

            # 直接从ChromaDB获取指定ID的文档
            result = self.chromadb.collection.get(ids=[f"artifact_{artifact_id}"])

            if result and result.get('metadatas'):
                return result['metadatas'][0]
            return None
        except Exception as e:
            logger.error(f"获取文物元数据失败: {e}")
            return None

    def get_collection_size(self) -> int:
        """
        获取向量库中文物的数量
        :return: 知识库中的文档数量
        """
        try:
            return self.chromadb.get_collection_size()
        except Exception as e:
            logger.error(f"获取集合大小失败: {e}")
            return 0

    def search_artifacts_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        根据关键词搜索文物（先向量检索，再查MySQL获取完整信息）
        :param keyword: 搜索关键词
        :return: 匹配的文物列表
        """
        try:
            docs = self.retrieve_relevant_documents(keyword, n_results=10)

            artifacts = []
            seen_ids = set()
            for doc in docs:
                metadata = doc.get('metadata', {})
                artifact_id = metadata.get('artifact_id')

                if artifact_id and artifact_id not in seen_ids:
                    seen_ids.add(artifact_id)
                    artifact = self.get_artifact_by_id(artifact_id)
                    if artifact:
                        artifacts.append(artifact)

            return artifacts
        except Exception as e:
            logger.error(f"关键词搜索失败: {e}")
            return []


vector_service = VectorService()
