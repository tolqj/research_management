# 数据库设计文档

本文档详细说明科研管理系统的数据库结构设计。

## 📊 数据库信息

- **数据库名称**: `research_management_system`
- **字符集**: `utf8mb4`
- **排序规则**: `utf8mb4_unicode_ci`
- **数据库引擎**: InnoDB
- **数据库版本**: MySQL 8.0+

## 📋 表结构概览

| 表名 | 说明 | 行数（估计） |
|------|------|-------------|
| users | 用户表 | 100-1000 |
| projects | 项目表 | 500-5000 |
| papers | 论文表 | 1000-10000 |
| funds | 经费表 | 2000-20000 |
| achievements | 成果表 | 500-5000 |
| operation_logs | 操作日志表 | 10000+ |

## 📝 详细表结构

### 1. users - 用户表

存储系统用户信息和安全相关字段（等保二级要求）。

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名（唯一）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希（bcrypt加密）',
    name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    role ENUM('管理员', '普通教师', '科研秘书') NOT NULL DEFAULT '普通教师' COMMENT '用户角色',
    title VARCHAR(50) COMMENT '职称（如：教授、副教授）',
    college VARCHAR(100) COMMENT '学院',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '电话号码',
    research_field TEXT COMMENT '研究方向',
    
    -- 等保二级安全字段
    password_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '密码最后更新时间',
    login_failures INT DEFAULT 0 COMMENT '登录失败次数',
    locked_until DATETIME COMMENT '账号锁定截止时间',
    last_login_at DATETIME COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键，自增 |
| username | VARCHAR(50) | 是 | 登录用户名，唯一 |
| password_hash | VARCHAR(255) | 是 | bcrypt加密的密码 |
| name | VARCHAR(50) | 是 | 真实姓名 |
| role | ENUM | 是 | 管理员/普通教师/科研秘书 |
| title | VARCHAR(50) | 否 | 职称 |
| college | VARCHAR(100) | 否 | 所属学院 |
| email | VARCHAR(100) | 否 | 邮箱地址 |
| phone | VARCHAR(20) | 否 | 联系电话 |
| research_field | TEXT | 否 | 研究方向描述 |
| password_updated_at | DATETIME | 是 | 密码更新时间（90天提醒） |
| login_failures | INT | 是 | 登录失败计数（5次锁定） |
| locked_until | DATETIME | 否 | 锁定截止时间 |
| last_login_at | DATETIME | 否 | 最后登录时间 |
| last_login_ip | VARCHAR(50) | 否 | 最后登录IP |

**索引说明**:
- `idx_username`: 登录查询优化
- `idx_email`: 邮箱查询优化
- `idx_role`: 角色过滤优化

### 2. projects - 项目表

存储科研项目信息。

