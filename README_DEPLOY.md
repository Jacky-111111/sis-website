# Render 部署说明

## 问题排查

如果遇到 `gunicorn: command not found` 错误，请检查：

### 方案 1：使用 render.yaml（推荐）

确保 `render.yaml` 中的启动命令使用 `python3 -m gunicorn`：

```yaml
startCommand: cd api && python3 -m gunicorn --bind 0.0.0.0:$PORT --workers 2 main:app
```

### 方案 2：在 Render Dashboard 手动设置

如果 render.yaml 不生效，在 Render Dashboard 中手动设置：

1. 进入你的 Web Service 设置
2. 在 "Start Command" 中输入：
   ```
   cd api && python3 -m gunicorn --bind 0.0.0.0:$PORT --workers 2 main:app
   ```
3. 确保 "Build Command" 是：
   ```
   pip install -r requirements.txt
   ```

### 方案 3：简化方案（如果 gunicorn 仍有问题）

如果 gunicorn 仍然有问题，可以暂时使用 Flask 内置服务器：

在 Render Dashboard 的 "Start Command" 中设置：
```
cd api && python3 main.py
```

注意：这仅适用于测试，生产环境建议使用 gunicorn。

## 检查清单

- [ ] `requirements.txt` 中包含 `gunicorn==21.2.0`
- [ ] `render.yaml` 中的 `startCommand` 使用 `python3 -m gunicorn`
- [ ] 或者 Render Dashboard 中的 Start Command 已正确设置
- [ ] 环境变量 PORT 已设置（Render 会自动设置）

## 常见问题

**Q: 为什么使用 `python3 -m gunicorn` 而不是直接 `gunicorn`？**
A: 使用 `python3 -m` 可以确保使用正确 Python 环境中的 gunicorn，避免 PATH 问题。

**Q: Render 使用 render.yaml 还是 Procfile？**
A: Render 优先使用 render.yaml，如果没有 render.yaml 则使用 Procfile。
