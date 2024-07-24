@echo off

for /f "tokens=1,2 delims==" %%G in (.env) do (
    set %%G=%%H
)

powershell -command "Compress-Archive -Path *.py, *.md, *.txt, bot  -DestinationPath code.zip -Force"

yc serverless function version create ^
    --function-id="%FUNCTION_ID%" ^
    --runtime python312 ^
    --entrypoint index.handler ^
    --memory 128m ^
    --execution-timeout 40s ^
    --source-path code.zip ^
    --service-account-id="%SERVICE_ACCOUNT_ID%" ^
    --environment YDB_DATABASE="%YDB_DATABASE%" ^
    --environment YDB_ENDPOINT="%YDB_ENDPOINT%" ^
    --environment BOT_TOKEN="%BOT_TOKEN%"