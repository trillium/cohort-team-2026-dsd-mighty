#!/bin/bash
# Type-check staged .ts/.tsx files
# Runs full project type-check but only fails on errors in staged files.
# Prefers tsgo (Go-native TS compiler) over tsc when available.
# Runs from frontend/ (the TypeScript project root), so staged paths are taken
# relative to it (--relative) to match tsc's output paths.

cd "$(dirname "$0")/.." || exit 1

STAGED=$(git diff --cached --name-only --diff-filter=ACM --relative | grep -E '\.(ts|tsx)$' || true)
if [ -z "$STAGED" ]; then
  exit 0
fi

# Prefer tsgo over tsc for speed
if command -v tsgo >/dev/null 2>&1; then
  TSC_CMD="tsgo"
elif command -v npx >/dev/null 2>&1; then
  TSC_CMD="npx tsc"
else
  echo "warning: Neither tsgo nor tsc found. Skipping type-check."
  exit 0
fi

# Next generates route types (LayoutProps, PageProps) that tsc needs on a fresh clone.
if [ -x node_modules/.bin/next ]; then
  node_modules/.bin/next typegen >/dev/null 2>&1 || true
fi

ERRORS=$($TSC_CMD --noEmit 2>&1 | grep "^[^ ].*error TS" || true)
if [ -z "$ERRORS" ]; then
  exit 0
fi

FAIL=0
for file in $STAGED; do
  MATCHED=$(echo "$ERRORS" | awk -v prefix="$file(" 'index($0, prefix) == 1')
  if [ -n "$MATCHED" ]; then
    if [ "$FAIL" -eq 0 ]; then
      echo "TypeScript errors in staged files:"
      echo ""
    fi
    echo "$MATCHED"
    FAIL=1
  fi
done

exit $FAIL
