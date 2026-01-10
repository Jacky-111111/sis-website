# 项目结构说明

这个文档帮助你理解项目的文件组织和每个文件的作用。

## 📂 目录结构

```
sis-website/
│
├── index.html              # 🌐 主 HTML 文件（网页入口）
├── README.md               # 📖 项目说明文档
├── PROJECT_STRUCTURE.md    # 📋 本文件（项目结构说明）
├── requirements.txt        # 📦 Python 依赖包列表
├── .gitignore             # 🚫 Git 忽略文件配置
│
├── css/                    # 🎨 样式文件目录
│   └── styles.css         #    所有 CSS 样式（从 index.html 分离出来）
│
├── js/                     # 💻 JavaScript 文件目录
│   └── script.js          #    所有 JavaScript 逻辑（从 index.html 分离出来）
│
├── api/                    # 🔧 后端 API 目录
│   └── main.py            #    Flask 后端服务器（处理 API 请求）
│
├── public/                 # 📁 静态资源目录（可选）
│   └── images/            #    图片文件（目前使用 Unsplash 在线图片）
│
├── start_backend.sh       # 🚀 Mac/Linux 启动脚本
└── start_backend.bat      # 🚀 Windows 启动脚本
```

## 📄 文件说明

### 前端文件

#### `index.html`
- **作用**：网页的主 HTML 文件，包含所有页面结构
- **内容**：
  - 导航栏（Navbar）
  - 首页（Home Section）- 成分输入表单
  - 结果页（Result Section）- 显示分析结果
  - 关于页（About Section）- 项目介绍
- **特点**：引用了外部的 CSS 和 JS 文件

#### `css/styles.css`
- **作用**：所有样式代码
- **内容**：
  - 全局样式重置
  - 颜色变量定义（粉色主题）
  - 各个组件的样式（导航栏、卡片、按钮等）
  - 响应式设计（手机端适配）
- **为什么分离**：代码更清晰，便于维护和修改样式

#### `js/script.js`
- **作用**：所有 JavaScript 逻辑代码
- **内容**：
  - 页面切换功能
  - 成分解析函数
  - API 调用函数（连接后端）
  - Mock 函数（后端不可用时的备用）
- **为什么分离**：代码更清晰，便于维护和调试

### 后端文件

#### `api/main.py`
- **作用**：Flask 后端服务器，提供 RESTful API
- **功能**：
  - `/api/analyze` - 分析成分冲突（POST 请求）
  - `/api/health` - 健康检查（GET 请求）
- **当前状态**：使用 Mock 函数，等待接入 GNN 模型
- **TODO**：在 `analyze_ingredients_with_gnn()` 函数中接入真实的 GNN 模型

### 配置文件

#### `requirements.txt`
- **作用**：Python 依赖包列表
- **使用**：`pip install -r requirements.txt` 安装所有依赖
- **当前包含**：
  - Flask（Web 框架）
  - flask-cors（处理跨域问题）
- **未来可能添加**：
  - torch（PyTorch 深度学习框架）
  - torch-geometric（图神经网络库）

#### `.gitignore`
- **作用**：告诉 Git 哪些文件不需要版本控制
- **包含**：Python 缓存、虚拟环境、IDE 配置等

### 启动脚本

#### `start_backend.sh` (Mac/Linux)
- **作用**：一键启动后端服务器
- **功能**：
  - 检查 Python 是否安装
  - 检查依赖是否安装
  - 启动 Flask 服务器

#### `start_backend.bat` (Windows)
- **作用**：Windows 版本的一键启动脚本
- **功能**：同上

## 🔄 数据流程

### 用户使用流程

1. **用户打开网页** → `index.html` 加载
2. **加载样式** → `css/styles.css` 应用样式
3. **加载脚本** → `js/script.js` 初始化页面
4. **用户输入成分** → 在表单中输入
5. **点击 Analyze** → JavaScript 调用 API
6. **发送请求** → 前端发送 POST 请求到后端
7. **后端处理** → `api/main.py` 处理请求（目前是 Mock）
8. **返回结果** → 后端返回 JSON 数据
9. **显示结果** → 前端更新页面显示结果

### API 调用流程

```
前端 (js/script.js)
    ↓
analyzeIngredients(ingredients)
    ↓
fetch('http://localhost:5000/api/analyze', {...})
    ↓
后端 (api/main.py)
    ↓
@app.route('/api/analyze', methods=['POST'])
    ↓
analyze_ingredients_with_gnn(ingredients)
    ↓
[未来：调用 GNN 模型]
    ↓
返回 JSON: {status, riskScore, summary}
    ↓
前端更新 UI
```

## 🎯 如何修改项目

### 修改样式
- 编辑 `css/styles.css`
- 修改颜色：找到 `:root` 中的颜色变量
- 修改布局：找到对应的类选择器

### 修改功能
- 编辑 `js/script.js`
- 修改 API 地址：找到 `API_BASE_URL` 常量
- 修改逻辑：找到对应的函数

### 接入 GNN 模型
1. 编辑 `api/main.py`
2. 找到 `analyze_ingredients_with_gnn()` 函数
3. 替换 Mock 代码为真实的模型调用
4. 确保返回格式一致：`{status, riskScore, summary}`

## 💡 为什么这样组织？

1. **分离关注点**：HTML（结构）、CSS（样式）、JS（逻辑）分开
2. **便于维护**：每个文件职责单一，容易找到和修改
3. **代码复用**：CSS 和 JS 可以被多个 HTML 文件引用
4. **团队协作**：不同人可以同时修改不同文件，减少冲突
5. **性能优化**：浏览器可以缓存 CSS 和 JS 文件

## 📚 学习建议

如果你是初学者，建议按以下顺序学习：

1. **先看 `index.html`** - 了解页面结构
2. **再看 `css/styles.css`** - 了解样式如何应用
3. **再看 `js/script.js`** - 了解交互逻辑
4. **最后看 `api/main.py`** - 了解后端 API

每个文件都有详细的中文注释，可以帮助你理解代码。
