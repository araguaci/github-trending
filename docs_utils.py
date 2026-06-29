# coding:utf-8

from collections import defaultdict
from datetime import datetime
from pathlib import Path

MONTHS = {
    '01': 'JAN', '02': 'FEV', '03': 'MAR', '04': 'ABR',
    '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AGO',
    '09': 'SET', '10': 'OUT', '11': 'NOV', '12': 'DEC',
}


def project_root(base_path=None):
    if base_path is None:
        return Path(__file__).resolve().parent
    return Path(base_path)


def daily_md_path(date_str=None, base_path=None):
    """Retorna o caminho do arquivo diário em docs/YYYY/YYYY-MM-DD.md."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    year = date_str[:4]
    year_dir = project_root(base_path) / 'docs' / year
    year_dir.mkdir(parents=True, exist_ok=True)
    return year_dir / f'{date_str}.md'


def generate_year_index(year, base_path=None):
    """Gera o conteúdo do index.md anual com links relativos."""
    year = str(year)
    year_dir = project_root(base_path) / 'docs' / year
    if not year_dir.exists():
        return ''

    files = sorted(
        f for f in year_dir.glob(f'{year}-*.md')
        if f.is_file()
    )

    by_month = defaultdict(list)
    for file_path in files:
        name = file_path.stem
        by_month[name[5:7]].append(name)

    lines = [f'# {year}', '']
    for month in sorted(by_month.keys()):
        lines.append(f'### {MONTHS[month]}')
        lines.append('')
        for name in by_month[month]:
            lines.append(f'- [{name}]({year}/{name}.md)')
        lines.append('')

    return '\n'.join(lines).rstrip() + '\n'


def update_year_index(date_str=None, base_path=None):
    """Regenera docs/YYYY/index.md com base nos arquivos existentes."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    year = date_str[:4]
    year_dir = project_root(base_path) / 'docs' / year
    year_dir.mkdir(parents=True, exist_ok=True)

    index_path = year_dir / 'index.md'
    index_path.write_text(generate_year_index(year, base_path), encoding='utf-8')
    return index_path
