# 配置管理

class Config:
    # 数据库配置
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "20060529cywl"
    MYSQL_DATABASE = "chatECNU"
    
    # ChromaDB配置
    CHROMA_DB_PATH = "./chromadb"
    
    # chatECNU API配置
    # 注意：实际使用时需要配置正确的API地址
    CHAT_ECNU_BASE_URL = "https://chat.ecnu.edu.cn/open/api/v1"
    CHAT_ECNU_API_KEY = "sk-e61bcaab500d47dbb5bd66b905964d57"
    
    # 应用配置
    APP_NAME = "华东师大博物馆AI智能导览系统"
    DEBUG = True
    
    # CORS配置
    CORS_ORIGINS = ["*"]
    
    # 模拟模式：当API不可用时使用
    USE_MOCK_MODE = True

# 实例化配置
config = Config()
