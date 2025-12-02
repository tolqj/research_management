# 科研管理系统 (Research Management System)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.3-brightgreen.svg)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 项目简介

科研管理系统是一个面向高校和科研机构的综合性管理平台，提供项目管理、论文管理、经费管理、成果管理等核心功能。系统采用前后端分离架构，符合**等保二级安全标准**。

### 核心特性

- 🎯 **项目管理** - 科研项目全生命周期管理
- 📄 **论文管理** - 论文发表记录与统计分析
- 💰 **经费管理** - 科研经费支出跟踪
- 🏆 **成果管理** - 专利、奖项、著作等成果记录
- 📊 **统计分析** - 多维度数据可视化展示
- 🔐 **等保二级** - 完整的安全审计与访问控制
- 👥 **权限管理** - 基于角色的访问控制(RBAC)

## 🏗️ 技术架构

### 后端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.13 | 编程语言 |
| FastAPI | 0.100+ | Web框架 |
| SQLAlchemy | 1.4.51 | ORM框架 |
| Pydantic | 2.0+ | 数据验证 |
| MySQL | 8.0+ | 数据库 |
| PyMySQL | 1.1.0 | MySQL驱动 |
| python-jose | 3.3.0 | JWT认证 |
| passlib | 1.7.4 | 密码加密 |
| openpyxl | 3.1.2 | Excel导出 |

### 前端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue.js | 3.3.4 | 前端框架 |
| Vue Router | 4.2.4 | 路由管理 |
| Pinia | 2.1.6 | 状态管理 |
| Element Plus | 2.3.14 | UI组件库 |
| Axios | 1.5.0 | HTTP客户端 |
| ECharts | 5.4.3 | 数据可视化 |
| Vite | 4.4.9 | 构建工具 |

## 📁 项目结构

```
科研管理系统/
├── backend/                    # 后端目录
│   ├── crud/                   # 数据库CRUD操作
│   │   ├── achievement.py      # 成果管理
│   │   ├── fund.py            # 经费管理
│   │   ├── paper.py           # 论文管理
│   │   ├── project.py         # 项目管理
│   │   └── user.py            # 用户管理
│   ├── routers/               # 路由模块
│   │   ├── achievement.py     # 成果API
│   │   ├── auth.py            # 认证API
│   │   ├── fund.py            # 经费API
│   │   ├── paper.py           # 论文API
│   │   ├── project.py         # 项目API
│   │   ├── statistics.py      # 统计API
│   │   └── user.py            # 用户API
│   ├── utils/                 # 工具模块
│   │   ├── audit.py           # 审计日志
│   │   ├── password_policy.py # 密码策略
│   │   └── security.py        # 安全工具
│   ├── database.py            # 数据库配置
│   ├── main.py               # 应用入口
│   ├── models.py             # 数据模型
│   ├── schemas.py            # Pydantic schemas
│   ├── requirements.txt      # Python依赖
│   ├── setup_database.py     # 数据库初始化
│   └── add_test_data.py      # 测试数据生成
├── frontend/                  # 前端目录
│   ├── src/
│   │   ├── assets/           # 静态资源
│   │   ├── router/           # 路由配置
│   │   ├── services/         # API服务
│   │   ├── store/            # 状态管理
│   │   ├── views/            # 页面组件
│   │   │   ├── achievement/  # 成果管理
│   │   │   ├── dashboard/    # 工作台
│   │   │   ├── fund/         # 经费管理
│   │   │   ├── paper/        # 论文管理
│   │   │   ├── project/      # 项目管理
│   │   │   ├── system/       # 系统管理
│   │   │   ├── layout.vue    # 布局组件
│   │   │   └── login.vue     # 登录页
│   │   ├── App.vue           # 根组件
│   │   └── main.js           # 入口文件
│   ├── index.html            # HTML模板
│   ├── package.json          # Node依赖
│   └── vite.config.js        # Vite配置
├── docs/                     # 文档目录
├── .gitignore               # Git忽略配置
├── README.md                # 项目说明
└── start_all.bat            # 一键启动脚本

```

## 🚀 快速开始

### 环境要求

- **Python**: 3.13 或更高版本
- **Node.js**: 18.x 或更高版本
- **MySQL**: 8.0 或更高版本
- **操作系统**: Windows 10/11, Linux, macOS

