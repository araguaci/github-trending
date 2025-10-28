# Configuração do Agendador de Tarefas - GitHub Trending Scraper
# ================================================================

## 📋 **Configuração Recomendada**

### **Nome da Tarefa:**
`GitHub Trending Scraper - Automação Diária`

### **Descrição:**
`Executa scraping diário do GitHub Trending e atualiza documentação com melhorias`

### **Configurações:**

#### **Geral:**
- ✅ Executar independentemente do usuário estar conectado
- ✅ Executar com privilégios mais altos
- ✅ Configurar para: Windows 10/11

#### **Disparadores:**
- **Tipo:** Diário
- **Iniciar:** 06:00:00
- **Recorrer a cada:** 1 dia
- **Repetir tarefa a cada:** 1 dia
- **Por um período de:** Indefinidamente

#### **Ações:**
**Opção 1 - PowerShell (Recomendado):**
- **Ação:** Iniciar um programa
- **Programa/script:** `powershell.exe`
- **Argumentos:** `-ExecutionPolicy Bypass -File "D:\_developer\github-trending\TODO_MELHORADO.ps1"`

**Opção 2 - Batch:**
- **Ação:** Iniciar um programa
- **Programa/script:** `D:\_developer\github-trending\TODO_MELHORADO.bat`

**Opção 3 - Python (Mais robusto):**
- **Ação:** Iniciar um programa
- **Programa/script:** `D:\_developer\github-trending\venv\Scripts\python.exe`
- **Argumentos:** `D:\_developer\github-trending\automacao_diaria.py`

#### **Condições:**
- ✅ Iniciar a tarefa apenas se o computador estiver em CA
- ✅ Parar se o computador alternar para energia de bateria
- ✅ Iniciar a tarefa apenas se a seguinte conexão de rede estiver disponível: Qualquer conexão

#### **Configurações:**
- ✅ Permitir que a tarefa seja executada sob demanda
- ✅ Executar tarefa assim que possível após um início agendado perdido
- ✅ Se a tarefa falhar, reiniciar a cada: 1 minuto
- ✅ Tentar reiniciar até: 3 vezes
- ✅ Parar a tarefa se ela for executada por mais de: 2 horas

## 🚀 **Como Configurar**

### **Método 1 - Interface Gráfica:**
1. Abra o **Agendador de Tarefas** (Task Scheduler)
2. Clique em **Criar Tarefa Básica**
3. Configure conforme as especificações acima

### **Método 2 - PowerShell (Automático):**
```powershell
# Criar tarefa automaticamente
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"D:\_developer\github-trending\TODO_MELHORADO.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 06:00
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "GitHub Trending Scraper" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Executa scraping diário do GitHub Trending e atualiza documentação"
```

### **Método 3 - XML (Importar):**
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Executa scraping diário do GitHub Trending e atualiza documentação com melhorias</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-01-27T06:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT2H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -File "D:\_developer\github-trending\TODO_MELHORADO.ps1"</Arguments>
    </Exec>
  </Actions>
</Task>
```

## 📊 **Monitoramento**

### **Logs:**
- **Localização:** `C:\Windows\System32\LogFiles\TaskScheduler\`
- **Arquivo:** `GitHub Trending Scraper.log`

### **Verificar Status:**
```powershell
# Verificar última execução
Get-ScheduledTask -TaskName "GitHub Trending Scraper" | Get-ScheduledTaskInfo

# Verificar histórico
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-TaskScheduler/Operational"; ID=200} | Where-Object {$_.Message -like "*GitHub Trending Scraper*"}
```

## 🔧 **Troubleshooting**

### **Problemas Comuns:**

1. **Erro de Política de Execução:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Erro de Permissões:**
   - Executar como Administrador
   - Verificar permissões na pasta do projeto

3. **Erro de Ambiente Virtual:**
   - Verificar se o venv está ativo
   - Verificar se o Python está instalado

4. **Erro de Git:**
   - Verificar configuração do Git
   - Verificar credenciais

### **Teste Manual:**
```powershell
# Testar script manualmente
cd D:\_developer\github-trending
.\TODO_MELHORADO.ps1
```

## 📈 **Benefícios da Automação**

### **Antes:**
- ❌ Execução manual diária
- ❌ Risco de esquecer
- ❌ Sem atualização da documentação
- ❌ Sem melhorias automáticas

### **Depois:**
- ✅ **Execução automática** diária
- ✅ **Atualização contínua** da documentação
- ✅ **Melhorias automáticas** aplicadas
- ✅ **Relatórios de status** via logs
- ✅ **Recuperação automática** de falhas
- ✅ **Monitoramento** via Agendador de Tarefas

## 🎯 **Resultado Final**

Com esta configuração, seu projeto GitHub Trending Scraper será:

1. **Atualizado automaticamente** todos os dias às 06:00
2. **Documentação sempre atualizada** com as melhorias
3. **Estatísticas sempre atualizadas** com dados recentes
4. **Categorização automática** de novos repositórios
5. **Interface Docsify sempre otimizada**

**🚀 Sua plataforma de análise de tendências GitHub será sempre atualizada e otimizada automaticamente!**
