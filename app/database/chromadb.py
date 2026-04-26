# ChromaDB连接 - 使用新版本API
import chromadb
from app.utils.config import config
import logging

logger = logging.getLogger(__name__)


class ChromaDBConnection:
    def __init__(self):
        """
        初始化ChromaDB连接
        使用新版本的PersistentClient API
        """
        self.client = None
        self.collection = None
        self.collection_name = "museum_artifacts"
        self._connect()  # 初始化时自动连接
    
    def _connect(self):
        """
        建立ChromaDB连接
        使用新版本的PersistentClient，移除了旧的Settings配置
        """
        try:
            # 新版本的PersistentClient不需要Settings参数
            self.client = chromadb.PersistentClient(
                path=config.CHROMA_DB_PATH
            )
            
            # 创建或获取集合
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "华东师大博物馆文物知识库"}
            )
            
            logger.info(f"ChromaDB连接成功，集合: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"ChromaDB连接失败: {e}")
            self.client = None
            self.collection = None
            return False
    
    def ensure_connection(self):
        """
        确保ChromaDB连接已建立
        如果连接失败，会自动重连
        """
        if not self.collection or not self.client:
            return self._connect()
        return True
    
    def add_documents(self, documents, metadatas=None, ids=None):
        """
        添加文档到向量库
        :param documents: 文档列表
        :param metadatas: 元数据列表
        :param ids: 文档ID列表
        :return: 是否添加成功
        """
        if not self.ensure_connection():
            logger.error("ChromaDB连接失败，无法添加文档")
            return False
        
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"成功添加{len(documents)}个文档到向量库")
            return True
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            return False
    
    def query(self, query_text, n_results=5):
        """
        查询相关文档
        :param query_text: 查询文本
        :param n_results: 返回结果数量
        :return: 查询结果
        """
        if not self.ensure_connection():
            logger.error("ChromaDB连接失败，无法查询")
            return None
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"查询失败: {e}")
            return None
    
    def get_collection_size(self):
        """
        获取集合大小
        :return: 集合中文档数量
        """
        if not self.ensure_connection():
            logger.error("ChromaDB连接失败，无法获取集合大小")
            return 0
        
        try:
            count = self.collection.count()
            logger.info(f"向量库文档数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取集合大小失败: {e}")
            return 0
    
    def clear_collection(self):
        """
        清空集合中的所有文档
        :return: 是否清空成功
        """
        if not self.ensure_connection():
            logger.error("ChromaDB连接失败，无法清空集合")
            return False
        
        try:
            # 先删除集合
            self.client.delete_collection(name=self.collection_name)
            # 重新创建集合
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "华东师大博物馆文物知识库"}
            )
            logger.info("向量库已清空并重新创建")
            return True
        except Exception as e:
            logger.error(f"清空集合失败: {e}")
            return False


# 实例化ChromaDB连接
chromadb_conn = ChromaDBConnection()
