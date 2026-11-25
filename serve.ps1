# ============================================================
# Risk Management Learning - build & preview helper (PowerShell)
# Usage:
#   .\serve.ps1                     # build zh + en + landing page
#   .\serve.ps1 -Action zh          # build Chinese only
#   .\serve.ps1 -Action en          # build English only
#   .\serve.ps1 -Action serve-zh    # live preview zh at :3000
#   .\serve.ps1 -Action serve-en    # live preview en at :3001
# ============================================================

param(
    [ValidateSet('build', 'zh', 'en', 'serve-zh', 'serve-en')]
    [string]$Action = 'build',
    [int]$Port = 0
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$mdbook = Get-Command mdbook -ErrorAction SilentlyContinue
if ($mdbook) {
    $MdBook = $mdbook.Source
}
else {
    $found = Get-ChildItem -Path (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages') `
        -Recurse -Filter 'mdbook.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $MdBook = $found.FullName
    }
    else {
        Write-Error "mdbook not found. Install it first: winget install Rustlang.mdBook"
    }
}

function Restore-ZhConfig {
    if (Test-Path -LiteralPath 'book.toml.zh_bak') {
        Copy-Item -LiteralPath 'book.toml.zh_bak' -Destination 'book.toml' -Force
        Remove-Item -LiteralPath 'book.toml.zh_bak' -Force
    }
}

function Build-Zh {
    Write-Host '[build] Chinese -> book/zh'
    & $MdBook build
}

function Build-En {
    Write-Host '[build] English -> book/en'
    Copy-Item -LiteralPath 'book.toml' -Destination 'book.toml.zh_bak' -Force
    try {
        Copy-Item -LiteralPath 'book-en.toml' -Destination 'book.toml' -Force
        & $MdBook build
    }
    finally {
        Restore-ZhConfig
    }
}

function Build-All {
    Build-Zh
    Build-En
    Copy-Item -LiteralPath 'root-index.html' -Destination 'book/index.html' -Force
    Write-Host '[done] open book/index.html or run .\serve.ps1 -Action serve-zh'
}

function Serve-En {
    param([int]$ListenPort = 3001)
    Copy-Item -LiteralPath 'book.toml' -Destination 'book.toml.zh_bak' -Force
    try {
        Copy-Item -LiteralPath 'book-en.toml' -Destination 'book.toml' -Force
        & $MdBook serve -p $ListenPort
    }
    finally {
        Restore-ZhConfig
    }
}

switch ($Action) {
    'build'    { Build-All }
    'zh'       { Build-Zh }
    'en'       { Build-En }
    'serve-zh' {
        $listen = if ($Port -gt 0) { $Port } else { 3000 }
        & $MdBook serve -p $listen
    }
    'serve-en' {
        $listen = if ($Port -gt 0) { $Port } else { 3001 }
        Serve-En -ListenPort $listen
    }
}
