# 测试 chatECNU API 连接
import openai
from app.utils.config import config

# 配置 OpenAI 客户端
client = openai.OpenAI(
    api_key=config.CHAT_ECNU_API_KEY,
    base_url=config.CHAT_ECNU_BASE_URL
)

try:
    print("测试 chatECNU API 连接...")
    print(f"Base URL: {config.CHAT_ECNU_BASE_URL}")
    print(f"API Key: {config.CHAT_ECNU_API_KEY[:10]}...")
    
    # 发送测试请求
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "你好，测试连接"}
        ],
        temperature=0.7
    )
    
    print("\n✅ API 连接成功！")
    print(f"响应: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ API 连接失败: {e}")
    print("请检查 API Key 和 Base URL 是否正确")
