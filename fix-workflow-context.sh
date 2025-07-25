#!/bin/bash
echo "🔧 Replacing WorkflowContext with ErrorHandlingContext..."

# Create backups first
echo "📁 Creating backups..."
find . -name "*.py" -exec cp {} {}.bak \; 2>/dev/null
find . -name "*.md" -exec cp {} {}.bak \; 2>/dev/null

# Replace in Python files
echo "🐍 Updating Python files..."
find . -name "*.py" -exec sed -i '' 's/WorkflowContext/ErrorHandlingContext/g' {} \; 2>/dev/null

# Replace in Markdown files
echo "📝 Updating Markdown files..."
find . -name "*.md" -exec sed -i '' 's/WorkflowContext/ErrorHandlingContext/g' {} \; 2>/dev/null

echo "✅ Replacements complete!"
echo "📁 Backup files created with .bak extension"

# Show what was changed
echo -e "\n📝 Files that were modified:"
find . -name "*.bak" 2>/dev/null | sed 's/\.bak$//' | while read file; do
    echo "  📄 $file"
    # Show differences
    if diff "$file" "$file.bak" >/dev/null 2>&1; then
        echo "    (no changes)"
    else
        echo "    ✅ modified"
    fi
done

echo -e "\n🧹 To remove backups later: find . -name '*.bak' -delete"
echo "🔍 To see changes: diff original.py.bak original.py"
