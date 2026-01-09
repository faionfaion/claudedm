#!/bin/bash
# Find all tasks from both global and feature-specific locations
# Priority: in_progress > todo

echo "=== GLOBAL IN_PROGRESS (aitasks/in_progress/) ==="
find aitasks/in_progress/ -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== GLOBAL TODO (aitasks/todo/) ==="
find aitasks/todo/ -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== FEATURE IN_PROGRESS ==="
find aidocs/sdd/*/features/*/tasks/in_progress/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/sdd/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done

echo ""
echo "=== FEATURE TODO ==="
find aidocs/sdd/*/features/*/tasks/todo/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/sdd/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done
