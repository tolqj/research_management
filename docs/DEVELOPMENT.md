# 开发指南

本文档为科研管理系统的开发规范和最佳实践指南。

## 📋 目录

- [开发环境搭建](#开发环境搭建)
- [代码规范](#代码规范)
- [项目结构](#项目结构)
- [后端开发](#后端开发)
- [前端开发](#前端开发)
- [API设计规范](#api设计规范)
- [测试指南](#测试指南)
- [Git工作流](#git工作流)

## 开发环境搭建

### IDE推荐

**后端开发**:
- PyCharm Professional
- VS Code + Python Extension

**前端开发**:
- VS Code
- WebStorm

### VS Code 推荐插件

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "vue.volar",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml"
  ]
}
```

### 开发环境配置

#### 后端环境

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖（包含开发依赖）
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

#### 前端环境

```bash
cd frontend

# 安装依赖
npm install

# 安装开发工具
npm install -D eslint prettier
```

## 代码规范

### Python 代码规范

遵循 **PEP 8** 规范，使用 Black 格式化代码。

#### 命名规范

```python
# 模块名：小写+下划线
# database_connection.py

# 类名：大驼峰
class UserModel:
    pass

# 函数名：小写+下划线
def get_user_by_id(user_id: int):
    pass

# 常量：大写+下划线
MAX_RETRY_COUNT = 3

# 私有方法：前缀单下划线
def _internal_method(self):
    pass
```

#### 类型注解

```python
from typing import List, Optional, Dict

def create_user(
    username: str,
    email: Optional[str] = None
) -> Dict[str, any]:
    \"\"\"
    创建用户
    
    Args:
        username: 用户名
        email: 邮箱（可选）
    
    Returns:
        用户信息字典
    \"\"\"
    pass
```

#### 文档字符串

```python
def calculate_budget(
    project_id: int,
    include_indirect: bool = False
) -> float:
    \"\"\"
    计算项目预算
    
    Args:
        project_id: 项目ID
        include_indirect: 是否包含间接费用
        
    Returns:
        预算总额（元）
        
    Raises:
        ValueError: 项目ID无效时抛出
        
    Example:
        >>> calculate_budget(1, include_indirect=True)
        150000.00
    \"\"\"
    pass
```

### JavaScript 代码规范

遵循 **Airbnb JavaScript Style Guide**。

#### 命名规范

```javascript
// 变量和函数：小驼峰
const userName = 'admin'
function getUserInfo() {}

// 组件名：大驼峰
const UserProfile = {}

// 常量：大写+下划线
const API_BASE_URL = 'http://localhost:8000'

// 私有属性：前缀下划线
const _internalState = {}
```

#### Vue 3 组件规范

```vue
<template>
  <div class=\"component-name\">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Props定义
const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

// Emits定义
const emit = defineEmits(['update', 'delete'])

// 响应式数据
const userInfo = ref({})

// 计算属性
const fullName = computed(() => {
  return `${userInfo.value.firstName} ${userInfo.value.lastName}`
})

// 方法
const loadUserInfo = async () => {
  // 实现逻辑
}

// 生命周期
onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.component-name {
  /* 样式 */
}
</style>
```

## 项目结构

### 后端目录结构

```
backend/
├── crud/                    # CRUD操作层
│   ├── __init__.py
│   ├── user.py             # 用户CRUD
│   ├── project.py          # 项目CRUD
│   └── ...
├── routers/                # 路由层（API端点）
│   ├── __init__.py
│   ├── auth.py            # 认证路由
│   ├── user.py            # 用户路由
│   └── ...
├── utils/                  # 工具函数
│   ├── security.py        # 安全工具
│   ├── audit.py           # 审计工具
│   └── password_policy.py # 密码策略
├── models.py              # SQLAlchemy模型
├── schemas.py             # Pydantic schemas
├── database.py            # 数据库配置
├── main.py               # 应用入口
└── requirements.txt      # Python依赖
```

### 前端目录结构

```
frontend/
├── src/
│   ├── assets/           # 静态资源
│   │   └── logo.png
│   ├── components/       # 公共组件
│   │   ├── Header.vue
│   │   └── Footer.vue
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── services/         # API服务
│   │   ├── request.js   # Axios封装
│   │   ├── auth.js      # 认证API
│   │   └── user.js      # 用户API
│   ├── store/            # 状态管理
│   │   └── user.js      # 用户状态
│   ├── views/            # 页面组件
│   │   ├── login.vue
│   │   ├── layout.vue
│   │   └── ...
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── index.html           # HTML模板
├── package.json         # Node依赖
└── vite.config.js       # Vite配置
```

## 后端开发

### 创建新的API端点

#### 1. 定义 Pydantic Schema

```python
# schemas.py
from pydantic import BaseModel
from datetime import date

class ProjectCreate(BaseModel):
    project_name: str
    pi_id: int
    start_date: date
```

#### 2. 实现 CRUD 操作

```python
# crud/project.py
from sqlalchemy.orm import Session
from models import Project
from schemas import ProjectCreate

def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
```

#### 3. 创建路由

```python
# routers/project.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import project as crud_project
from schemas import ProjectCreate, ProjectResponse

router = APIRouter()

@router.post(\"/\", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return crud_project.create_project(db, project)
```

#### 4. 注册路由

```python
# main.py
from routers import project

app.include_router(project.router, prefix=\"/api/projects\", tags=[\"项目管理\"])
```

### 添加认证和权限

```python
from utils.security import get_current_user, require_admin

@router.post(\"/\")
def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),  # 需要登录
    db: Session = Depends(get_db)
):
    pass

@router.delete(\"/{id}\")
def delete_project(
    id: int,
    current_user: User = Depends(require_admin),  # 需要管理员
    db: Session = Depends(get_db)
):
    pass
```

### 添加审计日志

```python
from utils.audit import AuditLogger
from fastapi import Request

@router.post(\"/\")
def create_project(
    project: ProjectCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_project = crud_project.create_project(db, project)
    
    # 记录审计日志
    AuditLogger.log_create(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        module=\"project\",
        resource_type=\"项目\",
        resource_id=new_project.id,
        request=request,
        data={\"project_name\": project.project_name}
    )
    
    return new_project
```

### 错误处理

```python
from fastapi import HTTPException, status

@router.get(\"/{id}\")
def get_project(id: int, db: Session = Depends(get_db)):
    project = crud_project.get_project_by_id(db, id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=\"项目不存在\"
        )
    return project
```

## 前端开发

### 创建新页面

#### 1. 创建页面组件

```vue
<!-- views/project/list.vue -->
<template>
  <el-card>
    <template #header>
      <div class=\"card-header\">
        <span>项目列表</span>
        <el-button type=\"primary\" @click=\"handleAdd\">新增</el-button>
      </div>
    </template>
    
    <el-table :data=\"projects\" v-loading=\"loading\">
      <el-table-column prop=\"id\" label=\"ID\" />
      <el-table-column prop=\"project_name\" label=\"项目名称\" />
      <el-table-column label=\"操作\" width=\"180\">
        <template #default=\"{ row }\">
          <el-button size=\"small\" @click=\"handleEdit(row)\">编辑</el-button>
          <el-button size=\"small\" type=\"danger\" @click=\"handleDelete(row)\">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjectList } from '@/services/project'

const projects = ref([])
const loading = ref(false)

const loadProjects = async () => {
  loading.value = true
  try {
    const res = await getProjectList()
    projects.value = res
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProjects()
})
</script>
```

#### 2. 添加API服务

```javascript
// services/project.js
import request from './request'

export const getProjectList = (params) => {
  return request({
    url: '/projects/',
    method: 'get',
    params
  })
}

export const createProject = (data) => {
  return request({
    url: '/projects/',
    method: 'post',
    data
  })
}
```

#### 3. 配置路由

```javascript
// router/index.js
{
  path: '/project',
  name: 'Project',
  component: () => import('@/views/project/list.vue'),
  meta: { title: '项目管理', requiresAuth: true }
}
```

### 状态管理（Pinia）

```javascript
// store/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const clearToken = () => {
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    setToken,
    clearToken
  }
})
```

## API设计规范

### RESTful API规范

| HTTP方法 | 路径 | 说明 |
|---------|------|------|
| GET | /api/projects | 获取项目列表 |
| GET | /api/projects/{id} | 获取单个项目 |
| POST | /api/projects | 创建项目 |
| PUT | /api/projects/{id} | 更新项目 |
| DELETE | /api/projects/{id} | 删除项目 |

### 请求响应格式

#### 成功响应

```json
{
  \"id\": 1,
  \"project_name\": \"人工智能研究\",
  \"status\": \"进行中\",
  \"created_at\": \"2023-12-01T10:00:00\"
}
```

#### 错误响应

```json
{
  \"detail\": \"项目不存在\"
}
```

### 分页参数

```python
@router.get(\"/\")
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    pass
```

## 测试指南

### 后端单元测试

```python
# tests/test_project.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_project():
    response = client.post(
        \"/api/projects/\",
        json={
            \"project_name\": \"测试项目\",
            \"pi_id\": 1
        },
        headers={\"Authorization\": \"Bearer test_token\"}
    )
    assert response.status_code == 200
    assert response.json()[\"project_name\"] == \"测试项目\"

def test_get_project():
    response = client.get(\"/api/projects/1\")
    assert response.status_code == 200
```

### 前端单元测试

```javascript
// tests/project.spec.js
import { mount } from '@vue/test-utils'
import ProjectList from '@/views/project/list.vue'

describe('ProjectList.vue', () => {
  it('renders project list', () => {
    const wrapper = mount(ProjectList)
    expect(wrapper.find('.card-header').text()).toBe('项目列表')
  })
})
```

### 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## Git工作流

### 分支管理

- `master`: 主分支，生产环境代码
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支
- `hotfix/*`: 紧急修复分支

### 提交规范

遵循 **Conventional Commits** 规范：

```bash
# 功能
git commit -m \"feat: 添加项目导出功能\"

# 修复
git commit -m \"fix: 修复用户登录失败问题\"

# 文档
git commit -m \"docs: 更新API文档\"

# 样式
git commit -m \"style: 优化项目列表页面布局\"

# 重构
git commit -m \"refactor: 重构项目CRUD代码\"

# 性能
git commit -m \"perf: 优化数据库查询性能\"

# 测试
git commit -m \"test: 添加项目模块单元测试\"
```

### 开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/project-export

# 2. 开发和提交
git add .
git commit -m \"feat: 添加项目导出功能\"

# 3. 推送到远程
git push origin feature/project-export

# 4. 创建Pull Request
# 在GitHub上创建PR，等待代码审查

# 5. 合并到develop分支
# 审查通过后合并

# 6. 删除功能分支
git branch -d feature/project-export
```

## 代码审查清单

### 后端代码审查

- [ ] 是否添加类型注解
- [ ] 是否添加文档字符串
- [ ] 是否处理异常情况
- [ ] 是否添加审计日志
- [ ] 是否验证权限
- [ ] 是否验证输入参数
- [ ] 是否使用事务
- [ ] SQL查询是否优化

### 前端代码审查

- [ ] 组件是否正确拆分
- [ ] 是否处理加载状态
- [ ] 是否处理错误状态
- [ ] 是否添加表单验证
- [ ] 是否使用计算属性
- [ ] 是否避免内存泄漏
- [ ] 是否优化性能
- [ ] 样式是否使用scoped

## 调试技巧

### 后端调试

```python
# 使用 logging
import logging

logger = logging.getLogger(__name__)
logger.info(f\"Creating project: {project.project_name}\")

# 使用 pdb
import pdb; pdb.set_trace()

# 使用 FastAPI 日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 前端调试

```javascript
// Vue Devtools
// 安装浏览器插件

// console.log
console.log('User info:', userInfo.value)

// debugger
debugger

// Vue warn
import { warn } from 'vue'
warn('Something went wrong')
```

## 性能优化

### 后端优化

- 使用数据库索引
- 使用 `select_related` 和 `joinedload` 减少查询
- 使用缓存（Redis）
- 使用异步操作
- 优化SQL查询

### 前端优化

- 使用 `v-if` 而非 `v-show`（条件渲染）
- 使用 `computed` 缓存计算结果
- 使用虚拟滚动（大列表）
- 使用懒加载（路由、组件）
- 优化打包体积

## 常用命令

### 后端

```bash
# 格式化代码
black .

# 检查代码规范
flake8 .

# 类型检查
mypy .

# 运行测试
pytest

# 生成测试覆盖率报告
pytest --cov=.
```

### 前端

```bash
# 格式化代码
npm run format

# 检查代码规范
npm run lint

# 修复代码问题
npm run lint:fix

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 下一步

- 查看 [安全规范](SECURITY.md) 了解安全开发实践
- 查看 [部署指南](DEPLOYMENT.md) 了解部署流程
- 查看 [数据库设计](DATABASE.md) 了解数据模型
