# coding:utf-8

import datetime
import codecs
import requests
import os
import time
import html2markdown
import re
from pyquery import PyQuery as pq
from dotenv import load_dotenv

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


def extract_stars_from_html(item):
    """Extrai o número de estrelas diretamente do HTML"""
    i = pq(item)
    
    # Procura por elementos que contenham estrelas
    stars_elements = i('a[href*="/stargazers"], a[href*="/stars"], .octicon-star, .js-social-count')
    
    for element in stars_elements:
        element_text = pq(element).text().strip()
        # Procura por números no texto (ex: "1.2k", "500", "1.5k")
        stars_match = re.search(r'([\d,\.]+[kK]?)\s*stars?', element_text, re.IGNORECASE)
        if stars_match:
            stars_str = stars_match.group(1)
            return format_stars_count(stars_str)
    
    # Fallback: procura por qualquer número seguido de 'k' ou números simples
    for element in stars_elements:
        element_text = pq(element).text().strip()
        if 'k' in element_text.lower() or element_text.isdigit():
            stars_match = re.search(r'([\d,\.]+[kK]?)', element_text)
            if stars_match:
                stars_str = stars_match.group(1)
                return format_stars_count(stars_str)
    
    return "N/A"


def format_stars_count(stars_str):
    """Formata o número de estrelas para um formato consistente"""
    if not stars_str:
        return "N/A"
    
    stars_str = stars_str.replace(',', '').strip()
    
    if 'k' in stars_str.lower():
        # Remove 'k' e converte para número
        number = float(stars_str.lower().replace('k', ''))
        return f"{int(number * 1000):,}"
    else:
        # Número simples
        try:
            return f"{int(stars_str):,}"
        except ValueError:
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
            return "N/A"
    except Exception as e:
        print(f"Erro ao obter estrelas via API para {owner}/{repo_name}: {e}")
        return "N/A"


def scrape(language, filename, use_api=False, github_token=None):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'pt-BR,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    
    print(f"Scraping: {url}")

    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')
    
    if language == "":
        markdown = html2markdown.convert(r.content)
        with open("trending.md", "w", encoding="utf-8") as file:
            file.write(markdown)

    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(filename, "a", "utf-8") as f:
        if language == "":
            language = "trending"
            
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            
            # Extrair nome do repositório do título
            repo_name = title.split('/')[-1].strip() if '/' in title else title.strip()
            owner_name = owner.strip() if owner else ""
            
            # Obter número de estrelas
            if use_api and owner_name and repo_name:
                stars = get_stars_from_api(owner_name, repo_name, github_token)
                # Adicionar delay para respeitar rate limits da API
                time.sleep(0.1)
            else:
                stars = extract_stars_from_html(item)
            
            # Formatar saída com estrelas
            f.write(u"* [{title}]({url}) ⭐ {stars}: {description}\n".format(
                title=title, url=url, stars=stars, description=description
            ))


def scrape_with_stars(language, filename, use_api=False, github_token=None):
    """Versão melhorada que inclui estrelas"""
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'pt-BR,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    
    print(f"Scraping: {url}")

    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    
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

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            
            # Extrair informações do repositório
            repo_name = title.split('/')[-1].strip() if '/' in title else title.strip()
            owner_name = owner.strip() if owner else ""
            
            # Obter número de estrelas
            if use_api and owner_name and repo_name:
                stars = get_stars_from_api(owner_name, repo_name, github_token)
                time.sleep(0.1)  # Rate limiting
            else:
                stars = extract_stars_from_html(item)
            
            # Formatar saída com estrelas
            f.write(u"* [{title}]({url}) ⭐ {stars}: {description}\n".format(
                title=title, url=url, stars=stars, description=description
            ))


def job(use_api=False, github_token=None):
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    # write markdown with stars
    scrape_with_stars('', filename, use_api, github_token)
    scrape_with_stars('c#', filename, use_api, github_token)
    scrape_with_stars('c++', filename, use_api, github_token)
    scrape_with_stars('go', filename, use_api, github_token)
    scrape_with_stars('html', filename, use_api, github_token)
    scrape_with_stars('javascript', filename, use_api, github_token)
    scrape_with_stars('php', filename, use_api, github_token)
    scrape_with_stars('rust', filename, use_api, github_token)
    scrape_with_stars('swift', filename, use_api, github_token)
    scrape_with_stars('vue', filename, use_api, github_token)
    scrape_with_stars('python', filename, use_api, github_token)
    scrape_with_stars('typescript', filename, use_api, github_token)
    
    # git add commit push
    # git_add_commit_push(strdate, filename)

# Carregar variáveis do arquivo .env
load_dotenv()

if __name__ == '__main__':
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    if GITHUB_TOKEN:
        job(use_api=True, github_token=GITHUB_TOKEN)
    else:
        print("Token não encontrado! Usando modo HTML.")
        job(use_api=False, github_token=None)

if __name__ == '__main__':
    # Para usar a API do GitHub, defina seu token aqui
    # GITHUB_TOKEN = "seu_token_aqui"
    
    # use_api=True para usar a API do GitHub (mais preciso, mas mais lento)
    # use_api=False para extrair do HTML (mais rápido, mas pode ser menos preciso)
    job(use_api=False, github_token=GITHUB_TOKEN)
