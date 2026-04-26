# 华东师大博物馆 AI 智能导览系统

## 📖 项目简介

基于学校 **chatECNU** 大模型，打造一个比官网更懂用户、比普通 AI 更懂文物的"数字导游"。我们将"查资料"变成"聊历史"，让博物馆的文物真正"活"起来。

本项目为参加"第三届全民数字素养与人工智能创新应用大赛"赛道二的作品，目标是基于 chatECNU API 和 RAG 技术，为华师大博物馆提供一个具备"卡片交互"能力的智能导览后端。

---

## 🎯 核心功能

| 功能模块 | 说明 |
|---------|------|
| 🏺 藏品"百科全书" | 用户问任何具体文物（如：大观通宝），AI 给出深度科普，并直接甩出官网的 3D 链接或高清图 |
| 📅 展览"百事通" | 实时同步校内展讯（如：年画展），回答展览时间、地点、必看亮点 |
| 🏛️ 校内"咨询台" | 解决场馆预约、开放时间、志愿者招募等琐碎问题 |
| 🎭 分馆"专业导引" | 针对古钱币馆、民俗馆等提供针对性的引导服务 |

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Python 3.10+ / FastAPI | 高性能异步框架 |
| 大模型编排 | LangChain | LLM 应用开发框架 |
| LLM 引擎 | chatECNU API | 华东师大大模型 API（兼容 OpenAI 格式） |
| 向量数据库 | ChromaDB | 本地持久化向量存储 |
| 主数据库 | MySQL 8.0+ | 关系型数据库存储文物和用户数据 |

---

## 📁 项目目录结构

```
chatECNU/
├── app/                          # 应用核心代码
│   ├── api/                      # API 路由层
│   │   ├── chat.py              # 聊天接口（POST /api/chat）
│   │   ├── exhibitions.py        # 展览接口（GET /api/exhibitions）
│   │   └── admin.py             # 管理端接口
│   ├── services/                 # 核心业务逻辑
│   │   ├── vector_service.py    # 向量检索服务（RAG 核心）
│   │   └── chat_service.py      # 聊天服务（LLM 调用）
│   ├── schemas/                  # Pydantic 数据模型
│   │   └── chat.py              # 聊天请求/响应模型
│   ├── database/                 # 数据库连接层
│   │   ├── mysql.py             # MySQL 连接管理
│   │   └── chromadb.py          # ChromaDB 连接管理
│   └── utils/                    # 工具函数
│       └── config.py            # 配置管理
├── scripts/                      # 运维脚本
│   └── init_vector_db.py         # 向量库初始化脚本
├── database/                     # 数据库脚本
│   ├── init.sql                 # MySQL 建表语句
│   └── test_data.sql            # 测试数据
├── main.py                       # FastAPI 应用入口
└── requirements.txt             # Python 依赖列表
```

---

## 🚀 环境配置与安装

### 前置要求

- **Python**: 3.10 或更高版本
- **MySQL**: 8.0 或更高版本
- **Git**: 用于版本控制

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd chatECNU
```

### 2. 创建虚拟环境（推荐）

```bash
# 使用 conda
conda create -n chatECNU python=3.10
conda activate chatECNU

# 或使用 venv
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

编辑 `app/utils/config.py` 或设置环境变量：

```python
# 数据库配置
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"  # 修改为你的密码
MYSQL_DATABASE = "chatECNU"

# API 配置
CHATECNU_API_KEY = "your_api_key"  # 从 developer.ecnu.edu.cn 获取
CHATECNU_BASE_URL = "https://developer.ecnu.edu.cn/"
```

### 5. 初始化数据库

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE IF NOT EXISTS chatECNU CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chatECNU;

-- 执行初始化脚本（在 MySQL 命令行中）
SOURCE D:/Projects/chatECNU/database/init.sql;
SOURCE D:/Projects/chatECNU/database/test_data.sql;
```

### 6. 初始化向量库

```bash
# 同步 MySQL 中的文物数据到 ChromaDB 向量库
python scripts/init_vector_db.py init

# 查看同步状态
python scripts/init_vector_db.py status
```

---

## 💻 本地开发运行

### 启动服务器

```bash
cd d:\Projects\chatECNU
uvicorn main:app --reload
```

服务器启动后，访问以下地址：

| 服务 | 地址 |
|------|------|
| API 文档 (Swagger) | http://localhost:8000/docs |
| ReDoc 文档 | http://localhost:8000/redoc |
| 欢迎页面 | http://localhost:8000/ |

### 测试 API

#### 1. 聊天接口

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "大观通宝是什么？", "stream": false}'
```

