"""
Skincare Ingredient Scout - Backend API
使用 Flask 框架提供 RESTful API 接口

TODO: 接入 GNN 模型后，在 analyze_ingredients 函数中调用模型进行预测
"""

from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理跨域问题
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 Flask 应用，配置静态文件服务
# static_folder 指向静态文件目录，static_url_path="" 表示静态文件在根路径
app = Flask(__name__, 
            static_folder='static', 
            static_url_path='')
CORS(app)  # 允许跨域请求


# ============================================
# Mock 检测逻辑（临时使用）
# TODO: 替换为真实的 GNN 模型调用
# ============================================
def analyze_ingredients_mock(ingredients):
    """
    Mock 函数：模拟成分冲突检测
    
    Args:
        ingredients: 成分列表，例如 ['retinol', 'vitamin C', 'niacinamide']
    
    Returns:
        dict: 包含 status, riskScore, summary 的字典
    """
    # 转换为小写以便匹配
    lower_ingredients = [ing.lower() for ing in ingredients]
    
    # 危险关键词
    danger_keywords = [
        'retinol',
        'aha',
        'bha',
        'salicylic',
        'benzoyl',
        'vitamin c',
        'niacinamide',
        'ascorbic acid',
        'glycolic acid',
        'lactic acid'
    ]
    
    # 检查危险关键词
    found_danger_keywords = [
        ing for ing in lower_ingredients
        if any(keyword in ing for keyword in danger_keywords)
    ]
    
    # 判断状态
    has_multiple_danger = len(found_danger_keywords) >= 2
    has_retinol_and_acid = (
        any('retinol' in ing for ing in lower_ingredients) and
        any(acid in ing for ing in lower_ingredients 
            for acid in ['aha', 'bha', 'salicylic', 'glycolic', 'lactic'])
    )
    has_vitamin_c_and_niacinamide = (
        any('vitamin c' in ing or 'ascorbic' in ing for ing in lower_ingredients) and
        any('niacinamide' in ing for ing in lower_ingredients)
    )
    
    is_danger = has_multiple_danger or has_retinol_and_acid or has_vitamin_c_and_niacinamide
    
    # 计算风险分数
    if is_danger:
        risk_score = min(100, 40 + len(found_danger_keywords) * 15)
    else:
        risk_score = max(0, len(found_danger_keywords) * 5)
    
    # 生成摘要
    if is_danger:
        if has_retinol_and_acid:
            summary = (
                'We detected a potential conflict: Retinol and acids (AHA/BHA) '
                'can cause excessive irritation and dryness when used together. '
                'Consider using them on alternate days or at different times (AM/PM).'
            )
        elif has_vitamin_c_and_niacinamide:
            summary = (
                'We detected a potential conflict: Vitamin C and Niacinamide may '
                'cause flushing and reduce effectiveness when combined at high concentrations. '
                'Consider applying them at different times of day.'
            )
        else:
            summary = (
                'We detected multiple active ingredients that may cause irritation '
                'or reduce effectiveness when combined. Please review the suggestions '
                'and consider spacing out active ingredients across different days.'
            )
    else:
        summary = (
            'Your ingredient combination appears to be safe! No significant conflicts '
            'were detected. You can proceed with confidence. Remember to patch test '
            'new products and use sunscreen daily, especially with active ingredients.'
        )
    
    return {
        'status': 'danger' if is_danger else 'safe',
        'riskScore': risk_score,
        'summary': summary
    }


# ============================================
# TODO: 接入 GNN 模型
# ============================================
def analyze_ingredients_with_gnn(ingredients):
    """
    使用 GNN 模型进行成分冲突检测
    
    Args:
        ingredients: 成分列表
    
    Returns:
        dict: 分析结果
    
    示例代码结构（需要根据实际模型调整）:
    ```
    import torch
    from your_gnn_model import YourGNNModel
    
    # 加载模型
    model = YourGNNModel()
    model.load_state_dict(torch.load('path/to/model.pth'))
    model.eval()
    
    # 预处理输入（将成分转换为图数据）
    graph_data = preprocess_ingredients(ingredients)
    
    # 模型预测
    with torch.no_grad():
        prediction = model(graph_data)
    
    # 后处理结果
    result = postprocess_prediction(prediction)
    return result
    ```
    """
    # TODO: 实现 GNN 模型调用
    # 目前先使用 mock 函数
    logger.warning("Using mock function. Please implement GNN model integration.")
    return analyze_ingredients_mock(ingredients)


# ============================================
# API 路由
# ============================================

@app.route('/')
def home():
    """根路径，返回首页"""
    return app.send_static_file('index.html')

@app.route('/about.html')
def about():
    """About 页面"""
    return app.send_static_file('about.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    分析成分冲突的 API 端点
    
    请求格式:
    {
        "ingredients": ["retinol", "vitamin C", "niacinamide"]
    }
    
    返回格式:
    {
        "status": "safe" | "danger",
        "riskScore": 0-100,
        "summary": "分析摘要文本"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'ingredients' not in data:
            return jsonify({
                'error': 'Missing ingredients in request body'
            }), 400
        
        ingredients = data['ingredients']
        
        if not isinstance(ingredients, list) or len(ingredients) == 0:
            return jsonify({
                'error': 'Ingredients must be a non-empty list'
            }), 400
        
        logger.info(f"Analyzing ingredients: {ingredients}")
        
        # 调用分析函数（目前是 mock，以后替换为 GNN）
        result = analyze_ingredients_with_gnn(ingredients)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error analyzing ingredients: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'Skincare Ingredient Scout API'
    }), 200


# ============================================
# 主程序入口
# ============================================
if __name__ == '__main__':
    # 开发模式运行
    # 生产环境使用 gunicorn (通过 Procfile 启动)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=port,        # 从环境变量读取端口（Render 会自动设置）
        debug=False       # 生产环境设为 False
    )
