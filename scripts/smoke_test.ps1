$ErrorActionPreference = "Stop"
Write-Host "Checking liveness..."
Invoke-RestMethod "http://127.0.0.1:8000/health/live"
Write-Host "Checking readiness..."
Invoke-RestMethod "http://127.0.0.1:8000/health/ready"
Write-Host "Sending generation request..."
$body = @{ prompt = "success comes from"; sentence_count = 2; temperature = 0.8; top_k = 8 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/generate" -Method Post -ContentType "application/json" -Body $body
