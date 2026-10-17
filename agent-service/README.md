# Agent Service

Enterprise Agent Execution Platform 的 Python 服务，目前实现 Phase 1 / Task 01：使用 FastAPI 提供订单查询 API，通过 Pydantic 定义订单模型，并使用内存字典保存三条模拟订单。当前尚未接入数据库或 LLM。

## 环境与依赖

需要 Python 3.13 或更高版本，以及已安装的 [uv](https://docs.astral.sh/uv/)。以下命令均在 `agent-service` 目录执行。

```bash
uv sync --locked
```

该命令根据 `uv.lock` 安装依赖，默认包含 pytest、httpx 等开发依赖，并创建项目虚拟环境 `.venv`。

## 启动服务

```bash
uv run uvicorn app.main:app --reload
```

服务默认地址为 http://127.0.0.1:8000，交互式 API 文档位于 http://127.0.0.1:8000/docs。`--reload` 用于开发时自动重载代码；按 `Ctrl+C` 停止服务。

## 运行测试

```bash
uv run pytest
```

测试覆盖订单查询成功、订单不存在以及 `reason` 为 `null` 的场景。测试使用 `TestClient`，无需提前启动服务。

## API 示例

### 查询订单

```bash
curl -i http://127.0.0.1:8000/orders/ORD-1001
```

返回 HTTP 200：

```json
{
  "order_id": "ORD-1001",
  "status": "PENDING",
  "reason": "INVENTORY_NOT_AVAILABLE"
}
```

### 查询不存在的订单

```bash
curl -i http://127.0.0.1:8000/orders/ORD-9999
```

返回 HTTP 404：

```json
{
  "detail": "Order not found"
}
```

### 模拟数据

| Order ID | Status | Reason |
| --- | --- | --- |
| ORD-1001 | PENDING | INVENTORY_NOT_AVAILABLE |
| ORD-1002 | SUBMITTED | null |
| ORD-1003 | CANCELLED | CUSTOMER_REQUEST |

## 项目结构

```text
app/
├── __init__.py
├── main.py         # FastAPI 应用与订单查询接口
├── models.py       # Order Pydantic 模型
└── data.py         # 内存模拟订单
tests/
└── test_orders.py  # API 自动化测试
pyproject.toml      # 项目依赖与 pytest 配置
uv.lock             # 依赖锁定文件
```

## 环境变量文件

当前服务无需配置环境变量。`.env` 和 `.env.*` 已加入 Git 忽略规则；后续如需提供配置模板，可提交不包含真实密钥的 `.env.example`。
