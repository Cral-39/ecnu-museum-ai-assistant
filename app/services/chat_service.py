# 聊天服务 - 与大模型交互的核心
# 负责处理用户查询，调用chatECNU API，解析回答并返回文物卡片

import re
import logging
from typing import Dict, List, Optional, Generator, Any
from openai import OpenAI
from app.utils.config import config
from app.services.vector_service import vector_service

logger = logging.getLogger(__name__)


class ChatService:
    """
    聊天服务类
    负责与大模型交互，实现文物知识问答、展览咨询等功能
    """

    def __init__(self):
        """
        初始化聊天服务
        配置openai客户端连接chatECNU API
        """
        if not config.USE_MOCK_MODE:
            self.client = OpenAI(
                api_key=config.CHAT_ECNU_API_KEY,
                base_url=config.CHAT_ECNU_BASE_URL
            )
        else:
            self.client = None
        self._system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """
        构建系统提示词
        定义AI的角色定位和回答风格
        :return: 系统提示词字符串
        """
        return """你是华东师大博物馆的资深导游，具备丰富的文物知识和讲解经验。

你的职责：
1. 为游客提供准确、专业的文物讲解和历史背景介绍
2. 解答关于博物馆展览、参观时间、预约方式等问题
3. 引导游客深入了解展品背后的历史文化故事

回答风格：
- 语调亲切友好，像学长学姐一样温暖
- 表达学术严谨，确保历史信息准确，绝不捏造
- 语言生动有趣，让文物"活"起来
- 适当使用类比和故事，帮助游客理解

重要规则：
1. 基于提供的文物知识进行回答，不要编造信息
2. 如果用户提到特定文物，请在回答末尾添加 [ID:xxx] 标签，其中xxx是文物的ID
3. 保持回答简洁明了，避免冗长的学术论述
4. 对于不确定的问题，坦诚告知并建议参考官方资料

现在开始与游客交流，做一个专业而亲切的博物馆导游。"""

    def generate_prompt(self, user_query: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """
        生成大模型提示词
        结合用户查询和相关文档
        :param user_query: 用户查询
        :param relevant_docs: 相关文档列表
        :return: 完整的提示词
        """
        context = ""
        for i, doc in enumerate(relevant_docs[:3]):
            context += f"【参考资料{i+1}】\n{doc['document']}\n\n"

        prompt = f"用户问题：{user_query}\n\n参考资料：\n{context}\n\n请基于以上参考资料回答用户问题，确保信息准确。如果提到特定文物，请在回答末尾添加 [ID:xxx] 标签。"
        return prompt

    def chat_completion(self, user_query: str) -> Dict[str, Any]:
        """
        聊天完成（非流式）
        :param user_query: 用户查询
        :return: 包含回答和元数据的字典
        """
        try:
            relevant_docs = vector_service.retrieve_relevant_documents(user_query)
            prompt = self.generate_prompt(user_query, relevant_docs)

            if config.USE_MOCK_MODE:
                # 使用模拟回答
                answer, artifact_id = self._get_mock_answer(user_query, relevant_docs)
            else:
                # 调用实际API
                response = self.client.chat.completions.create(
                    model="ecnu-plus",
                    messages=[
                        {"role": "system", "content": self._system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                answer = response.choices[0].message.content
                artifact_id = self.extract_artifact_id(answer)

            artifact_info = None
            if artifact_id:
                artifact_info = vector_service.get_artifact_by_id(artifact_id)
                answer = self._remove_artifact_tag(answer)

            result = {
                "text": answer,
                "metadata": {
                    "artifact": artifact_info,
                    "relevant_docs": relevant_docs,
                    "has_artifact_card": artifact_info is not None
                }
            }

            logger.info(f"回答完成，检索到{len(relevant_docs)}条相关文档")
            return result

        except Exception as e:
            logger.error(f"聊天完成失败: {e}")
            return {
                "text": "抱歉，我暂时无法回答您的问题，请稍后再试。",
                "metadata": {}
            }

    def stream_chat_completion(self, user_query: str) -> Generator[Dict[str, Any], None, None]:
        """
        流式聊天完成
        :param user_query: 用户查询
        :yield: 包含文本片段和元数据的字典
        """
        try:
            relevant_docs = vector_service.retrieve_relevant_documents(user_query)
            prompt = self.generate_prompt(user_query, relevant_docs)

            if config.USE_MOCK_MODE:
                # 模拟流式输出
                answer, artifact_id = self._get_mock_answer(user_query, relevant_docs)
                artifact_info = None
                if artifact_id:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    answer = self._remove_artifact_tag(answer)
                
                # 模拟流式输出
                chunks = answer.split(' ')
                for i, chunk in enumerate(chunks):
                    is_last = i == len(chunks) - 1
                    yield {
                        "text": chunk + (' ' if not is_last else ''),
                        "metadata": {
                            "artifact": artifact_info if is_last else None,
                            "relevant_docs": relevant_docs if is_last else None,
                            "has_artifact_card": (artifact_info is not None) if is_last else False,
                            "finish": is_last
                        }
                    }
            else:
                # 调用实际API流式输出
                stream = self.client.chat.completions.create(
                    model="ecnu-plus",
                    messages=[
                        {"role": "system", "content": self._system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    stream=True
                )

                full_answer = ""
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_answer += content
                        yield {
                            "text": content,
                            "metadata": {
                                "finish": False
                            }
                        }

                # 处理最终答案，提取文物ID
                artifact_id = self.extract_artifact_id(full_answer)
                artifact_info = None
                if artifact_id:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    full_answer = self._remove_artifact_tag(full_answer)

                # 发送最终的元数据
                yield {
                    "text": "",
                    "metadata": {
                        "artifact": artifact_info,
                        "relevant_docs": relevant_docs,
                        "has_artifact_card": artifact_info is not None,
                        "finish": True
                    }
                }

        except Exception as e:
            logger.error(f"流式聊天失败: {e}")
            yield {
                "text": "抱歉，我暂时无法回答您的问题，请稍后再试。",
                "metadata": {
                    "finish": True
                }
            }

    def extract_artifact_id(self, text: str) -> Optional[int]:
        """
        从回答中提取文物ID
        :param text: 回答文本
        :return: 文物ID，如果没有则返回None
        """
        match = re.search(r'\[ID:(\d+)\]', text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
        return None

    def _remove_artifact_tag(self, text: str) -> str:
        """
        从回答中移除文物ID标签
        :param text: 回答文本
        :return: 移除标签后的文本
        """
        return re.sub(r'\s*\[ID:\d+\]\s*$', '', text)

    def _get_mock_answer(self, user_query: str, relevant_docs: List[Dict[str, Any]]) -> tuple:
        """
        获取模拟回答（当API不可用时使用）
        :param user_query: 用户查询
        :param relevant_docs: 相关文档
        :return: (回答文本, 文物ID)
        """
        # 检测用户查询类型
        query_lower = user_query.lower()
        
        # 常见非文物相关问题
        if any(keyword in query_lower for keyword in ["预约", "参观", "怎么去", "如何", "联系"]):
            return "参观华东师大博物馆无需预约，凭有效证件即可免费入场。团体参观（10人以上）建议提前联系博物馆预约讲解服务。", None
        elif any(keyword in query_lower for keyword in ["开放时间", "什么时候", "几点", "闭馆"]):
            return "华东师大博物馆的开放时间为：周二至周日 9:00-17:00（16:30停止入场），周一闭馆。节假日开放时间可能有所调整，请关注官方通知。", None
        elif any(keyword in query_lower for keyword in ["展览", "展讯", "活动", "特展"]):
            return "目前华东师大博物馆有多个精彩展览正在进行，包括《历史文物特展》、《生物多样性展》等。您可以通过官网或本系统查询详细展览信息。", None
        elif any(keyword in query_lower for keyword in ["志愿者", "招募", "报名"]):
            return "华东师大博物馆常年招募志愿者，主要负责讲解、引导、活动协助等工作。有意者可关注博物馆官网或公众号了解招募信息并报名。", None
        
        # 检测用户查询中是否包含文物名称
        artifact_names = ["大观通宝", "鸭嘴兽", "青铜剑", "鎏金佛像", "敦煌写经", "壮族绣球", "明代一品文官补服"]
        artifact_ids = {
            "大观通宝": 1, 
            "鸭嘴兽": 11, 
            "青铜剑": 2, 
            "鎏金佛像": 3, 
            "敦煌写经": 4,
            "壮族绣球": 28,
            "明代一品文官补服": 8
        }
        
        # 检查是否提到特定文物
        mentioned_artifact = None
        for name, aid in artifact_ids.items():
            if name in user_query:
                mentioned_artifact = (name, aid)
                break
        
        # 生成模拟回答
        if mentioned_artifact:
            name, aid = mentioned_artifact
            return f"您询问的{name}是华东师大博物馆的珍贵藏品。{name}具有重要的历史价值，是研究相关历史时期的重要实物资料。[ID:{aid}]", aid
        elif relevant_docs:
            # 只有当有相关文档且距离较小时才返回文物信息
            doc = relevant_docs[0]
            if doc.get('distance', 100) < 1.0:
                metadata = doc.get('metadata', {})
                artifact_name = metadata.get('name', '文物')
                return f"关于您的问题，我可以为您提供相关信息。根据知识库，{artifact_name}是华东师大博物馆的重要藏品，具有丰富的历史文化价值。", metadata.get('artifact_id')
            else:
                return "您好！我是华东师大博物馆的AI导览助手，有什么可以帮助您的吗？", None
        else:
            return "您好！我是华东师大博物馆的AI导览助手，有什么可以帮助您的吗？", None


chat_service = ChatService()
