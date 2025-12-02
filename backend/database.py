"""
数据库配置文件
使用 SQLAlchemy 连接 MySQL 数据库
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 数据库配置
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "research_management_system"

# 数据库连接 URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 开发环境打印 SQL 语句
    pool_pre_ping=True,  # 自动重连
    pool_recycle=3600,  # 连接回收时间
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类
Base = declarative_base()


# 依赖注入：获取数据库会话
def get_db():
    """
    FastAPI 依赖注入函数
    每个请求获取独立的数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
