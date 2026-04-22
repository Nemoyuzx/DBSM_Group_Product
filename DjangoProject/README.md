# Django Backend

本目录包含 Django 后端项目、模型定义和 REST API 路由。

## Requirements

- Python 3.12
- MySQL 8.x
- 建议使用 conda 环境 `DjangoDBMS`

## Setup

```bash
conda activate DjangoDBMS
pip install -r requirements.txt
cp .env.example .env
```

然后根据你的本地 MySQL 配置编辑 `.env`。

## Environment Variables

`settings.py` 会自动读取当前目录下的 `.env` 文件。可配置项如下：

```env
DJANGO_SECRET_KEY=replace-with-a-strong-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CORS_ALLOW_ALL_ORIGINS=True
DB_ENGINE=django.db.backends.mysql
DB_NAME=DBMS_show
DB_USER=root
DB_PASSWORD=replace-with-your-db-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Run

```bash
python manage.py migrate
python manage.py runserver
```

默认服务地址：`http://127.0.0.1:8000`

## API Overview

项目通过 `DefaultRouter` 暴露多个资源，常用入口包括：

- `/api/students/`
- `/api/staffs/`
- `/api/courses/`
- `/api/departments/`
- `/api/programs/`
- `/api/persons/`
- `/api/table-counts/`
- `/api/table-data/<table_name>/`
- `/api/debug-info/`

## Troubleshooting

### `mysqlclient` 安装失败

在 macOS 上如果看到 `pkg-config` 或 MySQL 头文件相关错误，可以先安装依赖：

```bash
brew install mysql mysql-connector-c openssl pkg-config
```

然后重新执行：

```bash
pip install -r requirements.txt
```

### 数据库连接失败

- 确认 MySQL 服务正在运行
- 确认 `.env` 中的数据库名、用户、密码和端口正确
- 确认目标数据库已经创建