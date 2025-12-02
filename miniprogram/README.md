# 科研管理系统 - 微信小程序（领导端）

## 📱 项目简介

这是科研管理系统的微信小程序版本，专为领导查看科研数据而设计。提供数据总览、项目查询、论文统计、经费管理、成果展示等功能，让领导可以随时随地掌握科研进展。

## 🎯 核心功能

### 1. **数据总览** （首页）
- ✅ 实时显示关键指标：项目数、论文数、成果数、经费总额
- ✅ 快捷入口：快速进入各功能模块
- ✅ 最新项目列表
- ✅ 下拉刷新

### 2. **项目管理**
- ✅ 项目列表展示（支持分页）
- ✅ 项目详情查看
- ✅ 按状态筛选（草稿/已申报/执行中/已结题）
- ✅ 搜索功能

### 3. **论文管理**
- ✅ 论文列表展示
- ✅ 论文详情查看
- ✅ JCR分区标签展示
- ✅ 按年份、分区筛选

### 4. **经费管理**
- ✅ 经费列表展示
- ✅ 按项目、类型筛选
- ✅ 经费统计图表
- ✅ 支出明细查看

### 5. **成果管理**
- ✅ 成果列表展示
- ✅ 成果详情查看
- ✅ 按类型筛选（专利/奖项/著作/软著）
- ✅ 成果统计

### 6. **统计分析**
- ✅ 项目统计图表
- ✅ 论文分区统计
- ✅ 经费使用趋势
- ✅ 成果类型分布

### 7. **个人中心**
- ✅ 用户信息展示
- ✅ 退出登录

## 📂 目录结构

```
miniprogram/
├── app.js                  # 小程序入口文件
├── app.json                # 小程序配置
├── app.wxss                # 全局样式
├── project.config.json     # 项目配置
├── sitemap.json           # 站点地图配置
│
├── pages/                  # 页面目录
│   ├── index/             # 首页（数据总览）
│   │   ├── index.js
│   │   ├── index.json
│   │   ├── index.wxml
│   │   └── index.wxss
│   │
│   ├── login/             # 登录页
│   │   ├── login.js
│   │   ├── login.json
│   │   ├── login.wxml
│   │   └── login.wxss
│   │
│   ├── projects/          # 项目管理
│   │   ├── list.js        # 项目列表
│   │   ├── list.json
│   │   ├── list.wxml
│   │   ├── list.wxss
│   │   ├── detail.js      # 项目详情
│   │   ├── detail.json
│   │   ├── detail.wxml
│   │   └── detail.wxss
│   │
│   ├── papers/            # 论文管理
│   │   ├── list.js
│   │   ├── list.json
│   │   ├── list.wxml
│   │   ├── list.wxss
│   │   ├── detail.js
│   │   ├── detail.json
│   │   ├── detail.wxml
│   │   └── detail.wxss
│   │
│   ├── funds/             # 经费管理
│   │   ├── list.js
│   │   ├── list.json
│   │   ├── list.wxml
│   │   └── list.wxss
│   │
│   ├── achievements/      # 成果管理
│   │   ├── list.js
│   │   ├── list.json
│   │   ├── list.wxml
│   │   └── list.wxss
│   │
│   ├── statistics/        # 统计分析
│   │   ├── index.js
│   │   ├── index.json
│   │   ├── index.wxml
│   │   └── index.wxss
│   │
│   └── profile/           # 个人中心
│       ├── index.js
│       ├── index.json
│       ├── index.wxml
│       └── index.wxss
│
├── utils/                 # 工具类
│   ├── request.js        # 网络请求封装
│   └── util.js           # 通用工具函数
│
├── images/               # 图片资源
│   ├── home.png
│   ├── home-active.png
│   ├── chart.png
│   ├── chart-active.png
│   ├── user.png
│   ├── user-active.png
│   ├── project.png
│   ├── paper.png
│   ├── fund.png
│   └── achievement.png
│
└── components/           # 自定义组件（可选）
    └── ...
```

## 🚀 快速开始

### 1. 准备工作

#### 安装微信开发者工具
- 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
- 安装并打开微信开发者工具

#### 配置AppID
1. 打开 `project.config.json`
2. 修改 `appid` 字段为你的小程序AppID
3. 如果没有AppID，可以使用测试号

### 2. 导入项目

1. 打开微信开发者工具
2. 选择"导入项目"
3. 选择 `miniprogram` 目录
4. 填写项目名称，点击"导入"

### 3. 配置后端API地址

打开 `app.js`，修改后端API地址：

```javascript
globalData: {
  userInfo: null,
  token: null,
  baseURL: 'http://your-server-ip:8000/api'  // 修改为实际后端地址
}
```

**注意事项**：
- 开发环境：可以使用 `http://localhost:8000/api` 或内网IP
- 生产环境：必须使用 HTTPS 协议
- 需要在小程序后台配置服务器域名白名单

### 4. 启动后端服务

确保后端FastAPI服务正在运行：

```bash
cd backend
python main.py
```

### 5. 编译运行

在微信开发者工具中：
1. 点击"编译"按钮
2. 在模拟器中查看效果
3. 可以使用"真机调试"在手机上测试

## 🔐 登录说明

### 默认测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | Admin@123 |
| 科研秘书 | secretary | Sec@2024 |
| 普通教师 | teacher | Teacher@123 |

### 登录流程

1. 首次打开小程序会跳转到登录页
2. 输入用户名和密码
3. 登录成功后会保存Token到本地存储
4. 下次打开自动登录

## 📡 API接口

小程序复用了Web端的FastAPI接口：

