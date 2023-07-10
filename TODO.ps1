$hoje = Get-Date -Format "yyyy-MM-dd"
cd D:\var\www\html\github-trending
.\.venv\Scripts\activate.bat
python scraper.py
cp "$hoje.md" .\docs\README.md
git add .
git commit -m "$hoje.md"
git push
.\.venv\Scripts\deactivate.bat
