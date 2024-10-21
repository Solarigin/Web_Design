# 企业资源计划系统-使用说明书

### 一. 主要源代码文件名称

1. **登录界面**
   - 登录界面：`login.html`
   - 注册界面：`register.html`

2. **客户管理**
   - 客户管理界面：`customer.html`

3. **员工管理**
   - 员工管理界面：`employee.html`

4. **商品管理**
   - 商品管理界面：`good.html`

5. **采购管理**
   - 采购详情管理界面：`detail_management.html`
   - 采购主页面：`main_management.html`

6. **统计分析**
   - 统计页面：`statistics.html`
   - 仪表板界面：`dash_board.html`

7. **系统配置**
   - 配置文件：`config.py`
   - 数据库配置文件：`db.py`
   - 密码生成工具：`PasswordCreater.py`

8. **数据库**
   - SQL 数据文件：`nsm.sql`

9. **路由管理**
   - 客户路由：`customers.py`
   - 员工路由：`employees.py`
   - 商品路由：`goods.py`
   - 采购路由：`purchases.py`
   - 统计路由：`stats.py`

### 二. 账号密码(密码于数据库中为哈希加密 非明文)

1. **元管理员账号**
   - 用户名：A001
   - 密码：1345678
   - 角色：Admin

2. **客户经理账号**
   - 用户名：C001
   - 密码：1345678
   - 角色：CustomerManager

3. **访客账号**
   - 用户名：G001
   - 密码：1345678
   - 角色：Guest

4. **仓库管理员账号**
   - 用户名：W001
   - 密码：1345678
   - 角色：Warehouse

### 三. 运行环境

#### Python 版本

```
3.11.0
```

#### 所需库

运行此项目需要以下 Python 库：

- **Flask**：轻量级的 WSGI Web 应用框架。
- **mysql.connector**：用于连接 MySQL 数据库的 Python 库。
- **ImageCaptcha**：用于生成基于图片的验证码的 Python 库。

#### 安装命令

你可以使用以下命令安装所需库：

```bash
pip install flask mysql-connector-python captcha
```

#### Running the Application

To start the application, simply run the following Python script:

```bash
python app.py
```
