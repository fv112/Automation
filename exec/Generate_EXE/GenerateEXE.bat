@echo off

echo Deleting the package older version.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\venv\Scripts
python -m PyInstaller -y C:\QA-Automation\Automation\AutomationQA.spec --clean --log-level=DEBUG

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell -Command "$directoryToZip = 'C:\QA-Automation\Automation\exec\Automation_EXE'; $zipFileName = 'C:\QA-Automation\Automation\exec\Automation_EXE\Automation.zip'; $excludeFolderName = 'C:\QA-Automation\venv\Lib\site-packages\charset_normalizer'; $excludeFolderPath = Join-Path -Path $directoryToZip -ChildPath $excludeFolderName; $filesToInclude = Get-ChildItem -Path $directoryToZip -Recurse -File | Where-Object { $_.FullName -notlike ($excludeFolderPath + '*') }; if ($filesToInclude.Count -gt 0) { Compress-Archive -Path $filesToInclude.FullName -DestinationPath $zipFileName } else { Write-Output 'Nenhum arquivo para compactar.' }"

powershell -Command "Compress-Archive -Path 'C:\QA-Automation\Automation\exec\TestEnvironment' -DestinationPath 'C:\QA-Automation\Automation\exec\Automation_EXE\TestEnvironment.zip'"

powershell -Command "Compress-Archive -LiteralPath 'C:\QA-Automation\Automation\exec\Automation_EXE\TestEnvironment.zip', 'C:\QA-Automation\Automation\exec\Automation_EXE\Automation.zip' -DestinationPath 'C:\QA-Automation\Automation\exec\Automation_EXE\Automation_EXE.zip'"

echo Move from Automation_EXE folder to exec.
copy C:\QA-Automation\Automation\exec\Automation_EXE\Automation_EXE.zip C:\QA-Automation\Automation\exec

echo Deleting the Automation_EXE folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE
pause
