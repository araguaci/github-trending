# Exemplo Prático: Configuração do Token no scraper_improved.py

## 🔧 Configuração Rápida

### **Passo 1: Criar o Token**
1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token (classic)"
3. Marque apenas: `public_repo`
4. Copie o token (começa com `ghp_`)

### **Passo 2: Configurar no Script**

Edite o arquivo `scraper_improved.py` na linha 236:

```python
if __name__ == '__main__':
    # 🔑 SUBSTITUA pelo seu token do GitHub
    GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    # ✅ use_api=True para usar API (mais preciso)
    # ⚠️ use_api=False para usar HTML (mais rápido)
    job(use_api=True, github_token=GITHUB_TOKEN)
```

### **Passo 3: Executar**

```bash
python scraper_improved.py
```

## 🧪 Testar o Token

Antes de usar, teste se o token está funcionando:

```bash
python test_token.py
```

## 📊 Comparação: Com vs Sem Token

### **Sem Token (HTML):**
- ⚡ **Rápido**: ~30 segundos
- ⚠️ **Limitado**: 60 req/hora
- 📊 **Precisão**: Média (depende do HTML)

### **Com Token (API):**
- 🐌 **Mais lento**: ~2-3 minutos
- ✅ **Alto limite**: 5.000 req/hora
- 📊 **Precisão**: Alta (dados oficiais)

## 🎯 Exemplo de Saída com Token

```markdown
## 2025-01-15

#### python
* [microsoft/agent-lightning](https://github.com/microsoft/agent-lightning) ⭐ 2,456: The absolute trainer to light up AI agents.
* [public-apis/public-apis](https://github.com/public-apis/public-apis) ⭐ 15,678: A collective list of free APIs
* [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) ⭐ 3,456: Collection of awesome LLM apps with AI Agents and RAG
```

## 🔒 Segurança

### **❌ NUNCA faça:**
- Commitar token no Git
- Compartilhar token publicamente
- Deixar token em código público

### **✅ SEMPRE faça:**
- Usar variáveis de ambiente
- Renovar token periodicamente
- Usar escopos mínimos necessários

## 🚨 Solução de Problemas

### **Erro 401:**
- ✅ Verifique se o token está correto
- ✅ Verifique se não expirou

### **Erro 403:**
- ✅ Você atingiu o rate limit
- ✅ Aguarde 1 hora

### **Token não funciona:**
- ✅ Verifique se marcou `public_repo`
- ✅ Teste com `test_token.py`
