$hoje = Get-Date -Format "yyyy-MM-dd"
$ano = $hoje.Substring(0, 4)
$arquivoDiario = ".\docs\$ano\$hoje.md"
cd D:/_developer/github-trending
.\venv\Scripts\activate.bat
python scraper_fixed.py
cp "$arquivoDiario" .\docs\README.md
cp "$arquivoDiario" .\README.md
git add .
git commit -m "$hoje.md"
git push
.\venv\Scripts\deactivate.bat
