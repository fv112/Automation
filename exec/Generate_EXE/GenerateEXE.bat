@echo off

echo Deleting the package older version.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\venv\Scripts
python -m PyInstaller -y C:\QA-Automation\Automation\AutomationQA.spec --clean --log-level=DEBUG

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\Automation_EXE -Update -DestinationPath C:\QA-Automation\Automation\exec\Automation_EXE\Automation

powershell -Command "Compress-Archive -Path 'C:\QA-Automation\Automation\exec\TestEnvironment' -DestinationPath 'C:\QA-Automation\Automation\exec\Automation_EXE\TestEnvironment.zip'"

powershell -Command "Compress-Archive -LiteralPath 'C:\QA-Automation\Automation\exec\Automation_EXE\TestEnvironment.zip', 'C:\QA-Automation\Automation\exec\Automation_EXE\Automation.zip' -DestinationPath 'C:\QA-Automation\Automation\exec\Automation_EXE\Automation_EXE.zip'"

echo Move from Automation_EXE folder to exec.
copy C:\QA-Automation\Automation\exec\Automation_EXE\Automation_EXE.zip C:\QA-Automation\Automation\exec

echo Deleting the Automation_EXE folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE
pause
