"""
数据库安全升级脚本（等保二级改造）
添加安全相关字段到现有表
"""
from database import engine, SessionLocal
from sqlalchemy import text

def upgrade_users_table():
    """升级 users 表，添加安全字段"""
    print("正在升级 users 表...")
    
    with engine.connect() as conn:
        # 添加安全相关字段
        sqls = [
            "ALTER TABLE users ADD COLUMN password_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '密码最后修改时间'",
            "ALTER TABLE users ADD COLUMN login_failures INT DEFAULT 0 COMMENT '连续登录失败次数'",
            "ALTER TABLE users ADD COLUMN locked_until DATETIME NULL COMMENT '账号锁定截止时间'",
            "ALTER TABLE users ADD COLUMN last_login_at DATETIME NULL COMMENT '最后登录时间'",
            "ALTER TABLE users ADD COLUMN last_login_ip VARCHAR(50) NULL COMMENT '最后登录IP'"
        ]
        
        for sql in sqls:
            try:
                conn.execute(text(sql))
                conn.commit()
                print(f"  ✓ {sql[:50]}...")
            except Exception as e:
                # 如果字段已存在则跳过
                if "Duplicate column name" in str(e):
                    print(f"  - 字段已存在，跳过")
                else:
                    print(f"  ✗ 执行失败: {e}")

def upgrade_operation_logs_table():
    """升级 operation_logs 表，添加审计字段"""
    print("\n正在升级 operation_logs 表...")
    
    with engine.connect() as conn:
        sqls = [
            "ALTER TABLE operation_logs MODIFY COLUMN operation VARCHAR(100) NOT NULL COMMENT '操作类型'",
            "ALTER TABLE operation_logs MODIFY COLUMN module VARCHAR(50) NOT NULL COMMENT '模块名称'",
            "ALTER TABLE operation_logs ADD COLUMN method VARCHAR(10) COMMENT 'HTTP方法'",
            "ALTER TABLE operation_logs ADD COLUMN path VARCHAR(200) COMMENT '请求路径'",
            "ALTER TABLE operation_logs MODIFY COLUMN ip_address VARCHAR(50) NOT NULL COMMENT 'IP地址'",
            "ALTER TABLE operation_logs ADD COLUMN user_agent VARCHAR(500) COMMENT '用户代理'",
            "ALTER TABLE operation_logs ADD COLUMN status VARCHAR(20) COMMENT '操作结果'",
            "ALTER TABLE operation_logs ADD COLUMN error_msg TEXT COMMENT '错误信息'",
            "ALTER TABLE operation_logs ADD COLUMN duration INT COMMENT '执行时间(毫秒)'",
            "CREATE INDEX idx_created_at ON operation_logs(created_at)"
        ]
        
        for sql in sqls:
            try:
                conn.execute(text(sql))
                conn.commit()
                print(f"  ✓ {sql[:60]}...")
            except Exception as e:
                # 如果字段或索引已存在则跳过
                if "Duplicate column name" in str(e) or "Duplicate key name" in str(e):
                    print(f"  - 字段/索引已存在，跳过")
                else:
                    print(f"  ✗ 执行失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  科研管理系统 - 数据库安全升级")
    print("  等保二级改造")
    print("=" * 60)
    print()
    
    try:
        upgrade_users_table()
        upgrade_operation_logs_table()
        
        print("\n" + "=" * 60)
        print("  ✅ 数据库升级完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 升级失败: {e}")
