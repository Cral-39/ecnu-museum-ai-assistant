# FastAPI应用入口
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import config
from app.api import chat, exhibitions, admin

# 创建FastAPI应用
app = FastAPI(
    title=config.APP_NAME,
    description="华东师大博物馆AI智能导览系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(exhibitions.router, prefix="/api", tags=["exhibitions"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# 根路径
@app.get("/")
def read_root():
    return {
        "message": "欢迎使用华东师大博物馆AI智能导览系统",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
