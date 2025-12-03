# 快速开始指南

本指南帮助您在5分钟内快速部署和运行科研管理系统。

## 🚀 5分钟快速部署

### 前置条件

确保已安装以下软件：
- ✅ Python 3.13+
- ✅ Node.js 18+
- ✅ MySQL 8.0+

### Windows 一键启动

1. **下载项目**
```bash
git clone https://github.com/tolqj/research_management.git
cd research_management
```

2. **运行启动脚本**
```bash
start_all.bat
```

3. **访问系统**
- 前端: http://localhost:5173
- 后端API: http://localhost:8000/api/docs

### Linux/Mac 快速启动

```bash
# 1. 克隆项目
git clone https://github.com/tolqj/research_management.git
cd research_management

# 2. 安装后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 初始化数据库
python setup_database.py

# 4. 启动后端
python main.py &

# 5. 安装前端依赖
cd ../frontend
npm install

# 6. 启动前端
npm run dev
```

## 📝 默认账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | Admin@123 | 拥有所有权限 |
| 普通教师 | teacher | Teacher@123 | 管理自己的项目 |
| 科研秘书 | secretary | Sec@2024 | 查看所有项目 |

## 🎯 主要功能

### 1. 登录系统
![登录页面](screenshots/login.png)

访问 http://localhost:5173 使用默认账号登录。

### 2. 工作台
登录后进入工作台，可以看到：
- 项目统计
- 论文统计
- 经费统计
- 成果统计

### 3. 项目管理
1. 点击左侧菜单「项目管理」
2. 点击「新增项目」按钮
3. 填写项目信息并提交

### 4. 论文管理
1. 点击左侧菜单「论文管理」
2. 点击「新增论文」按钮
3. 填写论文信息并提交

### 5. 个人信息
1. 点击右上角用户名
2. 选择「个人信息」
3. 修改个人资料或密码

## 🔧 常见问题

### Q1: MySQL连接失败怎么办？

**A**: 
1. 确认MySQL服务已启动
2. 检查 `backend/database.py` 中的数据库配置
3. 确认数据库已创建

```bash
# 手动创建数据库
mysql -u root -p
CREATE DATABASE research_management_system CHARACTER SET utf8mb4;
```

### Q2: 端口被占用怎么办？

**A**: 
修改配置文件中的端口号：
- 后端: 修改 `backend/main.py` 中的端口
- 前端: 修改 `frontend/vite.config.js` 中的端口

### Q3: 前端无法连接后端？

**A**: 
1. 确认后端服务已启动 (http://localhost:8000)
2. 检查 `frontend/vite.config.js` 中的代理配置
3. 检查防火墙设置

### Q4: 如何重置数据库？

**A**: 
```bash
cd backend
python setup_database.py  # 重新初始化数据库
```

### Q5: 如何添加测试数据？

**A**: 
```bash
cd backend
python add_test_data.py  # 添加测试数据
```

## 📚 进一步学习

- **完整部署**: 查看 [部署指南](DEPLOYMENT.md)
- **数据库设计**: 查看 [数据库文档](DATABASE.md)
- **开发指南**: 查看 [开发指南](DEVELOPMENT.md)
- **安全规范**: 查看 [安全文档](SECURITY.md)

## 💡 下一步

### 管理员

1. **修改默认密码**
   - 进入「个人信息」页面
   - 点击「修改密码」
   - 输入新密码并保存

2. **创建用户**
   - 进入「系统管理」→「用户管理」
   - 点击「新增用户」
   - 填写用户信息并保存

3. **配置系统**
   - 检查数据库连接配置
   - 配置邮件服务（可选）
   - 配置备份策略

### 普通用户

1. **完善个人信息**
   - 填写职称、学院等信息
   - 添加研究方向

2. **创建项目**
   - 进入「项目管理」
   - 创建第一个科研项目

3. **记录成果**
   - 录入论文信息
   - 记录经费支出
   - 添加科研成果

## 🎉 开始使用

现在您可以开始使用科研管理系统了！

如有问题，请查看详细文档或提交Issue：
https://github.com/tolqj/research_management/issues
