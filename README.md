# 新 multi agent demo 5.8

这是从原项目中整理出来的新版多 Agent 内容审核项目包，按前端、后端、共享审核引擎分目录放置，便于单独查看、启动和后续继续整理。

## 目录结构

```text
新multi agent demo 5.8/
  frontend/        # 新版前端页面与组件
  backend/         # 新版后端 API、Agent、Core、Services
  audit_system/    # 共享审核引擎与提示词
  app.py           # Streamlit 兼容入口
  streamlit_app.py # Streamlit 兼容入口
  requirements.txt # Python 依赖
  work_units_config.yaml
  README.md
```

## 当前已整理的内容

### 前端
- 审核页 `AuditPage`
- 首页 `DashboardPage`
- 知识库管理页 `KnowledgePage`
- 判例库管理页 `CasePage`
- 模型配置页 `ModelConfigPage`
- 审核主流程组件、黑板视图、日志流、批量审核、配置弹窗等

### 后端
- 审核主入口 `backend/app/main.py`
- Agent：文本清洗、规则执行、对抗侦探、判例执行、置信度评估、大法官
- Core：黑板、Agent 基类、配置管理、聚合器
- Routers：批量审核、知识库批量导入、批量删除
- API：判例库管理
- Services：向量库、知识库、判例、LLM、审核流水线

### 共享审核引擎
- `audit_system/` 下的多 Agent 审核核心、提示词与网页入口

## 关于知识库 / 规则库数据

页面手动导入的规则库、知识库数据，代码里对应的是后端的持久化向量库，理论上会落到：

```text
backend/data/chroma/
backend/data/config.json
backend/data/model_configs.json
backend/data/agent_configs.json
```

目前在当前工作区里还没有找到这些实际数据文件，所以如果要迁移历史导入内容，需要把这些持久化数据一并找到并复制进来。

## 启动前建议

1. 安装依赖
2. 先启动后端，再启动前端
3. 确认前端代理或环境变量指向新的后端地址

## 终端启动说明

如果你想自己在终端里启动，按下面的顺序来。

### 1. 启动后端

先进入后端目录，然后启动 FastAPI：

```bash
cd "/Users/zhangyilong/Desktop/新multi agent demo 5.8_副本/backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动成功后，可以先检查：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### 2. 启动前端

再开一个新的终端窗口，进入前端目录，启动 Vite：

```bash
cd "/Users/zhangyilong/Desktop/新multi agent demo 5.8_副本/frontend"
npm install
npm run dev -- --host 0.0.0.0
```

如果你想让局域网设备也能访问，就打开终端里显示的 `Network:` 地址，比如：

```text
http://192.168.50.166:5174/
```

### 3. Streamlit 兼容入口

如果你要跑另一个 Streamlit 页面，用这个命令：

```bash
cd "/Users/zhangyilong/Desktop/新multi agent demo 5.8_副本"
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 4. 一键启动脚本

如果你想一次性启动前后端，可以直接运行：

```bash
cd "/Users/zhangyilong/Desktop/新multi agent demo 5.8_副本"
chmod +x start_demo.command
./start_demo.command
```

## 访问地址

- 前端网页：`http://localhost:5173`
- 局域网前端：`http://192.168.50.166:5174/`（以终端显示为准）
- 后端首页：`http://127.0.0.1:8000/`
- 后端接口文档：`http://127.0.0.1:8000/docs`
- 后端健康检查：`http://127.0.0.1:8000/health`

## 内网部署注意事项

### 前端 / 后端地址
如果前后端不是同域部署，需要配置前端 API 地址，例如：

```bash
VITE_API_BASE_URL=http://你的后端地址:8000/api
```

WebSocket 连接也依赖后端地址，确保浏览器能访问：

```text
ws://你的后端地址:8000/ws/audit/{audit_id}
```

### CORS
后端当前允许跨域，但如果你要限制内网来源，建议后续改成固定域名白名单。

### 模型服务
后端会读取模型配置和环境变量，确保内网可访问的大模型服务可用，或者提前配置好：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_SMALL_MODEL`
- `LLM_STRONG_MODEL`
- `LLM_EMBEDDING_MODEL`

### 数据持久化
如果要保留手动导入的规则库 / 知识库，请把以下目录和文件一并迁移：

- `backend/data/chroma/`
- `backend/data/config.json`
- `backend/data/model_configs.json`
- `backend/data/agent_configs.json`

## 常见问题

### 1. Streamlit 报 `removeChild` / `NotFoundError`
这通常是前端 DOM 重绘时的兼容问题，和 `unsafe_allow_html=True`、动态 HTML 拼接、频繁 rerun 有关。后续建议逐步改成更稳定的 Streamlit 原生组件写法。

### 2. 规则库 / 知识库是空的
说明持久化数据没有迁移进来，需要把 `backend/data/chroma/` 等目录带过来。

### 3. 后端启动报模块找不到
说明 `backend/app` 下还缺某些模块或路径没有放对，需要继续检查 `agents/`、`core/`、`api/`、`routers/`、`services/`、`workflows/` 的完整性。

## 备注

这个文件夹的目标是作为“新架构整理包”，后续可以继续在这里补充：
- 数据迁移
- 启动脚本
- 环境变量说明
- 打包部署说明
