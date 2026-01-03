#!/bin/bash

echo "========================================"
echo "EuPrime Lead Gen - GitHub Setup Helper"
echo "========================================"
echo ""

echo "Step 1: Create GitHub Repository"
echo "---------------------------------"
echo "1. Open your browser and go to: https://github.com/new"
echo "2. Repository name: euprime-lead-gen"
echo "3. Description: AI-powered lead generation tool for EuPrime"
echo "4. Keep it PUBLIC (so Render can access it for free)"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
read -p "Press Enter once you've created the repository..."

echo ""
read -p "Step 2: What's your GitHub username? " GITHUB_USER

echo ""
echo "Step 3: Pushing code to GitHub..."
echo "---------------------------------"

git remote add origin https://github.com/$GITHUB_USER/euprime-lead-gen.git 2>/dev/null || git remote set-url origin https://github.com/$GITHUB_USER/euprime-lead-gen.git

git branch -M main
git push -u origin main

echo ""
echo "========================================"
echo "SUCCESS! Code pushed to GitHub"
echo "========================================"
echo ""
echo "Your repository: https://github.com/$GITHUB_USER/euprime-lead-gen"
echo ""
echo "Next: Deploy on Render"
echo "1. Go to: https://dashboard.render.com/"
echo "2. Click 'New +' -> 'Web Service'"
echo "3. Connect your GitHub repo: euprime-lead-gen"
echo "4. Build Command: pip install -r requirements.txt"
echo "5. Start Command: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0 --server.headless=true"
echo "6. Click 'Create Web Service'"
echo ""
echo "Your app will be live in ~10 minutes!"
echo ""
