[CmdletBinding()]
param (
    [string] $Path
)

# Function to activate Python virtual environment
function Open-Venv {
    param (
        [string] $path
    )
    $venvPath = Join-Path $path ".venv"

    if (Test-Path $venvPath -PathType Container) {
        . "$venvPath\Scripts\Activate"
    }
    else {
        python -m venv "$venvPath" --prompt trans
        . "$venvPath\Scripts\Activate"
        pip install -r (Join-Path $path "requirements.txt")
    }
}

Open-Venv $Path
try {
    python (Join-Path $Path "src-python\app.py")
}
finally {
    deactivate
}
