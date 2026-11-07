# Low Ticket Kit — instalador para Windows (PowerShell 5.1+ ou 7).
#
#   powershell -ExecutionPolicy Bypass -File install.ps1              instala tudo
#   powershell -ExecutionPolicy Bypass -File install.ps1 -NoDeps      pula dependências (winget)
#   powershell -ExecutionPolicy Bypass -File install.ps1 -LinkOnly    só religa skills/scripts (usado pelo update.ps1)
#
# Skills viram "junctions" (atalho de pasta, não pede administrador). Scripts de bin\ são copiados
# e recopiados a cada atualização. Skill/script que você já tinha vira <nome>.bak-<data>.
# O Claude Code no Windows usa Git Bash para os scripts .sh: o instalador garante Git for Windows.
param([switch]$NoDeps, [switch]$LinkOnly, [switch]$DryRun)
$ErrorActionPreference = 'Continue'

$RepoUrl   = 'https://github.com/by-lua/low-ticket-kit.git'
$KitHome   = if ($env:LOW_TICKET_KIT_HOME) { $env:LOW_TICKET_KIT_HOME } else { Join-Path $env:USERPROFILE '.local\share\low-ticket-kit' }
$ClaudeDir = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $env:USERPROFILE '.claude' }
$Stamp     = Get-Date -Format 'yyyyMMdd-HHmmss'
$Here      = Split-Path -Parent $MyInvocation.MyCommand.Path

function Say($m)  { if (-not $LinkOnly) { Write-Host $m } }
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

# 1. Cópia fixa do repo (é dela que o auto-update puxa)
if ($Here -ne $KitHome) {
  if (-not (Have git)) { Say '→ instalando Git for Windows (winget)'; winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements; $env:Path += ';C:\Program Files\Git\cmd' }
  if (Test-Path (Join-Path $KitHome '.git')) { Say "→ atualizando $KitHome"; git -C $KitHome pull --ff-only -q }
  else { Say "→ clonando em $KitHome"; New-Item -ItemType Directory -Force -Path (Split-Path $KitHome) | Out-Null; git clone -q $RepoUrl $KitHome }
  if (-not $DryRun) { & (Join-Path $KitHome 'install.ps1') @PSBoundParameters; exit $LASTEXITCODE }
}

