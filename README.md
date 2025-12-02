# 科研管理系统 (Research Management System)

## 📖 项目简介

科研管理系统（RMS）是一个功能完善的科研项目管理平台，支持项目、论文、经费、成果等全流程管理，提供数据统计和可视化功能。

## ✨ 主要功能

- **用户管理**：支持多角色（管理员、科研秘书、普通教师）
- **项目管理**：项目申报、审批、执行、结题全流程管理
- **论文管理**：论文录入、检索、统计分析（支持JCR分区、中科院分区）
- **经费管理**：经费支出登记、预算对比、统计分析
- **成果管理**：专利、奖项、著作、软件著作权管理
- **统计分析**：多维度数据统计、ECharts可视化展示
- **数据导出**：Excel批量导入导出

## 🔧 技术栈

### 后端
- Python 3.10+
- FastAPI
- MySQL + PyMySQL
- SQLAlchemy
- JWT认证（python-jose）
- Excel处理（openpyxl）

### 前端
- Vue 3 + Vite
- Pinia状态管理
- Vue Router
- Element Plus UI
- ECharts图表
- Axios

## 📁 项目结构

```
科研管理系统/
├── backend/                 # 后端目录
│   ├── main.py             # 主应用入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic模式
│   ├── crud/               # CRUD操作
│   ├── routers/            # 路由模块
│   ├── utils/              # 工具函数
│   ├── setup_database.py  # 数据库初始化
│   └── requirements.txt    # Python依赖
│
├── frontend/               # 前端目录
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── router/        # 路由配置
│   │   ├── services/      # API服务
│   │   └── store/         # 状态管理
│   ├── package.json       # 前端依赖
│   └── vite.config.js     # Vite配置
│
├── start_all.bat          # 一键启动脚本
└── README.md              # 项目说明
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0+

### 2. 安装依赖

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 前端依赖
```bash
cd frontend
npm install
```

### 3. 数据库初始化

**方式一：使用脚本（推荐）**
```bash
cd backend
setup_database.bat
```

**方式二：手动初始化**
```bash
cd backend
python setup_database.py
```

### 4. 启动项目

**方式一：一键启动（推荐）**
```bash
start_all.bat
```

**方式二：分别启动**

启动后端：
```bash
cd backend
python main.py
```

启动前端：
```bash
cd frontend
npm run dev
```

### 5. 访问系统

- **前端地址**: http://localhost:5173
- **后端地址**: http://localhost:8000
- **API文档**: http://localhost:8000/api/docs

### 6. 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 科研秘书 | secretary | 123456 |
| 教师 | teacher | 123456 |

## 📝 数据库配置

默认配置（`backend/database.py`）：
```python
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "research_management_system"
```

如需修改，请编辑 `backend/database.py` 文件。

## 📦 生产部署

### 1. 构建前端
```bash
cd frontend
npm run build
```

### 2. 后端生产运行
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Nginx配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 安全建议

生产环境部署时，请务必：

1. 修改 `backend/utils/security.py` 中的 `SECRET_KEY`
2. 使用强密码并修改所有默认账号密码
3. 配置HTTPS证书
4. 限制数据库访问权限
5. 定期备份数据库

## 📄 API文档

启动后端服务后，访问以下地址查看完整API文档：

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📞 技术支持

如有问题，请提交Issue或联系开发团队。

## 📜 开源协议

MIT License

---

**祝您使用愉快！** 🎉
