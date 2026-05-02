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
        return """你是华东师大博物馆的智能导游。

回答规则：
1. 严格基于提供的文物知识回答，不要编造
2. 如果用户明确询问某件文物，回复末尾加 [ID:文物ID]
3. 回答控制在80字以内，精准传达核心信息
4. 不要主动扩展话题，用户问什么答什么

核心原则：简洁但不缺失关键信息，让用户快速获得有价值的内容。"""

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

            # 从检索结果中提取所有涉及的 artifact_id 和名称
            unique_artifact_ids = set()
            artifact_names_in_results = set()
            if relevant_docs:
                for doc in relevant_docs:
                    aid = doc.get('metadata', {}).get('artifact_id')
                    name = doc.get('metadata', {}).get('name')
                    if aid:
                        unique_artifact_ids.add(aid)
                    if name:
                        artifact_names_in_results.add(name)

            # 检查查询中提到了哪些文物名称（精确匹配）
            mentioned_artifacts_in_query = []
            for name in artifact_names_in_results:
                if name and name in user_query:
                    mentioned_artifacts_in_query.append(name)

            # 检查查询中是否有文物名称的部分匹配
            # 例如查询"鸭嘴兽"能匹配到"鸭嘴兽标本"
            partial_mentioned_artifacts = []
            for name in artifact_names_in_results:
                if name and name not in mentioned_artifacts_in_query:
                    for length in range(len(name), 2, -1):
                        if name[:length] in user_query:
                            partial_mentioned_artifacts.append(name)
                            break

            # 合并精确匹配和部分匹配，避免重复计数同一个文物
            all_mentioned_artifacts = mentioned_artifacts_in_query + [a for a in partial_mentioned_artifacts if a not in mentioned_artifacts_in_query]

            # 判断是否为多藏品查询
            # 如果查询中使用了并列词（和、与、以及、或者、还是、还是等），认为是多藏品查询
            multi_artifact_keywords = ['和', '与', '以及', '或者', '还是', '跟', '同', '还是']
            is_multi_query = any(kw in user_query for kw in multi_artifact_keywords)

            total_mentioned = len(all_mentioned_artifacts)

            # 显示卡片的策略：
            # 1. 如果检索结果只涉及唯一一个文物，显示卡片
            # 2. 如果查询中只提到了唯一一个文物名称（精确或部分匹配），且不是多藏品查询，显示卡片
            # 3. 如果查询中提到了多个不同文物，或使用了并列词，不显示卡片
            should_show_card = (len(unique_artifact_ids) == 1 and len(relevant_docs) > 0) or (total_mentioned == 1 and not is_multi_query)

            # 使用正确的 artifact_id 获取详细信息
            mentioned_artifact_id = None
            if total_mentioned == 1 and all_mentioned_artifacts:
                target_name = all_mentioned_artifacts[0]
                for doc in relevant_docs:
                    if doc.get('metadata', {}).get('name') == target_name:
                        mentioned_artifact_id = doc.get('metadata', {}).get('artifact_id')
                        break

            artifact_id = mentioned_artifact_id if mentioned_artifact_id else (list(unique_artifact_ids)[0] if unique_artifact_ids else None)

            artifact_info = None
            if artifact_id:
                artifact_info = vector_service.get_artifact_by_id(artifact_id)
                answer = self._remove_artifact_tag(answer)

            result = {
                "text": answer,
                "metadata": {
                    "artifact": artifact_info if should_show_card else None,
                    "relevant_docs": relevant_docs,
                    "has_artifact_card": should_show_card
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
                answer, artifact_id = self._get_mock_answer(user_query, relevant_docs)

                unique_artifact_ids = set()
                artifact_names_in_results = set()
                if relevant_docs:
                    for doc in relevant_docs:
                        aid = doc.get('metadata', {}).get('artifact_id')
                        name = doc.get('metadata', {}).get('name')
                        if aid:
                            unique_artifact_ids.add(aid)
                        if name:
                            artifact_names_in_results.add(name)

                mentioned_artifacts_in_query = []
                for name in artifact_names_in_results:
                    if name and name in user_query:
                        mentioned_artifacts_in_query.append(name)

                partial_mentioned_artifacts = []
                for name in artifact_names_in_results:
                    if name and name not in mentioned_artifacts_in_query:
                        for length in range(len(name), 2, -1):
                            if name[:length] in user_query:
                                partial_mentioned_artifacts.append(name)
                                break

                all_mentioned_artifacts = mentioned_artifacts_in_query + [a for a in partial_mentioned_artifacts if a not in mentioned_artifacts_in_query]

                multi_artifact_keywords = ['和', '与', '以及', '或者', '还是', '跟', '同']
                is_multi_query = any(kw in user_query for kw in multi_artifact_keywords)
                total_mentioned = len(all_mentioned_artifacts)

                should_show_card = (len(unique_artifact_ids) == 1 and len(relevant_docs) > 0) or (total_mentioned == 1 and not is_multi_query)

                mentioned_artifact_id = None
                if total_mentioned == 1 and all_mentioned_artifacts:
                    target_name = all_mentioned_artifacts[0]
                    for doc in relevant_docs:
                        if doc.get('metadata', {}).get('name') == target_name:
                            mentioned_artifact_id = doc.get('metadata', {}).get('artifact_id')
                            break

                if artifact_id is None:
                    artifact_id = mentioned_artifact_id if mentioned_artifact_id else (list(unique_artifact_ids)[0] if unique_artifact_ids else None)

                artifact_info = None
                if artifact_id:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    answer = self._remove_artifact_tag(answer)

                chunks = answer.split(' ')
                for i, chunk in enumerate(chunks):
                    is_last = i == len(chunks) - 1
                    yield {
                        "text": chunk + (' ' if not is_last else ''),
                        "metadata": {
                            "artifact": artifact_info if (is_last and should_show_card) else None,
                            "relevant_docs": relevant_docs if is_last else None,
                            "has_artifact_card": should_show_card if is_last else False,
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

                # 使用与 chat_completion 相同的逻辑确定 artifact_id
                unique_artifact_ids = set()
                artifact_names_in_results = set()
                mentioned_artifacts_in_query = []
                partial_mentioned_artifacts = []
                if relevant_docs:
                    for doc in relevant_docs:
                        aid = doc.get('metadata', {}).get('artifact_id')
                        name = doc.get('metadata', {}).get('name')
                        if aid:
                            unique_artifact_ids.add(aid)
                        if name:
                            artifact_names_in_results.add(name)
                        if name and name in user_query:
                            mentioned_artifacts_in_query.append(name)

                for name in artifact_names_in_results:
                    if name and name not in mentioned_artifacts_in_query:
                        for length in range(len(name), 2, -1):
                            if name[:length] in user_query:
                                partial_mentioned_artifacts.append(name)
                                break

                all_mentioned_artifacts = mentioned_artifacts_in_query + [a for a in partial_mentioned_artifacts if a not in mentioned_artifacts_in_query]

                multi_artifact_keywords = ['和', '与', '以及', '或者', '还是', '跟', '同']
                is_multi_query = any(kw in user_query for kw in multi_artifact_keywords)
                total_mentioned = len(all_mentioned_artifacts)

                should_show_card = (len(unique_artifact_ids) == 1 and len(relevant_docs) > 0) or (total_mentioned == 1 and not is_multi_query)

                mentioned_artifact_id = None
                if total_mentioned == 1 and all_mentioned_artifacts:
                    target_name = all_mentioned_artifacts[0]
                    for doc in relevant_docs:
                        if doc.get('metadata', {}).get('name') == target_name:
                            mentioned_artifact_id = doc.get('metadata', {}).get('artifact_id')
                            break

                if artifact_id is None:
                    artifact_id = mentioned_artifact_id if mentioned_artifact_id else (list(unique_artifact_ids)[0] if unique_artifact_ids else None)

                artifact_info = None
                if artifact_id:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    full_answer = self._remove_artifact_tag(full_answer)

                yield {
                    "text": "",
                    "metadata": {
                        "artifact": artifact_info if should_show_card else None,
                        "relevant_docs": relevant_docs,
                        "has_artifact_card": should_show_card,
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
