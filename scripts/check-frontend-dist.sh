#!/bin/bash
# Pre-commit hook to ensure frontend dist is staged when source changes

# Check if any frontend source files are staged
if git diff --cached --name-only | grep -q "frontend/src/"; then
    # Check if dist is also staged
    if ! git diff --cached --name-only | grep -q "frontend/dist/"; then
        echo "ERROR: Frontend source changed but dist/ not staged."
        echo ""
        echo "Run the following commands to build and stage:"
        echo "  cd custom_components/geekmagic/frontend"
        echo "  npm run build"
        echo "  git add custom_components/geekmagic/frontend/dist/"
        exit 1
    fi
fi

exit 0
