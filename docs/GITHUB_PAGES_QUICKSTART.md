# GitHub Pages Quick Start

## 1. Configure GitHub Repository (One-Time Setup)

### Enable GitHub Pages

1. Go to: `https://github.com/jmchilton/galaxy-architecture/settings/pages`

2. Under **"Build and deployment"**:
   - **Source**: Select **"GitHub Actions"** (not "Deploy from a branch")

   ![GitHub Actions Source](https://docs.github.com/assets/cb-47267/mw-1440/images/help/pages/select-github-actions-source.webp)

3. Click **Save** (if button appears)

### Enable Workflow Permissions

1. Go to: `https://github.com/jmchilton/galaxy-architecture/settings/actions`

2. Under **"Workflow permissions"**:
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**

3. Click **Save**

That's it! GitHub Pages is now configured.

---

## 2. Deploy Your First Build

### Option A: Push to Main (Automatic)

```bash
cd /Users/jxc755/projects/worktrees/galaxy-architecture/branch/updates_2025

# Commit the new workflow
git add .github/workflows/deploy-docs.yml docs/GITHUB_PAGES_*.md
git commit -m "Add GitHub Pages deployment workflow"

# Push to trigger deployment
git push origin main
```

### Option B: Manual Trigger

1. Go to: `https://github.com/jmchilton/galaxy-architecture/actions`
2. Click **"Build and Deploy Documentation"** workflow
3. Click **"Run workflow"** button
4. Select branch: `main`
5. Click **"Run workflow"**

---

## 3. Monitor Deployment

1. Go to Actions tab: `https://github.com/jmchilton/galaxy-architecture/actions`

2. Watch the workflow run (takes ~5 minutes):
   - ✅ **build** job: Builds documentation
   - ✅ **deploy** job: Publishes to GitHub Pages

3. Once complete, your site is live at:
   ```
   https://jmchilton.github.io/galaxy-architecture/
   ```

---

## 4. Verify Published Site

Open in browser:
```
https://jmchilton.github.io/galaxy-architecture/
```

You should see:
- ✅ Sphinx documentation home page
- ✅ Architecture section with topics
- ✅ Embedded slide presentations work
- ✅ Images load correctly
- ✅ Navigation works

---

## Daily Workflow (After Setup)

1. **Edit content** locally in `topics/`
2. **Build and test** locally: `make build && make view-sphinx`
3. **Commit changes**: `git add . && git commit -m "Update architecture docs"`
4. **Push to main**: `git push origin main`
5. **Wait ~5 minutes** for automatic deployment
6. **Verify**: Visit `https://jmchilton.github.io/galaxy-architecture/`

---

## Troubleshooting

### Workflow Fails

Check the Actions tab for error details:
```
https://github.com/jmchilton/galaxy-architecture/actions
```

Common fixes:
- Ensure `make build` works locally first
- Check PlantUML diagrams are valid
- Run `make validate` to catch errors early

### Site Shows 404

1. Verify workflow completed successfully (green checkmark)
2. Check repository settings still have "GitHub Actions" as source
3. Wait 2-3 minutes for CDN propagation
4. Try hard refresh (Cmd+Shift+R)

### Changes Not Appearing

1. Check workflow ran (should trigger automatically on push to main)
2. Clear browser cache
3. Wait 5 minutes for build + CDN cache clear
4. Check deployment completed in Actions tab

---

## Repository Settings Checklist

Before first deployment, verify:

- [ ] Repository settings → Pages → Source: **"GitHub Actions"**
- [ ] Repository settings → Actions → Workflow permissions: **"Read and write"**
- [ ] `.github/workflows/deploy-docs.yml` exists in main branch
- [ ] Workflow file committed and pushed to GitHub

---

## Site URL

Your documentation will always be available at:

```
https://jmchilton.github.io/galaxy-architecture/
```

Bookmark this URL or add it to your repository description!

---

## What's Published

The GitHub Pages site includes:

```
https://jmchilton.github.io/galaxy-architecture/
├── index.html                      # Sphinx home page
├── architecture/
│   ├── ecosystem.html             # Architecture topics
│   ├── project-management.html
│   └── ...
├── _downloads/
│   └── */slides.html              # Standalone slide presentations
├── images/
│   ├── *.svg                      # PlantUML diagrams
│   └── *.png                      # Screenshots
└── _static/                       # Sphinx CSS/JS
```

All JavaScript (Remark.js slides) works perfectly on GitHub Pages.
