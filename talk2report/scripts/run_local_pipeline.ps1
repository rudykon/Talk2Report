[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$AudioPath,

    [string]$ProjectPath,
    [string]$ConfigPath,
    [string]$OutputDir,
    [switch]$ProbeOnly,
    [switch]$NoResume
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$resolvedAudio = (Resolve-Path -LiteralPath $AudioPath).Path

function Find-TranscriptProject {
    param([string]$ExplicitPath, [string]$SourcePath)

    if ($ExplicitPath) {
        $resolved = (Resolve-Path -LiteralPath $ExplicitPath).Path
        if (Test-Path -LiteralPath (Join-Path $resolved "scripts\run.ps1")) {
            return $resolved
        }
        throw "ProjectPath does not contain scripts\run.ps1: $resolved"
    }

    $starts = @((Get-Location).Path, (Split-Path -Parent $SourcePath))
    $seen = @{}
    foreach ($start in $starts) {
        $cursor = $start
        while ($cursor -and -not $seen.ContainsKey($cursor)) {
            $seen[$cursor] = $true
            $directRunner = Join-Path $cursor "scripts\run.ps1"
            if ((Split-Path -Leaf $cursor) -eq "audio_transcript_agent" -and (Test-Path -LiteralPath $directRunner)) {
                return $cursor
            }
            $nested = Join-Path $cursor "audio_transcript_agent"
            if (Test-Path -LiteralPath (Join-Path $nested "scripts\run.ps1")) {
                return $nested
            }
            $parent = Split-Path -Parent $cursor
            if ($parent -eq $cursor) {
                break
            }
            $cursor = $parent
        }
    }
    throw "Could not find audio_transcript_agent. Pass -ProjectPath explicitly."
}

$resolvedProject = Find-TranscriptProject -ExplicitPath $ProjectPath -SourcePath $resolvedAudio
$runner = Join-Path $resolvedProject "scripts\run.ps1"

if ($ConfigPath) {
    $resolvedConfig = (Resolve-Path -LiteralPath $ConfigPath).Path
} else {
    $preferredConfig = Join-Path $resolvedProject "config.yaml"
    $exampleConfig = Join-Path $resolvedProject "config.example.yaml"
    if (Test-Path -LiteralPath $preferredConfig) {
        $resolvedConfig = $preferredConfig
    } elseif (Test-Path -LiteralPath $exampleConfig) {
        $resolvedConfig = $exampleConfig
    } else {
        throw "No config.yaml or config.example.yaml was found in $resolvedProject"
    }
}

Write-Output "Project: $resolvedProject"
Write-Output "Audio: $resolvedAudio"

if ($ProbeOnly) {
    $runnerArgs = @("probe", $resolvedAudio, "--config", $resolvedConfig)
} else {
    if ($OutputDir) {
        $resolvedOutput = [IO.Path]::GetFullPath($OutputDir, (Get-Location).Path)
    } else {
        $sourceItem = Get-Item -LiteralPath $resolvedAudio
        $resolvedOutput = Join-Path $sourceItem.DirectoryName ($sourceItem.BaseName + "_transcript_run")
    }
    Write-Output "Output: $resolvedOutput"
    $runnerArgs = @(
        "run",
        $resolvedAudio,
        "--config",
        $resolvedConfig,
        "--output-dir",
        $resolvedOutput
    )
    if ($NoResume) {
        $runnerArgs += "--no-resume"
    }
}

& $runner @runnerArgs
exit $LASTEXITCODE
