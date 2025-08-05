#!/bin/bash
# Delete the gh-pages branch (if it exists)
git branch -D gh-pages

# Build the site
uv run build.py

# Create and switch to gh-pages branch (which is the branch that GitHub Pages uses)
git switch -c gh-pages

# Copy built files to the root directory (which is the branch that GitHub Pages uses)
cp -r public/* .

# Commit and push
git add .
git commit -m "Update site"
# force push to overwrite the remote gh-pages branch if it exists
git push --force origin gh-pages

# Switch back to main branch
git switch main