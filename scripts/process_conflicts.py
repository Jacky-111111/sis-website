#!/usr/bin/env python3
"""
处理 Excel 文件中的成分冲突数据
将第一列和第二列的冲突关系转换为代码可用的格式
"""

import pandas as pd
import json
import sys
import os

def process_excel_to_conflicts(excel_path):
    """
    读取 Excel 文件，提取第一列和第二列的冲突关系
    
    Args:
        excel_path: Excel 文件路径
    
    Returns:
        dict: 包含冲突关系的字典
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_path)
        
        # 获取第一列和第二列
        col1 = df.iloc[:, 0].name  # 第一列名称
        col2 = df.iloc[:, 1].name  # 第二列名称
        
        print(f"读取列: {col1} 和 {col2}")
        print(f"总行数: {len(df)}")
        
        # 提取冲突对
        conflicts = []
        conflict_pairs = set()  # 使用 set 避免重复
        
        for idx, row in df.iterrows():
            ingredient1 = str(row.iloc[0]).strip().lower()
            ingredient2 = str(row.iloc[1]).strip().lower()
            
            # 跳过空值
            if pd.isna(row.iloc[0]) or pd.isna(row.iloc[1]):
                continue
            
            # 跳过空字符串
            if not ingredient1 or not ingredient2 or ingredient1 == 'nan' or ingredient2 == 'nan':
                continue
            
            # 创建双向冲突对（A-B 和 B-A 都算冲突）
            pair1 = (ingredient1, ingredient2)
            pair2 = (ingredient2, ingredient1)
            
            if pair1 not in conflict_pairs and pair2 not in conflict_pairs:
                conflict_pairs.add(pair1)
                conflicts.append({
                    'ingredient1': ingredient1,
                    'ingredient2': ingredient2
                })
        
        print(f"提取到 {len(conflicts)} 个冲突对")
        
        # 创建冲突映射（用于快速查找）
        conflict_map = {}
        for conflict in conflicts:
            ing1 = conflict['ingredient1']
            ing2 = conflict['ingredient2']
            
            if ing1 not in conflict_map:
                conflict_map[ing1] = []
            conflict_map[ing1].append(ing2)
            
            if ing2 not in conflict_map:
                conflict_map[ing2] = []
            conflict_map[ing2].append(ing1)
        
        return {
            'conflicts': conflicts,
            'conflict_map': conflict_map,
            'total_pairs': len(conflicts)
        }
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

def generate_python_code(conflicts_data, output_file='api/conflict_data.py', excel_path=None):
    """
    生成 Python 代码文件，包含冲突数据
    
    Args:
        conflicts_data: 冲突数据字典
        output_file: 输出文件路径
    """
    conflict_map = conflicts_data['conflict_map']
    
    # 生成注释，包含 Excel 文件路径信息
    excel_info = f"从 {excel_path} 自动生成" if excel_path else "从 Excel 文件自动生成"
    
    code = f'''"""
成分冲突数据
{excel_info}
使用 scripts/process_conflicts.py 来更新此文件
"""

# 冲突映射：key 是成分，value 是与该成分冲突的其他成分列表
INGREDIENT_CONFLICTS = {{
'''
    
    # 按字母顺序排序
    sorted_items = sorted(conflict_map.items())
    
    for ingredient, conflicts in sorted_items:
        conflicts_str = ', '.join([f"'{c}'" for c in sorted(conflicts)])
        code += f"    '{ingredient}': [{conflicts_str}],\n"
    
    code += '''}


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
'''
    
    # 写入文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"已生成代码文件: {output_file}")
    print(f"包含 {len(conflict_map)} 个成分的冲突数据")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python process_conflicts.py <excel文件路径>")
        print("示例: python process_conflicts.py /path/to/Ingredient conflicts.xlsx")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    
    if not os.path.exists(excel_path):
        print(f"错误: 文件不存在: {excel_path}")
        sys.exit(1)
    
    print(f"处理文件: {excel_path}")
    conflicts_data = process_excel_to_conflicts(excel_path)
    
    if conflicts_data:
        generate_python_code(conflicts_data, excel_path=excel_path)
        print("\n处理完成！")
    else:
        print("处理失败！")
        sys.exit(1)
