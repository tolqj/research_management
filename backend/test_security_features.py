"""
测试等保安全功能
测试密码策略、审计日志等新增功能
"""
import sys
from datetime import datetime, timedelta
from database import SessionLocal, engine
from models import User, OperationLog
from utils.password_policy import PasswordPolicy
from utils.audit import AuditLogger
from sqlalchemy import text, inspect


def test_database_schema():
    """测试数据库表结构是否正确"""
    print("=" * 60)
    print("1. 测试数据库表结构")
    print("=" * 60)
    
    inspector = inspect(engine)
    
    # 检查 users 表的新字段
    print("\n【Users 表字段检查】")
    users_columns = {col['name']: col for col in inspector.get_columns('users')}
    
    required_fields = [
        'password_updated_at',
        'login_failures', 
        'locked_until',
        'last_login_at',
        'last_login_ip'
    ]
    
    for field in required_fields:
        if field in users_columns:
            print(f"  ✅ {field} - {users_columns[field]['type']}")
        else:
            print(f"  ❌ {field} - 缺失！")
    
    # 检查 operation_logs 表的新字段
    print("\n【Operation_Logs 表字段检查】")
    logs_columns = {col['name']: col for col in inspector.get_columns('operation_logs')}
    
    required_fields = [
        'method',
        'path',
        'user_agent',
        'status',
        'error_msg',
        'duration'
    ]
    
    for field in required_fields:
        if field in logs_columns:
            print(f"  ✅ {field} - {logs_columns[field]['type']}")
        else:
            print(f"  ❌ {field} - 缺失！")
    
    # 检查索引
    print("\n【索引检查】")
    indexes = inspector.get_indexes('operation_logs')
    index_names = [idx['name'] for idx in indexes]
    
    if 'idx_created_at' in index_names:
        print(f"  ✅ idx_created_at 索引存在")
    else:
        print(f"  ❌ idx_created_at 索引缺失")
    
    return True


def test_password_policy():
    """测试密码策略"""
    print("\n" + "=" * 60)
    print("2. 测试密码策略")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        ("123456", False, "太短，无复杂度"),
        ("password", False, "弱密码"),
        ("Admin123", False, "缺少特殊字符"),
        ("admin123!", False, "缺少大写字母"),
        ("ADMIN123!", False, "缺少小写字母"),
        ("Admin!@#$", False, "缺少数字"),
        ("Admin123!", True, "符合要求"),
        ("MyP@ssw0rd", True, "符合要求"),
        ("Secure#2024", True, "符合要求"),
    ]
    
    print("\n【密码强度验证测试】")
    passed = 0
    failed = 0
    
    for password, expected_valid, description in test_cases:
        is_valid, message = PasswordPolicy.validate_password_strength(password)
        
        if is_valid == expected_valid:
            status = "✅ 通过"
            passed += 1
        else:
            status = "❌ 失败"
            failed += 1
        
        print(f"  {status} | '{password}' | {description}")
        if not is_valid:
            print(f"       原因: {message}")
    
    print(f"\n测试结果: {passed} 通过, {failed} 失败")
    
    # 测试密码过期
    print("\n【密码过期检测测试】")
    now = datetime.now()
    
    # 刚修改的密码
    recent = now - timedelta(days=1)
    if not PasswordPolicy.is_password_expired(recent):
        print(f"  ✅ 1天前的密码未过期")
    else:
        print(f"  ❌ 1天前的密码不应过期")
    
    # 快过期的密码
    almost_expired = now - timedelta(days=85)
    days_left = PasswordPolicy.days_until_expiry(almost_expired)
    print(f"  ℹ️  85天前的密码还有 {days_left} 天过期")
    
    # 已过期的密码
    expired = now - timedelta(days=100)
    if PasswordPolicy.is_password_expired(expired):
        print(f"  ✅ 100天前的密码已过期")
    else:
        print(f"  ❌ 100天前的密码应该过期")
    
    # 测试账号锁定
    print("\n【账号锁定检测测试】")
    
    # 未锁定
    if not PasswordPolicy.is_account_locked(None):
        print(f"  ✅ 无锁定时间 = 未锁定")
    
    # 锁定中
    locked = now + timedelta(minutes=10)
    if PasswordPolicy.is_account_locked(locked):
        print(f"  ✅ 未来10分钟 = 锁定中")
    
    # 锁定已过期
    unlocked = now - timedelta(minutes=10)
    if not PasswordPolicy.is_account_locked(unlocked):
        print(f"  ✅ 10分钟前 = 锁定已解除")
    
    return passed > 0 and failed == 0


