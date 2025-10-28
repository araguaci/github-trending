# 🔑 Guia Completo: Como Criar Token do GitHub para scraper_improved.py

## 📋 Pré-requisitos
- Conta no GitHub
- Acesso à internet
- Python instalado

## 🚀 Passo a Passo para Criar o Token

### **Passo 1: Acessar as Configurações do GitHub**

1. **Faça login** na sua conta do GitHub
2. **Clique no seu avatar** (canto superior direito)
3. **Selecione "Settings"** no menu dropdown

### **Passo 2: Navegar para Personal Access Tokens**

1. **No menu lateral esquerdo**, procure por "Developer settings"
2. **Clique em "Developer settings"**
3. **Selecione "Personal access tokens"**
4. **Clique em "Tokens (classic)"**

### **Passo 3: Gerar Novo Token**

1. **Clique no botão "Generate new token"**
2. **Selecione "Generate new token (classic)"**

### **Passo 4: Configurar o Token**

#### **Informações Básicas:**
- **Note**: `GitHub Trending Scraper` (ou qualquer nome descritivo)
- **Expiration**: Escolha uma data de expiração (recomendo 90 dias ou 1 ano)

#### **Selecionar Escopos (Scopes):**
✅ **Marque APENAS os seguintes escopos:**

- **`public_repo`** - Acesso completo a repositórios públicos
  - ✅ Read access to public repositories
  - ✅ Write access to public repositories

#### **Escopos NÃO necessários (NÃO marque):**
- ❌ `repo` (acesso completo a repositórios privados)
- ❌ `user` (informações do usuário)
- ❌ `admin` (acesso administrativo)
- ❌ `delete_repo` (deletar repositórios)

### **Passo 5: Gerar e Copiar o Token**

1. **Clique em "Generate token"** (botão verde)
2. **⚠️ IMPORTANTE**: Copie o token imediatamente
3. **⚠️ ATENÇÃO**: Você só verá o token UMA vez!

## 🔧 Como Usar o Token no Script

### **Opção 1: Modificar o Script Diretamente**

Edite o arquivo `scraper_improved.py` na linha 236:

```python
if __name__ == '__main__':
    # Substitua "seu_token_aqui" pelo token copiado
    GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    # use_api=True para usar a API do GitHub (mais preciso, mas mais lento)
    # use_api=False para extrair do HTML (mais rápido, mas pode ser menos preciso)
    job(use_api=True, github_token=GITHUB_TOKEN)
```

### **Opção 2: Usar Variável de Ambiente (Recomendado)**

#### **Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
python scraper_improved.py
```

#### **Windows (CMD):**
```cmd
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python scraper_improved.py
```

#### **Linux/Mac:**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
python scraper_improved.py
```

### **Opção 3: Arquivo de Configuração**

Crie um arquivo `.env` na mesma pasta do script:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

E modifique o script para ler o arquivo:

```python
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

if __name__ == '__main__':
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    if GITHUB_TOKEN:
        job(use_api=True, github_token=GITHUB_TOKEN)
    else:
        print("Token não encontrado! Usando modo HTML.")
        job(use_api=False, github_token=None)
```

## 📊 Limites da API com Token

### **Sem Token:**
- ⚠️ **60 requisições por hora**
- ⚠️ **Muito limitado** para scraping completo

### **Com Token:**
- ✅ **5.000 requisições por hora**
- ✅ **Suficiente** para scraping de todas as linguagens
- ✅ **Dados mais precisos** e atualizados

## 🔒 Segurança do Token

### **⚠️ IMPORTANTE - Nunca faça isso:**
- ❌ **NÃO** compartilhe o token publicamente
- ❌ **NÃO** commite o token no Git
- ❌ **NÃO** deixe o token em código público

### **✅ Boas Práticas:**
- ✅ **Use variáveis de ambiente**
- ✅ **Adicione `.env` ao `.gitignore`**
- ✅ **Renove o token periodicamente**
- ✅ **Use escopos mínimos necessários**

## 🧪 Testando o Token

### **Teste Simples:**

```python
import requests

def test_token(token):
    url = "https://api.github.com/user"
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'GitHub-Trending-Scraper'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Token válido!")
        print(f"Usuário: {response.json().get('login')}")
        print(f"Rate limit: {response.headers.get('X-RateLimit-Limit')}")
    else:
        print("❌ Token inválido!")
        print(f"Status: {response.status_code}")

# Teste seu token
test_token("seu_token_aqui")
```

## 🚨 Solução de Problemas

### **Erro 401 (Unauthorized):**
- ✅ Verifique se o token está correto
- ✅ Verifique se o token não expirou
- ✅ Verifique se o escopo `public_repo` está marcado

### **Erro 403 (Forbidden):**
- ✅ Você pode ter atingido o limite de rate
- ✅ Aguarde 1 hora ou use um token diferente

### **Erro 404 (Not Found):**
- ✅ Verifique se o repositório existe
- ✅ Verifique se não há erro de digitação

## 📝 Exemplo de Uso Completo

```python
# scraper_improved.py modificado
if __name__ == '__main__':
    # Token do GitHub (substitua pelo seu)
    GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    print("🚀 Iniciando scraping com estrelas...")
    print("📊 Usando API do GitHub para maior precisão")
    
    # Executar com API (mais preciso)
    job(use_api=True, github_token=GITHUB_TOKEN)
    
    print("✅ Scraping concluído!")
    print("📁 Arquivo gerado: {date}.md")
```

## 🎯 Resultado Esperado

Com o token configurado, você terá:

- ✅ **Estrelas precisas** de todos os repositórios
- ✅ **Rate limit alto** (5.000 req/hora)
- ✅ **Dados atualizados** em tempo real
- ✅ **Sem limitações** de scraping

---

**💡 Dica**: Comece testando com `use_api=False` para verificar se o script funciona, depois mude para `use_api=True` com o token para obter dados mais precisos!
