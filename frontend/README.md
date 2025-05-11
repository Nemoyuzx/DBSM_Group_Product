```markdown
# 📘 DBMS 系统 - 前后端运行指南

本项目为一个前后端分离的数据库管理系统，前端基于 **Vue 3 + Element Plus**，后端基于 **Django + Django REST Framework + MySQL**。

## 🧩 项目结构

```
DBSM_Group_Product-main/
├── DjangoProject/            # 后端 Django 项目文件夹
├── frontend/                 # 前端 Vue 项目文件夹
├── requirements.txt          # 后端依赖包（如未提供可自行生成）
└── README.md                 # 当前说明文档
```

---

## 🖥️ 一、后端（Django）

### 1.1 创建虚拟环境（推荐）

```bash
conda create -n DBMS_Django_env python=3.12
conda activate DBMS_Django_env
```

或使用 venv：

```bash
python -m venv env
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows
```

### 1.2 安装依赖

```bash
pip install -r requirements.txt
```

若没有 requirements.txt 文件，可手动安装：

```bash
pip install django djangorestframework django-cors-headers mysqlclient
```

### 1.3 数据库配置

确保你本地或远程 MySQL 已存在数据库：

- 数据库名：`DBMS_show`

在 `DjangoProject/DjangoProjectDBMS/settings.py` 中确认配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DBMS_show',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 1.4 启动后端服务

```bash
cd DjangoProject
python manage.py runserver
```

访问地址：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🌐 二、前端（Vue 3）

### 2.1 安装依赖

```bash
cd frontend
npm install
```

### 2.2 启动开发服务器

```bash
npm run serve
```

默认地址：[http://localhost:8082/](http://localhost:8082/)

---

## 🔄 三、前后端联调说明

- 前端 axios 全局默认前缀为 `/api`，代码如下：

```js
axios.defaults.baseURL = '/api'
```

- 后端已开启跨域（`CORS_ALLOW_ALL_ORIGINS = True`）；
- 你需要配置前端代理以避免跨域问题：

在 `frontend/vue.config.js` 文件中添加以下内容：

```js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' }
      }
    }
  }
}
```

---

## 🧪 四、接口路径示例

| 页面 | 示例路径 |
|------|----------|
| 学生列表 | `http://localhost:8082/students` |
| 课程详情 | `http://localhost:8082/courses/101` |
| 后端 API 根路径 | `http://localhost:8000/api/` |

---

## ⚠️ 常见问题

### ❓ 1. 数据库连接失败

- 确保 MySQL 正在运行；
- 用户名、密码、数据库名设置正确；
- 安装了 `mysqlclient` 库。

### ❓ 2. Axios 报错 404

- 确保请求路径以 `/api/` 开头；
- 后端服务器已成功运行；
- vue.config.js 代理配置正确。

### ❓ 3. 静态资源加载失败

- 可能是缓存问题；
- 可尝试清空 `node_modules` 并重新安装：

```bash
rm -rf node_modules
npm install
```

---

## 📮 联系与维护

**作者**：Rui Ma  
**团队**：Group19  
**联系方式**：[jp2023213616@qmul.ac.uk](mailto:jp2023213616@qmul.ac.uk)  
**说明**：项目仅用于教学演示，如需部署生产环境请做好安全配置。
```