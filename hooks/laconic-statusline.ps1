$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }
$Flag = Join-Path $ClaudeDir ".laconic-active"
if (-not (Test-Path $Flag)) { exit 0 }

try {
    $Item = Get-Item -LiteralPath $Flag -Force -ErrorAction Stop
    if ($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { exit 0 }
    if ($Item.Length -gt 64) { exit 0 }
} catch {
    exit 0
}

$Mode = ""
try {
    $Raw = Get-Content -LiteralPath $Flag -TotalCount 1 -ErrorAction Stop
    if ($null -ne $Raw) { $Mode = ([string]$Raw).Trim() }
} catch {
    exit 0
}

$Mode = $Mode.ToLowerInvariant()
$Mode = ($Mode -replace '[^a-z0-9-]', '')

switch ($Mode) {
    "off" { exit 0 }
    "terse" { $Mode = "terse"; break }
    "balanced" { $Mode = "balanced"; break }
    "commit" { break }
    "review" { break }
    "compress" { break }
    default { exit 0 }
}

$Esc = [char]27
if ($Mode -eq "terse") {
    [Console]::Write("${Esc}[38;5;172m[LACONIC]${Esc}[0m")
} else {
    $Suffix = $Mode.ToUpperInvariant()
    [Console]::Write("${Esc}[38;5;172m[LACONIC:$Suffix]${Esc}[0m")
}
