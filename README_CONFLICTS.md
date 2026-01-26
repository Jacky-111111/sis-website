# 扩展成分冲突知识库

## 使用方法

### 步骤 1: 将 Excel 文件放入项目

将你的 Excel 文件放到 `data/` 目录下，命名为 `Ingredient conflicts.xlsx`

**文件格式要求：**
- 第一列：成分 A
- 第二列：成分 B
- 每一行表示成分 A 和成分 B 之间存在冲突

### 步骤 2: 运行处理脚本

```bash
# 安装依赖（如果还没有）
pip install pandas openpyxl

# 如果文件在 data/ 目录下
python3 scripts/process_conflicts.py "data/Ingredient conflicts.xlsx"

# 或者如果文件在其他位置
python3 scripts/process_conflicts.py "/path/to/Ingredient conflicts.xlsx"
```

### 步骤 3: 脚本会自动

1. 读取 Excel 文件的第一列和第二列
2. 提取所有冲突对
3. 生成 `api/conflict_data.py` 文件，包含冲突数据

### 步骤 4: 更新 main.py

脚本生成后，需要更新 `api/main.py` 来使用新的冲突数据：

```python
from conflict_data import find_all_conflicts, check_conflict

# 在 analyze_ingredients_mock 函数中使用
conflicts = find_all_conflicts(ingredients)
```

## 生成的文件结构

`api/conflict_data.py` 包含：

- `INGREDIENT_CONFLICTS`: 冲突映射字典
- `get_conflicting_ingredients(ingredient)`: 获取与指定成分冲突的所有成分
- `check_conflict(ingredient1, ingredient2)`: 检查两个成分是否冲突
- `find_all_conflicts(ingredients)`: 在成分列表中查找所有冲突

## 注意事项

- Excel 文件中的成分名称会被转换为小写（不区分大小写）
- 冲突关系是双向的（A-B 和 B-A 都算冲突）
- 重复的冲突对会被自动去重
