"""
添加更多测试数据
用于演示和测试系统功能
"""
from datetime import date, datetime
from database import SessionLocal
from models import User, Project, Paper, Fund, Achievement, UserRole, ProjectStatus, AchievementType
from utils.security import hash_password

def add_more_test_data():
    """添加更多测试数据"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("开始添加测试数据...")
        print("=" * 60)
        print()
        
        # ==================== 添加更多用户 ====================
        print("[1/5] 添加用户数据...")
        
        users_data = [
            {
                "username": "zhangsan",
                "password": "123456",
                "name": "张三",
                "role": UserRole.TEACHER,
                "title": "副教授",
                "college": "计算机学院",
                "email": "zhangsan@example.com",
                "phone": "13900139001",
                "research_field": "计算机视觉、模式识别"
            },
            {
                "username": "lisi",
                "password": "123456",
                "name": "李四",
                "role": UserRole.TEACHER,
                "title": "讲师",
                "college": "计算机学院",
                "email": "lisi@example.com",
                "phone": "13900139002",
                "research_field": "自然语言处理"
            },
            {
                "username": "wangwu",
                "password": "123456",
                "name": "王五",
                "role": UserRole.TEACHER,
                "title": "教授",
                "college": "信息学院",
                "email": "wangwu@example.com",
                "phone": "13900139003",
                "research_field": "数据挖掘、大数据分析"
            },
            {
                "username": "zhaoliu",
                "password": "123456",
                "name": "赵六",
                "role": UserRole.TEACHER,
                "title": "副教授",
                "college": "信息学院",
                "email": "zhaoliu@example.com",
                "phone": "13900139004",
                "research_field": "网络安全、区块链"
            },
            {
                "username": "sunqi",
                "password": "123456",
                "name": "孙七",
                "role": UserRole.TEACHER,
                "title": "讲师",
                "college": "软件学院",
                "email": "sunqi@example.com",
                "phone": "13900139005",
                "research_field": "软件工程、敏捷开发"
            }
        ]
        
        created_users = {}
        for user_data in users_data:
            # 检查用户是否已存在
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing:
                password = user_data.pop("password")
                user = User(
                    **user_data,
                    password_hash=hash_password(password)
                )
                db.add(user)
                db.flush()
                created_users[user_data["username"]] = user
                print(f"  ✓ 创建用户: {user_data['name']} ({user_data['username']})")
            else:
                created_users[user_data["username"]] = existing
                print(f"  - 用户已存在: {user_data['name']} ({user_data['username']})")
        
        db.commit()
        print()
        
        # ==================== 添加更多项目 ====================
        print("[2/5] 添加项目数据...")
        
        # 获取已有用户
        admin = db.query(User).filter(User.username == "admin").first()
        
        projects_data = [
            {
                "project_name": "基于联邦学习的隐私保护研究",
                "pi_id": created_users["zhangsan"].id,
                "pi_name": created_users["zhangsan"].name,
                "members": '["张三", "李四", "王五"]',
                "project_type": "国家重点研发计划",
                "source": "科技部",
                "budget_total": 800000.0,
                "start_date": date(2023, 6, 1),
                "end_date": date(2026, 5, 31),
                "status": ProjectStatus.IN_PROGRESS,
                "description": "研究联邦学习框架下的隐私保护机制",
                "objectives": "提出新的隐私保护算法，发表高水平论文3篇"
            },
            {
                "project_name": "自然语言处理在医疗领域的应用",
                "pi_id": created_users["lisi"].id,
                "pi_name": created_users["lisi"].name,
                "members": '["李四", "张三"]',
                "project_type": "省级自然科学基金",
                "source": "省科技厅",
                "budget_total": 150000.0,
                "start_date": date(2024, 1, 1),
                "end_date": date(2026, 12, 31),
                "status": ProjectStatus.IN_PROGRESS,
                "description": "构建医疗文本分析系统"
            },
            {
                "project_name": "区块链技术在供应链金融中的应用研究",
                "pi_id": created_users["zhaoliu"].id,
                "pi_name": created_users["zhaoliu"].name,
                "members": '["赵六", "王五"]',
                "project_type": "企业横向课题",
                "source": "某科技公司",
                "budget_total": 300000.0,
                "start_date": date(2024, 3, 1),
                "end_date": date(2025, 12, 31),
                "status": ProjectStatus.APPROVED,
                "description": "开发基于区块链的供应链金融平台"
            },
            {
                "project_name": "大数据驱动的智慧城市治理系统",
                "pi_id": created_users["wangwu"].id,
                "pi_name": created_users["wangwu"].name,
                "members": '["王五", "赵六", "孙七"]',
                "project_type": "国家自然科学基金",
                "source": "国家自然科学基金委",
                "budget_total": 600000.0,
                "start_date": date(2023, 1, 1),
                "end_date": date(2025, 12, 31),
                "status": ProjectStatus.MID_CHECK,
                "description": "研究智慧城市数据治理关键技术"
            },
            {
                "project_name": "软件缺陷预测与质量保障技术",
                "pi_id": created_users["sunqi"].id,
                "pi_name": created_users["sunqi"].name,
                "project_type": "青年基金",
                "source": "国家自然科学基金委",
                "budget_total": 250000.0,
                "start_date": date(2024, 1, 1),
                "end_date": date(2026, 12, 31),
                "status": ProjectStatus.SUBMITTED,
                "description": "研究软件缺陷预测模型"
            }
        ]
        
        created_projects = []
        for proj_data in projects_data:
            project = Project(**proj_data)
            db.add(project)
            db.flush()
            created_projects.append(project)
            print(f"  ✓ 创建项目: {proj_data['project_name']}")
        
        db.commit()
        print()
        
        # ==================== 添加更多论文 ====================
        print("[3/5] 添加论文数据...")
        
        papers_data = [
            {
                "title": "Federated Learning with Differential Privacy: A Survey",
                "authors": "张三, 李四, 王五",
                "journal": "IEEE Transactions on Knowledge and Data Engineering",
                "publication_date": date(2024, 5, 15),
                "doi": "10.1109/TKDE.2024.001",
                "jcr_zone": "Q1",
                "cas_zone": "一区",
                "impact_factor": 18.7,
                "project_id": created_projects[0].id,
                "creator_id": created_users["zhangsan"].id
            },
            {
                "title": "Medical Text Mining Using Deep Learning Approaches",
                "authors": "李四, 张三",
                "journal": "Journal of Biomedical Informatics",
                "publication_date": date(2024, 4, 20),
                "doi": "10.1016/JBI.2024.002",
                "jcr_zone": "Q1",
                "cas_zone": "二区",
                "impact_factor": 12.3,
                "project_id": created_projects[1].id,
                "creator_id": created_users["lisi"].id
            },
            {
                "title": "Blockchain-Based Supply Chain Finance: A Comprehensive Review",
                "authors": "赵六, 王五",
                "journal": "IEEE Access",
                "publication_date": date(2024, 3, 10),
                "doi": "10.1109/ACCESS.2024.003",
                "jcr_zone": "Q2",
                "cas_zone": "三区",
                "impact_factor": 8.5,
                "project_id": created_projects[2].id,
                "creator_id": created_users["zhaoliu"].id
            },
            {
                "title": "Big Data Analytics for Smart City Governance",
                "authors": "王五, 赵六, 孙七",
                "journal": "Information Systems",
                "publication_date": date(2023, 11, 25),
                "doi": "10.1016/IS.2023.004",
                "jcr_zone": "Q1",
                "cas_zone": "二区",
                "impact_factor": 14.2,
                "project_id": created_projects[3].id,
                "creator_id": created_users["wangwu"].id
            },
            {
                "title": "Deep Learning for Software Defect Prediction",
                "authors": "孙七, 张三",
                "journal": "Empirical Software Engineering",
                "publication_date": date(2024, 6, 5),
                "doi": "10.1007/ESE.2024.005",
                "jcr_zone": "Q1",
                "cas_zone": "二区",
                "impact_factor": 11.8,
                "project_id": created_projects[4].id,
                "creator_id": created_users["sunqi"].id
            },
            {
                "title": "Privacy-Preserving Machine Learning: Recent Advances",
                "authors": "张三, 王五",
                "journal": "ACM Computing Surveys",
                "publication_date": date(2024, 2, 15),
                "doi": "10.1145/ACS.2024.006",
                "jcr_zone": "Q1",
                "cas_zone": "一区",
                "impact_factor": 23.8,
                "project_id": created_projects[0].id,
                "creator_id": created_users["zhangsan"].id
            }
        ]
        
        for paper_data in papers_data:
            paper = Paper(**paper_data)
            db.add(paper)
            print(f"  ✓ 创建论文: {paper_data['title'][:50]}...")
        
        db.commit()
        print()
        
        # ==================== 添加更多经费 ====================
        print("[4/5] 添加经费数据...")
        
        funds_data = [
            {
                "project_id": created_projects[0].id,
                "expense_type": "设备费",
                "amount": 200000.0,
                "expense_date": date(2023, 7, 15),
                "handler": "张三",
                "notes": "购买高性能服务器"
            },
            {
                "project_id": created_projects[0].id,
                "expense_type": "材料费",
                "amount": 50000.0,
                "expense_date": date(2023, 9, 20),
                "handler": "李四",
                "notes": "购买实验材料和软件"
            },
            {
                "project_id": created_projects[1].id,
                "expense_type": "差旅费",
                "amount": 25000.0,
                "expense_date": date(2024, 3, 10),
                "handler": "李四",
                "notes": "参加学术会议"
            },
            {
                "project_id": created_projects[2].id,
                "expense_type": "劳务费",
                "amount": 80000.0,
                "expense_date": date(2024, 4, 5),
                "handler": "赵六",
                "notes": "支付开发人员工资"
            },
            {
                "project_id": created_projects[3].id,
                "expense_type": "设备费",
                "amount": 180000.0,
                "expense_date": date(2023, 3, 20),
                "handler": "王五",
                "notes": "购买数据采集设备"
            },
            {
                "project_id": created_projects[3].id,
                "expense_type": "会议费",
                "amount": 35000.0,
                "expense_date": date(2023, 10, 15),
                "handler": "赵六",
                "notes": "组织学术研讨会"
            },
            {
                "project_id": created_projects[4].id,
                "expense_type": "测试化验加工费",
                "amount": 40000.0,
                "expense_date": date(2024, 2, 20),
                "handler": "孙七",
                "notes": "软件测试服务费"
            }
        ]
        
        for fund_data in funds_data:
            fund = Fund(**fund_data)
            db.add(fund)
            print(f"  ✓ 创建经费记录: {fund_data['expense_type']} - ¥{fund_data['amount']:,.0f}")
        
        db.commit()
        print()
        
        # ==================== 添加更多成果 ====================
        print("[5/5] 添加成果数据...")
        
        achievements_data = [
            {
                "achievement_type": AchievementType.PATENT,
                "title": "一种基于联邦学习的隐私保护方法",
                "owner": "张三",
                "members": "张三, 李四",
                "completion_date": date(2024, 1, 15),
                "certificate_no": "CN202410002345.6",
                "description": "本发明提出了一种新型联邦学习隐私保护方法"
            },
            {
                "achievement_type": AchievementType.PATENT,
                "title": "医疗文本智能分析系统",
                "owner": "李四",
                "members": "李四, 张三",
                "completion_date": date(2024, 3, 20),
                "certificate_no": "CN202410003456.7",
                "description": "基于自然语言处理的医疗文本分析系统"
            },
            {
                "achievement_type": AchievementType.SOFTWARE,
                "title": "供应链金融区块链平台V1.0",
                "owner": "赵六",
                "members": "赵六, 王五",
                "completion_date": date(2024, 5, 10),
                "certificate_no": "2024SR0123456",
                "description": "基于区块链的供应链金融管理系统"
            },
            {
                "achievement_type": AchievementType.AWARD,
                "title": "国家自然科学基金委优秀青年基金",
                "owner": "张三",
                "members": "张三",
                "completion_date": date(2024, 1, 5),
                "certificate_no": "NSFC-2024-YOUQING-001",
                "description": "在隐私保护与联邦学习领域取得突出成绩"
            },
            {
                "achievement_type": AchievementType.AWARD,
                "title": "省级教学成果一等奖",
                "owner": "王五",
                "members": "王五, 赵六, 孙七",
                "completion_date": date(2023, 9, 15),
                "certificate_no": "2023-JX-001",
                "description": "大数据技术教学改革与实践"
            },
            {
                "achievement_type": AchievementType.BOOK,
                "title": "深度学习与软件工程",
                "owner": "孙七",
                "members": "孙七, 张三",
                "completion_date": date(2024, 4, 20),
                "certificate_no": "ISBN 978-7-111-12345-6",
                "description": "清华大学出版社出版的专业教材"
            },
            {
                "achievement_type": AchievementType.SOFTWARE,
                "title": "智慧城市数据治理平台V2.0",
                "owner": "王五",
                "members": "王五, 赵六",
                "completion_date": date(2023, 12, 15),
                "certificate_no": "2023SR0234567",
                "description": "智慧城市大数据分析与治理系统"
            }
        ]
        
        for ach_data in achievements_data:
            achievement = Achievement(**ach_data)
            db.add(achievement)
            print(f"  ✓ 创建成果: {ach_data['title']}")
        
        db.commit()
        print()
        
        print("=" * 60)
        print("✓ 测试数据添加完成！")
        print("=" * 60)
        print()
        print("数据统计：")
        print(f"  - 新增用户: 5 个")
        print(f"  - 新增项目: 5 个")
        print(f"  - 新增论文: 6 篇")
        print(f"  - 新增经费: 7 条")
        print(f"  - 新增成果: 7 个")
        print()
        
    except Exception as e:
        print(f"✗ 添加数据失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_more_test_data()
