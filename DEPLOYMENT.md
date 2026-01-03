# Deployment Guide for Render

## Prerequisites

1. **GitHub Account**: Create a repository for your code
2. **Render Account**: Sign up at [render.com](https://render.com)

## Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - EuPrime Lead Generation Tool"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/euprime-lead-gen.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Render

### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/

2. **Click "New +"** → Select **"Web Service"**

3. **Connect GitHub Repository**:
   - Click "Connect account" if first time
   - Select your `euprime-lead-gen` repository

4. **Configure the Web Service**:
   
   | Setting | Value |
   |---------|-------|
   | **Name** | `euprime-lead-gen` |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true` |
   | **Instance Type** | `Free` (or paid for better performance) |

5. **Environment Variables** (Optional):
   - Click "Advanced" → "Add Environment Variable"
   - Add any API keys if needed:
     - `PUBMED_EMAIL=your-email@example.com`
     - `HUNTER_IO_API_KEY=your_key` (if using)

6. **Click "Create Web Service"**

7. **Wait for Deployment** (5-10 minutes):
   - Render will build and deploy your app
   - You'll see build logs in real-time

8. **Access Your App**:
   - Once deployed, you'll get a URL like: `https://euprime-lead-gen.onrender.com`
   - Share this URL with stakeholders!

### Option B: Using render.yaml (Infrastructure as Code)

Create a `render.yaml` file in your repository root:

```yaml
services:
  - type: web
    name: euprime-lead-gen
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
    envVars:
      - key: PUBMED_EMAIL
        value: your-email@example.com
```

Then:
1. Push to GitHub
2. In Render dashboard, click "New +" → "Blueprint"
3. Connect your repository
4. Render will auto-detect `render.yaml` and deploy

## Step 3: Verify Deployment

1. **Open the Render URL** in your browser
2. **Test Features**:
   - ✅ Lead table loads
   - ✅ Search functionality works
   - ✅ Analytics tab displays charts
   - ✅ CSV export works

## Troubleshooting

### Build Fails
- Check `requirements.txt` is in root directory
- Verify Python version compatibility
- Check build logs for specific errors

### App Doesn't Load
- Ensure start command includes `--server.port=$PORT`
- Check that `config.toml` has `headless = true`
- Verify no hardcoded ports in code

### Slow Performance (Free Tier)
- Free tier spins down after 15 min of inactivity
- First load after inactivity takes ~30 seconds
- Upgrade to paid tier ($7/month) for always-on service

## Post-Deployment

### Custom Domain (Optional)
1. In Render dashboard → Settings → Custom Domain
2. Add your domain (e.g., `leads.euprime.com`)
3. Update DNS records as instructed

### Monitoring
- Check "Logs" tab in Render dashboard
- Set up email alerts for deployment failures
- Monitor usage in "Metrics" tab

### Updates
```bash
# Make changes to code
git add .
git commit -m "Update feature X"
git push

# Render auto-deploys on push to main branch
```

## Cost Estimate

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | 750 hours/month, spins down after 15min idle |
| **Starter** | $7/month | Always-on, faster builds, custom domain |
| **Standard** | $25/month | More resources, better performance |

**Recommendation**: Start with Free tier for demo, upgrade to Starter for production use.

## Security Best Practices

1. **Environment Variables**: Store API keys in Render's environment variables, not in code
2. **HTTPS**: Render provides free SSL certificates automatically
3. **Access Control**: Consider adding authentication if needed (Streamlit supports this)

## Support

- **Render Docs**: https://render.com/docs
- **Streamlit Deployment**: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app

---

**Your app will be live at**: `https://euprime-lead-gen.onrender.com` (or your custom URL)

**Deployment time**: ~5-10 minutes

**Status**: Ready to deploy! 🚀
