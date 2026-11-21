@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; $url='http://127.0.0.1:8520'; function Ready { try { (Invoke-WebRequest -UseBasicParsing ( $url + '/_stcore/health' ) -TimeoutSec 2).Content -eq 'ok' } catch { $false } }; if (-not (Ready)) { $python=Join-Path $env:LOCALAPPDATA 'Programs\Python\Python314\python.exe'; if (-not (Test-Path -LiteralPath $python)) { $python=(Get-Command python.exe -ErrorAction Stop).Source }; $server=Start-Process -FilePath $python -ArgumentList '-B','-m','streamlit','run','meridian_app.py','--server.port','8520','--server.address','127.0.0.1','--server.headless','true' -WindowStyle Hidden -PassThru; for ($i=0; $i -lt 20; $i++) { if (Ready) { break }; if ($server.HasExited) { throw 'Streamlit stopped. Check the Python dependencies in README.md.' }; Start-Sleep -Milliseconds 500 }; if (-not (Ready)) { throw 'The app did not start in time.' } }; Start-Process $url"
if errorlevel 1 pause
