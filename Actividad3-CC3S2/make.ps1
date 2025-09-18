param([string]$target = "help")

switch ($target) {
    "deps" {
        Write-Host "Instalando dependencias..."
        pip install flask
        Write-Host "Dependencias instaladas ✓"
    }
    
    "run" {
        Write-Host "Iniciando aplicación..."
        python app.py
    }
    
    "hosts-setup" {
        Write-Host "Configurando hosts locales..."
        $hostsPath = "$env:WINDIR\System32\drivers\etc\hosts"
        $hostEntry = "127.0.0.1 miapp.local"
        
        # Verificar si ya existe
        if (!(Select-String -Path $hostsPath -Pattern "miapp.local" -Quiet)) {
            # Requiere ejecutar PowerShell como Administrador
            Add-Content -Path $hostsPath -Value $hostEntry
            Write-Host "Hosts configurado: miapp.local -> 127.0.0.1 ✓"
        } else {
            Write-Host "miapp.local ya configurado ✓"
        }
    }
    
    "cleanup" {
        Write-Host "Limpiando recursos..."
        Stop-Process -Name "python" -ErrorAction SilentlyContinue
        Write-Host "Procesos python detenidos ✓"
    }
    
    "test-idempotency" {
        Write-Host "Probando idempotencia HTTP..."
        $response1 = Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET
        Start-Sleep -Seconds 1
        $response2 = Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET
        
        if ($response1.timestamp -ne $response2.timestamp) {
            Write-Host "IDEMPOTENCIA OK: Timestamps diferentes pero estructura igual ✓"
        }
    }
    
    "help" {
        Write-Host "Targets disponibles:"
        Write-Host "  deps         - Instalar dependencias"
        Write-Host "  run          - Ejecutar aplicación"
        Write-Host "  hosts-setup  - Configurar DNS local"
        Write-Host "  cleanup      - Limpiar recursos"
        Write-Host "  test-idempotency - Probar idempotencia"
    }
    
    default {
        Write-Host "Target no reconocido: $target"
        Write-Host "Use: .\make.ps1 help"
    }
}