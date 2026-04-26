# 初始化向量库脚本
# 将MySQL中的文物数据同步到ChromaDB向量库

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vector_service import vector_service
from app.database.mysql import mysql_conn
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init_vector_db():
    """
    初始化向量数据库
    从MySQL读取文物数据，同步到ChromaDB向量库
    """
    logger.info("开始初始化向量数据库...")

    try:
        mysql_conn.connect()
        mysql_conn.execute("SELECT COUNT(*) as count FROM artifacts")
        result = mysql_conn.fetch_one()
        mysql_count = result['count']
        logger.info(f"MySQL中共有 {mysql_count} 件文物")

        mysql_conn.execute("SELECT * FROM artifacts")
        artifacts = mysql_conn.fetch_all()
        mysql_conn.close()

        if not artifacts:
            logger.warning("MySQL中没有文物数据，请先执行数据库初始化")
            return False

        success_count = 0
        for artifact in artifacts:
            if vector_service.add_artifact_to_knowledge_base(artifact):
                success_count += 1
                logger.info(f"同步文物: {artifact['name']}")

        logger.info(f"向量库初始化完成！成功同步 {success_count}/{mysql_count} 件文物")
        return True

    except Exception as e:
        logger.error(f"初始化向量库失败: {e}")
        return False


def check_database_status():
    """
    检查数据库状态
    """
    logger.info("检查数据库状态...")

    try:
        mysql_conn.connect()
        mysql_conn.execute("SELECT COUNT(*) as count FROM artifacts")
        mysql_count = mysql_conn.fetch_one()['count']

        mysql_conn.execute("SELECT COUNT(*) as count FROM exhibitions")
        exhibition_count = mysql_conn.fetch_one()['count']

        mysql_conn.execute("SELECT COUNT(*) as count FROM consultations")
        consultation_count = mysql_conn.fetch_one()['count']

        mysql_conn.close()

        vector_count = vector_service.get_collection_size()

        logger.info("=" * 50)
        logger.info("数据库状态报告")
        logger.info("=" * 50)
        logger.info(f"MySQL - 文物表: {mysql_count} 条记录")
        logger.info(f"MySQL - 展览表: {exhibition_count} 条记录")
        logger.info(f"MySQL - 咨询记录表: {consultation_count} 条记录")
        logger.info(f"ChromaDB - 向量库: {vector_count} 条索引")
        logger.info("=" * 50)

        return True

    except Exception as e:
        logger.error(f"检查数据库状态失败: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="向量数据库管理工具")
    parser.add_argument("action", choices=["init", "status"], help="操作: init(初始化) 或 status(状态检查)")

    args = parser.parse_args()

    if args.action == "init":
        init_vector_db()
    elif args.action == "status":
        check_database_status()
