# cicd.ps1
# This script assumes it is run from the "utilz" folder.
# The "src" folder is one level up from utilz.

function Lint-Code {
    Write-Host "Running lint..."
    Push-Location ..\src
    try {
        flake8 --max-line-length=120 --ignore=E203,E501,W503 .
        Write-Host "Linting passed."
    } catch {
        Write-Error "Linting failed: $($_.Exception.Message)"
    }
    Pop-Location
}

function Build-Package {
    Write-Host "Building package..."
    Push-Location ..\src
    try {
        python -m build
        Write-Host "Build completed successfully."
    } catch {
        Write-Error "Build failed: $($_.Exception.Message)"
    }
    Pop-Location
}

function Ship-Package {
    Write-Host "Shipping package..."
    Push-Location ..\src
    try {
        # ... (Implement configuration and environment variable handling) ...
        $repoConfig = "..\utilz\.pypirc"
        $distPath = ".\dist\*"
        twine upload --config-file "$repoConfig" $distPath
        Write-Host "Ship completed successfully."
    } catch {
        Write-Error "Ship failed: $($_.Exception.Message)"
    }
    Pop-Location
}

function Cleanup {
    Write-Host "Running cleanup..."
    Push-Location ..\src
    try {
        if (Test-Path -Path ".\dist") {
            Remove-Item -Path ".\dist" -Recurse -Force
            Write-Host "Removed dist directory."
        }
        Get-ChildItem -Path . -Directory -Filter "*.egg-info" | ForEach-Object {
            Remove-Item -Path $_.FullName -Recurse -Force
            Write-Host "Removed $($_.Name)."
        }
        Write-Host "Cleanup completed."
    } finally {
        Pop-Location
    }
}

$running = $true
while ($running) {
    Write-Host "CI/CD Menu:"
    Write-Host "1) Lint"
    Write-Host "2) Build"
    Write-Host "3) Build + Ship + Cleanup"
    Write-Host "4) Cleanup only"
    Write-Host "5) Exit"
    $choice = Read-Host "Enter your choice (1-5)"
    switch ($choice) {
        "1" { Lint-Code }
        "2" { Build-Package }
        "3" {
            Build-Package
            Ship-Package
            Cleanup
        }
        "4" { Cleanup }
        "5" {
            Write-Host "Exiting..."
            $running = $false
        }
        default {
            Write-Host "Invalid option. Please try again."
        }
    }
}