### 一键启动（Windows）

```bash
# 双击运行一键启动脚本
start_all.bat
```

该脚本会自动：
1. 检查MySQL服务状态
2. 创建数据库和表结构
3. 安装后端依赖
4. 启动后端服务(8000端口)
5. 安装前端依赖
6. 启动前端服务(5173端口)

启动成功后访问：
- **前端地址**: http://localhost:5173
- **后端API**: http://localhost:8000/api/docs

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | Admin@123 |
| 普通教师 | teacher | Teacher@123 |
| 科研秘书 | secretary | Sec@2024 |

## 📖 详细文档

- [部署指南](docs/DEPLOYMENT.md) - 完整的部署步骤说明
- [数据库设计](docs/DATABASE.md) - 数据库表结构和字段说明
- [API文档](http://localhost:8000/api/docs) - 在线Swagger文档
- [开发指南](docs/DEVELOPMENT.md) - 开发环境配置和规范
- [安全规范](docs/SECURITY.md) - 等保二级安全特性说明

## 🔐 安全特性（等保二级）

### 身份鉴别
- ✅ 密码复杂度要求（8位+大小写+数字+特殊字符）
- ✅ 密码定期更换提醒（90天）
- ✅ 登录失败锁定（5次/30分钟）
- ✅ 密码强度实时检测

### 访问控制
- ✅ 基于角色的访问控制(RBAC)
- ✅ 资源级权限验证
- ✅ 接口级权限控制

### 安全审计
- ✅ 完整的操作日志记录
- ✅ 登录日志（成功/失败）
- ✅ 数据变更审计
- ✅ 权限拒绝记录

### 数据完整性
- ✅ 数据库事务支持
- ✅ 外键约束
- ✅ 数据验证

## 🎯 功能模块

### 1. 项目管理
- 项目创建、编辑、删除
- 项目状态跟踪（草稿、进行中、已结题、已终止）
- 项目成员管理
- 项目预算管理
- 项目详情查看

### 2. 论文管理
- 论文信息录入
- JCR分区/中科院分区标注
- 影响因子记录
- 关联项目
- 论文导出

### 3. 经费管理
- 经费支出记录
- 支出类型分类
- 经费统计分析
- 关联项目

### 4. 成果管理
- 专利、奖项、著作、软著管理
- 成果类型分类
- 证书编号记录
- 成果导出

### 5. 统计分析
- 项目统计（按状态、学院、年份）
- 论文统计（按分区、影响因子）
- 经费统计（按类型、项目）
- 成果统计（按类型）
- 可视化图表展示

### 6. 用户管理
- 用户创建、编辑、删除（管理员）
- 个人信息管理
- 密码修改
- 角色权限管理

## 🔧 配置说明

### 后端配置

修改 `backend/database.py` 中的数据库连接信息：

```python
MYSQL_USER = "root"           # MySQL用户名
MYSQL_PASSWORD = "root"       # MySQL密码
MYSQL_HOST = "localhost"      # MySQL主机
MYSQL_PORT = "3306"          # MySQL端口
MYSQL_DATABASE = "research_management_system"  # 数据库名
```

### 前端配置

修改 `frontend/vite.config.js` 中的代理配置：

```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',  // 后端地址
    changeOrigin: true
  }
}
```

## 🐛 常见问题

### 1. MySQL连接失败

**问题**: `Can't connect to MySQL server`

**解决方案**:
- 确认MySQL服务已启动
- 检查数据库连接配置是否正确
- 确认数据库已创建

### 2. 端口被占用

**问题**: `Address already in use`

**解决方案**:
- 后端：修改 `main.py` 中的端口号
- 前端：修改 `vite.config.js` 中的端口号

### 3. 前端无法访问后端

**问题**: `Network Error`

**解决方案**:
- 确认后端服务已启动(http://localhost:8000)
- 检查 CORS 配置
- 检查防火墙设置

## 📊 系统截图

（待补充）

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

本项目采用 [MIT](LICENSE) 开源协议。

## 👥 联系方式

- 项目地址: https://github.com/tolqj/research_management
- 问题反馈: https://github.com/tolqj/research_management/issues

## 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
