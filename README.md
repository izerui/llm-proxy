# llm-proxy

## 项目简介
`llm-proxy` 是一个基于 Python 的轻量级代理服务，旨在为语言模型（LLM）提供流式数据传输支持。该项目使用 FastAPI 框架构建，并通过异步流式响应实现高效的数据处理。

## 功能特点
- **流式数据传输**：支持通过 `StreamingResponse` 实现实时数据流。
- **日志记录**：集成日志记录功能，便于调试和监控。
- **异步处理**：利用 Python 的异步特性提升性能。

## 项目结构
```
llm-proxy/
├── llm_proxy.py       # 核心代理服务代码
├── main.py            # 主程序入口
├── requirements.txt   # 项目依赖
├── pyproject.toml     # 项目配置文件
├── llm.log            # 日志文件
├── agent.md           # 相关文档
└── __pycache__/       # 编译缓存
```

## 快速开始

### 环境要求
- Python 3.11 或更高版本
- 推荐使用虚拟环境（`venv`）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
运行以下命令启动代理服务：
```bash
python llm_proxy.py
```
服务默认运行在 `http://0.0.0.0:8000`。

## 日志记录
日志文件 `llm.log` 用于记录服务运行过程中的重要信息，包括流式数据和错误信息。

## 注意事项
- 请确保敏感信息（如 API 密钥）未包含在提交的代码中。
- 如果需要修改端口或其他配置，请编辑 `llm_proxy.py` 文件中的 `uvicorn.run` 方法。

## 贡献
欢迎提交 Issue 或 Pull Request 来改进此项目。
