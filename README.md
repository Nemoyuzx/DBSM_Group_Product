
# DBMS Group Product

一个用于课程场景演示的前后端分离数据库管理系统。后端使用 Django REST Framework 提供数据接口，前端使用 Vue 3 展示院系、课程、学生、教师和多张关联表的数据视图。

## Tech Stack

- Backend: Django, Django REST Framework, MySQL
- Frontend: Vue 3, Vue Router, Element Plus, Axios, ECharts
- Tooling: Vue CLI, Babel, ESLint

## Repository Structure

```text
.
├── DjangoProject/   # Django backend and API
├── frontend/        # Vue frontend
└── README.md
```

## What The Project Does

- 提供多张数据库表的 REST API 访问入口
- 提供学生、教师、课程、院系、项目等页面与详情页
- 支持表数量统计、表数据浏览和 API 调试视图
- 支持中英文界面切换

## Quick Start

### 1. Backend

```bash
cd DjangoProject
conda activate DjangoDBMS
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

默认后端地址为 `http://127.0.0.1:8000`。

### 2. Frontend

```bash
cd frontend
npm install
npm run serve
```

默认前端地址为 `http://localhost:8082`。

## Configuration

后端配置通过 `DjangoProject/.env` 管理，仓库提供了 `DjangoProject/.env.example` 作为模板。请至少设置以下字段：

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

## Useful Routes

### Frontend

- `/`
- `/students`
- `/staffs`
- `/courses`
- `/departments`
- `/programs`
- `/all-tables`
- `/api-debug`

### Backend

- `/api/`
- `/api/students/`
- `/api/staffs/`
- `/api/courses/`
- `/api/departments/`
- `/api/programs/`
- `/api/table-counts/`
- `/api/table-data/<table_name>/`

## Security Notes

- 仓库不再包含真实密钥、数据库密码和本机路径。
- 如果这些凭据曾经用于公开提交，仍建议你在数据库和部署环境中轮换相关密钥。
- 当前默认配置适合本地开发，生产部署前需要收紧 `DEBUG`、`ALLOWED_HOSTS` 和跨域策略。

## Additional Docs

- 仅后端说明见 `DjangoProject/README.md`
- 仅前端说明见 `frontend/README.md`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