# 2. Dependências (winget). Cada uma só se faltar.
function Install-Deps {
  Write-Host '→ dependências do sistema (winget)'
  if (-not (Have winget)) { Write-Host '  ! winget ausente: instale à mão git, node (20+), python 3, ffmpeg, ImageMagick e Chrome'; return }
  $pk = [ordered]@{ git='Git.Git'; node='OpenJS.NodeJS.LTS'; python='Python.Python.3.12'; ffmpeg='Gyan.FFmpeg'; magick='ImageMagick.ImageMagick'; jq='jqlang.jq' }
  foreach ($k in $pk.Keys) { if (-not (Have $k)) { Write-Host "  instalando $k"; winget install -e --id $pk[$k] --accept-source-agreements --accept-package-agreements | Out-Null } }
  if (-not (Have uv)) { Write-Host '  instalando uv'; powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex" }
  $env:Path += ";$env:USERPROFILE\.local\bin"
  Write-Host '→ ferramentas Python (uv tool)'
  foreach ($t in 'yt-dlp','youtube-transcript-api','gflow-cli','browser-harness') { uv tool install -q $t 2>$null; if ($LASTEXITCODE -ne 0) { uv tool upgrade -q $t 2>$null } }
  if (Have python) { python -m pip install --user -q Pillow imagehash num2words }
  Write-Host '→ ferramentas Node (npm -g)'
  if (Have npm) { npm i -g -s agent-browser hyperframes '@remotion/cli' playwright-core; if (Have agent-browser) { agent-browser install 2>$null | Out-Null } }
  else { Write-Host '  ! npm ausente: instale Node.js 20+ (https://nodejs.org) e rode de novo' }
  $chrome = @("$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ }
  if (-not $chrome) { Write-Host '  instalando Google Chrome'; winget install -e --id Google.Chrome --accept-source-agreements --accept-package-agreements | Out-Null }
}

# 3. Ligar skills, plugin, scripts
function Link-One($src, $dst) {
  if (Test-Path $dst) {
    $it = Get-Item $dst -Force
    if ($it.LinkType -eq 'Junction') { if (@($it.Target) -contains $src) { return }; $it.Delete() }
    else { Say "  (backup: $dst.bak-$Stamp)"; Move-Item $dst "$dst.bak-$Stamp" -Force }
  }
  New-Item -ItemType Junction -Path $dst -Target $src | Out-Null
}
function Link-All {
  Say "→ skills em $ClaudeDir\skills"
  foreach ($d in 'skills','bin','plugins\cache','browser-workspace\domain-skills') { New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir $d) | Out-Null }
  Get-ChildItem (Join-Path $KitHome 'skills') -Directory | ForEach-Object { Link-One $_.FullName (Join-Path $ClaudeDir "skills\$($_.Name)") }
  Say '→ plugin get-brolls'
  Get-ChildItem (Join-Path $KitHome 'plugins') -Directory | ForEach-Object {
    $pn = $_.Name; New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir "plugins\cache\$pn") | Out-Null
    Get-ChildItem $_.FullName -Directory | ForEach-Object { Link-One $_.FullName (Join-Path $ClaudeDir "plugins\cache\$pn\$($_.Name)") } }
  Say "→ scripts em $ClaudeDir\bin (cópia, atualizada a cada update)"
  Get-ChildItem (Join-Path $KitHome 'bin') -File | Where-Object { $_.Name -notlike '*.example' } | ForEach-Object { Copy-Item $_.FullName (Join-Path $ClaudeDir "bin\$($_.Name)") -Force }
  $gc = Join-Path $ClaudeDir 'bin\gpt-contas.lst'
  if (-not (Test-Path $gc)) { Copy-Item (Join-Path $KitHome 'bin\gpt-contas.lst.example') $gc }
  Say '→ mapas de site (browser-workspace)'
  $ah = Join-Path $KitHome 'browser-workspace\agent_helpers.py'
  if (Test-Path $ah) { Copy-Item $ah (Join-Path $ClaudeDir 'browser-workspace\agent_helpers.py') -Force }
  Get-ChildItem (Join-Path $KitHome 'browser-workspace\domain-skills') -Directory -ErrorAction SilentlyContinue | ForEach-Object { Link-One $_.FullName (Join-Path $ClaudeDir "browser-workspace\domain-skills\$($_.Name)") }
}

