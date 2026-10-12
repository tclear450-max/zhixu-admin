param([switch]$Rebuild, [switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Invoke-Checked([scriptblock]$Command) {
    & $Command
    if ($LASTEXITCODE -ne 0) { throw "Command failed with exit code $LASTEXITCODE" }
}
function New-RandomBase64([int]$Length = 32) {
    $bytes = New-Object byte[] $Length
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    return [Convert]::ToBase64String($bytes)
}
try {
    Invoke-Checked { docker info --format '{{.ServerVersion}}' }
    if (!(Test-Path .env)) {
        $lines = @(
            "MYSQL_PASSWORD=$(New-RandomBase64 24)",
            "PG_PASSWORD=$(New-RandomBase64 24)",
            'MINIO_USER=hrmadmin',
            "MINIO_PASSWORD=$(New-RandomBase64 24)",
            "JWT_SECRET=$(New-RandomBase64 32)",
            'LLM_API_KEY=local-demo',
            'LLM_BASE_URL=http://demo-model:8090/compatible-mode',
            'LLM_CHAT_MODEL=hrm-demo-extractive',
            'LLM_EMBEDDING_MODEL=hrm-demo-hash-1024'
        )
        [IO.File]::WriteAllLines((Join-Path $PSScriptRoot '.env'), $lines, (New-Object Text.UTF8Encoding $false))
    }
    if ($Rebuild -or !(Test-Path 'zhixu-server/target/zhixu-server-1.0.0.jar')) {
        $mavenCommand = Get-Command mvn.cmd -ErrorAction SilentlyContinue
        if (!$mavenCommand) {
            $bundledMaven = Join-Path (Split-Path $PSScriptRoot -Parent) 'tools/apache-maven-3.9.16/bin/mvn.cmd'
            if (!(Test-Path $bundledMaven)) { throw 'Install Java 17+ and Maven 3.9+, and add them to PATH.' }
            $mavenPath = $bundledMaven
        } else { $mavenPath = $mavenCommand.Source }
        Invoke-Checked { & $mavenPath -s delivery/maven-settings.xml -f zhixu-server/pom.xml -B -ntp package '-DskipITs=true' }
    }
    if ($Rebuild -or !(Test-Path 'zhixu-admin/dist/index.html')) {
        Push-Location zhixu-admin
        try {
            Invoke-Checked { npm.cmd ci --no-audit --no-fund }
            $env:VUE_APP_BASE_API = '/api'
            $env:VUE_APP_BACKEND_TARGET = 'http://127.0.0.1:18888'
            Invoke-Checked { npm.cmd run build }
        } finally { Pop-Location }
    }
    if (!(Test-Path 'delivery/vendor/minio-source.tar.gz')) {
        New-Item -ItemType Directory 'delivery/vendor' -Force | Out-Null
        Invoke-WebRequest 'https://codeload.github.com/minio/minio/tar.gz/refs/tags/RELEASE.2025-04-22T22-12-26Z' -UseBasicParsing -OutFile 'delivery/vendor/minio-source.tar.gz'
    }
    $hash = (Get-FileHash 'delivery/vendor/minio-source.tar.gz' -Algorithm SHA256).Hash
    if ($hash -ne '1A63209927B9D1FB239B2A776B7B01D1902EFF19379A108F4BC7005EDCC0968C') { throw 'MinIO source checksum mismatch.' }
    Invoke-Checked { docker compose -f compose.delivery.yaml up -d --build --wait --wait-timeout 480 }
    Write-Host 'ZHIXU is ready: http://localhost:18080/login' -ForegroundColor Green
    Write-Host 'Demo account: admin / Zx@123456'
    if (!$NoBrowser) { Start-Process 'http://localhost:18080/guide.html' }
} catch {
    Write-Error $_
    exit 1
}
