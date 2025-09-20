# Deployment Guide - Cloudflare Pages

## Quick Deploy to Cloudflare Pages

### 1. Connect Your Repository

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Click "Create a project"
3. Connect to GitHub and select `XvsMetroid/singularity`

### 2. Configure Build Settings

Use these exact settings in Cloudflare:

- **Build command**: `pip install -r requirements.txt && mkdocs build`
- **Build output directory**: `site`
- **Environment variables**:
  - `PYTHON_VERSION`: `3.11`

### 3. Deploy

Click "Save and Deploy" - your site will be live in ~2 minutes!

## Your Site URLs

- **Production**: `https://singularity.pages.dev` (or your custom domain)
- **Preview**: Each PR gets a unique preview URL

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
mkdocs serve
# Visit http://localhost:8000

# Build static site
mkdocs build
# Output in site/ directory
```

## Automatic Deployments

Every push to `main` branch automatically deploys to production.

## Custom Domain (Optional)

1. Go to your Cloudflare Pages project settings
2. Click "Custom domains"
3. Add your domain (e.g., `axiomengine.org`)
4. Follow DNS configuration instructions

## Troubleshooting

- If build fails, check Python version is set to 3.11
- Ensure all markdown files have proper frontmatter
- Check that image paths are relative, not absolute