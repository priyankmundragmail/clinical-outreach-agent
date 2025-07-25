#!/bin/bash
echo "======================================"
echo "🔍 PRE-PUSH VERIFICATION REPORT"
echo "======================================"
echo -e "\n📊 REPOSITORY STATISTICS:"
echo "Total files to push: $(git ls-files --cached | wc -l)"
echo "Total directories: $(git ls-files --cached | cut -d'/' -f1 | sort -u | wc -l)"
echo -e "\n📁 MAIN DIRECTORIES:"
git ls-files --cached | cut -d'/' -f1 | sort -u | while read dir; do
    count=$(git ls-files --cached | grep "^$dir/" | wc -l)
    echo "  $dir/ ($count files)"
done
echo -e "\n📄 FILE TYPES:"
git ls-files --cached | grep -o '\.[^./]*$' | sort | uniq -c | sort -rn
echo -e "\n🔒 SECURITY CHECK:"
if git ls-files --cached | grep -E "\.(env|key|secret|pem)$" > /dev/null; then
    echo "⚠️  WARNING: Sensitive files detected!"
    git ls-files --cached | grep -E "\.(env|key|secret|pem)$"
else
    echo "✅ No sensitive files found"
fi
if git ls-files --cached | xargs grep -l "sk-\|pk-\|API_KEY\|SECRET" 2>/dev/null; then
    echo "⚠️  WARNING: Potential secrets found in files!"
else
    echo "✅ No API keys or secrets detected"
fi
echo -e "\n📋 COMPLETE FILE LIST:"
git ls-files --cached | sort
