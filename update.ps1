# Atualiza o Low Ticket Kit no Windows: git pull + religa skills novas.
#   powershell -ExecutionPolicy Bypass -File update.ps1              atualiza agora, mostrando o que mudou
#   powershell -ExecutionPolicy Bypass -File update.ps1 -Background  usado pelo hook do Claude Code: no máximo 1x a cada 6h, silencioso
param([switch]$Background)
$ErrorActionPreference = 'SilentlyContinue'
$KitHome  = Split-Path -Parent $MyInvocation.MyCommand.Path
$Stamp    = Join-Path $KitHome '.last-update'
$Interval = 6 * 3600

function Do-Update([bool]$Quiet) {
  $before = git -C $KitHome rev-parse HEAD
  git -C $KitHome fetch -q origin
  if ($LASTEXITCODE -ne 0) { return }
  git -C $KitHome reset -q --hard origin/main
  if ($LASTEXITCODE -ne 0) { return }
  $after = git -C $KitHome rev-parse HEAD
  [int][double]::Parse((Get-Date -UFormat %s)) | Set-Content $Stamp
  if ($before -ne $after) {
    & (Join-Path $KitHome 'install.ps1') -LinkOnly
    # dependência nova que o kit passou a exigir (ex.: playwright-core do qa-performance.js), sem derrubar a atualização
    if ((Get-Command npm) -and -not (npm ls -g --depth=0 playwright-core 2>$null | Select-String playwright-core)) { npm i -g -s playwright-core 2>$null | Out-Null }
    Write-Host "Low Ticket Kit atualizado: $(Get-Content (Join-Path $KitHome 'VERSION'))"
    git -C $KitHome log --oneline "$before..$after" | Select-Object -First 10
  } elseif (-not $Quiet) { Write-Host "Low Ticket Kit já está na última versão ($(Get-Content (Join-Path $KitHome 'VERSION')))." }
}

if ($Background) {
  $last = if (Test-Path $Stamp) { [int](Get-Content $Stamp) } else { 0 }
  $now = [int][double]::Parse((Get-Date -UFormat %s))
  if (($now - $last) -lt $Interval) { exit 0 }
  Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$($MyInvocation.MyCommand.Path)`"" | Out-Null
  exit 0
}
Do-Update $false