#### 2. 展览列表

```bash
curl -X GET "http://localhost:8000/api/exhibitions"
```

#### 3. 文物详情

```bash
curl -X GET "http://localhost:8000/api/artifacts/1"
```

#### 4. 知识库统计

```bash
curl -X GET "http://localhost:8000/api/knowledge-base/stats"
```

---

## 🔀 分支管理策略

### 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|---------|---------|------|
| 功能分支 | feature/<功能名称> | feature/user-auth |
| 修复分支 | fix/<问题描述> | fix/chat-stream-error |
| 发布分支 | release/<版本号> | release/v1.0.0 |
| 热修复分支 | hotfix/<问题描述> | hotfix/login-crash |

### 工作流程

```
1. 从 main 分支创建新分支
   git checkout -b feature/add-chat-streaming

2. 开发并提交代码
   git add .
   git commit -m "feat: 添加聊天流式输出功能"

3. 推送到远程仓库
   git push origin feature/add-chat-streaming

4. 创建 Pull Request
   - 描述清楚功能或修复内容
   - 指定至少一位团队成员 review

5. 合并后删除分支
   git checkout main
   git pull origin main
   git branch -d feature/add-chat-streaming
```

### Commit 消息规范

采用 **Conventional Commits** 规范：

```
<type>(<scope>): <subject>

feat(api): 添加流式输出支持
fix(vector): 修复向量检索距离计算错误
docs(readme): 更新项目文档
refactor(service): 重构聊天服务逻辑
test(chat): 添加聊天服务单元测试
```

---

## 👥 贡献规范

### 代码风格

- 遵循 **PEP 8** Python 代码规范
- 使用中文注释，关键函数添加文档字符串
- 变量和函数命名使用有意义的英文名称

### 提交规范

- 每次提交应该是一个独立的逻辑单元
- 提交信息清晰描述做了什么修改
- 不要提交敏感信息（密码、API Key 等）

### PR 流程

1. Fork 项目到个人仓库
2. 创建功能分支进行开发
3. 确保本地测试通过
4. 提交 PR 并描述改动内容
5. 等待代码 review
6. 合并后同步更新

### Review 检查清单

- [ ] 代码逻辑正确无误
- [ ] 有适当的单元测试
- [ ] 文档已更新（如有必要）
- [ ] 没有敏感信息泄露
- [ ] 遵循项目代码风格

---

## ❓ 常见问题解答

### Q1: 启动服务器报错 "ModuleNotFoundError"

**A**: 确认已激活虚拟环境并安装依赖：

```bash
conda activate chatECNU
pip install -r requirements.txt
```

### Q2: MySQL 连接失败

**A**: 检查以下配置：

1. MySQL 服务是否启动
2. 密码是否正确
3. 数据库是否已创建
4. 用户权限是否足够

```bash
# 测试 MySQL 连接
mysql -u root -p -e "SHOW DATABASES;"
```

### Q3: ChromaDB 初始化失败

**A**: 检查依赖是否安装完整，尝试重新安装：

```bash
pip uninstall chromadb
pip install chromadb
python scripts/init_vector_db.py init
```

### Q4: API 返回 401 错误

**A**: 检查 `config.py` 中的 `CHATECNU_API_KEY` 是否正确配置，或当前使用模拟模式（`USE_MOCK_MODE = True`）。

### Q5: 向量检索不准确

**A**:

1. 确认向量库已同步最新数据：`python scripts/init_vector_db.py status`
2. 检查相关性阈值设置是否合理
3. 确认文物描述信息是否完整

### Q6: 如何查看详细的调试日志？

**A**: 在 `config.py` 中将 `DEBUG = True`，重启服务器后控制台会输出详细的执行日志。

---

## 📊 系统架构图

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端      │────▶│   FastAPI   │────▶│  chatECNU  │
│   Vue.js    │◀────│   Backend   │◀────│    API      │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              ┌─────────┐   ┌───────────┐
              │ ChromaDB│   │   MySQL   │
              │ (向量库) │   │ (关系库)  │
              └─────────┘   └───────────┘
```

---

## 📝 许可证

本项目仅供学习和研究使用，禁止商业用途。

---

## 👏 致谢

感谢华东师范大学数字博物馆提供的数据支持，以及 chatECNU 团队提供的 API 服务。
