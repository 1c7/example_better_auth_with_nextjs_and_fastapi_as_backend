# FastAPI Hello World

这是一个简单的 FastAPI Hello World 示例项目。

## 环境管理

### 安装 uv
```bash
pip install uv
```

### 创建虚拟环境
```bash
uv venv
```

### 激活虚拟环境
```bash
source .venv/bin/activate  # Unix/macOS
# 或
.venv\Scripts\activate  # Windows
```

### 使用 uv 安装依赖
```bash
uv pip install -r requirements.txt
```

## 运行项目

```bash
uvicorn main:app --reload
```

运行后，您可以访问以下地址：

- API 文档：http://127.0.0.1:8000/docs
- Hello World 接口：http://127.0.0.1:8000/

## 其他常用 uv 命令

- 查看已安装的包：`uv pip list`
- 添加新的依赖：`uv pip install <package_name>`
- 更新依赖文件：`uv pip freeze > requirements.txt`
- 退出虚拟环境：`deactivate` 