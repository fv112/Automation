@echo off

echo Deleting the package older version.
rmdir /s /q C:\QA-Automation\Automation\exec\Green

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\venv\Scripts
python -m PyInstaller -y C:\QA-Automation\Automation\AutomationQA.spec --clean --log-level=DEBUG

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\Green -Update -DestinationPath C:\QA-Automation\Automation\exec\Green\Automation

powershell -Command "Compress-Archive -Path 'C:\QA-Automation\Automation\exec\TestEnvironment' -DestinationPath 'C:\QA-Automation\Automation\exec\Green\TestEnvironment.zip'"

powershell -Command "Compress-Archive -LiteralPath 'C:\QA-Automation\Automation\exec\Green\TestEnvironment.zip', 'C:\QA-Automation\Automation\exec\Green\Automation.zip' -DestinationPath 'C:\QA-Automation\Automation\exec\Green\Green.zip'"

echo Move from Green folder to exec.
copy C:\QA-Automation\Automation\exec\Green\Green.zip C:\QA-Automation\Automation\exec

echo Deleting the Green folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Green
pause
