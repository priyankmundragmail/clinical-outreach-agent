#!/bin/bash
echo "🔍 Searching for WorkflowContext references in the project..."
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

echo -e "\n📁 Usage patterns with 'with' statements:"
find . -name "*.py" -exec grep -l "with.*WorkflowContext\|with.*ErrorHandlingContext" {} \; 2>/dev/null | while read file; do
    echo "  📄 $file"
    grep -n "with.*WorkflowContext\|with.*ErrorHandlingContext" "$file" 2>/dev/null | sed 's/^/    /'
done

echo -e "\n🎯 Summary:"
echo "Files that need updating:"
find . -name "*.py" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | wc -l | xargs echo "  Python files:"
find . -name "*.md" -exec grep -l "WorkflowContext" {} \; 2>/dev/null | wc -l | xargs echo "  Markdown files:"

echo -e "\n✅ Files already using ErrorHandlingContext:"
find . -name "*.py" -exec grep -l "ErrorHandlingContext" {} \; 2>/dev/null | while read file; do
    echo "  📄 $file"
done

echo -e "\n🔧 Next steps:"
echo "1. Update all 'WorkflowContext' to 'ErrorHandlingContext'"
echo "2. Update import statements"
echo "3. Update documentation files"
echo "4. Test the changes"
