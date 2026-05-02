# 向量检索测试脚本
import sys
sys.path.insert(0, '.')

from app.services.vector_service import vector_service

query = "壮族绣球"
print(f"测试查询: {query}")
docs = vector_service.retrieve_relevant_documents(query)
print(f"检索到 {len(docs)} 条文档")
for i, doc in enumerate(docs[:5]):
    print(f"\n--- 文档 {i+1} ---")
    print(f"距离: {doc['distance']}")
    print(f"内容: {doc['document'][:100]}...")
    print(f"元数据: {doc['metadata']}")
