# coding:utf-8

import datetime
import codecs
import requests
import os
import time
import html2markdown
import re
from pyquery import PyQuery as pq


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(date, filename):
    with open(filename, 'w') as f:
        f.write("## " + date + "\n")


def extract_stars_from_html_improved(item):
    """Versão melhorada para extrair estrelas do HTML do GitHub"""
    i = pq(item)
    
    # Múltiplos seletores para encontrar estrelas
    selectors = [
        'a[href*="/stargazers"]',
        'a[href*="/stars"]', 
        '.octicon-star',
        '.js-social-count',
        '[data-ga-click*="star"]',
        '[aria-label*="star"]',
        '.social-count',
        '.Counter',
        'span[title*="star"]',
        'a[title*="star"]',
        '.text-bold',
        '.f6',
        '.text-gray'
    ]
    
    for selector in selectors:
        elements = i(selector)
        for element in elements:
            element_text = pq(element).text().strip()
            
            # Procura por padrões de números de estrelas
            patterns = [
                r'([\d,\.]+[kK]?)\s*stars?',  # "1.2k stars"
                r'([\d,\.]+[kK]?)',           # "1.2k" ou "1234"
                r'(\d{1,3}(?:,\d{3})*)',     # "1,234"
                r'(\d+\.?\d*[kK])',          # "1.2k" ou "12k"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, element_text, re.IGNORECASE)
                if match:
                    stars_str = match.group(1)
                    formatted_stars = format_stars_count(stars_str)
                    if formatted_stars != "N/A":
                        return formatted_stars
    
    # Fallback: procurar em todos os elementos do item
    all_text = i.text()
    patterns = [
        r'([\d,\.]+[kK]?)\s*stars?',
        r'([\d,\.]+[kK]?)',
        r'(\d{1,3}(?:,\d{3})*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        for match in matches:
            formatted_stars = format_stars_count(match)
            if formatted_stars != "N/A":
                # Verificar se é um número razoável de estrelas
                try:
                    num_stars = int(formatted_stars.replace(',', ''))
                    if 0 <= num_stars <= 1000000:  # Range razoável
                        return formatted_stars
                except:
                    continue
    
    return "N/A"


def format_stars_count(stars_str):
    """Formata o número de estrelas para um formato consistente"""
    if not stars_str:
        return "N/A"
    
    stars_str = str(stars_str).replace(',', '').strip()
    
    # Remover caracteres não numéricos exceto k/K e ponto
    stars_str = re.sub(r'[^\d\.kK]', '', stars_str)
    
    if not stars_str:
        return "N/A"
    
    try:
        if 'k' in stars_str.lower():
            # Remove 'k' e converte para número
            number = float(stars_str.lower().replace('k', ''))
            return f"{int(number * 1000):,}"
        else:
            # Número simples
            number = float(stars_str)
            return f"{int(number):,}"
    except (ValueError, TypeError):
        return "N/A"


def get_stars_from_api(owner, repo_name, github_token=None):
    """Obtém o número de estrelas usando a API do GitHub"""
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'
    }
    
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('stargazers_count', 0):,}"
        else:
            print(f"⚠️ API Error {response.status_code} for {owner}/{repo_name}")
            return "N/A"
    except Exception as e:
        print(f"❌ API Error for {owner}/{repo_name}: {e}")
        return "N/A"


def scrape_with_stars_improved(language, filename, use_api=False, github_token=None):
    """Versão melhorada que inclui estrelas com múltiplas estratégias"""
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'pt-BR,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    
    print(f"🔍 Scraping: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"❌ Erro HTTP {r.status_code} para {url}")
            return
    except Exception as e:
        print(f"❌ Erro de conexão para {url}: {e}")
        return
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')
    
    if language == "":
        markdown = html2markdown.convert(r.content)
        with open("trending.md", "w", encoding="utf-8") as file:
            file.write(markdown)

    with codecs.open(filename, "a", "utf-8") as f:
        if language == "":
            language = "trending"
            
        f.write('\n#### {language}\n'.format(language=language))

        success_count = 0
        total_count = 0

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            
            if not title or not url:
                continue
                
            total_count += 1
            
            # Extrair informações do repositório
            repo_name = title.split('/')[-1].strip() if '/' in title else title.strip()
            owner_name = owner.strip() if owner else ""
            
            # Obter número de estrelas com estratégia híbrida
            stars = "N/A"
            
            if use_api and owner_name and repo_name:
                # Tentar API primeiro
                stars = get_stars_from_api(owner_name, repo_name, github_token)
                if stars != "N/A":
                    success_count += 1
                else:
                    # Fallback para HTML se API falhar
                    stars = extract_stars_from_html_improved(item)
                    if stars != "N/A":
                        success_count += 1
                time.sleep(0.1)  # Rate limiting
            else:
                # Usar apenas HTML
                stars = extract_stars_from_html_improved(item)
                if stars != "N/A":
                    success_count += 1
            
            # Formatar saída com estrelas
            f.write(u"* [{title}]({url}) ⭐ {stars}: {description}\n".format(
                title=title, url=url, stars=stars, description=description
            ))
        
        # Estatísticas
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"📊 {language}: {success_count}/{total_count} estrelas obtidas ({success_rate:.1f}%)")


def job_improved(use_api=False, github_token=None):
    """Versão melhorada da função job"""
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    print("🚀 Iniciando GitHub Trending Scraper Melhorado")
    print(f"📅 Data: {strdate}")
    print(f"📁 Arquivo: {filename}")
    print(f"🔧 Modo: {'API' if use_api else 'HTML'}")
    print("=" * 50)

    # create markdown file
    createMarkdown(strdate, filename)

    # write markdown with stars
    languages = ['', 'c#', 'c++', 'go', 'html', 'javascript', 'php', 'rust', 'swift', 'vue', 'python', 'typescript']
    
    for lang in languages:
        scrape_with_stars_improved(lang, filename, use_api, github_token)
        time.sleep(1)  # Delay entre linguagens
    
    print("=" * 50)
    print("✅ Scraping concluído!")
    print(f"📁 Arquivo gerado: {filename}")
    
    # git add commit push
    # git_add_commit_push(strdate, filename)


if __name__ == '__main__':
    # Para usar a API do GitHub, defina seu token aqui
    # GITHUB_TOKEN = "seu_token_aqui"
    GITHUB_TOKEN = None
    
    print("🔧 GitHub Trending Scraper - Versão Melhorada")
    print("=" * 50)
    print("💡 Dicas:")
    print("   - use_api=True para maior precisão (mais lento)")
    print("   - use_api=False para maior velocidade")
    print("   - Configure GITHUB_TOKEN para usar API")
    print("=" * 50)
    
    # use_api=True para usar a API do GitHub (mais preciso, mas mais lento)
    # use_api=False para extrair do HTML (mais rápido, mas pode ser menos preciso)
    job_improved(use_api=False, github_token=GITHUB_TOKEN)
