# 部署指南

本文档提供科研管理系统的完整部署步骤，适用于 Windows、Linux 和 macOS 系统。

## 📋 目录

- [环境准备](#环境准备)
- [Windows 部署](#windows-部署)
- [Linux 部署](#linux-部署)
- [Docker 部署](#docker-部署)
- [生产环境部署](#生产环境部署)
- [常见问题](#常见问题)

## 环境准备

### 1. 安装 MySQL 8.0+

#### Windows
1. 下载MySQL安装包: https://dev.mysql.com/downloads/mysql/
2. 运行安装程序，选择"Server only"
3. 设置root密码（建议: `root`）
4. 启动MySQL服务

验证安装：
```bash
mysql --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### 2. 安装 Python 3.13+

#### Windows
1. 下载Python: https://www.python.org/downloads/
2. 运行安装程序，**勾选"Add Python to PATH"**
3. 完成安装

验证安装：
```bash
python --version
pip --version
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt install python3.13 python3-pip

# CentOS/RHEL
sudo yum install python313 python3-pip
```

### 3. 安装 Node.js 18.x+

#### Windows
1. 下载Node.js: https://nodejs.org/
2. 运行安装程序（LTS版本）
3. 完成安装

验证安装：
```bash
node --version
npm --version
```

#### Linux
```bash
# 使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

## Windows 部署

### 方式一：一键启动（推荐）

1. **克隆或下载项目**
```bash
git clone https://github.com/tolqj/research_management.git
cd research_management
```

2. **运行一键启动脚本**
```bash
start_all.bat
```

脚本会自动完成以下步骤：
- ✅ 检查MySQL服务
- ✅ 创建数据库
- ✅ 初始化表结构
- ✅ 安装后端依赖
- ✅ 启动后端服务(8000端口)
- ✅ 安装前端依赖
- ✅ 启动前端服务(5173端口)

3. **访问系统**
- 前端: http://localhost:5173
- 后端API: http://localhost:8000/api/docs

### 方式二：手动部署

#### 步骤1: 创建数据库

```bash
# 进入MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE research_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
EXIT;
```

#### 步骤2: 配置后端

```bash
cd backend

# 修改数据库配置（如需要）
# 编辑 database.py 文件，修改以下内容：
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "root"
# MYSQL_HOST = "localhost"
# MYSQL_PORT = "3306"

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库表结构
python setup_database.py

# （可选）添加测试数据
python add_test_data.py
```

#### 步骤3: 启动后端

```bash
# 在 backend 目录下
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

后端启动成功后，访问 http://localhost:8000/api/docs 查看API文档。

#### 步骤4: 配置前端

```bash
cd frontend

# 安装Node依赖
npm install

# 或使用 cnpm（国内推荐）
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

#### 步骤5: 启动前端

```bash
# 在 frontend 目录下
npm run dev
```

前端启动成功后，访问 http://localhost:5173

## Linux 部署

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server python3.13 python3-pip nodejs npm git

# CentOS/RHEL
sudo yum install mysql-server python313 python3-pip nodejs npm git
```

### 2. 克隆项目

```bash
git clone https://github.com/tolqj/research_management.git
cd research_management
```

### 3. 创建数据库

```bash
sudo mysql -u root -p
```

```sql
CREATE DATABASE research_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rms_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON research_management_system.* TO 'rms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. 部署后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 修改数据库配置
vi database.py
# 修改 MYSQL_USER、MYSQL_PASSWORD 等配置

# 初始化数据库
python setup_database.py

# 启动后端（使用 screen 或 tmux 保持后台运行）
screen -S rms-backend
python main.py
# 按 Ctrl+A+D 分离会话
```

### 5. 部署前端

```bash
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 使用 nginx 部署（推荐）
sudo apt install nginx
sudo cp -r dist/* /var/www/html/
sudo systemctl restart nginx
```

## Docker 部署

### 1. 创建 Dockerfile（后端）

在 `backend` 目录创建 `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

### 2. 创建 Dockerfile（前端）

在 `frontend` 目录创建 `Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. 创建 docker-compose.yml

在项目根目录创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: research_management_system
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: root

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
```

### 4. 启动服务

```bash
docker-compose up -d
```

访问 http://localhost

## 生产环境部署

### 1. 使用 Gunicorn（后端）

```bash
# 安装 gunicorn
pip install gunicorn

# 启动（4个工作进程）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 使用 Nginx（前端）

#### nginx.conf 配置

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 前端静态文件
    location / {
        root /var/www/html/rms-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 3. 使用 Systemd 管理服务

#### 创建后端服务文件

`/etc/systemd/system/rms-backend.service`:

```ini
[Unit]
Description=Research Management System Backend
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/research_management/backend
Environment="PATH=/opt/research_management/backend/venv/bin"
ExecStart=/opt/research_management/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable rms-backend
sudo systemctl start rms-backend
sudo systemctl status rms-backend
```

## 常见问题

### 1. MySQL 连接失败

**错误**: `Can't connect to MySQL server on 'localhost'`

**解决方案**:
```bash
# 检查MySQL服务状态
# Windows
net start MySQL80

# Linux
sudo systemctl status mysql

# 检查端口占用
netstat -an | findstr 3306
```

### 2. 端口被占用

**错误**: `Address already in use: ('0.0.0.0', 8000)`

**解决方案**:
```bash
# Windows - 查找占用端口的进程
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux - 查找并终止进程
lsof -i :8000
kill -9 <PID>
```

### 3. Python 依赖安装失败

**错误**: `pip install` 超时或失败

**解决方案**:
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. npm 依赖安装失败

**错误**: `npm install` 超时

**解决方案**:
```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 5. 数据库表不存在

**错误**: `Table 'research_management_system.users' doesn't exist`

**解决方案**:
```bash
# 重新运行数据库初始化脚本
cd backend
python setup_database.py
```

### 6. 跨域问题

**错误**: `CORS policy: No 'Access-Control-Allow-Origin'`

**解决方案**:
检查 `backend/main.py` 中的 CORS 配置：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 添加前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. 前端页面空白

**解决方案**:
1. 检查浏览器控制台错误
2. 确认后端服务已启动
3. 检查 `vite.config.js` 中的代理配置
4. 清除浏览器缓存

## 性能优化建议

### 后端优化
1. 使用数据库连接池
2. 启用 Redis 缓存
3. 使用 Gunicorn 多进程部署
4. 启用 Gzip 压缩

### 前端优化
1. 构建生产版本 `npm run build`
2. 启用 CDN 加速
3. 使用 Nginx 缓存静态资源
4. 启用 Gzip 压缩

### 数据库优化
1. 添加适当的索引
2. 定期备份数据
3. 优化慢查询
4. 使用主从复制（高可用）

## 安全建议

1. **修改默认密码**: 部署后立即修改管理员密码
2. **使用 HTTPS**: 生产环境启用SSL证书
3. **防火墙配置**: 只开放必要的端口
4. **定期更新**: 及时更新依赖包
5. **备份策略**: 定期备份数据库和代码

## 监控建议

1. **日志管理**: 使用 ELK Stack 或 Loki
2. **性能监控**: 使用 Prometheus + Grafana
3. **错误追踪**: 使用 Sentry
4. **服务健康检查**: 使用 `/api/health` 接口

## 下一步

- 查看 [开发指南](DEVELOPMENT.md) 了解开发规范
- 查看 [数据库设计](DATABASE.md) 了解数据结构
- 查看 [安全规范](SECURITY.md) 了解安全特性
