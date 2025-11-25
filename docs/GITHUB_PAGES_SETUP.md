# GitHub Pages Setup

This repository is configured to automatically build and publish documentation to GitHub Pages.

## How It Works

1. **Push to `main` branch** triggers the GitHub Actions workflow
2. **Build process** runs `make build` which:
   - Validates all topics
   - Generates training slides (Remark.js presentations)
   - Generates Sphinx documentation
   - Builds PlantUML diagrams
   - Creates final HTML output in `doc/build/html/`
3. **Deployment** uploads `doc/build/html/` to GitHub Pages
4. **Site is live** at: `https://jmchilton.github.io/galaxy-architecture/`

## Initial Setup (One-Time Configuration)

### 1. Configure Repository Settings

Go to your repository settings on GitHub:

```
https://github.com/jmchilton/galaxy-architecture/settings/pages
```

Configure:
- **Source**: GitHub Actions (not "Deploy from a branch")
- This option appears under "Build and deployment" section

### 2. Enable Workflows

Ensure GitHub Actions are enabled:
- Go to `Settings` → `Actions` → `General`
- Under "Actions permissions", select "Allow all actions and reusable workflows"
- Under "Workflow permissions", select "Read and write permissions"

### 3. Trigger First Build

Option A - Push to main:
```bash
git push origin main
```

Option B - Manual trigger:
- Go to `Actions` tab
- Select "Build and Deploy Documentation"
- Click "Run workflow" → "Run workflow"

### 4. Verify Deployment

After ~5 minutes:
- Check the Actions tab for build status
- Visit: `https://jmchilton.github.io/galaxy-architecture/`

## Workflow Details

### Build Environment

The workflow (`../.github/workflows/deploy-docs.yml`) installs:
- Python 3.11 with uv package manager
- Java 17 (for PlantUML)
- PlantUML and Graphviz
- All Python dependencies from `pyproject.toml`

### Build Steps

1. **Validate**: `make validate` - Ensures all topics are valid
2. **Build**: `make build` - Generates all output formats
3. **Upload**: Packages `doc/build/html/` for GitHub Pages
4. **Deploy**: Publishes to GitHub Pages

### What Gets Published

The published site includes:
- **Sphinx HTML documentation** (`/architecture/*.html`)
- **Standalone slide presentations** (`/_downloads/*/slides.html`)
- **Images** (`/images/*.svg`, `*.png`)
- **Static assets** (`/_static/*`)

### .nojekyll File

The workflow creates a `.nojekyll` file to:
- Disable Jekyll processing on GitHub Pages
- Ensure files starting with `_` (like `_static/`) are served correctly
- Allow Sphinx's directory structure to work as-is

## Troubleshooting

### Build Fails

Check the Actions tab for error logs:
```
https://github.com/jmchilton/galaxy-architecture/actions
```

Common issues:
- **PlantUML errors**: Check diagram syntax in `images/*.plantuml.txt`
- **Validation errors**: Run `make validate` locally first
- **Python errors**: Ensure `pyproject.toml` dependencies are correct

### Site Not Updating

1. Check that workflow completed successfully
2. Wait ~5 minutes for CDN cache to clear
3. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
4. Check GitHub Pages settings still point to "GitHub Actions"

### 404 Errors

- Ensure `.nojekyll` file is present in deployment
- Check that paths in HTML don't assume a base URL
- Verify `doc/build/html/` contains `index.html`

## Local Development

To preview before pushing:

```bash
# Build everything
make build

# Open locally
make view-sphinx

# Or manually
open doc/build/html/index.html
```

## Manual Deployment (Alternative)

If you need to deploy manually without GitHub Actions:

```bash
# Install ghp-import
pip install ghp-import

# Build docs
make build

# Deploy to gh-pages branch
ghp-import -n -p -f doc/build/html

# Site will be live at:
# https://jmchilton.github.io/galaxy-architecture/
```

## Custom Domain (Optional)

To use a custom domain:

1. Add `CNAME` file to `doc/source/`:
   ```bash
   echo "docs.example.com" > doc/source/CNAME
   ```

2. Update GitHub Pages settings with custom domain

3. Configure DNS:
   ```
   CNAME docs.example.com -> jmchilton.github.io
   ```

## Monitoring

- **Build status**: Check Actions tab for green checkmarks
- **Build time**: Typically 3-5 minutes
- **Site URL**: Always `https://jmchilton.github.io/galaxy-architecture/`
- **Deploy frequency**: On every push to `main`

## Next Steps

After initial setup:
1. Make changes to `topics/`
2. Commit and push to `main`
3. GitHub Actions automatically rebuilds and deploys
4. Changes live in ~5 minutes
