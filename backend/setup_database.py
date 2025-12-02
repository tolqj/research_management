"""
数据库初始化脚本
创建数据库、表结构并插入测试数据
"""
import pymysql
from sqlalchemy import create_engine
from database import Base, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
from models import User, Project, Paper, Fund, Achievement, UserRole, ProjectStatus, AchievementType
from utils.security import hash_password
from datetime import date, datetime

def create_database():
    """创建数据库"""
    try:
        # 连接 MySQL（不指定数据库）
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=int(MYSQL_PORT),
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DATABASE}")
        cursor.execute(f"CREATE DATABASE {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ 数据库 '{MYSQL_DATABASE}' 创建成功")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"✗ 数据库创建失败: {e}")
        raise


def create_tables():
    """创建所有表"""
    try:
        from database import engine
        Base.metadata.create_all(bind=engine)
        print("✓ 数据表创建成功")
    except Exception as e:
        print(f"✗ 数据表创建失败: {e}")
        raise


def insert_test_data():
    """插入测试数据"""
    try:
        from database import SessionLocal
        db = SessionLocal()
        
        # 创建管理员用户
        admin_user = User(
            username="admin",
            password_hash=hash_password("admin123"),
            name="系统管理员",
            role=UserRole.ADMIN,
            title="教授",
            college="计算机学院",
            email="admin@example.com",
            phone="13800138000",
            research_field="人工智能"
        )
        db.add(admin_user)
        
        # 创建科研秘书
        secretary_user = User(
            username="secretary",
            password_hash=hash_password("123456"),
            name="科研秘书",
            role=UserRole.SECRETARY,
            title="讲师",
            college="科研处",
            email="secretary@example.com",
            phone="13800138001",
            research_field="科研管理"
        )
        db.add(secretary_user)
        
        # 创建普通教师
        teacher_user = User(
            username="teacher",
            password_hash=hash_password("123456"),
            name="张教授",
            role=UserRole.TEACHER,
            title="教授",
            college="计算机学院",
            email="teacher@example.com",
            phone="13800138002",
            research_field="机器学习、深度学习"
        )
        db.add(teacher_user)
        
        db.commit()
        print("✓ 用户数据插入成功")
        
        # 创建测试项目
        project1 = Project(
            project_name="基于深度学习的图像识别研究",
            pi_id=admin_user.id,
            pi_name=admin_user.name,
            members='["张教授", "李副教授", "王讲师"]',
            project_type="国家自然科学基金",
            source="国家自然科学基金委",
            budget_total=500000.0,
            start_date=date(2023, 1, 1),
            end_date=date(2025, 12, 31),
            status=ProjectStatus.IN_PROGRESS,
            description="研究深度学习在图像识别领域的应用",
            objectives="提出新的图像识别算法，发表高水平论文"
        )
        db.add(project1)
        
        project2 = Project(
            project_name="智能推荐系统关键技术研究",
            pi_id=teacher_user.id,
            pi_name=teacher_user.name,
            project_type="省级科技计划",
            source="省科技厅",
            budget_total=200000.0,
            start_date=date(2024, 1, 1),
            end_date=date(2026, 12, 31),
            status=ProjectStatus.IN_PROGRESS,
            description="研究智能推荐系统的核心算法"
        )
        db.add(project2)
        
        db.commit()
        print("✓ 项目数据插入成功")
        
        # 创建测试论文
        paper1 = Paper(
            title="Deep Learning for Image Classification: A Survey",
            authors="张教授, 李副教授",
            journal="IEEE Transactions on Pattern Analysis and Machine Intelligence",
            publication_date=date(2024, 3, 15),
            doi="10.1109/TPAMI.2024.001",
            jcr_zone="Q1",
            cas_zone="一区",
            impact_factor=24.5,
            project_id=project1.id,
            creator_id=admin_user.id
        )
        db.add(paper1)
        
        paper2 = Paper(
            title="A Novel Recommendation Algorithm Based on Graph Neural Networks",
            authors="张教授, 王讲师",
            journal="ACM Transactions on Information Systems",
            publication_date=date(2024, 6, 20),
            doi="10.1145/ACM.2024.002",
            jcr_zone="Q1",
            cas_zone="二区",
            impact_factor=15.3,
            project_id=project2.id,
            creator_id=teacher_user.id
        )
        db.add(paper2)
        
        db.commit()
        print("✓ 论文数据插入成功")
        
        # 创建经费记录
        fund1 = Fund(
            project_id=project1.id,
            expense_type="设备费",
            amount=150000.0,
            expense_date=date(2023, 3, 10),
            handler="张教授",
            notes="购买GPU服务器"
        )
        db.add(fund1)
        
        fund2 = Fund(
            project_id=project1.id,
            expense_type="差旅费",
            amount=30000.0,
            expense_date=date(2023, 6, 15),
            handler="李副教授",
            notes="参加国际会议"
        )
        db.add(fund2)
        
        db.commit()
        print("✓ 经费数据插入成功")
        
        # 创建成果记录
        achievement1 = Achievement(
            achievement_type=AchievementType.PATENT,
            title="一种基于深度学习的图像识别方法",
            owner="张教授",
            members="张教授, 李副教授",
            completion_date=date(2024, 2, 1),
            certificate_no="CN202410001234.5",
            description="本发明提出了一种新的图像识别方法"
        )
        db.add(achievement1)
        
        achievement2 = Achievement(
            achievement_type=AchievementType.AWARD,
            title="省级科技进步二等奖",
            owner="张教授",
            members="张教授, 李副教授, 王讲师",
            completion_date=date(2023, 12, 10),
            certificate_no="2023-KJ-002",
            description="智能图像识别系统及其应用"
        )
        db.add(achievement2)
        
        db.commit()
        print("✓ 成果数据插入成功")
        
        db.close()
        
    except Exception as e:
        print(f"✗ 测试数据插入失败: {e}")
        raise


def main():
    """主函数"""
    print("=" * 50)
    print("科研管理系统 - 数据库初始化")
    print("=" * 50)
    print()
    
    try:
        print("步骤 1/3: 创建数据库...")
        create_database()
        print()
        
        print("步骤 2/3: 创建数据表...")
        create_tables()
        print()
        
        print("步骤 3/3: 插入测试数据...")
        insert_test_data()
        print()
        
        print("=" * 50)
        print("✓ 数据库初始化完成！")
        print("=" * 50)
        print()
        print("默认账号信息：")
        print("-" * 50)
        print("管理员: admin / admin123")
        print("科研秘书: secretary / 123456")
        print("教师: teacher / 123456")
        print("-" * 50)
        
    except Exception as e:
        print()
        print("=" * 50)
        print("✗ 数据库初始化失败！")
        print(f"错误信息: {e}")
        print("=" * 50)
        exit(1)


if __name__ == "__main__":
    main()
