#!/bin/bash
# Read first 6 lines of each task from all locations
# Used by doalltasks to get overview of all tasks

echo "=== GLOBAL IN_PROGRESS ==="
for f in /home/moskalyuk_ruslan/aitasks/in_progress/*.md 2>/dev/null; do
  [ -f "$f" ] && echo "--- $(basename $f) ---" && head -6 "$f" && echo ""
done

echo "=== GLOBAL TODO ==="
for f in /home/moskalyuk_ruslan/aitasks/todo/*.md 2>/dev/null; do
  [ -f "$f" ] && echo "--- $(basename $f) ---" && head -6 "$f" && echo ""
done

echo "=== FEATURE TASKS ==="
for dir in /home/moskalyuk_ruslan/aidocs/sdd/projects/*/features/*/tasks; do
  [ -d "$dir" ] || continue

  feature=$(echo "$dir" | sed 's|.*/projects/\([^/]*\)/features/\([^/]*\)/.*|\1/\2|')

  # in_progress
  for f in "$dir/in_progress"/*.md 2>/dev/null; do
    [ -f "$f" ] && echo "--- [$feature] $(basename $f) [IN_PROGRESS] ---" && head -6 "$f" && echo ""
  done

  # todo
  for f in "$dir/todo"/*.md 2>/dev/null; do
    [ -f "$f" ] && echo "--- [$feature] $(basename $f) ---" && head -6 "$f" && echo ""
  done
done

# Count
echo "=== SUMMARY ==="
GLOBAL_IP=$(find /home/moskalyuk_ruslan/aitasks/in_progress/ -name "TASK_*.md" 2>/dev/null | wc -l)
GLOBAL_TODO=$(find /home/moskalyuk_ruslan/aitasks/todo/ -name "TASK_*.md" 2>/dev/null | wc -l)
FEATURE_IP=$(find /home/moskalyuk_ruslan/aidocs/sdd/projects/*/features/*/tasks/in_progress/ -name "TASK_*.md" 2>/dev/null | wc -l)
FEATURE_TODO=$(find /home/moskalyuk_ruslan/aidocs/sdd/projects/*/features/*/tasks/todo/ -name "TASK_*.md" 2>/dev/null | wc -l)

echo "Global: $GLOBAL_IP in_progress, $GLOBAL_TODO todo"
echo "Feature: $FEATURE_IP in_progress, $FEATURE_TODO todo"
echo "Total: $((GLOBAL_IP + GLOBAL_TODO + FEATURE_IP + FEATURE_TODO))"
