# How to Push to GitHub

## 1. Create a GitHub Repository
1. Go to https://github.com/new
2. Name your repository (e.g., "venue-cafe-finder")
3. Choose Public or Private
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"

## 2. Push Your Code

```bash
cd /home/lucy/Q/coffeemap

# Add all files (gitignore will exclude sensitive files)
git add .

# Commit your changes
git commit -m "Initial commit: Venue cafe finder app"

# Add your GitHub repository as remote (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 3. Verify Security

After pushing, check on GitHub that these files are **NOT** visible:
- ❌ `config.js` (contains your Kakao JavaScript key)
- ❌ `.env` (contains backend API keys)
- ❌ `venue.db` (your database)
- ❌ `__pycache__/` (Python cache)
- ❌ `server.log` (log files)

These files should be visible:
- ✅ `config.example.js` (template)
- ✅ `.env.example` (template)
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ All source code files

## 4. For Other Developers

When someone clones your repo, they need to:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
cp config.example.js config.js
cp .env.example .env
# Edit both files with their own API keys
./start.sh
```

## Quick Commands Reference

```bash
# Check what will be committed
git status

# See what's ignored
git status --ignored

# Add new changes
git add .
git commit -m "Your commit message"
git push

# View remote URL
git remote -v
```
