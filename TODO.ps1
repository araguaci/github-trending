$hoje = Get-Date -Format "yyyy-MM-dd"
cd D:/_developer/github-trending
.\.venv\Scripts\activate.bat
python scraper.py
cp "$hoje.md" .\docs\README.md
cp "$hoje.md" .\README.md
git add .
git commit -m "$hoje.md"
git push
.\.venv\Scripts\deactivate.bat
