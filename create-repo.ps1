<#
create-repo.ps1
Helper script to initialize a local git repo, commit, create a GitHub repo with `gh` (if available), and push.
Run locally after installing Git and (optionally) GitHub CLI.
#>
param(
    [string]$RepoName = "rexonweldsandtools",
    [string]$Username = $null
)

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

Write-Info "Checking for git..."
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Err "Git not found in PATH. Install Git first: https://git-scm.com/downloads"
    exit 1
}

# Initialize repo if not exists
if (-not (Test-Path .git)) {
    Write-Info "Initializing local git repository..."
    git init
    git add .
    git -c user.name="Local User" -c user.email="local@localhost" commit -m "Initial commit: add website files"
} else {
    Write-Info "Local git repository already exists. Adding & committing changes..."
    git add .
    git commit -m "Update files" 2>$null
}

# Attempt to use gh to create the repo and push
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Info "GitHub CLI detected. Creating remote repo and pushing..."
    try {
        gh repo create $RepoName --public --source=. --remote=origin --push --confirm | Out-Null
        Write-Info "Repository created and pushed."
    } catch {
        Write-Warn "gh repo create failed: $_. Attempting to add remote manually (if provided)."
    }
} else {
    Write-Warn "GitHub CLI (gh) not found. Please create the repo on github.com and then add remote and push."
    Write-Host "After creating the repo on github.com, run the following (replace <your-remote-url>):" -ForegroundColor White
    Write-Host "git remote add origin <your-remote-url>" -ForegroundColor Green
    Write-Host "git branch -M main" -ForegroundColor Green
    Write-Host "git push -u origin main" -ForegroundColor Green
    exit 0
}

# If we have a username param or can detect username via gh, compute Pages URL
if (-not $Username -and (Get-Command gh -ErrorAction SilentlyContinue)) {
    try { $Username = gh api user --jq .login } catch { $Username = $null }
}

if ($Username) {
    $pagesUrl = "https://$Username.github.io/$RepoName/"
    Write-Info "Possible Pages URL after enabling Pages: $pagesUrl"
    Write-Host "Note: To serve via GitHub Pages, open the repo Settings → Pages and select the 'main' branch (root) as the source. Then use the URL above." -ForegroundColor Yellow
} else {
    Write-Info "Created repo. Visit GitHub to enable Pages (Settings → Pages). The Pages URL will be https://<your-username>.github.io/$RepoName/ after enabling." 
}

Write-Info "Done. If push failed, check the git output and ensure you are authenticated with GitHub."