def test_audit_logger():
    """测试审计日志记录"""
    print("\n" + "=" * 60)
    print("3. 测试审计日志功能")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 创建一个模拟的 Request 对象
        class MockRequest:
            def __init__(self):
                self.method = "POST"
                self.url = type('obj', (object,), {'path': '/api/test'})()
                self.client = type('obj', (object,), {'host': '127.0.0.1'})()
                self.headers = {
                    "User-Agent": "TestClient/1.0",
                    "X-Forwarded-For": "192.168.1.100"
                }
        
        request = MockRequest()
        
        # 测试基本日志记录
        print("\n【基本日志记录测试】")
        AuditLogger.log_operation(
            db=db,
            user_id=1,
            username="test_user",
            operation="测试操作",
            module="test",
            request=request,
            details={"action": "test", "value": 123},
            status="SUCCESS"
        )
        print("  ✅ 成功记录基本操作日志")
        
        # 测试登录日志
        print("\n【登录日志测试】")
        AuditLogger.log_login_attempt(
            db=db,
            username="admin",
            request=request,
            success=True
        )
        print("  ✅ 成功记录登录日志")
        
        # 测试失败日志
        AuditLogger.log_login_attempt(
            db=db,
            username="hacker",
            request=request,
            success=False,
            error_msg="用户名或密码错误"
        )
        print("  ✅ 成功记录登录失败日志")
        
        # 测试创建操作日志
        print("\n【CRUD日志测试】")
        AuditLogger.log_create(
            db=db,
            user_id=1,
            username="admin",
            module="project",
            resource_type="项目",
            resource_id=123,
            request=request,
            data={"name": "测试项目"}
        )
        print("  ✅ 成功记录创建操作日志")
        
        # 测试更新操作日志
        AuditLogger.log_update(
            db=db,
            user_id=1,
            username="admin",
            module="project",
            resource_type="项目",
            resource_id=123,
            request=request,
            changes={"status": "已批准"}
        )
        print("  ✅ 成功记录更新操作日志")
        
        # 测试删除操作日志
        AuditLogger.log_delete(
            db=db,
            user_id=1,
            username="admin",
            module="project",
            resource_type="项目",
            resource_id=123,
            request=request
        )
        print("  ✅ 成功记录删除操作日志")
        
        # 测试权限拒绝日志
        AuditLogger.log_permission_denied(
            db=db,
            user_id=2,
            username="normal_user",
            module="admin",
            request=request,
            reason="权限不足"
        )
        print("  ✅ 成功记录权限拒绝日志")
        
        # 查询刚才插入的日志
        print("\n【日志查询验证】")
        logs = db.query(OperationLog).order_by(OperationLog.id.desc()).limit(10).all()
        
        if len(logs) >= 6:
            print(f"  ✅ 成功查询到 {len(logs)} 条日志记录")
            print(f"\n  最新的3条日志:")
            for i, log in enumerate(logs[:3], 1):
                print(f"    {i}. [{log.status}] {log.operation} - {log.module}")
                print(f"       用户: {log.username}, IP: {log.ip_address}")
                if log.details:
                    print(f"       详情: {log.details[:50]}...")
        else:
            print(f"  ⚠️  只查询到 {len(logs)} 条日志，可能少于预期")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_get_client_ip():
    """测试IP地址获取"""
    print("\n" + "=" * 60)
    print("4. 测试IP地址获取")
    print("=" * 60)
    
    # 测试不同场景下的IP获取
    print("\n【IP地址获取测试】")
    
    # 场景1: X-Forwarded-For
    class Request1:
        headers = {"X-Forwarded-For": "203.0.113.1, 198.51.100.1"}
        client = type('obj', (object,), {'host': '127.0.0.1'})()
    
    ip = AuditLogger.get_client_ip(Request1())
    print(f"  ✅ X-Forwarded-For: {ip} (应为 203.0.113.1)")
    
    # 场景2: X-Real-IP
    class Request2:
        headers = {"X-Real-IP": "203.0.113.2"}
        client = type('obj', (object,), {'host': '127.0.0.1'})()
    
    ip = AuditLogger.get_client_ip(Request2())
    print(f"  ✅ X-Real-IP: {ip} (应为 203.0.113.2)")
    
    # 场景3: 直连
    class Request3:
        headers = {}
        client = type('obj', (object,), {'host': '192.168.1.100'})()
    
    ip = AuditLogger.get_client_ip(Request3())
    print(f"  ✅ 直连: {ip} (应为 192.168.1.100)")
    
    return True


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "等保安全功能测试套件" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # 运行所有测试
    try:
        results.append(("数据库表结构", test_database_schema()))
    except Exception as e:
        print(f"❌ 数据库表结构测试失败: {e}")
        results.append(("数据库表结构", False))
    
    try:
        results.append(("密码策略", test_password_policy()))
    except Exception as e:
        print(f"❌ 密码策略测试失败: {e}")
        results.append(("密码策略", False))
    
    try:
        results.append(("审计日志", test_audit_logger()))
    except Exception as e:
        print(f"❌ 审计日志测试失败: {e}")
        results.append(("审计日志", False))
    
    try:
        results.append(("IP地址获取", test_get_client_ip()))
    except Exception as e:
        print(f"❌ IP地址获取测试失败: {e}")
        results.append(("IP地址获取", False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} - {name}")
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！等保安全功能工作正常！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，请检查！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
