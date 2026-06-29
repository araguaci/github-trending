Backup dos scrapers antes da migração para docs/YYYY/ (2026-06-29).

Arquivos:
- scraper.py              — versão original, saída na raiz ({date}.md)
- scraper_with_stars.py   — versão original, saída na raiz
- scraper_improved.py     — versão original, saída na raiz
- scraper_fixed.py        — última versão commitada (saída na raiz)
- automacao_diaria.py     — última versão commitada (lia da raiz)

Versão atual (alinhada) usa docs_utils.py:
  daily_md_path()    -> docs/YYYY/YYYY-MM-DD.md
  update_year_index() -> docs/YYYY/index.md
