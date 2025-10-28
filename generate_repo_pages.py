# coding:utf-8

import os
import re
import requests
from datetime import datetime, timedelta
from collections import defaultdict

class RepoPageGenerator:
    def __init__(self, docs_path="docs"):
        self.docs_path = docs_path
        self.repos_path = os.path.join(docs_path, "repos")
        
    def generate_enhanced_repo_page(self, repo_name, repo_data):
        """Gera página melhorada para um repositório"""
        
        # Extrair informações do repositório
        owner, repo = repo_name.split('/') if '/' in repo_name else ('', repo_name)
        
        # Obter dados da API do GitHub
        github_data = self.get_github_data(owner, repo)
        
        # Calcular métricas de trending
        trending_stats = self.calculate_trending_stats(repo_name)
        
        # Gerar conteúdo da página
        content = f"""# 📦 Repository Analysis: {repo_name}

## 🎯 Overview
- **Repository**: [{repo_name}](https://github.com/{repo_name})
- **Language**: {repo_data.get('language', 'Unknown')}
- **Category**: {self.categorize_repo(repo_data)}
- **First Trending**: {trending_stats.get('first_seen', 'N/A')}
- **Last Trending**: {trending_stats.get('last_seen', 'N/A')}
- **Total Trending Days**: {trending_stats.get('total_days', 0)}

## 📊 Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| ⭐ Stars | {github_data.get('stars', 'N/A'):,} | {self.get_star_trend(github_data)} |
| 🍴 Forks | {github_data.get('forks', 'N/A'):,} | {self.get_fork_trend(github_data)} |
| 📝 Issues | {github_data.get('issues', 'N/A'):,} | {self.get_issue_trend(github_data)} |
| 🔄 Last Update | {github_data.get('last_update', 'N/A')} | {self.get_update_status(github_data)} |
| 📦 License | {github_data.get('license', 'N/A')} | - |
| 🌐 Website | {self.get_website_status(github_data)} | - |

## 🏷️ Trending History
"""
        
        # Adicionar histórico de trending
        for entry in trending_stats.get('history', [])[:10]:
            content += f"- **{entry['date']}**: ⭐ {entry['stars']:,} - {entry['description']}\n"
        
        content += f"""

## 🔍 Analysis
### Why is it trending?
{self.generate_trending_analysis(repo_data, github_data)}

### Key Features
{self.generate_key_features(repo_data, github_data)}

## 📈 Growth Pattern
```
Stars Growth Over Time:
{self.generate_growth_chart(trending_stats)}
```

## 🔗 Related Repositories
{self.generate_related_repos(repo_name)}

## 📚 Resources
- [GitHub Repository](https://github.com/{repo_name})
- [Documentation]({github_data.get('homepage', 'https://github.com/' + repo_name)})
- [Issues](https://github.com/{repo_name}/issues)
- [Pull Requests](https://github.com/{repo_name}/pulls)

## 🏆 Achievements
{self.generate_achievements(trending_stats, github_data)}

---
*Análise gerada automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Salvar arquivo
        filename = repo_name.replace('/', '-').lower() + '.md'
        filepath = os.path.join(self.repos_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Página gerada: {filepath}")
        return filepath
    
    def get_github_data(self, owner, repo):
        """Obtém dados da API do GitHub"""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'stars': data.get('stargazers_count', 0),
                    'forks': data.get('forks_count', 0),
                    'issues': data.get('open_issues_count', 0),
                    'last_update': data.get('updated_at', ''),
                    'license': data.get('license', {}).get('name', 'N/A'),
                    'homepage': data.get('homepage', ''),
                    'description': data.get('description', ''),
                    'language': data.get('language', ''),
                    'created_at': data.get('created_at', ''),
                    'size': data.get('size', 0)
                }
        except Exception as e:
            print(f"Erro ao obter dados do GitHub para {owner}/{repo}: {e}")
        
        return {}
    
    def calculate_trending_stats(self, repo_name):
        """Calcula estatísticas de trending para um repositório"""
        stats = {
            'total_days': 0,
            'first_seen': '',
            'last_seen': '',
            'history': [],
            'max_stars': 0,
            'avg_stars': 0
        }
        
        # Carregar dados históricos
        trending_data = self.load_repo_trending_data(repo_name)
        
        if trending_data:
            stats['total_days'] = len(trending_data)
            stats['first_seen'] = min(item['date'] for item in trending_data)
            stats['last_seen'] = max(item['date'] for item in trending_data)
            stats['history'] = sorted(trending_data, key=lambda x: x['date'], reverse=True)
            stats['max_stars'] = max(item['stars'] for item in trending_data)
            stats['avg_stars'] = sum(item['stars'] for item in trending_data) // len(trending_data)
        
        return stats
    
    def load_repo_trending_data(self, repo_name):
        """Carrega dados históricos de trending para um repositório"""
        data = []
        
        # Buscar em todos os arquivos de trending
        for year in range(2017, 2026):
            year_path = os.path.join(self.docs_path, str(year))
            if os.path.exists(year_path):
                for file in os.listdir(year_path):
                    if file.endswith('.md') and file != 'index.md':
                        file_path = os.path.join(year_path, file)
                        date = file.replace('.md', '')
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Procurar pelo repositório
                            pattern = rf'\* \[{re.escape(repo_name)}\]\([^)]+\)(?:\s*⭐\s*([^:]+))?:\s*(.+)'
                            match = re.search(pattern, content)
                            
                            if match:
                                stars_str = match.group(1) if match.group(1) else "0"
                                description = match.group(2)
                                
                                data.append({
                                    'date': date,
                                    'stars': self.parse_stars(stars_str),
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
    
    def categorize_repo(self, repo_data):
        """Categoriza um repositório baseado em sua descrição"""
        description = repo_data.get('description', '').lower()
        language = repo_data.get('language', '').lower()
        
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
        
        for category, keywords in categories.items():
            if any(keyword in description or keyword in language for keyword in keywords):
                return category
        
        return 'General'
    
    def get_star_trend(self, github_data):
        """Determina tendência de estrelas"""
        # Implementar lógica para determinar tendência
        return "↗️ Growing"
    
    def get_fork_trend(self, github_data):
        """Determina tendência de forks"""
        return "↗️ Growing"
    
    def get_issue_trend(self, github_data):
        """Determina tendência de issues"""
        return "↘️ Decreasing"
    
    def get_update_status(self, github_data):
        """Determina status de atualização"""
        last_update = github_data.get('last_update', '')
        if last_update:
            try:
                update_date = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                days_ago = (datetime.now() - update_date).days
                
                if days_ago < 7:
                    return "🟢 Active"
                elif days_ago < 30:
                    return "🟡 Recent"
                else:
                    return "🔴 Stale"
            except:
                pass
        return "❓ Unknown"
    
    def get_website_status(self, github_data):
        """Verifica se tem website"""
        return "✅ Yes" if github_data.get('homepage') else "❌ No"
    
    def generate_trending_analysis(self, repo_data, github_data):
        """Gera análise de por que está trending"""
        analysis = []
        
        description = repo_data.get('description', '').lower()
        
        if 'performance' in description:
            analysis.append("- **Performance**: Otimizações de performance")
        if 'new' in description or 'latest' in description:
            analysis.append("- **Novidade**: Lançamento de novas funcionalidades")
        if 'security' in description:
            analysis.append("- **Segurança**: Melhorias de segurança")
        if 'bug' in description or 'fix' in description:
            analysis.append("- **Correções**: Correção de bugs importantes")
        
        if not analysis:
            analysis.append("- **Crescimento**: Crescimento orgânico da comunidade")
        
        return '\n'.join(analysis)
    
    def generate_key_features(self, repo_data, github_data):
        """Gera lista de características principais"""
        features = []
        
        description = repo_data.get('description', '')
        language = repo_data.get('language', '')
        
        if language:
            features.append(f"- **Language**: {language}")
        
        if 'framework' in description.lower():
            features.append("- **Framework**: Estrutura de desenvolvimento")
        if 'library' in description.lower():
            features.append("- **Library**: Biblioteca de código")
        if 'tool' in description.lower():
            features.append("- **Tool**: Ferramenta de desenvolvimento")
        if 'api' in description.lower():
            features.append("- **API**: Interface de programação")
        
        return '\n'.join(features) if features else "- **Open Source**: Projeto de código aberto"
    
    def generate_growth_chart(self, trending_stats):
        """Gera gráfico ASCII de crescimento"""
        if not trending_stats.get('history'):
            return "No trending data available"
        
        # Implementar gráfico ASCII simples
        return "Growth chart would be generated here"
    
    def generate_related_repos(self, repo_name):
        """Gera lista de repositórios relacionados"""
        # Implementar lógica para encontrar repositórios relacionados
        return "- Related repositories would be listed here"
    
    def generate_achievements(self, trending_stats, github_data):
        """Gera lista de conquistas"""
        achievements = []
        
        if trending_stats.get('total_days', 0) > 30:
            achievements.append("- 🏆 **Consistent Trending**: Appeared in trending for 30+ days")
        
        if github_data.get('stars', 0) > 10000:
            achievements.append("- ⭐ **Star Power**: Over 10,000 stars")
        
        if github_data.get('forks', 0) > 1000:
            achievements.append("- 🍴 **Fork Popularity**: Over 1,000 forks")
        
        return '\n'.join(achievements) if achievements else "- 📈 **Growing Project**: Active development and community"


def main():
    """Função principal para testar o gerador"""
    print("Repository Page Generator")
    print("=" * 50)
    
    generator = RepoPageGenerator()
    
    # Exemplo de uso
    repo_data = {
        'language': 'TypeScript',
        'description': 'A modern web framework for building fast applications'
    }
    
    generator.generate_enhanced_repo_page('microsoft/fast', repo_data)


if __name__ == '__main__':
    main()
