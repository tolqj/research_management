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
        
        # ==================== 创建用户（10个） ====================
        # 创建管理员用户
        admin_user = User(
            username="admin",
            password_hash=hash_password("Admin@123"),
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
            password_hash=hash_password("Sec@2024"),
            name="王秘书",
            role=UserRole.SECRETARY,
            title="讲师",
            college="科研处",
            email="secretary@example.com",
            phone="13800138001",
            research_field="科研管理"
        )
        db.add(secretary_user)
        
        # 创建普通教师（8个）
        teacher1 = User(
            username="teacher",
            password_hash=hash_password("Teacher@123"),
            name="张教授",
            role=UserRole.TEACHER,
            title="教授",
            college="计算机学院",
            email="teacher@example.com",
            phone="13800138002",
            research_field="机器学习、深度学习"
        )
        db.add(teacher1)
        
        teacher2 = User(
            username="lisi",
            password_hash=hash_password("Pass@2024"),
            name="李教授",
            role=UserRole.TEACHER,
            title="教授",
            college="计算机学院",
            email="lisi@example.com",
            phone="13900139000",
            research_field="计算机视觉、图像处理"
        )
        db.add(teacher2)
        
        teacher3 = User(
            username="wangwu",
            password_hash=hash_password("Pass@2024"),
            name="王副教授",
            role=UserRole.TEACHER,
            title="副教授",
            college="数学学院",
            email="wangwu@example.com",
            phone="13900139001",
            research_field="应用数学、优化理论"
        )
        db.add(teacher3)
        
        teacher4 = User(
            username="zhaoliu",
            password_hash=hash_password("Pass@2024"),
            name="赵讲师",
            role=UserRole.TEACHER,
            title="讲师",
            college="物理学院",
            email="zhaoliu@example.com",
            phone="13900139002",
            research_field="量子计算、量子信息"
        )
        db.add(teacher4)
        
        teacher5 = User(
            username="sunqi",
            password_hash=hash_password("Pass@2024"),
            name="孙教授",
            role=UserRole.TEACHER,
            title="教授",
            college="电子工程学院",
            email="sunqi@example.com",
            phone="13900139003",
            research_field="信号处理、通信系统"
        )
        db.add(teacher5)
        
        teacher6 = User(
            username="zhouba",
            password_hash=hash_password("Pass@2024"),
            name="周副教授",
            role=UserRole.TEACHER,
            title="副教授",
            college="生物学院",
            email="zhouba@example.com",
            phone="13900139004",
            research_field="生物信息学、基因组学"
        )
        db.add(teacher6)
        
        teacher7 = User(
            username="wujiu",
            password_hash=hash_password("Pass@2024"),
            name="吴教授",
            role=UserRole.TEACHER,
            title="教授",
            college="化学学院",
            email="wujiu@example.com",
            phone="13900139005",
            research_field="材料化学、纳米材料"
        )
        db.add(teacher7)
        
        teacher8 = User(
            username="zhengshi",
            password_hash=hash_password("Pass@2024"),
            name="郑讲师",
            role=UserRole.TEACHER,
            title="讲师",
            college="环境学院",
            email="zhengshi@example.com",
            phone="13900139006",
            research_field="环境监测、污染控制"
        )
        db.add(teacher8)
        
        db.commit()
        print("✓ 用户数据插入成功（10个）")
        
        # ==================== 创建项目（12个，覆盖所有状态） ====================
        projects = [
            Project(
                project_name="基于深度学习的图像识别研究",
                pi_id=admin_user.id,
                pi_name=admin_user.name,
                members='["张教授", "李教授", "王副教授"]',
                project_type="国家自然科学基金",
                source="国家自然科学基金委",
                budget_total=500000.0,
                start_date=date(2023, 1, 1),
                end_date=date(2025, 12, 31),
                status=ProjectStatus.IN_PROGRESS,
                description="研究深度学习在图像识别领域的应用，探索新型卷积神经网络架构",
                objectives="提出新的图像识别算法，发表高水平论文，申请发明专利"
            ),
            Project(
                project_name="智能推荐系统关键技术研究",
                pi_id=teacher1.id,
                pi_name=teacher1.name,
                members='["张教授", "李教授"]',
                project_type="省级科技计划",
                source="省科技厅",
                budget_total=200000.0,
                start_date=date(2024, 1, 1),
                end_date=date(2026, 12, 31),
                status=ProjectStatus.IN_PROGRESS,
                description="研究智能推荐系统的核心算法，提升推荐准确率"
            ),
            Project(
                project_name="量子计算在密码学中的应用研究",
                pi_id=teacher4.id,
                pi_name=teacher4.name,
                members='["赵讲师", "孙教授"]',
                project_type="国家重点研发计划",
                source="科技部",
                budget_total=800000.0,
                start_date=date(2022, 6, 1),
                end_date=date(2025, 5, 31),
                status=ProjectStatus.MID_CHECK,
                description="探索量子算法在密码破译和安全通信中的应用",
                objectives="开发新型量子密码协议，发表顶级会议论文"
            ),
            Project(
                project_name="生物医学大数据分析平台",
                pi_id=teacher6.id,
                pi_name=teacher6.name,
                members='["周副教授", "郑讲师"]',
                project_type="国家自然科学基金",
                source="国家自然科学基金委",
                budget_total=450000.0,
                start_date=date(2023, 7, 1),
                end_date=date(2026, 6, 30),
                status=ProjectStatus.IN_PROGRESS,
                description="构建生物医学数据分析平台，支持基因组数据挖掘"
            ),
            Project(
                project_name="新型纳米材料的制备与应用",
                pi_id=teacher7.id,
                pi_name=teacher7.name,
                members='["吴教授"]',
                project_type="横向项目",
                source="某新材料公司",
                budget_total=300000.0,
                start_date=date(2024, 3, 1),
                end_date=date(2025, 2, 28),
                status=ProjectStatus.IN_PROGRESS,
                description="研发高性能纳米复合材料，应用于新能源领域"
            ),
            Project(
                project_name="智慧城市交通优化系统",
                pi_id=teacher2.id,
                pi_name=teacher2.name,
                members='["李教授", "王副教授", "张教授"]',
                project_type="省级重点项目",
                source="省科技厅",
                budget_total=600000.0,
                start_date=date(2021, 1, 1),
                end_date=date(2023, 12, 31),
                status=ProjectStatus.COMPLETED,
                description="基于AI的城市交通流量预测与优化调度系统",
                objectives="已完成系统开发，在3个城市试点应用"
            ),
            Project(
                project_name="工业机器人视觉导航技术",
                pi_id=teacher2.id,
                pi_name=teacher2.name,
                members='["李教授", "孙教授"]',
                project_type="国家自然科学基金",
                source="国家自然科学基金委",
                budget_total=420000.0,
                start_date=date(2024, 1, 1),
                end_date=date(2026, 12, 31),
                status=ProjectStatus.IN_PROGRESS,
                description="研究机器人实时视觉定位与路径规划算法"
            ),
            Project(
                project_name="环境污染智能监测系统",
                pi_id=teacher8.id,
                pi_name=teacher8.name,
                members='["郑讲师"]',
                project_type="市级科技项目",
                source="市科技局",
                budget_total=150000.0,
                start_date=date(2024, 4, 1),
                end_date=date(2025, 3, 31),
                status=ProjectStatus.IN_PROGRESS,
                description="开发基于传感器网络的环境监测预警系统"
            ),
            Project(
                project_name="区块链技术在供应链中的应用",
                pi_id=teacher3.id,
                pi_name=teacher3.name,
                members='["王副教授"]',
                project_type="企业委托项目",
                source="某物流公司",
                budget_total=250000.0,
                start_date=date(2023, 10, 1),
                end_date=date(2024, 9, 30),
                status=ProjectStatus.MID_CHECK,
                description="利用区块链技术提升供应链透明度和可信度"
            ),
            Project(
                project_name="5G通信关键技术研究",
                pi_id=teacher5.id,
                pi_name=teacher5.name,
                members='["孙教授", "赵讲师"]',
                project_type="国家重点研发计划",
                source="科技部",
                budget_total=1000000.0,
                start_date=date(2021, 7, 1),
                end_date=date(2024, 6, 30),
                status=ProjectStatus.COMPLETED,
                description="研究5G通信中的信号处理与抗干扰技术",
                objectives="已完成技术攻关，获得2项发明专利"
            ),
            Project(
                project_name="智能问答系统的研究与开发",
                pi_id=admin_user.id,
                pi_name=admin_user.name,
                members='["系统管理员", "张教授"]',
                project_type="校级项目",
                source="校科研处",
                budget_total=100000.0,
                start_date=date(2024, 9, 1),
                end_date=date(2025, 8, 31),
                status=ProjectStatus.DRAFT,
                description="基于大语言模型的智能问答系统"
            ),
            Project(
                project_name="基因编辑技术优化研究",
                pi_id=teacher6.id,
                pi_name=teacher6.name,
                members='["周副教授", "吴教授"]',
                project_type="国家自然科学基金",
                source="国家自然科学基金委",
                budget_total=550000.0,
                start_date=date(2024, 1, 1),
                end_date=date(2027, 12, 31),
                status=ProjectStatus.IN_PROGRESS,
                description="CRISPR基因编辑技术的精准度提升研究"
            )
        ]
        
        for p in projects:
            db.add(p)
        db.commit()
        print("✓ 项目数据插入成功（12个）")
        
        # 获取项目ID（用于后续关联）
        project1 = projects[0]
        project2 = projects[1]
        project3 = projects[2]
        project4 = projects[3]
        project5 = projects[4]
        project6 = projects[5]
        project7 = projects[6]
        project8 = projects[7]
        project9 = projects[8]
        project10 = projects[9]
        
        # ==================== 创建论文（20篇，覆盖各分区） ====================
        papers = [
            # Q1区论文（8篇）
            Paper(
                title="Deep Learning for Image Classification: A Survey",
                authors="系统管理员, 李教授",
                journal="IEEE Transactions on Pattern Analysis and Machine Intelligence",
                publication_date=date(2024, 3, 15),
                doi="10.1109/TPAMI.2024.001",
                jcr_zone="Q1",
                cas_zone="一区",
                impact_factor=24.5,
                project_id=project1.id,
                creator_id=admin_user.id
            ),
            Paper(
                title="A Novel Recommendation Algorithm Based on Graph Neural Networks",
                authors="张教授, 李教授",
                journal="ACM Transactions on Information Systems",
                publication_date=date(2024, 6, 20),
                doi="10.1145/TOIS.2024.002",
                jcr_zone="Q1",
                cas_zone="二区",
                impact_factor=15.3,
                project_id=project2.id,
                creator_id=teacher1.id
            ),
            Paper(
                title="Quantum Error Correction with Surface Codes",
                authors="赵讲师, 孙教授",
                journal="Physical Review Letters",
                publication_date=date(2023, 11, 10),
                doi="10.1103/PhysRevLett.2023.003",
                jcr_zone="Q1",
                cas_zone="一区",
                impact_factor=32.1,
                project_id=project3.id,
                creator_id=teacher4.id
            ),
            Paper(
                title="Genomic Data Analysis Using Machine Learning",
                authors="周副教授, 郑讲师",
                journal="Nature Biotechnology",
                publication_date=date(2024, 2, 5),
                doi="10.1038/nbt.2024.004",
                jcr_zone="Q1",
                cas_zone="一区",
                impact_factor=28.7,
                project_id=project4.id,
                creator_id=teacher6.id
            ),
            Paper(
                title="Advanced Nanomaterials for Energy Storage Applications",
                authors="吴教授",
                journal="Advanced Materials",
                publication_date=date(2024, 4, 12),
                doi="10.1002/adma.2024.005",
                jcr_zone="Q1",
                cas_zone="一区",
                impact_factor=27.4,
                project_id=project5.id,
                creator_id=teacher7.id
            ),
            Paper(
                title="Real-time Traffic Flow Prediction Using LSTM Networks",
                authors="李教授, 王副教授, 张教授",
                journal="IEEE Transactions on Intelligent Transportation Systems",
                publication_date=date(2023, 9, 18),
                doi="10.1109/TITS.2023.006",
                jcr_zone="Q1",
                cas_zone="二区",
                impact_factor=18.5,
                project_id=project6.id,
                creator_id=teacher2.id
            ),
            Paper(
                title="Robot Visual Navigation in Dynamic Environments",
                authors="李教授, 孙教授",
                journal="International Journal of Robotics Research",
                publication_date=date(2024, 5, 8),
                doi="10.1177/IJRR.2024.007",
                jcr_zone="Q1",
                cas_zone="二区",
                impact_factor=16.2,
                project_id=project7.id,
                creator_id=teacher2.id
            ),
            Paper(
                title="5G Signal Processing with Low Latency",
                authors="孙教授, 赵讲师",
                journal="IEEE Communications Magazine",
                publication_date=date(2023, 12, 20),
                doi="10.1109/MCOM.2023.008",
                jcr_zone="Q1",
                cas_zone="二区",
                impact_factor=19.8,
                project_id=project10.id,
                creator_id=teacher5.id
            ),
            # Q2区论文（6篇）
            Paper(
                title="Attention Mechanisms in Computer Vision: A Review",
                authors="系统管理员, 张教授",
                journal="Pattern Recognition",
                publication_date=date(2024, 1, 25),
                doi="10.1016/j.patcog.2024.009",
                jcr_zone="Q2",
                cas_zone="二区",
                impact_factor=12.5,
                project_id=project1.id,
                creator_id=admin_user.id
            ),
            Paper(
                title="Collaborative Filtering with Deep Learning",
                authors="张教授",
                journal="Expert Systems with Applications",
                publication_date=date(2024, 7, 10),
                doi="10.1016/j.eswa.2024.010",
                jcr_zone="Q2",
                cas_zone="三区",
                impact_factor=10.8,
                project_id=project2.id,
                creator_id=teacher1.id
            ),
            Paper(
                title="Blockchain-based Supply Chain Traceability System",
                authors="王副教授",
                journal="Computers & Industrial Engineering",
                publication_date=date(2024, 3, 5),
                doi="10.1016/j.cie.2024.011",
                jcr_zone="Q2",
                cas_zone="三区",
                impact_factor=9.2,
                project_id=project9.id,
                creator_id=teacher3.id
            ),
            Paper(
                title="Environmental Monitoring Using IoT Sensors",
                authors="郑讲师",
                journal="Environmental Science & Technology",
                publication_date=date(2024, 6, 15),
                doi="10.1021/est.2024.012",
                jcr_zone="Q2",
                cas_zone="二区",
                impact_factor=11.4,
                project_id=project8.id,
                creator_id=teacher8.id
            ),
            Paper(
                title="CRISPR Gene Editing Efficiency Optimization",
                authors="周副教授, 吴教授",
                journal="Molecular Biology Reports",
                publication_date=date(2024, 4, 20),
                doi="10.1007/mbr.2024.013",
                jcr_zone="Q2",
                cas_zone="三区",
                impact_factor=8.9,
                project_id=project4.id,
                creator_id=teacher6.id
            ),
            Paper(
                title="Nanomaterial Synthesis via Green Chemistry",
                authors="吴教授",
                journal="Journal of Materials Chemistry A",
                publication_date=date(2024, 5, 30),
                doi="10.1039/jmca.2024.014",
                jcr_zone="Q2",
                cas_zone="二区",
                impact_factor=13.1,
                project_id=project5.id,
                creator_id=teacher7.id
            ),
            # Q3区论文（4篇）
            Paper(
                title="Image Segmentation Using U-Net Variants",
                authors="李教授",
                journal="Neural Computing and Applications",
                publication_date=date(2024, 2, 10),
                doi="10.1007/nca.2024.015",
                jcr_zone="Q3",
                cas_zone="三区",
                impact_factor=6.5,
                project_id=project1.id,
                creator_id=teacher2.id
            ),
            Paper(
                title="Quantum Cryptography Protocol Analysis",
                authors="赵讲师",
                journal="Quantum Information Processing",
                publication_date=date(2024, 3, 22),
                doi="10.1007/qip.2024.016",
                jcr_zone="Q3",
                cas_zone="四区",
                impact_factor=5.8,
                project_id=project3.id,
                creator_id=teacher4.id
            ),
            Paper(
                title="Traffic Congestion Prediction Using Statistical Methods",
                authors="王副教授",
                journal="Transportation Research Part C",
                publication_date=date(2023, 10, 5),
                doi="10.1016/trc.2023.017",
                jcr_zone="Q3",
                cas_zone="三区",
                impact_factor=7.2,
                project_id=project6.id,
                creator_id=teacher3.id
            ),
            Paper(
                title="Bioinformatics Tools for Gene Expression Analysis",
                authors="周副教授",
                journal="BMC Bioinformatics",
                publication_date=date(2024, 7, 8),
                doi="10.1186/bmcb.2024.018",
                jcr_zone="Q3",
                cas_zone="四区",
                impact_factor=4.9,
                project_id=project4.id,
                creator_id=teacher6.id
            ),
            # Q4区论文（2篇）
            Paper(
                title="Data Preprocessing Techniques for Machine Learning",
                authors="张教授",
                journal="Applied Intelligence",
                publication_date=date(2024, 8, 12),
                doi="10.1007/ai.2024.019",
                jcr_zone="Q4",
                cas_zone="四区",
                impact_factor=3.5,
                project_id=project2.id,
                creator_id=teacher1.id
            ),
            Paper(
                title="Environmental Data Visualization Techniques",
                authors="郑讲师",
                journal="Environmental Monitoring and Assessment",
                publication_date=date(2024, 9, 1),
                doi="10.1007/ema.2024.020",
                jcr_zone="Q4",
                cas_zone="四区",
                impact_factor=2.8,
                project_id=project8.id,
                creator_id=teacher8.id
            )
        ]
        
        for paper in papers:
            db.add(paper)
        db.commit()
        print("✓ 论文数据插入成功（20篇：Q1-8篇、Q2-6篇、Q3-4篇、Q4-2篇）")
        
        # ==================== 创建经费记录（30条，覆盖7种类型） ====================
        funds = [
            # 项目1的经费（6条）
            Fund(project_id=project1.id, expense_type="设备费", amount=150000.0, expense_date=date(2023, 3, 10), handler="系统管理员", notes="购买GPU服务器（NVIDIA A100）"),
            Fund(project_id=project1.id, expense_type="差旅费", amount=30000.0, expense_date=date(2023, 6, 15), handler="李教授", notes="参加CVPR 2023国际会议"),
            Fund(project_id=project1.id, expense_type="会议费", amount=15000.0, expense_date=date(2023, 9, 5), handler="系统管理员", notes="主办计算机视觉研讨会"),
            Fund(project_id=project1.id, expense_type="材料费", amount=20000.0, expense_date=date(2024, 1, 12), handler="张教授", notes="购买实验数据集和标注服务"),
            Fund(project_id=project1.id, expense_type="劳务费", amount=50000.0, expense_date=date(2024, 3, 20), handler="系统管理员", notes="研究生助研津贴"),
            Fund(project_id=project1.id, expense_type="出版费", amount=12000.0, expense_date=date(2024, 4, 8), handler="李教授", notes="论文开放获取发表费用"),
            
            # 项目2的经费（4条）
            Fund(project_id=project2.id, expense_type="设备费", amount=80000.0, expense_date=date(2024, 2, 15), handler="张教授", notes="购买服务器和存储设备"),
            Fund(project_id=project2.id, expense_type="差旅费", amount=25000.0, expense_date=date(2024, 5, 20), handler="张教授", notes="参加RecSys 2024推荐系统会议"),
            Fund(project_id=project2.id, expense_type="材料费", amount=15000.0, expense_date=date(2024, 6, 10), handler="李教授", notes="购买推荐系统测试数据"),
            Fund(project_id=project2.id, expense_type="劳务费", amount=35000.0, expense_date=date(2024, 7, 5), handler="张教授", notes="算法工程师兼职费用"),
            
            # 项目3的经费（4条）
            Fund(project_id=project3.id, expense_type="设备费", amount=200000.0, expense_date=date(2022, 8, 12), handler="赵讲师", notes="量子计算模拟器"),
            Fund(project_id=project3.id, expense_type="差旅费", amount=45000.0, expense_date=date(2023, 3, 18), handler="孙教授", notes="参加QIP量子信息国际会议"),
            Fund(project_id=project3.id, expense_type="会议费", amount=25000.0, expense_date=date(2023, 7, 10), handler="赵讲师", notes="组织量子计算学术研讨会"),
            Fund(project_id=project3.id, expense_type="出版费", amount=18000.0, expense_date=date(2023, 11, 15), handler="孙教授", notes="Physical Review Letters论文发表费"),
            
            # 项目4的经费（3条）
            Fund(project_id=project4.id, expense_type="设备费", amount=180000.0, expense_date=date(2023, 9, 5), handler="周副教授", notes="生物信息分析工作站"),
            Fund(project_id=project4.id, expense_type="材料费", amount=60000.0, expense_date=date(2024, 1, 20), handler="周副教授", notes="基因测序服务费用"),
            Fund(project_id=project4.id, expense_type="劳务费", amount=40000.0, expense_date=date(2024, 3, 15), handler="郑讲师", notes="数据分析兼职人员"),
            
            # 项目5的经费（3条）
            Fund(project_id=project5.id, expense_type="材料费", amount=120000.0, expense_date=date(2024, 4, 8), handler="吴教授", notes="纳米材料原料采购"),
            Fund(project_id=project5.id, expense_type="设备费", amount=80000.0, expense_date=date(2024, 5, 12), handler="吴教授", notes="材料表征仪器租赁"),
            Fund(project_id=project5.id, expense_type="差旅费", amount=18000.0, expense_date=date(2024, 6, 5), handler="吴教授", notes="参加材料学会年会"),
            
            # 项目6的经费（3条）
            Fund(project_id=project6.id, expense_type="设备费", amount=250000.0, expense_date=date(2021, 3, 15), handler="李教授", notes="交通数据采集设备"),
            Fund(project_id=project6.id, expense_type="差旅费", amount=35000.0, expense_date=date(2022, 6, 20), handler="王副教授", notes="考察智慧交通试点城市"),
            Fund(project_id=project6.id, expense_type="劳务费", amount=80000.0, expense_date=date(2023, 5, 10), handler="张教授", notes="系统开发人员费用"),
            
            # 项目7的经费（2条）
            Fund(project_id=project7.id, expense_type="设备费", amount=160000.0, expense_date=date(2024, 2, 8), handler="李教授", notes="工业机器人平台"),
            Fund(project_id=project7.id, expense_type="材料费", amount=35000.0, expense_date=date(2024, 5, 15), handler="孙教授", notes="视觉传感器及配件"),
            
            # 项目8的经费（2条）
            Fund(project_id=project8.id, expense_type="设备费", amount=80000.0, expense_date=date(2024, 5, 10), handler="郑讲师", notes="环境监测传感器网络"),
            Fund(project_id=project8.id, expense_type="差旅费", amount=12000.0, expense_date=date(2024, 7, 8), handler="郑讲师", notes="环境监测现场调研"),
            
            # 项目9的经费（2条）
            Fund(project_id=project9.id, expense_type="设备费", amount=100000.0, expense_date=date(2023, 11, 5), handler="王副教授", notes="区块链服务器节点"),
            Fund(project_id=project9.id, expense_type="差旅费", amount=22000.0, expense_date=date(2024, 2, 15), handler="王副教授", notes="参加区块链技术峰会"),
            
            # 项目10的经费（1条）
            Fund(project_id=project10.id, expense_type="设备费", amount=350000.0, expense_date=date(2021, 9, 20), handler="孙教授", notes="5G通信测试设备")
        ]
        
        for fund in funds:
            db.add(fund)
        db.commit()
        print("✓ 经费数据插入成功（30条：设备费、差旅费、会议费、材料费、劳务费、出版费等）")
        
        # ==================== 创建成果记录（16项，覆盖4种类型） ====================
        achievements = [
            # 专利（6项）
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="一种基于深度学习的图像识别方法",
                owner="系统管理员",
                members="系统管理员, 李教授",
                completion_date=date(2024, 2, 1),
                certificate_no="CN202410001234.5",
                description="本发明提出了一种新的卷积神经网络架构，用于提高图像分类准确率"
            ),
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="一种量子密钥分发系统及方法",
                owner="赵讲师",
                members="赵讲师, 孙教授",
                completion_date=date(2023, 10, 15),
                certificate_no="CN202310005678.9",
                description="基于量子纠缠的安全密钥分发技术"
            ),
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="智能交通流量预测装置",
                owner="李教授",
                members="李教授, 王副教授, 张教授",
                completion_date=date(2023, 8, 20),
                certificate_no="CN202308009012.3",
                description="基于LSTM神经网络的实时交通流量预测系统"
            ),
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="新型纳米复合材料及其制备方法",
                owner="吴教授",
                members="吴教授",
                completion_date=date(2024, 5, 8),
                certificate_no="CN202405003456.7",
                description="高性能石墨烯纳米复合材料的绿色制备技术"
            ),
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="基于区块链的供应链溯源系统",
                owner="王副教授",
                members="王副教授",
                completion_date=date(2024, 3, 12),
                certificate_no="CN202403007890.1",
                description="利用区块链技术实现供应链全流程可追溯"
            ),
            Achievement(
                achievement_type=AchievementType.PATENT,
                title="智能环境监测预警装置",
                owner="郑讲师",
                members="郑讲师",
                completion_date=date(2024, 7, 5),
                certificate_no="CN202407002345.6",
                description="基于物联网的多参数环境实时监测系统"
            ),
            
            # 奖项（6项）
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="省级科技进步二等奖",
                owner="系统管理员",
                members="系统管理员, 李教授, 张教授",
                completion_date=date(2023, 12, 10),
                certificate_no="2023-KJ-002",
                description="智能图像识别系统及其在工业检测中的应用"
            ),
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="国家自然科学二等奖",
                owner="孙教授",
                members="孙教授, 赵讲师",
                completion_date=date(2024, 1, 15),
                certificate_no="2024-ZRK-021",
                description="5G通信抗干扰理论与关键技术"
            ),
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="市级科技创新一等奖",
                owner="李教授",
                members="李教授, 王副教授",
                completion_date=date(2023, 11, 20),
                certificate_no="2023-SJ-015",
                description="智慧城市交通优化系统"
            ),
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="省级教学成果一等奖",
                owner="张教授",
                members="张教授, 李教授",
                completion_date=date(2023, 9, 5),
                certificate_no="2023-JX-008",
                description="人工智能课程体系改革与实践"
            ),
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="中国青年科技奖",
                owner="周副教授",
                members="周副教授",
                completion_date=date(2024, 6, 1),
                certificate_no="2024-QN-056",
                description="生物信息学领域突出贡献"
            ),
            Achievement(
                achievement_type=AchievementType.AWARD,
                title="校级优秀科研成果奖",
                owner="王副教授",
                members="王副教授",
                completion_date=date(2024, 4, 10),
                certificate_no="2024-XJ-012",
                description="应用数学研究优秀成果"
            ),
            
            # 著作（2项）
            Achievement(
                achievement_type=AchievementType.BOOK,
                title="深度学习理论与实践",
                owner="系统管理员",
                members="系统管理员, 张教授, 李教授",
                completion_date=date(2023, 6, 15),
                certificate_no="ISBN 978-7-111-12345-6",
                description="系统介绍深度学习的理论基础和工程实践，清华大学出版社"
            ),
            Achievement(
                achievement_type=AchievementType.BOOK,
                title="量子计算导论",
                owner="赵讲师",
                members="赵讲师, 孙教授",
                completion_date=date(2024, 3, 20),
                certificate_no="ISBN 978-7-302-67890-1",
                description="量子计算原理与算法设计，北京大学出版社"
            ),
            
            # 软件著作权（2项）
            Achievement(
                achievement_type=AchievementType.SOFTWARE,
                title="智能推荐系统软件V1.0",
                owner="张教授",
                members="张教授, 李教授",
                completion_date=date(2024, 5, 10),
                certificate_no="软著登字第1234567号",
                description="基于深度学习的个性化推荐系统软件"
            ),
            Achievement(
                achievement_type=AchievementType.SOFTWARE,
                title="环境监测数据分析平台V2.0",
                owner="郑讲师",
                members="郑讲师",
                completion_date=date(2024, 8, 1),
                certificate_no="软著登字第2345678号",
                description="实时环境数据采集、分析与可视化平台"
            )
        ]
        
        for achievement in achievements:
            db.add(achievement)
        db.commit()
        print("✓ 成果数据插入成功（16项：专利6项、奖项6项、著作2项、软著2项）")
        
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
        print("管理员: admin / Admin@123")
        print("普通教师: teacher / Teacher@123")
        print("科研秘书: secretary / Sec@2024")
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
