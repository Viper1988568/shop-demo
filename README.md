# 川香小馆 · 点餐 H5

移动端点餐 H5 Demo：清爽年轻化的珊瑚橙视觉，前后端分离，订单真实落库。

## 技术栈

- **前端**：Vue 3 + Vite + TypeScript + Vant 4 + Pinia + Vue Router
- **后端**：FastAPI + SQLite（uv 管理 Python 环境）

## 功能

- 首页品牌展示、分类点餐、购物车（localStorage）、结算下单、订单列表
- 订单金额由**服务端**按菜单价计算，数据持久化到 SQLite（`backend/shop.db`）
- 首页 `/`，点餐 `/menu`，结算 `/checkout`，订单 `/orders`

## 本地运行

### 后端（端口 8000）

```bash
cd backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> 国内网络说明：PyPI 镜像（清华）已写入 `backend/pyproject.toml`。

### 前端（端口 5173）

```bash
npm install
npm run dev
```

打开 http://localhost:5173 ，`/api` 请求由 Vite 自动代理到后端 :8000。

## 接口自测

```bash
cd backend
uv run python test_api.py   # 14 项断言，含异常场景
```

## 目录结构

```
src/       前端页面；api/ 与 types/ 是前后端数据契约
backend/   FastAPI 应用；app/database.py 负责建表与种子数据（18 道川菜）
```
