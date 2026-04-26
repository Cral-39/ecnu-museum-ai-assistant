# 配置管理

class Config:
    # 数据库配置
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_DATABASE = "chatECNU"
    
    # ChromaDB配置
    CHROMA_DB_PATH = "./chromadb"
    
    # chatECNU API配置
    CHAT_ECNU_BASE_URL = "https://developer.ecnu.edu.cn/"
    CHAT_ECNU_API_KEY = "sk-e61bcaab500d47dbb5bd66b905964d57"  # 在这里填写您的API key
    
    # 应用配置
    APP_NAME = "华东师大博物馆AI智能导览系统"
    DEBUG = True
    
    # CORS配置
    CORS_ORIGINS = ["*"]

# 实例化配置
config = Config()