# 数据文件目录

## Ingredient conflicts.xlsx

请将你的 Excel 冲突数据文件放在这个目录下，命名为 `Ingredient conflicts.xlsx`。

### 文件格式要求

- **第一列**：成分 A
- **第二列**：成分 B
- 每一行表示成分 A 和成分 B 之间存在冲突

### 处理文件

运行以下命令来处理 Excel 文件并生成冲突数据：

```bash
python3 scripts/process_conflicts.py data/Ingredient\ conflicts.xlsx
```

或者如果文件在其他位置：

```bash
python3 scripts/process_conflicts.py "/path/to/Ingredient conflicts.xlsx"
```

### 注意事项

- Excel 文件会被 Git 追踪（版本控制）
- 更新 Excel 文件后需要重新运行处理脚本
- 处理后的数据会生成到 `api/conflict_data.py`
