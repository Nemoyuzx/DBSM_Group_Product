# Vue Frontend

本目录包含面向浏览器的单页应用，负责展示数据库课程项目中的主要实体和统计信息。

## Stack

- Vue 3
- Vue Router
- Element Plus
- Axios
- ECharts

## Install

```bash
npm install
```

## Development

```bash
npm run serve
```

默认开发地址：`http://localhost:8082`

当前代理配置会将以下请求转发到本地 Django 服务 `http://localhost:8000`：

- `/api`
- `/table-counts`
- `/table-data`

## Build

```bash
npm run build
```

## Main Routes

- `/`
- `/students`
- `/students/:id`
- `/staffs`
- `/persons/:id`
- `/courses`
- `/courses/:id`
- `/departments`
- `/programs`
- `/all-tables`
- `/table-data/:tableName`
- `/api-debug`

## Local Development Notes

- 启动前请先确认 Django 后端已经运行
- 如果前端接口返回 404，优先检查 `vue.config.js` 代理配置和后端端口
- 如果依赖安装异常，可删除 `node_modules` 后重新执行 `npm install`