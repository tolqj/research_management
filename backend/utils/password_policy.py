"""
密码安全策略（等保二级要求）
- 密码复杂度要求
- 密码历史记录
- 密码过期策略
"""
import re
from datetime import datetime, timedelta
from typing import Tuple


class PasswordPolicy:
    """密码策略类"""
    
    # 密码策略配置
    MIN_LENGTH = 8  # 最小长度
    MAX_LENGTH = 32  # 最大长度
    REQUIRE_UPPERCASE = True  # 要求大写字母
    REQUIRE_LOWERCASE = True  # 要求小写字母
    REQUIRE_DIGIT = True  # 要求数字
    REQUIRE_SPECIAL = True  # 要求特殊字符
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # 允许的特殊字符
    PASSWORD_EXPIRE_DAYS = 90  # 密码过期天数
    MAX_LOGIN_FAILURES = 5  # 最大登录失败次数
    LOCKOUT_DURATION_MINUTES = 30  # 锁定时长（分钟）
    
    @classmethod
    def validate_password_strength(cls, password: str) -> Tuple[bool, str]:
        """
        验证密码强度
        
        Returns:
            (是否有效, 错误消息)
        """
        # 检查长度
        if len(password) < cls.MIN_LENGTH:
            return False, f"密码长度至少为 {cls.MIN_LENGTH} 位"
        
        if len(password) > cls.MAX_LENGTH:
            return False, f"密码长度不能超过 {cls.MAX_LENGTH} 位"
        
        # 检查大写字母
        if cls.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            return False, "密码必须包含至少一个大写字母"
        
        # 检查小写字母
        if cls.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            return False, "密码必须包含至少一个小写字母"
        
        # 检查数字
        if cls.REQUIRE_DIGIT and not re.search(r'\d', password):
            return False, "密码必须包含至少一个数字"
        
        # 检查特殊字符
        if cls.REQUIRE_SPECIAL:
            special_pattern = f"[{re.escape(cls.SPECIAL_CHARS)}]"
            if not re.search(special_pattern, password):
                return False, f"密码必须包含至少一个特殊字符 ({cls.SPECIAL_CHARS[:10]}...)"
        
        # 检查常见弱密码
        weak_passwords = [
            'password', '12345678', 'admin123', 'qwerty123',
            'abc12345', '11111111', '00000000'
        ]
        if password.lower() in weak_passwords:
            return False, "密码过于简单，请使用更复杂的密码"
        
        return True, "密码强度符合要求"
    
    @classmethod
    def is_password_expired(cls, password_updated_at: datetime) -> bool:
        """
        检查密码是否过期
        
        Args:
            password_updated_at: 密码最后修改时间
        
        Returns:
            是否过期
        """
        if not password_updated_at:
            return True
        
        expiry_date = password_updated_at + timedelta(days=cls.PASSWORD_EXPIRE_DAYS)
        return datetime.now() > expiry_date
    
    @classmethod
    def days_until_expiry(cls, password_updated_at: datetime) -> int:
        """
        计算密码距离过期还有多少天
        
        Returns:
            剩余天数（负数表示已过期）
        """
        if not password_updated_at:
            return -1
        
        expiry_date = password_updated_at + timedelta(days=cls.PASSWORD_EXPIRE_DAYS)
        delta = expiry_date - datetime.now()
        return delta.days
    
    @classmethod
    def is_account_locked(cls, locked_until: datetime) -> bool:
        """
        检查账号是否被锁定
        
        Args:
            locked_until: 锁定截止时间
        
        Returns:
            是否锁定
        """
        if not locked_until:
            return False
        
        return datetime.now() < locked_until
    
    @classmethod
    def calculate_lockout_time(cls) -> datetime:
        """
        计算锁定截止时间
        
        Returns:
            锁定截止时间
        """
        return datetime.now() + timedelta(minutes=cls.LOCKOUT_DURATION_MINUTES)
    
    @classmethod
    def get_password_requirements(cls) -> str:
        """
        获取密码要求描述
        
        Returns:
            密码要求文本
        """
        requirements = [
            f"长度为 {cls.MIN_LENGTH}-{cls.MAX_LENGTH} 位"
        ]
        
        if cls.REQUIRE_UPPERCASE:
            requirements.append("包含至少一个大写字母")
        
        if cls.REQUIRE_LOWERCASE:
            requirements.append("包含至少一个小写字母")
        
        if cls.REQUIRE_DIGIT:
            requirements.append("包含至少一个数字")
        
        if cls.REQUIRE_SPECIAL:
            requirements.append(f"包含至少一个特殊字符 ({cls.SPECIAL_CHARS[:10]}...)")
        
        return "；".join(requirements)
