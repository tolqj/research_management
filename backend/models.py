"""
数据库模型定义
包括：用户、项目、论文、经费、成果等表
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# 用户角色枚举
class UserRole(str, enum.Enum):
    ADMIN = "管理员"
    SECRETARY = "科研秘书"
    TEACHER = "普通教师"


# 项目状态枚举
class ProjectStatus(str, enum.Enum):
    DRAFT = "草稿"
    SUBMITTED = "已申报"
    APPROVED = "已批准"
    IN_PROGRESS = "执行中"
    MID_CHECK = "中期检查"
    COMPLETED = "已结题"
    REJECTED = "已拒绝"


# 成果类型枚举
class AchievementType(str, enum.Enum):
    PATENT = "专利"
    AWARD = "奖项"
    BOOK = "著作"
    SOFTWARE = "软件著作权"


# 用户表
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    name = Column(String(50), nullable=False, comment="姓名")
    role = Column(Enum(UserRole), default=UserRole.TEACHER, comment="角色")
    title = Column(String(50), comment="职称")
    college = Column(String(100), comment="学院")
    email = Column(String(100), unique=True, comment="邮箱")
    phone = Column(String(20), comment="电话")
    research_field = Column(String(200), comment="研究方向")
    
    # 安全相关字段（等保要求）
    password_updated_at = Column(DateTime, server_default=func.now(), comment="密码最后修改时间")
    login_failures = Column(Integer, default=0, comment="连续登录失败次数")
    locked_until = Column(DateTime, nullable=True, comment="账号锁定截止时间")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(50), nullable=True, comment="最后登录IP")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    projects = relationship("Project", back_populates="pi_user", foreign_keys="[Project.pi_id]")
    papers = relationship("Paper", back_populates="creator_user")


# 科研项目表
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_name = Column(String(200), nullable=False, comment="项目名称")
    pi_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="负责人ID")
    pi_name = Column(String(50), nullable=False, comment="负责人姓名")
    members = Column(Text, comment="项目成员（JSON格式）")
    project_type = Column(String(100), comment="项目类型")
    source = Column(String(100), comment="项目来源")
    budget_total = Column(Float, default=0.0, comment="总预算")
    start_date = Column(Date, comment="开始日期")
    end_date = Column(Date, comment="结束日期")
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, comment="项目状态")
    description = Column(Text, comment="项目描述")
    objectives = Column(Text, comment="研究目标")
    attachments = Column(Text, comment="附件（JSON格式）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    pi_user = relationship("User", back_populates="projects", foreign_keys=[pi_id])
    funds = relationship("Fund", back_populates="project", cascade="all, delete-orphan")
    papers = relationship("Paper", back_populates="project")


# 论文表
class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(300), nullable=False, comment="论文标题")
    authors = Column(String(500), nullable=False, comment="作者列表")
    journal = Column(String(200), comment="期刊名称")
    publication_date = Column(Date, comment="发表日期")
    doi = Column(String(100), comment="DOI")
    jcr_zone = Column(String(10), comment="JCR分区")
    cas_zone = Column(String(10), comment="中科院分区")
    impact_factor = Column(Float, comment="影响因子")
    project_id = Column(Integer, ForeignKey("projects.id"), comment="关联项目ID")
    creator_id = Column(Integer, ForeignKey("users.id"), comment="录入人ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="papers")
    creator_user = relationship("User", back_populates="papers")


# 经费表
class Fund(Base):
    __tablename__ = "funds"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    expense_type = Column(String(100), nullable=False, comment="支出类型")
    amount = Column(Float, nullable=False, comment="金额")
    expense_date = Column(Date, nullable=False, comment="支出日期")
    handler = Column(String(50), comment="经办人")
    notes = Column(Text, comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关系
    project = relationship("Project", back_populates="funds")


# 科研成果表
class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    achievement_type = Column(Enum(AchievementType), nullable=False, comment="成果类型")
    title = Column(String(200), nullable=False, comment="成果名称")
    owner = Column(String(100), nullable=False, comment="成果所有人")
    members = Column(String(500), comment="参与人员")
    completion_date = Column(Date, comment="完成日期")
    certificate_no = Column(String(100), comment="证书编号")
    description = Column(Text, comment="成果描述")
    attachments = Column(Text, comment="附件（JSON格式）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


# 操作日志表（符合等保二级要求）
class OperationLog(Base):
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    username = Column(String(50), comment="用户名")
    operation = Column(String(100), nullable=False, comment="操作类型")
    module = Column(String(50), nullable=False, comment="模块名称")
    method = Column(String(10), comment="HTTP方法")
    path = Column(String(200), comment="请求路径")
    details = Column(Text, comment="操作详情")
    ip_address = Column(String(50), nullable=False, comment="IP地址")
    user_agent = Column(String(500), comment="用户代理")
    status = Column(String(20), comment="操作结果")
    error_msg = Column(Text, comment="错误信息")
    duration = Column(Integer, comment="执行时间(毫秒)")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="操作时间")
