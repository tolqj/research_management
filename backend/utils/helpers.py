"""
通用辅助函数
"""
from typing import Optional
from datetime import datetime
import json


def parse_json_field(field: Optional[str]) -> dict:
    """
    解析 JSON 字段
    """
    if not field:
        return {}
    try:
        return json.loads(field)
    except:
        return {}


def to_json_string(data: dict) -> str:
    """
    转换为 JSON 字符串
    """
    return json.dumps(data, ensure_ascii=False)


def format_datetime(dt: Optional[datetime], fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """
    格式化日期时间
    """
    if dt is None:
        return None
    return dt.strftime(fmt)


def paginate_query(query, page: int = 1, page_size: int = 20):
    """
    分页查询
    
    Args:
        query: SQLAlchemy 查询对象
        page: 页码（从1开始）
        page_size: 每页数量
    
    Returns:
        tuple: (总数, 分页数据)
    """
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return total, items


def success_response(data=None, message="操作成功"):
    """
    成功响应
    """
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error_response(message="操作失败", code=400):
    """
    错误响应
    """
    return {
        "code": code,
        "message": message,
        "data": None
    }
