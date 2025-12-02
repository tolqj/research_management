"""
科研管理系统（Research Management System）
FastAPI 主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, user, project, paper, fund, achievement, statistics

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="科研管理系统 API",
    description="Research Management System - 提供科研项目、论文、经费、成果等管理功能",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc",  # ReDoc
)

# 配置 CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # 前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/users", tags=["用户管理"])
app.include_router(project.router, prefix="/api/projects", tags=["项目管理"])
app.include_router(paper.router, prefix="/api/papers", tags=["论文管理"])
app.include_router(fund.router, prefix="/api/funds", tags=["经费管理"])
app.include_router(achievement.router, prefix="/api/achievements", tags=["成果管理"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计分析"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用科研管理系统 API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "RMS Backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式自动重载
        log_level="info"
    )
