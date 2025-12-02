# 安全规范文档

本文档说明科研管理系统的安全特性和等保二级合规要求。

## 📋 目录

- [等保二级概述](#等保二级概述)
- [身份鉴别](#身份鉴别)
- [访问控制](#访问控制)
- [安全审计](#安全审计)
- [数据完整性](#数据完整性)
- [安全配置](#安全配置)
- [安全最佳实践](#安全最佳实践)

## 等保二级概述

### 什么是等保二级？

**等级保护二级**（简称"等保二级"）是中国网络安全等级保护制度的第二级，适用于:
- 一般性的信息系统
- 高校、科研机构的管理系统
- 地市级单位的业务系统

### 核心要求

本系统已实现以下等保二级核心要求：

| 类别 | 要求 | 实现状态 |
|------|------|---------|
| 身份鉴别 | 密码复杂度、定期更换、登录限制 | ✅ 已实现 |
| 访问控制 | 基于角色的访问控制(RBAC) | ✅ 已实现 |
| 安全审计 | 操作日志记录、审计追踪 | ✅ 已实现 |
| 数据完整性 | 事务保护、约束验证 | ✅ 已实现 |
| 数据保密性 | 密码加密存储、传输加密 | ✅ 已实现 |

## 身份鉴别

### 1. 密码复杂度要求

系统强制执行以下密码策略：

```python
# utils/password_policy.py

密码要求：
✅ 最小长度：8位
✅ 必须包含：大写字母
✅ 必须包含：小写字母  
✅ 必须包含：数字
✅ 必须包含：特殊字符(!@#$%^&*()等)
```

**示例合格密码**:
- `Admin@123`
- `Secure#Pass2024`
- `MyP@ssw0rd!`

**前端实时验证**:

```javascript
// 密码强度检测
const checkPasswordStrength = (password) => {
  let strength = 0
  if (password.length >= 8) strength += 20
  if (/[a-z]/.test(password)) strength += 15
  if (/[A-Z]/.test(password)) strength += 15
  if (/[0-9]/.test(password)) strength += 15
  if (/[!@#$%^&*]/.test(password)) strength += 15
  
  return {
    percentage: strength,
    text: strength < 40 ? '弱' : strength < 70 ? '中' : '强'
  }
}
```

### 2. 密码定期更换

```python
# 密码有效期：90天
PASSWORD_EXPIRE_DAYS = 90

# 提前7天提醒
PASSWORD_WARNING_DAYS = 7

# 检查密码是否过期
def is_password_expired(password_updated_at: datetime) -> bool:
    days_since_update = (datetime.now() - password_updated_at).days
    return days_since_update >= PASSWORD_EXPIRE_DAYS
```

**用户体验**:
- 密码过期前7天，登录时显示警告
- 密码过期后，强制修改密码

### 3. 登录失败锁定

```python
# 登录失败策略
MAX_LOGIN_FAILURES = 5      # 最大失败次数
LOCKOUT_DURATION_MINUTES = 30  # 锁定时长(分钟)

# 登录失败处理
if user.login_failures >= MAX_LOGIN_FAILURES:
    user.locked_until = datetime.now() + timedelta(minutes=30)
    raise HTTPException(
        status_code=403,
        detail=f\"账号已被锁定，请{LOCKOUT_DURATION_MINUTES}分钟后再试\"
    )
```

**安全机制**:
- ✅ 5次登录失败 → 锁定30分钟
- ✅ 显示剩余尝试次数
- ✅ 登录成功后重置失败计数
- ✅ 记录所有登录尝试（成功/失败）

### 4. 会话管理

```python
# JWT Token 配置
SECRET_KEY = \"your-secret-key-here-change-in-production\"
ALGORITHM = \"HS256\"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token 生成
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({\"exp\": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**安全特性**:
- ✅ Token 有效期：30分钟
- ✅ 自动过期机制
- ✅ 包含用户ID和角色信息
- ✅ 使用 HS256 算法签名

## 访问控制

### 1. 基于角色的访问控制(RBAC)

系统定义了3个角色，权限如下：

| 功能模块 | 管理员 | 普通教师 | 科研秘书 |
|---------|-------|---------|---------|
| 用户管理 | ✅ | ❌ | ❌ |
| 项目管理（自己的） | ✅ | ✅ | ✅ |
| 项目管理（所有） | ✅ | ❌ | ✅ |
| 论文管理 | ✅ | ✅ | ✅ |
| 经费管理 | ✅ | ✅ | ✅ |
| 成果管理 | ✅ | ✅ | ✅ |
| 统计分析 | ✅ | ✅ | ✅ |

### 2. 权限验证实现

**后端权限装饰器**:

```python
# utils/security.py

# 需要登录
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # 验证Token并返回用户
    pass

# 需要管理员权限
async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != '管理员':
        raise HTTPException(status_code=403, detail=\"权限不足\")
    return current_user
```

**使用示例**:

```python
# 需要登录
@router.get(\"/projects/\")
def get_projects(
    current_user: User = Depends(get_current_user)
):
    pass

# 需要管理员权限
@router.delete(\"/users/{user_id}\")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin)
):
    pass
```

### 3. 资源级权限控制

```python
# 检查用户是否有权限修改项目
@router.put(\"/projects/{project_id}\")
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = crud_project.get_project_by_id(db, project_id)
    
    # 权限检查：只有项目负责人或管理员可以修改
    if project.pi_id != current_user.id and current_user.role != '管理员':
        # 记录权限拒绝
        AuditLogger.log_permission_denied(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module=\"project\",
            request=request,
            reason=f\"尝试修改项目ID={project_id}，但无权限\"
        )
        raise HTTPException(status_code=403, detail=\"无权限修改此项目\")
    
    # 执行更新操作
    return crud_project.update_project(db, project_id, project_update)
```

### 4. 前端路由守卫

```javascript
// router/index.js

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
    return
  }
  
  // 检查管理员权限
  if (to.meta.requiresAdmin && userStore.user?.role !== '管理员') {
    ElMessage.error('权限不足')
    next(false)
    return
  }
  
  next()
})
```

## 安全审计

### 1. 操作日志记录

系统记录以下所有操作：

| 操作类型 | 记录内容 | 示例 |
|---------|---------|------|
| 登录 | 用户名、IP、时间、结果 | 用户admin从192.168.1.1登录成功 |
| 创建 | 操作人、资源类型、资源ID | 用户admin创建了项目ID=1 |
| 更新 | 操作人、资源ID、变更内容 | 用户teacher修改了项目ID=1的预算 |
| 删除 | 操作人、资源ID、删除前数据 | 用户admin删除了用户ID=10 |
| 权限拒绝 | 操作人、尝试的操作、原因 | 用户teacher尝试删除项目ID=1被拒绝 |

### 2. 审计日志结构

```python
# models.py - operation_logs 表

class OperationLog(Base):
    __tablename__ = \"operation_logs\"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)              # 操作用户ID
    username = Column(String(50))          # 操作用户名
    operation = Column(String(100))        # 操作名称
    module = Column(String(50))            # 模块名称
    method = Column(String(10))            # HTTP方法
    path = Column(String(200))             # 请求路径
    details = Column(Text)                 # 操作详情(JSON)
    ip_address = Column(String(50))        # IP地址
    user_agent = Column(String(500))       # 用户代理
    status = Column(String(20))            # 状态(SUCCESS/FAILED)
    error_msg = Column(Text)               # 错误信息
    duration = Column(Integer)             # 执行耗时(ms)
    created_at = Column(DateTime)          # 操作时间
```

### 3. 审计日志API

```python
# utils/audit.py

class AuditLogger:
    @staticmethod
    def log_create(db, user_id, username, module, resource_type, 
                   resource_id, request, data):
        \"\"\"记录创建操作\"\"\"
        log = OperationLog(
            user_id=user_id,
            username=username,
            operation=f\"创建{resource_type}\",
            module=module,
            method=request.method,
            path=str(request.url.path),
            details=json.dumps(data, ensure_ascii=False),
            ip_address=get_client_ip(request),
            user_agent=request.headers.get(\"user-agent\"),
            status=\"SUCCESS\"
        )
        db.add(log)
        db.commit()
```

### 4. 日志查询示例

```sql
-- 查询用户的所有操作
SELECT * FROM operation_logs 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 100;

-- 查询失败的操作
SELECT * FROM operation_logs 
WHERE status = 'FAILED' 
ORDER BY created_at DESC;

-- 查询特定模块的操作
SELECT * FROM operation_logs 
WHERE module = 'project' 
AND operation LIKE '%删除%';

-- 统计每个用户的操作次数
SELECT username, COUNT(*) as count 
FROM operation_logs 
GROUP BY username 
ORDER BY count DESC;
```

## 数据完整性

### 1. 数据库约束

```sql
-- 主键约束
ALTER TABLE users ADD PRIMARY KEY (id);

-- 唯一约束
ALTER TABLE users ADD UNIQUE KEY (username);
ALTER TABLE users ADD UNIQUE KEY (email);

-- 外键约束
ALTER TABLE projects 
ADD FOREIGN KEY (pi_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE papers 
ADD FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL;

-- 非空约束
ALTER TABLE users MODIFY COLUMN username VARCHAR(50) NOT NULL;
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NOT NULL;

-- 检查约束
ALTER TABLE funds ADD CHECK (amount > 0);
```

### 2. 事务处理

```python
from sqlalchemy.orm import Session

def transfer_project_ownership(
    db: Session,
    project_id: int,
    new_pi_id: int
):
    try:
        # 开始事务
        project = db.query(Project).filter(Project.id == project_id).first()
        old_pi_id = project.pi_id
        
        # 更新项目负责人
        project.pi_id = new_pi_id
        project.pi_name = db.query(User).filter(User.id == new_pi_id).first().name
        
        # 记录审计日志
        log = OperationLog(
            operation=\"转移项目负责人\",
            details=json.dumps({
                \"project_id\": project_id,
                \"old_pi_id\": old_pi_id,
                \"new_pi_id\": new_pi_id
            })
        )
        db.add(log)
        
        # 提交事务
        db.commit()
        
    except Exception as e:
        # 回滚事务
        db.rollback()
        raise e
```

### 3. 输入验证

```python
from pydantic import BaseModel, Field, validator

class ProjectCreate(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)
    budget_total: float = Field(default=0.0, ge=0)
    
    @validator('project_name')
    def validate_project_name(cls, v):
        if not v.strip():
            raise ValueError('项目名称不能为空')
        return v.strip()
    
    @validator('budget_total')
    def validate_budget(cls, v):
        if v < 0:
            raise ValueError('预算金额不能为负数')
        return v
```

## 安全配置

### 1. 生产环境配置清单

```python
# database.py - 生产环境配置

# ❌ 开发环境（不安全）
echo=True  # 打印所有SQL语句

# ✅ 生产环境（安全）
echo=False  # 不打印SQL

# 使用环境变量存储敏感信息
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_PASSWORD = os.getenv(\"MYSQL_PASSWORD\")
SECRET_KEY = os.getenv(\"SECRET_KEY\")
```

### 2. 环境变量配置

创建 `.env` 文件：

```bash
# .env（不要提交到Git）

# 数据库配置
MYSQL_USER=rms_user
MYSQL_PASSWORD=your_secure_password_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=research_management_system

# JWT配置
SECRET_KEY=your_secret_key_min_32_characters_long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 其他配置
DEBUG=False
ALLOW_ORIGINS=https://your-domain.com
```

### 3. HTTPS配置

**Nginx配置示例**:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL证书
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # 安全头
    add_header Strict-Transport-Security \"max-age=31536000\" always;
    add_header X-Frame-Options \"SAMEORIGIN\" always;
    add_header X-Content-Type-Options \"nosniff\" always;
    add_header X-XSS-Protection \"1; mode=block\" always;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 安全最佳实践

### 1. 定期安全检查

- [ ] 每月更新依赖包
- [ ] 每季度进行安全审计
- [ ] 定期备份数据库
- [ ] 监控异常登录行为
- [ ] 检查审计日志

### 2. 密码管理

- ✅ 不在代码中硬编码密码
- ✅ 使用环境变量存储敏感信息
- ✅ 使用bcrypt加密密码
- ✅ 定期更换JWT SECRET_KEY
- ✅ 强制用户定期更换密码

### 3. SQL注入防护

```python
# ❌ 不安全（SQL注入风险）
query = f\"SELECT * FROM users WHERE username = '{username}'\"
db.execute(query)

# ✅ 安全（使用参数化查询）
user = db.query(User).filter(User.username == username).first()
```

### 4. XSS防护

```javascript
// ❌ 不安全
el.innerHTML = userInput

// ✅ 安全（Element Plus自动转义）
<el-input v-model=\"userInput\" />
```

### 5. CSRF防护

```python
# FastAPI自动防护CSRF
# 使用 JWT Token 代替 Cookie Session
```

### 6. 依赖安全

```bash
# 检查Python依赖漏洞
pip install safety
safety check

# 检查Node.js依赖漏洞
npm audit
npm audit fix
```

### 7. 日志脱敏

```python
# 不记录敏感信息
def log_user_action(user):
    # ❌ 不要记录密码
    logger.info(f\"User {user.username} logged in, password: {user.password}\")
    
    # ✅ 只记录必要信息
    logger.info(f\"User {user.username} logged in from {ip_address}\")
```

## 安全检查清单

### 部署前检查

- [ ] 修改默认管理员密码
- [ ] 修改JWT SECRET_KEY
- [ ] 关闭SQL echo
- [ ] 配置HTTPS
- [ ] 配置防火墙
- [ ] 限制数据库访问
- [ ] 删除测试账号
- [ ] 配置日志轮转
- [ ] 配置备份策略
- [ ] 检查依赖漏洞

### 运行时检查

- [ ] 监控登录失败次数
- [ ] 监控API调用频率
- [ ] 监控异常错误
- [ ] 定期审查日志
- [ ] 定期备份数据
- [ ] 定期更新系统

## 应急响应

### 1. 安全事件处理

**发现异常登录**:
1. 立即锁定相关账号
2. 查看审计日志确认影响范围
3. 通知用户修改密码
4. 检查是否有数据泄露

**发现数据篡改**:
1. 立即备份当前数据库
2. 查看审计日志确认操作记录
3. 从备份恢复数据
4. 加强权限控制

### 2. 联系方式

- **安全问题反馈**: security@your-domain.com
- **紧急联系**: 电话号码

## 合规证明

本系统已实现等保二级的核心要求，建议每年进行一次等保测评以获取合规证书。

测评机构可重点检查以下模块：
- 身份鉴别模块: `utils/password_policy.py`, `routers/auth.py`
- 访问控制模块: `utils/security.py`, 路由权限装饰器
- 安全审计模块: `utils/audit.py`, `operation_logs` 表
- 数据库安全: `database.py`, SQL约束

## 参考资料

- [GB/T 22239-2019 信息安全技术 网络安全等级保护基本要求](http://www.gb688.cn/bzgk/gb/newGbInfo?hcno=BAFB47E8874764186BDB7865E8344DAF)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

## 下一步

- 查看 [开发指南](DEVELOPMENT.md) 了解安全开发实践
- 查看 [部署指南](DEPLOYMENT.md) 了解安全部署配置
