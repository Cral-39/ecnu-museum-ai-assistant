# MySQL数据库连接
import mysql.connector
from app.utils.config import config

class MySQLConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = mysql.connector.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE
            )
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def execute(self, query, params=None):
        """执行SQL查询"""
        try:
            if not self.conn:
                self.connect()
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            print(f"SQL执行失败: {e}")
            return False
    
    def fetch_all(self):
        """获取所有结果"""
        return self.cursor.fetchall()
    
    def fetch_one(self):
        """获取单个结果"""
        return self.cursor.fetchone()
    
    def commit(self):
        """提交事务"""
        if self.conn:
            self.conn.commit()

# 实例化数据库连接
mysql_conn = MySQLConnection()