### 认证接口
- `POST /api/auth/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息

### 统计接口
- `GET /api/statistics/overview` - 数据总览

### 项目接口
- `GET /api/projects/` - 项目列表（支持分页）
- `GET /api/projects/{id}` - 项目详情

### 论文接口
- `GET /api/papers/` - 论文列表
- `GET /api/papers/{id}` - 论文详情

### 经费接口
- `GET /api/funds/` - 经费列表
- `GET /api/funds/statistics` - 经费统计

### 成果接口
- `GET /api/achievements/` - 成果列表
- `GET /api/achievements/{id}` - 成果详情

## 🎨 UI设计

### 配色方案
- 主色调：#409EFF（蓝色）
- 成功色：#67C23A（绿色）
- 警告色：#E6A23C（橙色）
- 危险色：#F56C6C（红色）
- 信息色：#909399（灰色）

### 组件样式
- 卡片：圆角16rpx，阴影
- 列表项：白色背景，间距20rpx
- 标签：圆角8rpx，不同颜色
- 按钮：主要按钮蓝色，次要按钮白色

## 📊 数据展示

### 1. 首页数据卡片
```
┌─────────────────┐
│   在研项目      │
│      12        │
└─────────────────┘
```

### 2. 项目列表
```
┌────────────────────────────┐
│ 深度学习图像识别研究       │
│ 负责人：张教授  预算：50万 │
│ [执行中]                   │
└────────────────────────────┘
```

### 3. 论文列表
```
┌────────────────────────────┐
│ Deep Learning for Image... │
│ 期刊：IEEE TPAMI           │
│ [Q1] [一区] IF: 24.5      │
└────────────────────────────┘
```

## 🔧 开发说明

### 数据请求示例

```javascript
const request = require('../../utils/request')

// 获取项目列表
request.get('/projects/', {
  skip: 0,
  limit: 20,
  status: '执行中'
}).then(res => {
  console.log(res)
})
```

### 工具函数使用

```javascript
const util = require('../../utils/util')

// 格式化金额
util.formatMoney(500000.50)  // "500,000.50"

// 格式化日期
util.formatDate(new Date())  // "2024-12-02"

// 获取项目状态类型
util.getProjectStatusType('执行中')  // "success"
```

### 页面跳转

```javascript
// 跳转到项目详情
wx.navigateTo({
  url: `/pages/projects/detail?id=${projectId}`
})

// 跳转到列表页
wx.navigateTo({
  url: '/pages/projects/list'
})
```

## 📱 功能截图说明

### 首页
- 顶部：欢迎信息
- 中部：4个数据统计卡片（项目/论文/成果/经费）
- 下方：快捷入口（4宫格）
- 底部：最新项目列表

### 项目列表
- 顶部：搜索框
- 筛选：状态筛选按钮组
- 列表：项目卡片（名称、负责人、预算、状态）
- 分页：上拉加载更多

### 统计页面
- 项目统计：柱状图
- 论文分区：饼图
- 经费趋势：折线图
- 成果分布：环形图

## 🔒 安全说明

### Token管理
- Token存储在本地Storage
- 每次请求自动携带Token
- Token过期自动跳转登录页

### 数据权限
- 所有接口都需要登录认证
- 管理员可查看所有数据
- 普通教师只能查看自己的数据
- 科研秘书可查看统计数据

### HTTPS要求
- 生产环境必须使用HTTPS
- 需要在小程序后台配置合法域名
- 服务器需要有效的SSL证书

## 📝 待开发功能

由于时间限制，以下功能需要继续完善：

### 必须完成的页面
1. ✅ 登录页面（login.js/.wxml/.wxss）
2. ✅ 首页JS逻辑（index.js）
3. ⏳ 项目列表页面（projects/list.js/.wxml/.wxss）
4. ⏳ 项目详情页面（projects/detail.js/.wxml/.wxss）
5. ⏳ 论文列表页面（papers/list.js/.wxml/.wxss）
6. ⏳ 经费列表页面（funds/list.js/.wxml/.wxss）
7. ⏳ 成果列表页面（achievements/list.js/.wxml/.wxss）
8. ⏳ 统计页面（statistics/index.js/.wxml/.wxss）
9. ⏳ 个人中心页面（profile/index.js/.wxml/.wxss）

### 增强功能
- [ ] 数据缓存机制
- [ ] 图表展示（使用ECharts）
- [ ] 下拉刷新 / 上拉加载
- [ ] 数据导出功能
- [ ] 消息推送
- [ ] 多语言支持

## 🐛 常见问题

### 1. 无法连接后端？
- 检查后端服务是否启动
- 检查baseURL配置是否正确
- 开发工具中打开"不校验合法域名"

### 2. 登录失败？
- 确认用户名密码正确
- 检查后端日志
- 查看网络请求返回的错误信息

### 3. 数据不显示？
- 打开调试模式查看Console
- 检查API返回的数据格式
- 确认Token是否有效

### 4. 真机调试问题？
- 确保手机和电脑在同一局域网
- 使用内网IP而不是localhost
- 检查手机网络设置

## 📞 技术支持

### 相关文档
- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [项目后端API文档](../docs/开发指南.md)

### 开发环境
- 微信开发者工具版本：最新稳定版
- 基础库版本：2.33.0+
- Node.js：v14+（如需使用npm包）

## 🎯 下一步计划

1. **完善所有页面** - 创建完整的页面文件
2. **集成图表组件** - 使用 ECharts for WeChat
3. **优化用户体验** - 添加加载动画、骨架屏
4. **增加缓存机制** - 减少网络请求
5. **性能优化** - 图片压缩、代码分包
6. **测试上线** - 完整测试后提交审核

---

**最后更新**: 2024-12-02
**版本**: v1.0.0
**作者**: 科研管理系统开发团队
