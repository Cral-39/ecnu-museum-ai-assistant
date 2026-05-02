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
2. 如果你的回答只介绍一个文物，在回复末尾加 [ID:文物ID]
3. 如果你的回答介绍多个文物，不要添加任何ID标签
4. 回答应内容完整、信息丰富，详细介绍相关文物知识
5. 不要主动扩展话题，用户问什么答什么

核心原则：基于馆方资料，提供准确、完整的文物信息。"""

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
                artifact_id = self.extract_artifact_id(answer, relevant_docs)

            # 卡片显示策略：完全依赖AI返回的[ID:X]标签
            # AI会自己决定：如果只介绍一个文物就带[ID:X]，介绍多个就不带
            should_show_card = artifact_id is not None
            artifact_info = None
            if should_show_card:
                artifact_info = vector_service.get_artifact_by_id(artifact_id)
                answer = self._remove_artifact_tag(answer)

            result = {
                "text": answer,
                "metadata": {
                    "artifact": artifact_info,
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
                # 使用模拟回答
                answer, artifact_id = self._get_mock_answer(user_query, relevant_docs)

                # 卡片显示策略：完全依赖AI返回的[ID:X]标签
                should_show_card = artifact_id is not None
                artifact_info = None
                if should_show_card:
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
                artifact_id = self.extract_artifact_id(full_answer, relevant_docs)

                # 卡片显示策略：完全依赖AI返回的[ID:X]标签
                should_show_card = artifact_id is not None
                artifact_info = None
                if should_show_card:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    full_answer = self._remove_artifact_tag(full_answer)

                yield {
                    "text": "",
                    "metadata": {
                        "artifact": artifact_info,
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

    def extract_artifact_id(self, text: str, relevant_docs: List[Dict[str, Any]] = None) -> Optional[int]:
        """
        从回答中提取文物ID
        :param text: 回答文本
        :param relevant_docs: 相关文档列表，用于根据名称查找ID
        :return: 文物ID，如果没有则返回None
        """
        # 先尝试提取数字ID [ID:28]
        match = re.search(r'\[ID:(\d+)\]', text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
        
        # 如果没有找到数字ID，尝试提取名称形式的ID [ID:文物名称]
        name_match = re.search(r'\[ID:([^\]]+)\]', text)
        if name_match and relevant_docs:
            artifact_name = name_match.group(1).strip()
            # 在相关文档中查找匹配的文物名称
            for doc in relevant_docs:
                doc_name = doc.get('metadata', {}).get('name', '').strip()
                if doc_name and artifact_name in doc_name:
                    return doc.get('metadata', {}).get('artifact_id')
                # 也检查文档内容中是否包含该名称
                doc_content = doc.get('document', '')
                if artifact_name in doc_content:
                    return doc.get('metadata', {}).get('artifact_id')
        
        return None

    def _remove_artifact_tag(self, text: str) -> str:
        """
        从回答中移除文物ID标签
        :param text: 回答文本
        :return: 移除标签后的文本
        """
        return re.sub(r'\s*\[ID:\d+\]\s*$', '', text)

    def image_recognition(self, image_base64: str) -> Dict[str, Any]:
        """
        图片识别功能
        :param image_base64: Base64编码的图片数据
        :return: 包含识别结果和文物信息的字典
        """
        try:
            if config.USE_MOCK_MODE:
                # 使用模拟识别结果
                result = self._get_mock_image_recognition()
            else:
                # 调用多模态API进行图片识别
                prompt = """请识别这张图片中的物品，并描述它是什么。如果是文物，请提供详细信息，包括名称、年代、类别等。如果识别到文物，请在回答末尾添加 [ID:文物ID] 标签。"""
                
                response = self.client.chat.completions.create(
                    model="ecnu-plus",
                    messages=[
                        {"role": "system", "content": self._system_prompt},
                        {"role": "user", "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        ]}
                    ],
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                
                # 提取文物ID并查找相关信息
                artifact_id = self.extract_artifact_id(answer)
                should_show_card = artifact_id is not None
                artifact_info = None
                
                if should_show_card:
                    artifact_info = vector_service.get_artifact_by_id(artifact_id)
                    answer = self._remove_artifact_tag(answer)
                
                result = {
                    "text": answer,
                    "metadata": {
                        "artifact": artifact_info,
                        "relevant_docs": [],
                        "has_artifact_card": should_show_card
                    }
                }
            
            logger.info("图片识别完成")
            return result
        
        except Exception as e:
            logger.error(f"图片识别失败: {e}")
            return {
                "text": "抱歉，图片识别失败，请重试。",
                "metadata": {}
            }
    
    def _get_mock_image_recognition(self) -> Dict[str, Any]:
        """
        获取模拟图片识别结果
        :return: 识别结果字典
        """
        # 模拟识别到一个随机文物
        mock_artifacts = [
            {
                "id": 1,
                "name": "大观通宝",
                "category": "古钱币",
                "collection": "古代钱币馆",
                "era": "北宋",
                "description": "北宋徽宗大观年间铸造的铜钱，钱文为瘦金体，制作精美，具有重要的历史价值。",
                "image_url": "https://digitalmuseum.ecnu.edu.cn/images/coin1.jpg",
                "three_d_url": "https://digitalmuseum.ecnu.edu.cn/artifacts/1"
            },
            {
                "id": 11,
                "name": "鸭嘴兽标本",
                "category": "标本",
                "collection": "生物标本馆",
                "era": "现代",
                "description": "珍贵的单孔类哺乳动物标本，全国仅三件。鸭嘴兽是进化论的重要证据，具有哺乳动物和爬行动物的双重特征。",
                "image_url": "https://digitalmuseum.ecnu.edu.cn/images/specimen1.jpg",
                "three_d_url": "https://digitalmuseum.ecnu.edu.cn/artifacts/16"
            },
            {
                "id": 28,
                "name": "壮族绣球",
                "category": "民俗工艺品",
                "collection": "海上风民俗博物馆",
                "era": "现代",
                "description": "壮族传统手工刺绣工艺品，绣球是壮族青年男女定情信物。刺绣图案精美，色彩鲜艳，寓意吉祥。",
                "image_url": "https://digitalmuseum.ecnu.edu.cn/images/folk8.jpg",
                "three_d_url": "https://digitalmuseum.ecnu.edu.cn/artifacts/28"
            }
        ]
        
        import random
        artifact = random.choice(mock_artifacts)
        
        return {
            "text": f"图片识别完成：这是{artifact['name']}，属于{artifact['category']}，收藏于{artifact['collection']}。[ID:{artifact['id']}]",
            "metadata": {
                "artifact": artifact,
                "relevant_docs": [],
                "has_artifact_card": True
            }
        }
    
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
