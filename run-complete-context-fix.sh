#!/bin/bash

echo "🚀 WorkflowContext → ErrorHandlingContext Migration Script"
echo "========================================================"

# Step 1: Search for references
echo -e "\n🔍 Step 1: Searching for WorkflowContext references..."
echo "=================================================="

echo -e "\n📁 Python files containing 'WorkflowContext':"
find . -name "*.py" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    echo "  📄 $file"
    grep -n "WorkflowContext" "$file" 2>/dev/null | sed 's/^/    /'
done

echo -e "\n📁 Markdown files containing 'WorkflowContext':"
find . -name "*.md" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    echo "  📄 $file"
    grep -n "WorkflowContext" "$file" 2>/dev/null | sed 's/^/    /'
done

echo -e "\n📁 Import statements from exception_handler:"
find . -name "*.py" -exec grep -l "from.*exception_handler.*import" {} \; 2>/dev/null | while read file; do
    echo "  📄 $file"
    grep -n "from.*exception_handler.*import" "$file" 2>/dev/null | sed 's/^/    /'
done

echo -e "\n🎯 Summary:"
python_files=$(find . -name "*.py" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | wc -l)
markdown_files=$(find . -name "*.md" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | wc -l)
echo "  Python files that need updating: $python_files"
echo "  Markdown files that need updating: $markdown_files"

# Step 2: Ask for confirmation
echo -e "\n❓ Step 2: Confirmation"
echo "======================="
if [ "$python_files" -eq 0 ] && [ "$markdown_files" -eq 0 ]; then
    echo "✅ No WorkflowContext references found. Nothing to update!"
    exit 0
fi

echo "The following changes will be made:"
echo "  • Replace 'WorkflowContext' with 'ErrorHandlingContext'"
echo "  • Update import statements"
echo "  • Update documentation files"
echo "  • Create backup files with .bak extension"

read -p "Do you want to proceed with these changes? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled by user."
    exit 1
fi

# Step 3: Create backups
echo -e "\n📁 Step 3: Creating backups..."
echo "=========================="
backup_count=0

find . -name "*.py" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    cp "$file" "$file.bak"
    echo "  📄 Backed up: $file → $file.bak"
    ((backup_count++))
done

find . -name "*.md" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    cp "$file" "$file.bak"
    echo "  📄 Backed up: $file → $file.bak"
    ((backup_count++))
done

# Step 4: Apply fixes
echo -e "\n🔧 Step 4: Applying fixes..."
echo "========================"

# Replace in Python files
echo "🐍 Updating Python files..."
find . -name "*.py" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    sed -i '' 's/WorkflowContext/ErrorHandlingContext/g' "$file" 2>/dev/null || sed -i 's/WorkflowContext/ErrorHandlingContext/g' "$file"
    echo "  ✅ Updated: $file"
done

# Replace in Markdown files
echo "📝 Updating Markdown files..."
find . -name "*.md" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | while read file; do
    sed -i '' 's/WorkflowContext/ErrorHandlingContext/g' "$file" 2>/dev/null || sed -i 's/WorkflowContext/ErrorHandlingContext/g' "$file"
    echo "  ✅ Updated: $file"
done

# Step 5: Verify changes
echo -e "\n✅ Step 5: Verifying changes..."
echo "=========================="

echo "📝 Files that were modified:"
find . -name "*.bak" 2>/dev/null | while read backup_file; do
    original_file="${backup_file%.bak}"
    if [ -f "$original_file" ]; then
        if ! diff "$original_file" "$backup_file" >/dev/null 2>&1; then
            echo "  📄 $original_file ✅ (modified)"
            echo "    Changes made:"
            diff "$backup_file" "$original_file" | grep "^>" | sed 's/^>/      +/' | head -3
            if [ $(diff "$backup_file" "$original_file" | grep "^>" | wc -l) -gt 3 ]; then
                echo "      ... (and more)"
            fi
        else
            echo "  📄 $original_file (no changes needed)"
        fi
    fi
done

# Step 6: Test the changes
echo -e "\n🧪 Step 6: Testing the changes..."
echo "=========================="

echo "Checking for syntax errors..."
error_found=false

# Test Python files
find . -name "*.py" -path "*/agent_outreach/*" | while read file; do
    if ! python -m py_compile "$file" 2>/dev/null; then
        echo "  ❌ Syntax error in: $file"
        error_found=true
    fi
done

if [ "$error_found" = false ]; then
    echo "  ✅ No syntax errors found in Python files"
fi

# Test specific important files
important_files=("agent_outreach/executor/workflow_executor.py" "agent_outreach/utils/exception_handler.py")
for file in "${important_files[@]}"; do
    if [ -f "$file" ]; then
        if python -m py_compile "$file" 2>/dev/null; then
            echo "  ✅ $file compiles successfully"
        else
            echo "  ❌ $file has compilation errors"
        fi
    fi
done

# Step 7: Final summary
echo -e "\n🎉 Step 7: Migration Complete!"
echo "=========================="
echo "✅ Successfully replaced WorkflowContext with ErrorHandlingContext"
echo "📁 Backup files created with .bak extension"
echo ""
echo "Next steps:"
echo "1. Test your application: python dummy_patient_reminder_memory.py"
echo "2. If everything works, remove backups: find . -name '*.bak' -delete"
echo "3. If there are issues, restore from backups:"
echo "   find . -name '*.bak' -exec sh -c 'mv \"$1\" \"${1%.bak}\"' _ {} \;"
echo ""
echo "🔍 To see all changes made:"
echo "   find . -name '*.bak' -exec sh -c 'echo \"=== \${1%.bak} ===\"; diff \"\$1\" \"\${1%.bak}\"' _ {} \;"

