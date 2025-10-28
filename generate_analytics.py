# coding:utf-8

import os
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import requests

class GitHubTrendingAnalyzer:
    def __init__(self, docs_path="docs"):
        self.docs_path = docs_path
        self.repos_path = os.path.join(docs_path, "repos")
        self.data = self.load_trending_data()
    
    def load_trending_data(self):
        """Carrega dados históricos de trending"""
        data = []
        
        # Carregar dados dos arquivos de trending
        for year in range(2017, 2026):
            year_path = os.path.join(self.docs_path, str(year))
            if os.path.exists(year_path):
                for file in os.listdir(year_path):
                    if file.endswith('.md') and file != 'index.md':
                        file_path = os.path.join(year_path, file)
                        data.extend(self.parse_trending_file(file_path))
        
        return data
    
    def parse_trending_file(self, file_path):
        """Extrai dados de um arquivo de trending"""
        data = []
        date = os.path.basename(file_path).replace('.md', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extrair repositórios por linguagem
            sections = re.split(r'#### (\w+)', content)[1:]
            
            for i in range(0, len(sections), 2):
                language = sections[i]
                repos_text = sections[i+1] if i+1 < len(sections) else ""
                
                # Extrair repositórios individuais
                repo_pattern = r'\* \[([^\]]+)\]\(([^)]+)\)(?:\s*⭐\s*([^:]+))?:\s*(.+)'
                matches = re.findall(repo_pattern, repos_text)
                
                for match in matches:
                    repo_name, url, stars, description = match
                    data.append({
                        'date': date,
                        'language': language,
                        'repo_name': repo_name,
                        'url': url,
                        'stars': self.parse_stars(stars),
                        'description': description
                    })
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
        
        return data
    
    def parse_stars(self, stars_str):
        """Converte string de estrelas para número"""
        if not stars_str or stars_str == "N/A":
            return 0
        
        stars_str = stars_str.replace(',', '').replace('⭐', '').strip()
        
        if 'k' in stars_str.lower():
            try:
                return int(float(stars_str.lower().replace('k', '')) * 1000)
            except:
                return 0
        else:
            try:
                return int(stars_str)
            except:
                return 0
    
    def generate_stats_page(self):
        """Gera página de estatísticas gerais"""
        stats = self.calculate_statistics()
        
        content = f"""# 📊 GitHub Trending Statistics

*Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 🌟 Top Repositories by Trending Frequency

| Repository | Language | Trending Days | First Seen | Last Seen | Max Stars |
|------------|----------|---------------|------------|-----------|-----------|
"""
        
        # Top 20 repositórios mais frequentes
        for i, repo in enumerate(stats['most_frequent'][:20], 1):
            content += f"| {i}. [{repo['name']}]({repo['url']}) | {repo['language']} | {repo['days']} | {repo['first_seen']} | {repo['last_seen']} | {repo['max_stars']:,} |\n"
        
        content += f"""

## 📈 Language Distribution

| Language | Repositories | Total Trending Days | Avg Stars |
|----------|--------------|---------------------|-----------|
"""
        
        for lang, data in stats['by_language'].items():
            content += f"| {lang} | {data['count']} | {data['total_days']} | {data['avg_stars']:,} |\n"
        
        content += f"""

## 🚀 Growth Leaders (Last 30 Days)

| Repository | Language | Growth | Current Stars |
|------------|----------|--------|---------------|
"""
        
        for repo in stats['growth_leaders'][:10]:
            content += f"| [{repo['name']}]({repo['url']}) | {repo['language']} | +{repo['growth']:,} | {repo['current_stars']:,} |\n"
        
        content += f"""

## 📅 Trending Calendar

### Most Active Months
| Month | Trending Repositories | Unique Languages |
|-------|----------------------|------------------|
"""
        
        for month, data in stats['monthly_activity'].items():
            content += f"| {month} | {data['repos']} | {data['languages']} |\n"
        
        # Salvar arquivo
        stats_file = os.path.join(self.docs_path, 'stats.md')
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Estatísticas geradas: {stats_file}")
    
    def calculate_statistics(self):
        """Calcula estatísticas dos dados"""
        stats = {
            'most_frequent': [],
            'by_language': defaultdict(lambda: {'count': 0, 'total_days': 0, 'stars': []}),
            'growth_leaders': [],
            'monthly_activity': defaultdict(lambda: {'repos': 0, 'languages': set()})
        }
        
        # Agrupar por repositório
        repo_data = defaultdict(lambda: {
            'name': '',
            'url': '',
            'language': '',
            'days': 0,
            'first_seen': '',
            'last_seen': '',
            'stars': [],
            'descriptions': []
        })
        
        for item in self.data:
            repo_key = item['repo_name']
            repo_data[repo_key]['name'] = item['repo_name']
            repo_data[repo_key]['url'] = item['url']
            repo_data[repo_key]['language'] = item['language']
            repo_data[repo_key]['days'] += 1
            repo_data[repo_key]['stars'].append(item['stars'])
            repo_data[repo_key]['descriptions'].append(item['description'])
            
            if not repo_data[repo_key]['first_seen'] or item['date'] < repo_data[repo_key]['first_seen']:
                repo_data[repo_key]['first_seen'] = item['date']
            
            if not repo_data[repo_key]['last_seen'] or item['date'] > repo_data[repo_key]['last_seen']:
                repo_data[repo_key]['last_seen'] = item['date']
            
            # Estatísticas por linguagem
            stats['by_language'][item['language']]['count'] += 1
            stats['by_language'][item['language']]['total_days'] += 1
            stats['by_language'][item['language']]['stars'].append(item['stars'])
            
            # Atividade mensal
            month = item['date'][:7]  # YYYY-MM
            stats['monthly_activity'][month]['repos'] += 1
            stats['monthly_activity'][month]['languages'].add(item['language'])
        
        # Processar dados agregados
        for repo_name, data in repo_data.items():
            max_stars = max(data['stars']) if data['stars'] else 0
            stats['most_frequent'].append({
                'name': data['name'],
                'url': data['url'],
                'language': data['language'],
                'days': data['days'],
                'first_seen': data['first_seen'],
                'last_seen': data['last_seen'],
                'max_stars': max_stars
            })
        
        # Ordenar por frequência
        stats['most_frequent'].sort(key=lambda x: x['days'], reverse=True)
        
        # Calcular médias por linguagem
        for lang, data in stats['by_language'].items():
            data['avg_stars'] = sum(data['stars']) // len(data['stars']) if data['stars'] else 0
        
        # Converter sets para contadores
        for month, data in stats['monthly_activity'].items():
            data['languages'] = len(data['languages'])
        
        return stats
    
    def generate_trending_now_page(self):
        """Gera página de trending atual"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = f"{today}.md"
        
        if not os.path.exists(today_file):
            print(f"⚠️ Arquivo de hoje não encontrado: {today_file}")
            return
        
        # Ler dados de hoje
        with open(today_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair repositórios
        sections = re.split(r'#### (\w+)', content)[1:]
        trending_data = {}
        
        for i in range(0, len(sections), 2):
            language = sections[i]
            repos_text = sections[i+1] if i+1 < len(sections) else ""
            
            repo_pattern = r'\* \[([^\]]+)\]\(([^)]+)\)(?:\s*⭐\s*([^:]+))?:\s*(.+)'
            matches = re.findall(repo_pattern, repos_text)
            
            trending_data[language] = []
            for match in matches:
                repo_name, url, stars, description = match
                trending_data[language].append({
                    'name': repo_name,
                    'url': url,
                    'stars': self.parse_stars(stars),
                    'description': description
                })
        
        # Gerar página
        page_content = f"""# 🔥 Trending Now - Live Dashboard

*Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📅 Today's Top Trending

### 🌟 Overall Trending
"""
        
        # Combinar todos os repositórios e ordenar por estrelas
        all_repos = []
        for lang, repos in trending_data.items():
            all_repos.extend(repos)
        
        all_repos.sort(key=lambda x: x['stars'], reverse=True)
        
        for i, repo in enumerate(all_repos[:10], 1):
            page_content += f"{i}. [{repo['name']}]({repo['url']}) ⭐ {repo['stars']:,}\n"
        
        page_content += "\n### 🐍 Python Trending\n"
        for i, repo in enumerate(trending_data.get('python', [])[:5], 1):
            page_content += f"{i}. [{repo['name']}]({repo['url']}) ⭐ {repo['stars']:,}\n"
        
        page_content += "\n### ⚡ JavaScript Trending\n"
        for i, repo in enumerate(trending_data.get('javascript', [])[:5], 1):
            page_content += f"{i}. [{repo['name']}]({repo['url']}) ⭐ {repo['stars']:,}\n"
        
        page_content += "\n### 🦀 Rust Trending\n"
        for i, repo in enumerate(trending_data.get('rust', [])[:5], 1):
            page_content += f"{i}. [{repo['name']}]({repo['url']}) ⭐ {repo['stars']:,}\n"
        
        # Salvar arquivo
        trending_file = os.path.join(self.docs_path, 'trending-now.md')
        with open(trending_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        print(f"Página de trending atual gerada: {trending_file}")
    
    def generate_categories_page(self):
        """Gera página de categorias"""
        categories = {
            'AI & Machine Learning': ['ai', 'ml', 'machine', 'learning', 'neural', 'deep', 'tensorflow', 'pytorch', 'openai', 'langchain'],
            'Web Development': ['web', 'frontend', 'backend', 'react', 'vue', 'angular', 'svelte', 'next', 'nuxt'],
            'Developer Tools': ['tool', 'dev', 'cli', 'vscode', 'editor', 'debug', 'testing', 'build'],
            'Mobile Development': ['mobile', 'ios', 'android', 'flutter', 'react-native', 'expo'],
            'Data Science': ['data', 'analytics', 'pandas', 'numpy', 'jupyter', 'notebook'],
            'DevOps & Infrastructure': ['devops', 'docker', 'kubernetes', 'ci', 'cd', 'deploy', 'infrastructure'],
            'Game Development': ['game', 'gaming', 'unity', 'unreal', 'engine', 'graphics'],
            'Security': ['security', 'crypto', 'encryption', 'auth', 'oauth', 'jwt']
        }
        
        # Classificar repositórios por categoria
        categorized_repos = defaultdict(list)
        
        for item in self.data:
            repo_name = item['repo_name'].lower()
            description = item['description'].lower()
            
            for category, keywords in categories.items():
                if any(keyword in repo_name or keyword in description for keyword in keywords):
                    categorized_repos[category].append({
                        'name': item['repo_name'],
                        'url': item['url'],
                        'language': item['language'],
                        'stars': item['stars'],
                        'description': item['description']
                    })
                    break
        
        # Gerar página
        content = "# 🏷️ Repository Categories\n\n"
        
        for category, repos in categorized_repos.items():
            content += f"## {category}\n\n"
            
            # Ordenar por estrelas
            repos.sort(key=lambda x: x['stars'], reverse=True)
            
            for repo in repos[:10]:  # Top 10 por categoria
                content += f"- [{repo['name']}]({repo['url']}) ({repo['language']}) ⭐ {repo['stars']:,}\n"
                content += f"  - {repo['description']}\n\n"
        
        # Salvar arquivo
        categories_file = os.path.join(self.docs_path, 'categories.md')
        with open(categories_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Página de categorias gerada: {categories_file}")
    
    def update_sidebar(self):
        """Atualiza sidebar com novas páginas"""
        sidebar_file = os.path.join(self.docs_path, '_sidebar.md')
        
        new_entries = [
            "- [📊 Statistics](/stats)",
            "- [🔥 Trending Now](/trending-now)",
            "- [🏷️ Categories](/categories)",
            "- [📈 Analytics](/analytics)"
        ]
        
        try:
            with open(sidebar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Adicionar novas entradas se não existirem
            for entry in new_entries:
                if entry not in content:
                    content = content.replace("- [repos](/repos/index)", f"- [repos](/repos/index)\n{entry}")
            
            with open(sidebar_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("Sidebar atualizada")
        except Exception as e:
            print(f"Erro ao atualizar sidebar: {e}")


def main():
    """Função principal"""
    print("GitHub Trending Analyzer")
    print("=" * 50)
    
    analyzer = GitHubTrendingAnalyzer()
    
    print("Gerando estatísticas...")
    analyzer.generate_stats_page()
    
    print("Gerando página de trending atual...")
    analyzer.generate_trending_now_page()
    
    print("Gerando categorias...")
    analyzer.generate_categories_page()
    
    print("Atualizando sidebar...")
    analyzer.update_sidebar()
    
    print("\nAnálise concluída!")
    print("Arquivos gerados:")
    print("   - docs/stats.md")
    print("   - docs/trending-now.md")
    print("   - docs/categories.md")
    print("   - docs/_sidebar.md (atualizada)")


if __name__ == '__main__':
    main()
