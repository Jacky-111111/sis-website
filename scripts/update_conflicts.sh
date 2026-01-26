#!/bin/bash
# 自动更新冲突数据的脚本
# 在部署前运行此脚本，自动处理 Excel 文件并生成冲突数据

echo "🔄 更新成分冲突数据..."

# 检查 Excel 文件是否存在
EXCEL_FILE="data/Ingredient conflicts.xlsx"

if [ ! -f "$EXCEL_FILE" ]; then
    echo "⚠️  警告: $EXCEL_FILE 不存在"
    echo "   跳过冲突数据更新，使用默认规则"
    exit 0
fi

# 检查 Python 和依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 检查依赖
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖..."
    pip3 install --upgrade pip
    pip3 install pandas==2.2.0 openpyxl==3.1.2
fi

# 运行处理脚本
echo "📊 处理 Excel 文件..."
python3 scripts/process_conflicts.py "$EXCEL_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 冲突数据更新成功！"
else
    echo "❌ 更新失败，使用默认规则"
    exit 1
fi
