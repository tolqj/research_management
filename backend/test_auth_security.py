"""
测试认证安全功能
验证密码策略、登录锁定、审计日志等功能
"""
import sys
import requests
import json
from datetime import datetime
from database import SessionLocal
from models import User, OperationLog
from sqlalchemy import desc


BASE_URL = "http://localhost:8000/api/auth"


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_register_with_weak_password():
    """测试弱密码注册"""
    print_section("1. 测试弱密码注册（应该失败）")
    
    weak_passwords = [
        ("123456", "太短"),
        ("password", "无复杂度"),
        ("Admin123", "缺特殊字符"),
    ]
    
    for password, reason in weak_passwords:
        response = requests.post(f"{BASE_URL}/register", json={
            "username": f"test_{datetime.now().timestamp()}",
            "password": password,
            "name": "测试用户",
            "email": f"test{datetime.now().timestamp()}@test.com"
        })
        
        if response.status_code == 400:
            print(f"  ✅ {reason} 被正确拒绝: {password}")
            print(f"     错误信息: {response.json()['detail']}")
        else:
            print(f"  ❌ {reason} 应该被拒绝但通过了: {password}")


def test_register_with_strong_password():
    """测试强密码注册"""
    print_section("2. 测试强密码注册（应该成功）")
    
    username = f"testuser_{int(datetime.now().timestamp())}"
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": "StrongP@ss123",
        "name": "测试用户",
        "email": f"{username}@test.com",
        "role": "普通教师"
    })
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"  ✅ 注册成功")
        print(f"     用户名: {user_data['username']}")
        print(f"     用户ID: {user_data['id']}")
        return username
    else:
        print(f"  ❌ 注册失败: {response.json()}")
        return None


def test_login_with_wrong_password(username):
    """测试错误密码登录（测试锁定机制）"""
    print_section("3. 测试错误密码登录（触发锁定）")
    
    for i in range(6):
        response = requests.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": "WrongPassword123!"
        })
        
        if response.status_code == 401:
            detail = response.json()['detail']
            print(f"  第{i+1}次失败: {detail}")
        elif response.status_code == 403:
            detail = response.json()['detail']
            print(f"  ✅ 账号已锁定: {detail}")
            break
        else:
            print(f"  ❓ 意外响应: {response.status_code}")


def test_locked_account_login(username):
    """测试被锁定账号登录"""
    print_section("4. 测试锁定状态下登录")
    
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": "StrongP@ss123"
    })
    
    if response.status_code == 403:
        print(f"  ✅ 锁定中的账号无法登录")
        print(f"     提示: {response.json()['detail']}")
    else:
        print(f"  ❌ 锁定的账号不应该能登录")


def test_successful_login():
    """测试成功登录"""
    print_section("5. 测试正确密码登录")
    
    # 使用默认测试账号
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ 登录成功")
        print(f"     Token: {data['access_token'][:50]}...")
        print(f"     用户: {data['user']['username']} ({data['user']['name']})")
        
        # 检查是否有密码过期警告
        if 'warning' in data and data['warning']:
            print(f"     ⚠️  警告: {data['warning']}")
        
        return data['access_token']
    else:
        print(f"  ❌ 登录失败: {response.json()}")
        return None


def check_audit_logs():
    """检查审计日志"""
    print_section("6. 检查审计日志记录")
    
    db = SessionLocal()
    try:
        # 查询最近的审计日志
        logs = db.query(OperationLog).filter(
            OperationLog.module == 'auth'
        ).order_by(desc(OperationLog.created_at)).limit(10).all()
        
        print(f"\n  最近10条认证相关日志:\n")
        
        for i, log in enumerate(logs, 1):
            status_icon = "✅" if log.status == "SUCCESS" else "❌"
            print(f"  {i}. [{status_icon}] {log.operation}")
            print(f"     用户: {log.username}, IP: {log.ip_address}")
            print(f"     时间: {log.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if log.error_msg:
                print(f"     错误: {log.error_msg}")
            print()
        
        # 统计
        total_logs = db.query(OperationLog).filter(OperationLog.module == 'auth').count()
        success_logs = db.query(OperationLog).filter(
            OperationLog.module == 'auth',
            OperationLog.status == 'SUCCESS'
        ).count()
        failed_logs = db.query(OperationLog).filter(
            OperationLog.module == 'auth',
            OperationLog.status == 'FAILED'
        ).count()
        
        print(f"  认证日志统计:")
        print(f"    总计: {total_logs} 条")
        print(f"    成功: {success_logs} 条")
        print(f"    失败: {failed_logs} 条")
        
    finally:
        db.close()


def check_user_security_fields():
    """检查用户安全字段"""
    print_section("7. 检查用户安全字段")
    
    db = SessionLocal()
    try:
        # 查询admin用户
        user = db.query(User).filter(User.username == 'admin').first()
        
        if user:
            print(f"\n  Admin 用户安全信息:")
            print(f"    登录失败次数: {user.login_failures}")
            print(f"    锁定截止时间: {user.locked_until or '未锁定'}")
            print(f"    最后登录时间: {user.last_login_at or '从未登录'}")
            print(f"    最后登录IP: {user.last_login_ip or '无'}")
            print(f"    密码更新时间: {user.password_updated_at}")
            
            # 检查密码是否过期
            from utils.password_policy import PasswordPolicy
            if PasswordPolicy.is_password_expired(user.password_updated_at):
                print(f"    ⚠️  密码已过期")
            else:
                days = PasswordPolicy.days_until_expiry(user.password_updated_at)
                print(f"    ✅ 密码还有 {days} 天过期")
        
    finally:
        db.close()


def main():
    """主测试流程"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "认证安全功能测试" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 检查后端是否运行
    try:
        requests.get("http://localhost:8000/api/docs", timeout=2)
    except:
        print("\n❌ 后端服务未运行！请先启动后端服务。")
        print("   命令: cd backend && python main.py")
        return 1
    
    # 执行测试
    try:
        # 测试弱密码
        test_register_with_weak_password()
        
        # 测试强密码注册
        new_username = test_register_with_strong_password()
        
        if new_username:
            # 测试错误密码（触发锁定）
            test_login_with_wrong_password(new_username)
            
            # 测试锁定账号登录
            test_locked_account_login(new_username)
        
        # 测试正常登录
        test_successful_login()
        
        # 检查审计日志
        check_audit_logs()
        
        # 检查用户安全字段
        check_user_security_fields()
        
        print("\n" + "=" * 60)
        print("  ✅ 所有测试完成！")
        print("=" * 60)
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
