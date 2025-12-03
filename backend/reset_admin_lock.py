"""
重置管理员账号锁定状态
用于解除账号锁定
"""
from database import SessionLocal
from models import User

def reset_admin_lock():
    """重置admin账号的锁定状态"""
    db = SessionLocal()
    try:
        # 查找admin用户
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("✗ 未找到admin用户")
            return
        
        print(f"当前状态:")
        print(f"  用户名: {admin.username}")
        print(f"  登录失败次数: {admin.login_failures or 0}")
        print(f"  锁定至: {admin.locked_until or '未锁定'}")
        print()
        
        # 重置锁定状态
        admin.login_failures = 0
        admin.locked_until = None
        db.commit()
        
        print("✓ 已重置admin账号锁定状态")
        print()
        print("现在可以使用以下账号登录：")
        print("-" * 40)
        print("用户名: admin")
        print("密码: Admin@123")
        print("-" * 40)
        
    except Exception as e:
        print(f"✗ 重置失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("重置管理员账号锁定状态")
    print("=" * 50)
    print()
    reset_admin_lock()
