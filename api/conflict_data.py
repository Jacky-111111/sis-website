"""
成分冲突数据
从 data/Ingredient conflicts.xlsx 自动生成
使用 scripts/process_conflicts.py 来更新此文件
"""

# 冲突映射：key 是成分，value 是与该成分冲突的其他成分列表
INGREDIENT_CONFLICTS = {
    'ahas': ['hydroquinone'],
    'ahas/bahs': ['niacinamide', 'retinoids', 'vitamin c'],
    'ahas/bhas': ['retinoids'],
    'ahas/bhcs': ['vitamin c'],
    'alcohol': ['protein'],
    'alpha hydroxy acid': ['retinol'],
    'benzoyl peroxide': ['hydroquinone', 'retinoids', 'retinol', 'vitamin c'],
    'bhas': ['retinoids'],
    'chemical exfoliants': ['physical exfoliants'],
    'citrus/lavender essential oils': ['photosensitizing acids'],
    'copper peptides': ['vitamin c'],
    'formaldehyde-releasing preservatives': ['sulfites'],
    'fragrance-rich essential oils': ['niacinamide'],
    'fruit acid': ['retinol'],
    'glycolic acid': ['salicylic acid'],
    'high-concentration acids': ['high-concentration alkalis'],
    'high-concentration alkalis': ['high-concentration acids'],
    'high-concentration benzoyl peroxide': ['high-concentration salicylic acid'],
    'high-concentration salicylic acid': ['high-concentration benzoyl peroxide'],
    'high-content alcohol': ['retinoids'],
    'high-molecular-weight hyaluronic acid': ['silicone-heavy occlusives'],
    'hydroquinone': ['ahas', 'benzoyl peroxide', 'vitamin c'],
    'incompatible vitamin e formulations': ['vitamin c'],
    'low-ph niacinamide': ['pure vitamin c (ascorbic acid)'],
    'niacinamide': ['ahas/bahs', 'fragrance-rich essential oils', 'vitamin c'],
    'nicotinamid': ['vitamin c'],
    'nicotinamide': ['salicylic acid'],
    'oil-based skincare': ['water based'],
    'peptides': ['sles/sls harsh surfactants'],
    'photosensitizing acids': ['citrus/lavender essential oils'],
    'physical exfoliants': ['chemical exfoliants'],
    'protein': ['alcohol'],
    'pure vitamin c (ascorbic acid)': ['low-ph niacinamide'],
    'retinoides': ['salicylic acid'],
    'retinoids': ['ahas/bahs', 'ahas/bhas', 'benzoyl peroxide', 'bhas', 'high-content alcohol', 'vitamin c'],
    'retinol': ['alpha hydroxy acid', 'benzoyl peroxide', 'fruit acid', 'vitamin c'],
    'salicylic acid': ['glycolic acid', 'nicotinamide', 'retinoides'],
    'silicone-heavy occlusives': ['high-molecular-weight hyaluronic acid'],
    'sles/sls harsh surfactants': ['peptides'],
    'sulfites': ['formaldehyde-releasing preservatives'],
    'unstable antioxidants': ['uv filter sunscreens'],
    'uv filter sunscreens': ['unstable antioxidants'],
    'vitamin c': ['ahas/bahs', 'ahas/bhcs', 'benzoyl peroxide', 'copper peptides', 'hydroquinone', 'incompatible vitamin e formulations', 'niacinamide', 'nicotinamid', 'retinoids', 'retinol'],
    'water based': ['oil-based skincare'],
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
