# Quick Deployment Steps for Render

## 1. Push to GitHub

```bash
# Initialize git (already done)
git add .
git commit -m "EuPrime Lead Generation Tool - Ready for deployment"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/euprime-lead-gen.git
git branch -M main
git push -u origin main
```

## 2. Deploy on Render

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
5. Click **"Create Web Service"**

## 3. Done! 🎉

Your app will be live at: `https://euprime-lead-gen.onrender.com`

---

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
