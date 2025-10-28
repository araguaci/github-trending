# Configuração para o GitHub Trending Scraper com Estrelas

## Como usar os scripts melhorados

### 1. Script Simples com Estrelas (`scraper_with_stars.py`)
Este é o script mais simples que adiciona estrelas ao script original:

```bash
python scraper_with_stars.py
```

**Características:**
- ✅ Extrai estrelas diretamente do HTML
- ✅ Mais rápido
- ✅ Não precisa de token da API
- ✅ Compatível com o script original

### 2. Script Avançado (`scraper_improved.py`)
Este script oferece mais opções e funcionalidades:

```bash
# Usando apenas HTML (mais rápido)
python scraper_improved.py

# Usando API do GitHub (mais preciso)
python scraper_improved.py --use-api --token SEU_TOKEN_AQUI
```

**Características:**
- ✅ Duas opções: HTML ou API
- ✅ Rate limiting automático
- ✅ Tratamento de erros melhorado
- ✅ Formatação consistente de números

## Configuração da API do GitHub

Para usar a API do GitHub e obter dados mais precisos:

1. **Criar um Personal Access Token:**
   - Vá para: https://github.com/settings/tokens
   - Clique em "Generate new token"
   - Selecione apenas o escopo `public_repo`
   - Copie o token gerado

2. **Usar o token:**
   ```python
   GITHUB_TOKEN = "seu_token_aqui"
   job(use_api=True, github_token=GITHUB_TOKEN)
   ```

## Limites da API

- **Sem autenticação:** 60 requisições por hora
- **Com autenticação:** 5.000 requisições por hora
- **Rate limiting:** O script inclui delays automáticos

## Formato de Saída

O novo formato inclui estrelas:

```markdown
* [nome/repositorio](https://github.com/nome/repositorio) ⭐ 1,234: Descrição do repositório
```

## Exemplo de Saída

```markdown
## 2025-01-15

#### python
* [microsoft/agent-lightning](https://github.com/microsoft/agent-lightning) ⭐ 2,456: The absolute trainer to light up AI agents.
* [public-apis/public-apis](https://github.com/public-apis/public-apis) ⭐ 15,678: A collective list of free APIs
```

## Troubleshooting

### Problemas comuns:

1. **"N/A" nas estrelas:**
   - O GitHub pode ter mudado a estrutura HTML
   - Use a opção `--use-api` para maior precisão

2. **Rate limiting:**
   - Adicione delays maiores entre requisições
   - Use um token de autenticação

3. **Erro de conexão:**
   - Verifique sua conexão com a internet
   - O GitHub pode estar temporariamente indisponível

## Melhorias Implementadas

- ✅ **Extração de estrelas** do HTML
- ✅ **Integração com API** do GitHub
- ✅ **Formatação consistente** de números
- ✅ **Rate limiting** automático
- ✅ **Tratamento de erros** robusto
- ✅ **Compatibilidade** com script original
- ✅ **Configuração flexível**
