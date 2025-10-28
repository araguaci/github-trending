#!/usr/bin/env python3
# coding:utf-8

"""
GitHub Trending Scraper - Script de Automação Diária Melhorado
===============================================================

Este script executa o scraping diário e atualiza a documentação
com as melhorias implementadas.

Autor: Assistant AI
Data: 2025-01-27
"""

import os
import sys
import subprocess
import datetime
import time
from pathlib import Path

class DailyAutomation:
    def __init__(self):
        self.project_path = Path("D:/_developer/github-trending")
        self.venv_path = self.project_path / "venv" / "Scripts"
        self.python_exe = self.venv_path / "python.exe"
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def log(self, message, color="white"):
        """Log com timestamp"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def check_environment(self):
        """Verifica se o ambiente está configurado"""
        self.log("Verificando ambiente...")
        
        if not self.project_path.exists():
            self.log("ERRO: Diretório do projeto não encontrado!", "red")
            return False
            
        if not self.python_exe.exists():
            self.log("ERRO: Ambiente virtual não encontrado!", "red")
            return False
            
        self.log(f"Diretório: {self.project_path}")
        return True
        
    def run_scraper(self):
        """Executa o scraper principal"""
        self.log("Executando scraping principal...")
        
        try:
            result = subprocess.run([
                str(self.python_exe), 
                "scraper_fixed.py"
            ], cwd=self.project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Scraping executado com sucesso!")
                return True
            else:
                self.log(f"ERRO no scraping: {result.stderr}", "red")
                return False
                
        except Exception as e:
            self.log(f"ERRO ao executar scraper: {e}", "red")
            return False
            
    def update_readme(self):
        """Atualiza os arquivos README"""
        self.log("Atualizando README...")
        
        trending_file = self.project_path / f"{self.today}.md"
        
        if not trending_file.exists():
            self.log(f"ERRO: Arquivo {self.today}.md não encontrado!", "red")
            return False
            
        try:
            # Copiar para docs/README.md
            docs_readme = self.project_path / "docs" / "README.md"
            docs_readme.write_text(trending_file.read_text(encoding='utf-8'), encoding='utf-8')
            
            # Copiar para README.md
            main_readme = self.project_path / "README.md"
            main_readme.write_text(trending_file.read_text(encoding='utf-8'), encoding='utf-8')
            
            self.log("README atualizado com sucesso!")
            return True
            
        except Exception as e:
            self.log(f"ERRO ao atualizar README: {e}", "red")
            return False
            
    def run_improvement_scripts(self):
        """Executa os scripts de melhoria da documentação"""
        self.log("Executando scripts de melhoria da documentação...")
        
        scripts = [
            ("generate_analytics.py", "Gerando estatísticas"),
            ("generate_repo_pages.py", "Gerando páginas de repositórios"),
            ("generate_docsify_config.py", "Atualizando configuração Docsify")
        ]
        
        for script, description in scripts:
            self.log(f"  - {description}...")
            
            try:
                result = subprocess.run([
                    str(self.python_exe), script
                ], cwd=self.project_path, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log(f"  ✓ {description} - Sucesso!")
                else:
                    self.log(f"  ✗ {description} - Erro: {result.stderr}", "red")
                    
            except Exception as e:
                self.log(f"  ✗ {description} - Erro: {e}", "red")
                
        # Atualizar configuração Docsify se o arquivo melhorado existir
        enhanced_config = self.project_path / "docs" / "index_enhanced.html"
        current_config = self.project_path / "docs" / "index.html"
        
        if enhanced_config.exists():
            self.log("  - Aplicando configuração Docsify melhorada...")
            try:
                current_config.write_text(enhanced_config.read_text(encoding='utf-8'), encoding='utf-8')
                self.log("  ✓ Configuração Docsify aplicada!")
            except Exception as e:
                self.log(f"  ✗ Erro ao aplicar configuração: {e}", "red")
                
    def git_commit_push(self):
        """Faz commit e push das alterações"""
        self.log("Fazendo commit das alterações...")
        
        try:
            # Git add
            subprocess.run(["git", "add", "."], cwd=self.project_path, check=True)
            
            # Git commit
            commit_message = f"Atualização diária {self.today} - Trending + Melhorias documentação"
            subprocess.run([
                "git", "commit", "-m", commit_message
            ], cwd=self.project_path, check=True)
            
            # Git push
            subprocess.run(["git", "push"], cwd=self.project_path, check=True)
            
            self.log("Commit e push realizados com sucesso!")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"ERRO no git: {e}", "red")
            return False
        except Exception as e:
            self.log(f"ERRO inesperado no git: {e}", "red")
            return False
            
    def generate_summary(self):
        """Gera resumo da execução"""
        self.log("=" * 50)
        self.log("EXECUÇÃO CONCLUÍDA COM SUCESSO!")
        self.log("=" * 50)
        self.log("Arquivos atualizados:")
        self.log(f"  - {self.today}.md (trending do dia)")
        self.log("  - docs/README.md")
        self.log("  - README.md")
        self.log("  - docs/stats.md (estatísticas)")
        self.log("  - docs/trending-now.md (trending atual)")
        self.log("  - docs/categories.md (categorias)")
        self.log("  - docs/index.html (configuração Docsify)")
        self.log("=" * 50)
        
        next_run = datetime.datetime.now() + datetime.timedelta(days=1)
        self.log(f"Próxima execução: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 50)
        
    def run(self):
        """Executa o processo completo"""
        self.log("=" * 50)
        self.log("GitHub Trending Scraper - Execução Diária")
        self.log(f"Data: {self.timestamp}")
        self.log("=" * 50)
        
        # Verificar ambiente
        if not self.check_environment():
            return False
            
        # Executar scraper
        if not self.run_scraper():
            return False
            
        # Atualizar README
        if not self.update_readme():
            return False
            
        # Executar scripts de melhoria
        self.run_improvement_scripts()
        
        # Git commit e push
        if not self.git_commit_push():
            return False
            
        # Gerar resumo
        self.generate_summary()
        
        return True


def main():
    """Função principal"""
    try:
        automation = DailyAutomation()
        success = automation.run()
        
        if success:
            print("\n🎉 Automação diária concluída com sucesso!")
        else:
            print("\n❌ Automação diária falhou!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Automação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
