# coding:utf-8

import requests
import re
from pyquery import PyQuery as pq

def analyze_github_trending_structure():
    """Analisa a estrutura HTML atual do GitHub Trending para identificar onde estão as estrelas"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'pt-BR,zh;q=0.8'
    }

    print("🔍 Analisando estrutura HTML do GitHub Trending...")
    print("=" * 60)
    
    # Testar diferentes URLs
    urls_to_test = [
        'https://github.com/trending',
        'https://github.com/trending/python',
        'https://github.com/trending/javascript'
    ]
    
    for url in urls_to_test:
        print(f"\n📡 Testando: {url}")
        print("-" * 40)
        
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                print(f"❌ Erro HTTP {r.status_code}")
                continue
                
            d = pq(r.content)
            items = d('div.Box article.Box-row')
            
            print(f"📦 Encontrados {len(items)} repositórios")
            
            if len(items) > 0:
                # Analisar o primeiro item em detalhes
                first_item = pq(items[0])
                
                print("\n🔍 Análise do primeiro repositório:")
                print(f"   Título: {first_item('.lh-condensed a').text()}")
                print(f"   Owner: {first_item('.lh-condensed span.text-normal').text()}")
                
                # Procurar por elementos que podem conter estrelas
                print("\n⭐ Procurando elementos com estrelas:")
                
                # Seletores para testar
                selectors_to_test = [
                    'a[href*="star"]',
                    'a[href*="/stargazers"]',
                    '.octicon-star',
                    '.js-social-count',
                    '.social-count',
                    '.Counter',
                    '[data-ga-click*="star"]',
                    '[aria-label*="star"]',
                    'span[title*="star"]',
                    'a[title*="star"]',
                    '.text-bold',
                    '.f6',
                    '.text-gray',
                    '.text-muted',
                    '.d-inline-block',
                    '.mr-3',
                    '.mr-2'
                ]
                
                found_elements = []
                
                for selector in selectors_to_test:
                    elements = first_item(selector)
                    if elements:
                        for element in elements:
                            element_text = pq(element).text().strip()
                            element_html = pq(element).html()
                            element_attrs = dict(pq(element).items())
                            
                            if element_text and any(char.isdigit() for char in element_text):
                                found_elements.append({
                                    'selector': selector,
                                    'text': element_text,
                                    'html': element_html[:100] + '...' if len(element_html) > 100 else element_html,
                                    'attrs': element_attrs
                                })
                
                if found_elements:
                    print(f"   ✅ Encontrados {len(found_elements)} elementos com números:")
                    for i, elem in enumerate(found_elements[:5]):  # Mostrar apenas os primeiros 5
                        print(f"      {i+1}. Seletor: {elem['selector']}")
                        print(f"         Texto: '{elem['text']}'")
                        print(f"         HTML: {elem['html']}")
                        print(f"         Attrs: {elem['attrs']}")
                        print()
                else:
                    print("   ❌ Nenhum elemento com números encontrado")
                
                # Procurar por padrões de texto que podem ser estrelas
                print("\n🔍 Procurando padrões de texto:")
                all_text = first_item.text()
                
                patterns = [
                    r'(\d{1,3}(?:,\d{3})*)\s*stars?',
                    r'(\d+\.?\d*[kK])\s*stars?',
                    r'(\d{1,3}(?:,\d{3})*)',
                    r'(\d+\.?\d*[kK])',
                    r'(\d+)'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, all_text, re.IGNORECASE)
                    if matches:
                        print(f"   Padrão '{pattern}': {matches[:3]}")  # Mostrar apenas os primeiros 3
                
                # Salvar HTML do primeiro item para análise manual
                with open(f'debug_first_item_{url.split("/")[-1] or "trending"}.html', 'w', encoding='utf-8') as f:
                    f.write(first_item.html())
                print(f"\n💾 HTML salvo em: debug_first_item_{url.split('/')[-1] or 'trending'}.html")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("📋 Resumo da Análise:")
    print("1. Verifique os arquivos HTML salvos para análise manual")
    print("2. Use os seletores encontrados no script")
    print("3. Teste diferentes padrões de regex")
    print("4. Considere usar a API do GitHub para maior precisão")


def test_star_extraction():
    """Testa diferentes métodos de extração de estrelas"""
    
    print("\n🧪 Testando métodos de extração de estrelas...")
    print("=" * 60)
    
    # Dados de teste simulados
    test_cases = [
        "1,234 stars",
        "2.5k stars", 
        "567",
        "12.3k",
        "1,234",
        "⭐ 1,234",
        "stars 567",
        "1.2k",
        "1234 stars"
    ]
    
    def format_stars_count(stars_str):
        """Formata o número de estrelas para um formato consistente"""
        if not stars_str:
            return "N/A"
        
        stars_str = str(stars_str).replace(',', '').strip()
        stars_str = re.sub(r'[^\d\.kK]', '', stars_str)
        
        if not stars_str:
            return "N/A"
        
        try:
            if 'k' in stars_str.lower():
                number = float(stars_str.lower().replace('k', ''))
                return f"{int(number * 1000):,}"
            else:
                number = float(stars_str)
                return f"{int(number):,}"
        except (ValueError, TypeError):
            return "N/A"
    
    patterns = [
        r'([\d,\.]+[kK]?)\s*stars?',
        r'([\d,\.]+[kK]?)',
        r'(\d{1,3}(?:,\d{3})*)',
        r'(\d+\.?\d*[kK])',
    ]
    
    for test_case in test_cases:
        print(f"\n📝 Testando: '{test_case}'")
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, test_case, re.IGNORECASE)
            if match:
                stars_str = match.group(1)
                formatted = format_stars_count(stars_str)
                print(f"   Padrão {i+1}: '{stars_str}' → '{formatted}'")


if __name__ == '__main__':
    analyze_github_trending_structure()
    test_star_extraction()
