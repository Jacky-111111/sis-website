"""
成分冲突数据
从 Excel 文件自动生成
使用 scripts/process_conflicts.py 来更新此文件
"""

# 冲突映射：key 是成分，value 是与该成分冲突的其他成分列表
# 这个文件会通过运行 scripts/process_conflicts.py 自动生成
INGREDIENT_CONFLICTS = {
    # 示例数据（运行脚本后会被替换）
    # 'retinol': ['aha', 'bha', 'salicylic acid'],
    # 'vitamin c': ['niacinamide'],
}


def get_conflicting_ingredients(ingredient):
    """
    获取与指定成分冲突的所有成分
    
    Args:
        ingredient: 成分名称（小写）
    
    Returns:
        list: 冲突成分列表
    """
    return INGREDIENT_CONFLICTS.get(ingredient.lower(), [])


def check_conflict(ingredient1, ingredient2):
    """
    检查两个成分是否冲突
    
    Args:
        ingredient1: 第一个成分（小写）
        ingredient2: 第二个成分（小写）
    
    Returns:
        bool: 如果冲突返回 True，否则返回 False
    """
    ing1_lower = ingredient1.lower()
    ing2_lower = ingredient2.lower()
    
    conflicting = get_conflicting_ingredients(ing1_lower)
    return ing2_lower in conflicting


def find_all_conflicts(ingredients):
    """
    在成分列表中查找所有冲突
    
    Args:
        ingredients: 成分列表
    
    Returns:
        list: 冲突对列表，格式为 [{'ingredient1': '...', 'ingredient2': '...'}, ...]
    """
    conflicts = []
    ingredients_lower = [ing.lower() for ing in ingredients]
    
    for i, ing1 in enumerate(ingredients_lower):
        for ing2 in ingredients_lower[i+1:]:
            if check_conflict(ing1, ing2):
                conflicts.append({
                    'ingredient1': ing1,
                    'ingredient2': ing2
                })
    
    return conflicts
