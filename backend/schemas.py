"""
Pydantic 数据模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from models import UserRole, ProjectStatus, AchievementType


# ==================== 用户相关 ====================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    name: str = Field(..., max_length=50, description="姓名")
    role: UserRole = Field(default=UserRole.TEACHER, description="角色")
    title: Optional[str] = Field(None, max_length=50, description="职称")
    college: Optional[str] = Field(None, max_length=100, description="学院")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="电话")
    research_field: Optional[str] = Field(None, max_length=200, description="研究方向")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="密码")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    college: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    research_field: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PasswordChange(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


# ==================== 认证相关 ====================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    warning: Optional[str] = None  # 密码过期等安全警告


# ==================== 项目相关 ====================

class ProjectBase(BaseModel):
    project_name: str = Field(..., max_length=200, description="项目名称")
    pi_name: str = Field(..., max_length=50, description="负责人姓名")
    members: Optional[str] = Field(None, description="项目成员（JSON）")
    project_type: Optional[str] = Field(None, max_length=100, description="项目类型")
    source: Optional[str] = Field(None, max_length=100, description="项目来源")
    budget_total: float = Field(default=0.0, description="总预算")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT, description="项目状态")
    description: Optional[str] = Field(None, description="项目描述")
    objectives: Optional[str] = Field(None, description="研究目标")
    attachments: Optional[str] = Field(None, description="附件（JSON）")


class ProjectCreate(ProjectBase):
    pi_id: int = Field(..., description="负责人ID")


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    members: Optional[str] = None
    project_type: Optional[str] = None
    source: Optional[str] = None
    budget_total: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None
    description: Optional[str] = None
    objectives: Optional[str] = None
    attachments: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    pi_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 论文相关 ====================

class PaperBase(BaseModel):
    title: str = Field(..., max_length=300, description="论文标题")
    authors: str = Field(..., max_length=500, description="作者列表")
    journal: Optional[str] = Field(None, max_length=200, description="期刊名称")
    publication_date: Optional[date] = Field(None, description="发表日期")
    doi: Optional[str] = Field(None, max_length=100, description="DOI")
    jcr_zone: Optional[str] = Field(None, max_length=10, description="JCR分区")
    cas_zone: Optional[str] = Field(None, max_length=10, description="中科院分区")
    impact_factor: Optional[float] = Field(None, description="影响因子")
    project_id: Optional[int] = Field(None, description="关联项目ID")


class PaperCreate(PaperBase):
    creator_id: int = Field(..., description="录入人ID")


class PaperUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    journal: Optional[str] = None
    publication_date: Optional[date] = None
    doi: Optional[str] = None
    jcr_zone: Optional[str] = None
    cas_zone: Optional[str] = None
    impact_factor: Optional[float] = None
    project_id: Optional[int] = None


class PaperResponse(PaperBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 经费相关 ====================

class FundBase(BaseModel):
    project_id: int = Field(..., description="项目ID")
    expense_type: str = Field(..., max_length=100, description="支出类型")
    amount: float = Field(..., gt=0, description="金额")
    expense_date: date = Field(..., description="支出日期")
    handler: Optional[str] = Field(None, max_length=50, description="经办人")
    notes: Optional[str] = Field(None, description="备注")


class FundCreate(FundBase):
    pass


class FundUpdate(BaseModel):
    expense_type: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    handler: Optional[str] = None
    notes: Optional[str] = None


class FundResponse(FundBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 成果相关 ====================

class AchievementBase(BaseModel):
    achievement_type: AchievementType = Field(..., description="成果类型")
    title: str = Field(..., max_length=200, description="成果名称")
    owner: str = Field(..., max_length=100, description="成果所有人")
    members: Optional[str] = Field(None, max_length=500, description="参与人员")
    completion_date: Optional[date] = Field(None, description="完成日期")
    certificate_no: Optional[str] = Field(None, max_length=100, description="证书编号")
    description: Optional[str] = Field(None, description="成果描述")
    attachments: Optional[str] = Field(None, description="附件（JSON）")


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    achievement_type: Optional[AchievementType] = None
    title: Optional[str] = None
    owner: Optional[str] = None
    members: Optional[str] = None
    completion_date: Optional[date] = None
    certificate_no: Optional[str] = None
    description: Optional[str] = None
    attachments: Optional[str] = None


class AchievementResponse(AchievementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 统计相关 ====================

class ProjectStatistics(BaseModel):
    total: int
    by_status: dict
    by_college: dict
    by_year: dict


class PaperStatistics(BaseModel):
    total: int
    by_year: dict
    by_jcr_zone: dict
    by_cas_zone: dict


class FundStatistics(BaseModel):
    total_budget: float
    total_expense: float
    by_type: dict
    by_project: dict


# ==================== 通用响应 ====================

class MessageResponse(BaseModel):
    message: str
    code: int = 200


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List
