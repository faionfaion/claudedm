#!/bin/bash
# Find all tasks from both global and feature-specific locations
# Usage: find-tasks.sh [base_path]
# Default base_path: $HOME

BASE="${1:-$HOME}"

echo "=== GLOBAL IN_PROGRESS (${BASE}/aitasks/in_progress/) ==="
find "${BASE}/aitasks/in_progress/" -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== GLOBAL TODO (${BASE}/aitasks/todo/) ==="
find "${BASE}/aitasks/todo/" -name "TASK_*.md" 2>/dev/null | sort -V

echo ""
echo "=== FEATURE IN_PROGRESS ==="
find "${BASE}/aidocs/sdd/"*/features/*/tasks/in_progress/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/sdd/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done

echo ""
echo "=== FEATURE TODO ==="
find "${BASE}/aidocs/sdd/"*/features/*/tasks/todo/ -name "TASK_*.md" 2>/dev/null | while read f; do
  feature=$(echo "$f" | sed 's|.*/sdd/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')
  echo "[$feature] $f"
done