# 3b. Google Flow pelo MCP google-flow (caminho oficial da skill flow-mcp)
# Fork com rótulos pt-BR e correção do anexo: github.com/by-lua/google-flow-mcp (branch pt-br-labels).
function Setup-FlowMcp {
  if (-not ((Have node) -and (Have npm) -and (Have git))) { Say '  ! flow-mcp: precisa de node, npm e git (pulei)'; return }
  $fm = if ($env:FLOW_MCP_HOME) { $env:FLOW_MCP_HOME } else { Join-Path $env:USERPROFILE '.local\share\google-flow-mcp' }
  $build = $false
  if (Test-Path (Join-Path $fm '.git')) {
    git -C $fm fetch -q origin pt-br-labels 2>$null
    if ($LASTEXITCODE -ne 0) { return }
    if (((git -C $fm rev-parse HEAD) -ne (git -C $fm rev-parse FETCH_HEAD)) -or -not (Test-Path (Join-Path $fm 'dist\cli.js'))) { Say '→ flow-mcp: atualizando o servidor'; git -C $fm reset -q --hard FETCH_HEAD; $build = $true }
  } else {
    Say "→ flow-mcp: baixando o servidor em $fm"
    New-Item -ItemType Directory -Force -Path (Split-Path $fm) | Out-Null
    git clone -q --branch pt-br-labels 'https://github.com/by-lua/google-flow-mcp.git' $fm
    if ($LASTEXITCODE -ne 0) { Say '  ! flow-mcp: clone falhou'; return }
    $build = $true
  }
  if ($build) {
    Push-Location $fm; npm ci --no-audit --no-fund -s 2>$null | Out-Null; npm run -s build 2>$null | Out-Null; $ok = $LASTEXITCODE -eq 0; Pop-Location
    if (-not $ok) { Say "  ! flow-mcp: build falhou (cd $fm; npm ci; npm run build)"; return }
  }
  $chrome = @("$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $chrome) { Say '  ! flow-mcp: Google Chrome não encontrado'; return }
  $cfg = Join-Path $env:USERPROFILE '.config\google-flow-mcp\config.json'
  if (-not (Test-Path $cfg)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $cfg) | Out-Null
    [pscustomobject]@{ chromePath = $chrome; userDataDir = (Join-Path $env:USERPROFILE '.google-flow-chrome'); cdpPort = 9333; stateDir = (Join-Path $env:USERPROFILE '.google-flow-mcp') } | ConvertTo-Json | Set-Content $cfg -Encoding UTF8
  }
  if (Have claude) {
    claude mcp get google-flow *> $null
    if ($LASTEXITCODE -ne 0) { Say '→ flow-mcp: registrando o MCP google-flow no Claude Code'; claude mcp add --scope user google-flow -- node (Join-Path $fm 'dist\cli.js') *> $null }
  }
}

# 4. Auto-update: hook SessionStart do Claude Code
function Add-Hook {
  Say "→ auto-update (hook SessionStart em $ClaudeDir\settings.json)"
  $upd = Join-Path $KitHome 'update.ps1'
  $cmd = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$upd`" -Background"
  $path = Join-Path $ClaudeDir 'settings.json'
  $data = if (Test-Path $path) { $raw = Get-Content $path -Raw; if ($raw.Trim()) { $raw | ConvertFrom-Json } else { [pscustomobject]@{} } } else { [pscustomobject]@{} }
  if (-not $data.PSObject.Properties['hooks']) { $data | Add-Member hooks ([pscustomobject]@{}) }
  if (-not $data.hooks.PSObject.Properties['SessionStart']) { $data.hooks | Add-Member SessionStart @() }
  foreach ($g in @($data.hooks.SessionStart)) { foreach ($h in @($g.hooks)) { if ($h.command -eq $cmd) { return } } }
  if (Test-Path $path) { Copy-Item $path "$path.bak-lowticketkit" -Force }
  $data.hooks.SessionStart = @($data.hooks.SessionStart) + ([pscustomobject]@{ hooks = @([pscustomobject]@{ type = 'command'; command = $cmd }) })
  $data | ConvertTo-Json -Depth 20 | Set-Content $path -Encoding UTF8
  Write-Host '  hook adicionado'
}

if (-not $NoDeps -and -not $LinkOnly) { Install-Deps }
Link-All
Setup-FlowMcp
if ($LinkOnly) { exit 0 }
Add-Hook
Write-Host ''
Write-Host "Pronto. Versão: $(Get-Content (Join-Path $KitHome 'VERSION') -ErrorAction SilentlyContinue)"
Write-Host 'Atualiza sozinho: toda vez que o Claude Code abre (no máximo 1x a cada 6h).'
Write-Host "Atualizar na mão: powershell -ExecutionPolicy Bypass -File `"$KitHome\update.ps1`""
Write-Host 'Google Flow (uma vez): node %USERPROFILE%\.local\share\google-flow-mcp\dist\cli.js doctor  e entre na conta na janela do Chrome que abrir.'
Write-Host 'Reinicie o Claude Code e peça: "vamos criar uma oferta low ticket do zero".'
