# coding:utf-8

import requests
import os
from datetime import datetime

def test_github_token(token=None):
    """Testa se o token do GitHub está funcionando corretamente"""
    
    if not token:
        print("❌ Token não fornecido!")
        return False
    
    print("🔍 Testando token do GitHub...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Teste 1: Informações do usuário
    print("📋 Teste 1: Informações do usuário")
    url = "https://api.github.com/user"
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'GitHub-Trending-Scraper-Test'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Token válido!")
            print(f"👤 Usuário: {user_data.get('login')}")
            print(f"📧 Email: {user_data.get('email', 'Não público')}")
            print(f"🏢 Empresa: {user_data.get('company', 'Não informado')}")
        else:
            print(f"❌ Erro na autenticação: {response.status_code}")
            print(f"📝 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # Teste 2: Rate limits
    print("\n📊 Teste 2: Rate limits")
    rate_limit_url = "https://api.github.com/rate_limit"
    
    try:
        response = requests.get(rate_limit_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            rate_data = response.json()
            core_limit = rate_data.get('resources', {}).get('core', {})
            
            print(f"✅ Rate limit obtido!")
            print(f"🔢 Limite: {core_limit.get('limit', 'N/A')} requisições/hora")
            print(f"📈 Restantes: {core_limit.get('remaining', 'N/A')} requisições")
            print(f"🔄 Reset em: {datetime.fromtimestamp(core_limit.get('reset', 0))}")
            
            # Verificar se tem limite suficiente
            if core_limit.get('limit', 0) >= 5000:
                print("✅ Limite alto detectado - Token autenticado!")
            else:
                print("⚠️ Limite baixo - Token pode não estar autenticado")
                
        else:
            print(f"❌ Erro ao obter rate limit: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar rate limit: {e}")
    
    # Teste 3: Acesso a repositório público
    print("\n📁 Teste 3: Acesso a repositório público")
    test_repo_url = "https://api.github.com/repos/microsoft/vscode"
    
    try:
        response = requests.get(test_repo_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Acesso a repositório público OK!")
            print(f"📦 Repositório: {repo_data.get('full_name')}")
            print(f"⭐ Estrelas: {repo_data.get('stargazers_count', 0):,}")
            print(f"🍴 Forks: {repo_data.get('forks_count', 0):,}")
            print(f"📅 Criado: {repo_data.get('created_at', 'N/A')}")
        else:
            print(f"❌ Erro ao acessar repositório: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar acesso a repositório: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Resumo do Teste:")
    print("✅ Token configurado corretamente!")
    print("✅ Pronto para usar com scraper_improved.py")
    print("✅ Use: job(use_api=True, github_token=token)")
    
    return True

def test_without_token():
    """Testa o acesso sem token (modo limitado)"""
    
    print("🔍 Testando acesso SEM token...")
    print("-" * 50)
    
    # Teste de rate limit sem token
    url = "https://api.github.com/rate_limit"
    headers = {
        'User-Agent': 'GitHub-Trending-Scraper-Test'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            rate_data = response.json()
            core_limit = rate_data.get('resources', {}).get('core', {})
            
            print(f"📊 Limite sem token: {core_limit.get('limit', 'N/A')} req/hora")
            print(f"📈 Restantes: {core_limit.get('remaining', 'N/A')} req/hora")
            
            if core_limit.get('limit', 0) <= 60:
                print("⚠️ Limite baixo - Recomendado usar token")
            else:
                print("✅ Limite OK para testes")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def main():
    """Função principal para testar o token"""
    
    print("🚀 GitHub Token Tester")
    print("=" * 50)
    
    # Verificar se há token em variável de ambiente
    token_from_env = os.getenv('GITHUB_TOKEN')
    
    if token_from_env:
        print("🔑 Token encontrado na variável de ambiente!")
        test_github_token(token_from_env)
    else:
        print("⚠️ Token não encontrado na variável de ambiente")
        print("💡 Você pode:")
        print("   1. Definir GITHUB_TOKEN no sistema")
        print("   2. Modificar o script com seu token")
        print("   3. Testar modo sem token")
        
        # Perguntar se quer testar sem token
        choice = input("\n❓ Testar modo sem token? (s/n): ").lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            test_without_token()
        
        # Perguntar se quer inserir token manualmente
        choice = input("\n❓ Inserir token manualmente? (s/n): ").lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            token = input("🔑 Cole seu token aqui: ").strip()
            if token:
                test_github_token(token)
            else:
                print("❌ Token vazio!")

if __name__ == '__main__':
    main()