```sql
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '项目ID',
    project_name VARCHAR(200) NOT NULL COMMENT '项目名称',
    pi_id INT NOT NULL COMMENT '负责人ID',
    pi_name VARCHAR(50) NOT NULL COMMENT '负责人姓名',
    members TEXT COMMENT '项目成员（JSON格式）',
    project_type VARCHAR(100) COMMENT '项目类型（如：国家级、省部级）',
    source VARCHAR(100) COMMENT '项目来源（如：国家自然科学基金）',
    budget_total DECIMAL(15,2) DEFAULT 0.00 COMMENT '总预算（元）',
    start_date DATE COMMENT '开始日期',
    end_date DATE COMMENT '结束日期',
    status ENUM('草稿', '进行中', '已结题', '已终止') DEFAULT '草稿' COMMENT '项目状态',
    description TEXT COMMENT '项目描述',
    objectives TEXT COMMENT '研究目标',
    attachments TEXT COMMENT '附件列表（JSON格式）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (pi_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_pi_id (pi_id),
    INDEX idx_status (status),
    INDEX idx_project_type (project_type),
    INDEX idx_start_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键 |
| project_name | VARCHAR(200) | 是 | 项目全称 |
| pi_id | INT | 是 | 负责人用户ID（外键） |
| pi_name | VARCHAR(50) | 是 | 负责人姓名（冗余字段，提高查询效率） |
| members | TEXT | 否 | 项目成员JSON数组 |
| project_type | VARCHAR(100) | 否 | 项目级别类型 |
| source | VARCHAR(100) | 否 | 资助来源 |
| budget_total | DECIMAL(15,2) | 否 | 总预算，精确到分 |
| start_date | DATE | 否 | 项目开始日期 |
| end_date | DATE | 否 | 项目结束日期 |
| status | ENUM | 是 | 当前状态 |
| description | TEXT | 否 | 详细描述 |
| objectives | TEXT | 否 | 研究目标和内容 |
| attachments | TEXT | 否 | 附件信息JSON数组 |

**约束说明**:
- `pi_id` 外键关联 `users.id`，删除限制
- 项目名称不能为空
- 预算金额默认为0

### 3. papers - 论文表

存储发表论文信息。

```sql
CREATE TABLE papers (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '论文ID',
    title VARCHAR(300) NOT NULL COMMENT '论文标题',
    authors VARCHAR(500) NOT NULL COMMENT '作者列表',
    journal VARCHAR(200) COMMENT '期刊名称',
    publication_date DATE COMMENT '发表日期',
    doi VARCHAR(100) COMMENT 'DOI号',
    jcr_zone VARCHAR(10) COMMENT 'JCR分区（Q1/Q2/Q3/Q4）',
    cas_zone VARCHAR(10) COMMENT '中科院分区（1区/2区/3区/4区）',
    impact_factor DECIMAL(6,3) COMMENT '影响因子',
    project_id INT COMMENT '关联项目ID',
    creator_id INT NOT NULL COMMENT '录入人ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_creator_id (creator_id),
    INDEX idx_project_id (project_id),
    INDEX idx_publication_date (publication_date),
    INDEX idx_jcr_zone (jcr_zone),
    INDEX idx_cas_zone (cas_zone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论文表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键 |
| title | VARCHAR(300) | 是 | 论文完整标题 |
| authors | VARCHAR(500) | 是 | 所有作者，逗号分隔 |
| journal | VARCHAR(200) | 否 | 发表期刊名称 |
| publication_date | DATE | 否 | 正式发表日期 |
| doi | VARCHAR(100) | 否 | 数字对象标识符 |
| jcr_zone | VARCHAR(10) | 否 | JCR分区 |
| cas_zone | VARCHAR(10) | 否 | 中科院分区 |
| impact_factor | DECIMAL(6,3) | 否 | 影响因子，保留3位小数 |
| project_id | INT | 否 | 所属项目（可为空） |
| creator_id | INT | 是 | 录入人 |

### 4. funds - 经费表

存储科研经费支出记录。

```sql
CREATE TABLE funds (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '经费ID',
    project_id INT NOT NULL COMMENT '项目ID',
    expense_type VARCHAR(100) NOT NULL COMMENT '支出类型（如：设备费、差旅费）',
    amount DECIMAL(15,2) NOT NULL COMMENT '金额（元）',
    expense_date DATE NOT NULL COMMENT '支出日期',
    handler VARCHAR(50) COMMENT '经办人',
    notes TEXT COMMENT '备注说明',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_expense_date (expense_date),
    INDEX idx_expense_type (expense_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='经费表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键 |
| project_id | INT | 是 | 所属项目ID |
| expense_type | VARCHAR(100) | 是 | 支出类别 |
| amount | DECIMAL(15,2) | 是 | 支出金额，必须>0 |
| expense_date | DATE | 是 | 支出发生日期 |
| handler | VARCHAR(50) | 否 | 经办人姓名 |
| notes | TEXT | 否 | 详细说明 |

**约束说明**:
- 级联删除：项目删除时，关联经费记录也删除
- 金额字段不能为负数

### 5. achievements - 成果表

存储各类科研成果信息。

```sql
CREATE TABLE achievements (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '成果ID',
    achievement_type ENUM('专利', '奖项', '著作', '软著') NOT NULL COMMENT '成果类型',
    title VARCHAR(200) NOT NULL COMMENT '成果名称',
    owner VARCHAR(100) NOT NULL COMMENT '成果所有人',
    members VARCHAR(500) COMMENT '参与人员',
    completion_date DATE COMMENT '完成日期',
    certificate_no VARCHAR(100) COMMENT '证书编号',
    description TEXT COMMENT '成果描述',
    attachments TEXT COMMENT '附件列表（JSON格式）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_achievement_type (achievement_type),
    INDEX idx_completion_date (completion_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成果表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键 |
| achievement_type | ENUM | 是 | 成果分类 |
| title | VARCHAR(200) | 是 | 成果名称 |
| owner | VARCHAR(100) | 是 | 主要完成人 |
| members | VARCHAR(500) | 否 | 其他参与人 |
| completion_date | DATE | 否 | 完成日期 |
| certificate_no | VARCHAR(100) | 否 | 证书编号 |
| description | TEXT | 否 | 详细说明 |
| attachments | TEXT | 否 | 附件JSON数组 |

### 6. operation_logs - 操作日志表

存储系统操作审计日志（等保二级要求）。

```sql
CREATE TABLE operation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id INT COMMENT '操作用户ID（可为空，如登录失败）',
    username VARCHAR(50) COMMENT '操作用户名',
    operation VARCHAR(100) NOT NULL COMMENT '操作名称（如：创建项目、删除用户）',
    module VARCHAR(50) NOT NULL COMMENT '模块名称（如：project、user）',
    method VARCHAR(10) COMMENT 'HTTP方法（GET/POST/PUT/DELETE）',
    path VARCHAR(200) COMMENT '请求路径',
    details TEXT COMMENT '操作详情（JSON格式）',
    ip_address VARCHAR(50) COMMENT '操作IP地址',
    user_agent VARCHAR(500) COMMENT '用户代理信息',
    status VARCHAR(20) DEFAULT 'SUCCESS' COMMENT '操作状态（SUCCESS/FAILED）',
    error_msg TEXT COMMENT '错误信息（失败时记录）',
    duration INT COMMENT '执行耗时（毫秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_module (module),
    INDEX idx_operation (operation),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT | 是 | 主键 |
| user_id | INT | 否 | 操作用户ID |
| username | VARCHAR(50) | 否 | 用户名 |
| operation | VARCHAR(100) | 是 | 操作类型 |
| module | VARCHAR(50) | 是 | 功能模块 |
| method | VARCHAR(10) | 否 | HTTP方法 |
| path | VARCHAR(200) | 否 | 请求路径 |
| details | TEXT | 否 | 详细信息JSON |
| ip_address | VARCHAR(50) | 否 | 客户端IP |
| user_agent | VARCHAR(500) | 否 | 浏览器信息 |
| status | VARCHAR(20) | 是 | 成功/失败状态 |
| error_msg | TEXT | 否 | 失败原因 |
| duration | INT | 否 | 执行时间（ms） |
| created_at | DATETIME | 是 | 记录时间 |

**索引说明**:
- 多字段索引优化审计查询
- `created_at` 索引支持时间范围查询

## 🔗 表关系图

```
users (用户表)
  ├─→ projects (项目表) [pi_id]
  ├─→ papers (论文表) [creator_id]
  └─→ operation_logs (日志表) [user_id]

projects (项目表)
  ├─→ papers (论文表) [project_id]
  └─→ funds (经费表) [project_id]

achievements (成果表) [独立表]

operation_logs (日志表) [独立表，记录所有操作]
```

## 📊 数据统计SQL

### 1. 项目统计

```sql
-- 按状态统计项目数
SELECT status, COUNT(*) as count
FROM projects
GROUP BY status;

-- 按学院统计项目数
SELECT pi_college, COUNT(*) as count
FROM projects
JOIN users ON projects.pi_id = users.id
GROUP BY users.college;

-- 按年份统计项目数
SELECT YEAR(start_date) as year, COUNT(*) as count
FROM projects
WHERE start_date IS NOT NULL
GROUP BY YEAR(start_date)
ORDER BY year DESC;
```

### 2. 论文统计

```sql
-- 按分区统计论文数
SELECT jcr_zone, COUNT(*) as count
FROM papers
WHERE jcr_zone IS NOT NULL
GROUP BY jcr_zone;

-- 统计高影响因子论文
SELECT COUNT(*) as count
FROM papers
WHERE impact_factor >= 5.0;
```

### 3. 经费统计

```sql
-- 按支出类型统计总金额
SELECT expense_type, SUM(amount) as total
FROM funds
GROUP BY expense_type;

-- 按项目统计经费支出
SELECT p.project_name, SUM(f.amount) as total
FROM funds f
JOIN projects p ON f.project_id = p.id
GROUP BY p.id, p.project_name;
```

### 4. 成果统计

```sql
-- 按类型统计成果数
SELECT achievement_type, COUNT(*) as count
FROM achievements
GROUP BY achievement_type;
```

## 🔧 维护SQL

### 1. 清理过期日志

```sql
-- 删除6个月前的操作日志
DELETE FROM operation_logs
WHERE created_at < DATE_SUB(NOW(), INTERVAL 6 MONTH);
```

### 2. 重置登录失败次数

```sql
-- 重置所有用户的登录失败次数
UPDATE users
SET login_failures = 0, locked_until = NULL
WHERE login_failures > 0 OR locked_until IS NOT NULL;
```

### 3. 数据备份

```bash
# 备份整个数据库
mysqldump -u root -p research_management_system > backup_$(date +%Y%m%d).sql

# 仅备份数据（不含结构）
mysqldump -u root -p --no-create-info research_management_system > data_backup.sql

# 备份特定表
mysqldump -u root -p research_management_system users projects > backup_core_tables.sql
```

### 4. 数据恢复

```bash
# 恢复数据库
mysql -u root -p research_management_system < backup_20231202.sql
```

## 📈 性能优化建议

### 1. 索引优化

- ✅ 已添加外键索引
- ✅ 已添加状态字段索引
- ✅ 已添加日期字段索引
- ⚠️ 大数据量时考虑复合索引

### 2. 查询优化

```sql
-- 使用EXPLAIN分析查询
EXPLAIN SELECT * FROM projects WHERE status = '进行中';

-- 避免SELECT *，只查询需要的字段
SELECT id, project_name, status FROM projects;

-- 使用JOIN代替子查询
SELECT p.*, u.name
FROM projects p
JOIN users u ON p.pi_id = u.id;
```

### 3. 表优化

```sql
-- 优化表结构
OPTIMIZE TABLE operation_logs;

-- 分析表统计信息
ANALYZE TABLE projects;
```

## 🔒 安全建议

1. **定期备份**: 每天自动备份数据库
2. **访问控制**: 使用专用数据库用户，限制权限
3. **加密存储**: 敏感字段加密存储
4. **审计日志**: 保留足够的操作日志
5. **慢查询日志**: 开启慢查询日志，优化性能

## 下一步

- 查看 [部署指南](DEPLOYMENT.md) 了解如何初始化数据库
- 查看 [开发指南](DEVELOPMENT.md) 了解如何使用ORM操作数据库
