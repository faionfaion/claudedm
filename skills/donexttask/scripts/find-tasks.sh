#!/bin/bash
# Find all tasks from both global and feature-specific locations
# Priority: in_progress > todo

echo "=== GLOBAL IN_PROGRESS (/aitasks/in_progress/) ==="
find /home/moskalyuk_ruslan/aitasks/in_progress/ -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== GLOBAL TODO (/aitasks/todo/) ==="
find /home/moskalyuk_ruslan/aitasks/todo/ -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== FEATURE IN_PROGRESS ==="
find /home/moskalyuk_ruslan/aidocs/sdd/projects/*/features/*/tasks/in_progress/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/projects/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done

echo ""
echo "=== FEATURE TODO ==="
find /home/moskalyuk_ruslan/aidocs/sdd/projects/*/features/*/tasks/todo/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/projects/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done
