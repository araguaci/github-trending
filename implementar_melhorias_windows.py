#!/usr/bin/env python3
# coding:utf-8

"""
GitHub Trending Scraper - Implementação de Melhorias (Windows Compatible)
========================================================================

Este script implementa todas as melhorias sugeridas para o projeto
GitHub Trending Scraper, compatível com Windows.

Autor: Assistant AI
Data: 2025-01-27
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class GitHubTrendingImprovements:
    def __init__(self):
        self.docs_path = "docs"
        self.repos_path = os.path.join(self.docs_path, "repos")
        self.scripts = [
            "generate_analytics.py",
            "generate_repo_pages.py", 
            "generate_docsify_config.py"
        ]
        
    def check_environment(self):
        """Verifica se o ambiente está configurado corretamente"""
        print("Verificando ambiente...")
        
        # Verificar se estamos no diretório correto
        if not os.path.exists("scraper.py"):
            print("Erro: Execute este script no diretório raiz do projeto")
            return False
        
        # Verificar se a pasta docs existe
        if not os.path.exists(self.docs_path):
            print("Erro: Pasta 'docs' não encontrada")
            return False
        
        # Verificar se a pasta repos existe
        if not os.path.exists(self.repos_path):
            print("Erro: Pasta 'docs/repos' não encontrada")
            return False
        
        print("Ambiente verificado com sucesso")
        return True
    
    def check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        print("Verificando dependências...")
        
        required_packages = [
            "requests",
            "pyquery", 
            "lxml",
            "html2markdown"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"OK: {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"FALTANDO: {package}")
        
        if missing_packages:
            print(f"\nPacotes faltando: {', '.join(missing_packages)}")
            print("Execute: pip install " + " ".join(missing_packages))
            return False
        
        print("Todas as dependências estão instaladas")
        return True
    
    def backup_existing_files(self):
        """Faz backup dos arquivos existentes"""
        print("Fazendo backup dos arquivos existentes...")
        
        backup_files = [
            "docs/index.html",
            "docs/_sidebar.md"
        ]
        
        for file_path in backup_files:
            if os.path.exists(file_path):
                backup_path = file_path + ".backup"
                try:
                    with open(file_path, 'r', encoding='utf-8') as original:
                        with open(backup_path, 'w', encoding='utf-8') as backup:
                            backup.write(original.read())
                    print(f"Backup criado: {backup_path}")
                except Exception as e:
                    print(f"Erro ao criar backup de {file_path}: {e}")
            else:
                print(f"Arquivo não encontrado: {file_path}")
    
    def run_scripts(self):
        """Executa os scripts de melhoria"""
        print("Executando scripts de melhoria...")
        
        for script in self.scripts:
            if os.path.exists(script):
                print(f"\nExecutando {script}...")
                try:
                    # Configurar encoding para Windows
                    result = subprocess.run([sys.executable, script], 
                                          capture_output=True, text=True,
                                          encoding='utf-8', errors='replace')
                    
                    if result.returncode == 0:
                        print(f"SUCESSO: {script} executado")
                        if result.stdout:
                            print(f"Output: {result.stdout.strip()}")
                    else:
                        print(f"ERRO ao executar {script}")
                        print(f"Erro: {result.stderr.strip()}")
                        return False
                        
                except Exception as e:
                    print(f"ERRO ao executar {script}: {e}")
                    return False
            else:
                print(f"Script não encontrado: {script}")
        
        return True
    
    def verify_results(self):
        """Verifica se os resultados foram gerados corretamente"""
        print("Verificando resultados...")
        
        expected_files = [
            "docs/stats.md",
            "docs/trending-now.md", 
            "docs/categories.md",
            "docs/index_enhanced.html"
        ]
        
        all_generated = True
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"OK: {file_path} ({file_size} bytes)")
            else:
                print(f"FALTANDO: {file_path}")
                all_generated = False
        
        return all_generated
    
    def update_docsify_config(self):
        """Atualiza a configuração do Docsify"""
        print("Atualizando configuração Docsify...")
        
        enhanced_config = "docs/index_enhanced.html"
        current_config = "docs/index.html"
        
        if os.path.exists(enhanced_config):
            try:
                with open(enhanced_config, 'r', encoding='utf-8') as enhanced:
                    with open(current_config, 'w', encoding='utf-8') as current:
                        current.write(enhanced.read())
                print("Configuração Docsify atualizada")
                return True
            except Exception as e:
                print(f"Erro ao atualizar configuração: {e}")
                return False
        else:
            print("Arquivo de configuração melhorada não encontrado")
            return False
    
    def generate_summary(self):
        """Gera resumo das melhorias implementadas"""
        print("\n" + "="*60)
        print("RESUMO DAS MELHORIAS IMPLEMENTADAS")
        print("="*60)
        
        print("\nNOVAS FUNCIONALIDADES:")
        print("   - Dashboard de estatísticas gerais")
        print("   - Página de trending em tempo real")
        print("   - Sistema de categorização inteligente")
        print("   - Páginas de repositórios melhoradas")
        print("   - Configuração Docsify avançada")
        
        print("\nARQUIVOS CRIADOS:")
        print("   - docs/stats.md - Estatísticas gerais")
        print("   - docs/trending-now.md - Trending atual")
        print("   - docs/categories.md - Categorias")
        print("   - docs/index_enhanced.html - Config Docsify")
        
        print("\nPROXIMOS PASSOS:")
        print("   1. Testar a documentação localmente")
        print("   2. Verificar responsividade")
        print("   3. Configurar analytics (opcional)")
        print("   4. Deploy para produção")
        
        print("\nCOMO TESTAR:")
        print("   python -m http.server 8000")
        print("   Acesse: http://localhost:8000/docs/")
        
        print("\nIMPLEMENTACAO CONCLUIDA!")
        print("="*60)
    
    def run(self):
        """Executa o processo completo de implementação"""
        print("GitHub Trending Scraper - Implementação de Melhorias")
        print("="*60)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Verificar ambiente
        if not self.check_environment():
            return False
        
        # Verificar dependências
        if not self.check_dependencies():
            return False
        
        # Fazer backup
        self.backup_existing_files()
        
        # Executar scripts
        if not self.run_scripts():
            print("Falha na execução dos scripts")
            return False
        
        # Verificar resultados
        if not self.verify_results():
            print("Falha na verificação dos resultados")
            return False
        
        # Atualizar configuração Docsify
        if not self.update_docsify_config():
            print("Falha na atualização da configuração")
            return False
        
        # Gerar resumo
        self.generate_summary()
        
        return True


def main():
    """Função principal"""
    try:
        improvements = GitHubTrendingImprovements()
        success = improvements.run()
        
        if success:
            print("\nImplementação concluída com sucesso!")
            print("Seu projeto GitHub Trending Scraper agora tem:")
            print("   - Dashboard interativo de estatísticas")
            print("   - Sistema de categorização inteligente")
            print("   - Páginas de repositórios melhoradas")
            print("   - Interface Docsify avançada")
            print("   - Análise de tendências em tempo real")
            
            print("\nPara mais informações, consulte:")
            print("   - SUGESTOES_MELHORIAS_DOCSIFY.md")
            print("   - README_IMPLEMENTACAO.md")
            
        else:
            print("\nImplementação falhou!")
            print("Verifique os erros acima e tente novamente")
            
    except KeyboardInterrupt:
        print("\nImplementação cancelada pelo usuário")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Verifique o ambiente e tente novamente")


if __name__ == '__main__':
    main()
