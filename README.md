Rexon Welds And Tools

Static website showcasing industrial welding machinery and power tools.

Goal: create a public GitHub repo and a shareable URL so others can view the project.

Option A — Recommended (one-command using GitHub CLI `gh`)
1. Install Git: https://git-scm.com/downloads
2. Install GitHub CLI and authenticate: https://cli.github.com/
3. From PowerShell run (replace `<your-username>` if desired):

```powershell
cd C:\rexonweldsandtools
# create & push repo, then set remote
gh repo create rexonweldsandtools --public --source=. --remote=origin --push
```

4. Enable GitHub Pages in the repo settings (choose `main` branch -> root) or use `gh` if available. The project URL will be:

```
https://<your-username>.github.io/rexonweldsandtools/
```

Option B — Manual (no `gh`)
1. Create a new repository on https://github.com (name: `rexonweldsandtools`).
2. Run these commands locally (replace `<your-remote-url>`):

```powershell
cd C:\rexonweldsandtools
git init
git add .
git -c user.name="Your Name" -c user.email="you@example.com" commit -m "Initial commit"
git branch -M main
git remote add origin <your-remote-url>
git push -u origin main
```

3. Enable GitHub Pages (repository Settings → Pages → select `main` branch root). URL will be:

```
https://<your-username>.github.io/rexonweldsandtools/
```

Quick alternatives
- Drag & drop the site folder to Netlify Drop (https://app.netlify.com/drop) for an immediate public URL.
- Use GitHub Gist for single files (not suitable for full site).

Script
- There's a helper script `create-repo.ps1` included which attempts the automated flow. Run it locally after installing Git and (optionally) `gh`:

```powershell
# allow running the script once
powershell -ExecutionPolicy Bypass -File .\create-repo.ps1 -RepoName rexonweldsandtools
```
