param(
    [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

function RelPath([string]$PathValue) {
    $full = [IO.Path]::GetFullPath($PathValue)
    if ($full.StartsWith($Root)) {
        return $full.Substring($Root.Length).TrimStart("\")
    }
    return $full
}

$database = Join-Path $Root "Database"
$review = Join-Path $Root "Review_Packets"
$upscaledDir = Join-Path $Root "Output\Adobe_Stock\Daily_Production_Upscaled"
$queuePath = Join-Path $database "Adobe_Stock_Daily_Production_Queue.csv"
$rexQaPath = Join-Path $database "Adobe_Stock_Rex_Visual_QA.csv"
$ledgerPath = Join-Path $database "Adobe_Stock_Submission_Ledger.csv"
$outPath = Join-Path $database "Adobe_Stock_Local_Upscaled_Candidates.csv"
$reportPath = Join-Path $review "Adobe_Stock_Local_Upscaled_Candidates_Recovered_latest.md"
$oldManifestPath = Join-Path $Root "adobe_stock_factory\upload_ready\_superseded_exact_duplicate_batch_001_20260518_1115\batch_manifest.csv"

$meta = @{}
if (Test-Path -LiteralPath $queuePath) {
    Import-Csv -LiteralPath $queuePath | ForEach-Object {
        $seq = ($_.Queue_ID -split "-")[-1]
        if ($seq -and -not $meta.ContainsKey($seq)) {
            $meta[$seq] = $_
        }
    }
}

$decisions = @{}
if (Test-Path -LiteralPath $rexQaPath) {
    Import-Csv -LiteralPath $rexQaPath | ForEach-Object {
        if ($_.Parent_Asset_ID) {
            $decisions[$_.Parent_Asset_ID] = [PSCustomObject]@{
                Decision = ($_.Decision).ToUpperInvariant()
                Reason = $_.Reason
            }
        }
    }
}

$ledger = @{}
if (Test-Path -LiteralPath $ledgerPath) {
    Import-Csv -LiteralPath $ledgerPath | ForEach-Object {
        if ($_.Filename) {
            $ledger[$_.Filename.ToLowerInvariant()] = ($_.Status).ToUpperInvariant()
        }
    }
}

$oldManifest = @{}
if (Test-Path -LiteralPath $oldManifestPath) {
    Import-Csv -LiteralPath $oldManifestPath | ForEach-Object {
        if ($_.Parent_Asset_ID) {
            $oldManifest[$_.Parent_Asset_ID] = $_
        }
    }
}

$rows = New-Object System.Collections.Generic.List[object]
$pattern = [regex]"adobe_stock_(?<date>\d{8})_(?<seq>\d{3})_(?<variant>u[1-4])_3000x2000\.jpg$"

Get-ChildItem -LiteralPath $upscaledDir -Filter "adobe_stock_*_3000x2000.jpg" | Sort-Object Name | ForEach-Object {
    $match = $pattern.Match($_.Name)
    if (-not $match.Success) {
        return
    }

    $date = $match.Groups["date"].Value
    $seq = $match.Groups["seq"].Value
    $variantLower = $match.Groups["variant"].Value
    $variant = $variantLower.ToUpperInvariant()
    $parent = "ADOBE-STOCK-$date-$seq-$variant"
    $asset = "$parent-LOCAL3000"
    $queueRow = $meta[$seq]
    $pendingSource = "adobe_stock_factory\Pending_Upscale\adobe_stock_${date}_${seq}_${variantLower}.png"
    $ledgerFile = "adobe-stock-$date-$seq-$variantLower.jpg"

    $width = 3000
    $height = 2000

    $qaStatus = "HOLD_RECOVERED_NEEDS_DETAIL_RECHECK"
    $uploadStatus = "HOLD_DO_NOT_UPLOAD"
    $issues = "recovered after index truncation; rerun Python detail QA before adding new upload packs"

    if ($oldManifest.ContainsKey($parent)) {
        $qaStatus = "QA_PASS_ADOBE_MACRO_FULL_RES_PRODUCTION"
        $uploadStatus = "QA_PASS_NOT_UPLOADED"
        $issues = "recovered from pre-truncation upload-ready manifest; exact-hash dedupe required before upload"
    }

    if ($ledger.ContainsKey($ledgerFile)) {
        $qaStatus = "QA_PASS_ADOBE_MACRO_FULL_RES_PRODUCTION"
        $uploadStatus = $ledger[$ledgerFile]
        $issues = "ledger status recovered; do not reuse for new upload pack"
    }

    if ($decisions.ContainsKey($parent)) {
        $decision = $decisions[$parent]
        if ($decision.Decision -eq "REJECT") {
            $qaStatus = "HOLD_REX_REJECTED_NO_UPLOAD"
            $uploadStatus = "HOLD_DO_NOT_UPLOAD"
            $issues = "REX_REJECTED_VISUAL_DIRECTION; $($decision.Reason)"
        } elseif ($decision.Decision -eq "HOLD") {
            $qaStatus = "HOLD_REX_REVIEW_NO_UPLOAD"
            $uploadStatus = "HOLD_DO_NOT_UPLOAD"
            $issues = "REX_HELD_FOR_REVIEW; $($decision.Reason)"
        }
    }

    $title = "High resolution texture background"
    $keywords = "texture background,background,texture,abstract,design,commercial use"
    if ($oldManifest.ContainsKey($parent)) {
        $title = $oldManifest[$parent].Title
        $keywords = $oldManifest[$parent].Keywords
    } elseif ($queueRow) {
        $title = $queueRow.Adobe_Title
        $keywords = $queueRow.Adobe_Keywords
    }

    $category = "8"
    if ($queueRow -and $queueRow.Adobe_Category) {
        $category = $queueRow.Adobe_Category
    }

    $createdUsingAi = "true"
    if ($queueRow -and $queueRow.Created_Using_AI) {
        $createdUsingAi = $queueRow.Created_Using_AI
    }

    $family = "Sequence $seq"
    if ($queueRow -and $queueRow.Family) {
        $family = $queueRow.Family
    }

    $rows.Add([PSCustomObject]@{
        Asset_ID = $asset
        Parent_Asset_ID = $parent
        Family = $family
        Title = $title
        Keywords = $keywords
        Category = $category
        Created_Using_AI = $createdUsingAi
        Source_Path = if (Test-Path -LiteralPath (Join-Path $Root $pendingSource)) { $pendingSource } else { "" }
        Upscaled_Path = RelPath $_.FullName
        Source_Width = ""
        Source_Height = ""
        Width = $width
        Height = $height
        Pixels = ($width * $height)
        File_Bytes = $_.Length
        Edge_Detail_Score = ""
        Sharp_Tile_Coverage = ""
        QA_Status = $qaStatus
        Upload_Status = $uploadStatus
        Issues = $issues
    })
}

$rows | Export-Csv -LiteralPath $outPath -NoTypeInformation -Encoding utf8

$readyCount = ($rows | Where-Object {
    $_.QA_Status -eq "QA_PASS_ADOBE_MACRO_FULL_RES_PRODUCTION" -and
    $_.Upload_Status -eq "QA_PASS_NOT_UPLOADED"
}).Count

$qaLines = $rows | Group-Object QA_Status | Sort-Object Count -Descending | ForEach-Object {
    "- $($_.Name): $($_.Count)"
}
$uploadLines = $rows | Group-Object Upload_Status | Sort-Object Count -Descending | ForEach-Object {
    "- $($_.Name): $($_.Count)"
}

$report = @(
    "# Adobe Stock Local Upscaled Candidate Recovery",
    "",
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
    "",
    "- Existing local-upscaled files indexed: $($rows.Count)",
    "- Ready and not yet uploaded/submitted: $readyCount",
    "- Recovery mode: PowerShell conservative restore after source index truncation; Python detail scores remain blank until runtime is available.",
    "- Output CSV: Database\Adobe_Stock_Local_Upscaled_Candidates.csv",
    "",
    "## QA Status",
    ""
) + $qaLines + @(
    "",
    "## Upload Status",
    ""
) + $uploadLines + @(
    "",
    "## Policy",
    "",
    "- Only rows recovered from the pre-truncation upload-ready manifest remain `QA_PASS_NOT_UPLOADED`.",
    "- Unknown rows are held until the Python quality policy can rescore edge/detail coverage.",
    "- Ledger submitted/pending files remain blocked from reuse.",
    ""
)

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

[PSCustomObject]@{
    Indexed = $rows.Count
    ReadyNotUploaded = $readyCount
    Output = "Database\Adobe_Stock_Local_Upscaled_Candidates.csv"
}
