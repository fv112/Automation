@echo off

echo Deleting the package older version.
DEL /F /Q C:\QA-Automation\Automation\exec\Automation_EXE.zip
DEL /F /Q C:\QA-Automation\Automation\exec\TestEnvironment.zip

echo Deleting all the CMD files and maintain only the AutomationQA.exe.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\Automation\.venv\Scripts
python -m PyInstaller -y C:\QA-Automation\Automation\AutomationQA.spec --clean --log-level=DEBUG

echo Save the .exe CMD file.
copy C:\QA-Automation\Automation\exec\Automation_EXE\Automation\AutomationQA.exe C:\QA-Automation\Automation\exec\Automation_EXE

REM echo Move from _internal folder to Automation.
REM robocopy /E /MOV C:\QA-Automation\Automation\exec\Automation_EXE\Automation\_internal\ C:\QA-Automation\Automation\exec\Automation_EXE\Automation\

REM echo Deleting the _internal folder.
REM rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE\Automation\_internal

echo Deleting the AutomationQA.exe file.
DEL /F /Q C:\QA-Automation\Automation\exec\AutomationQA.exe

echo Creating the folder.
mkdir C:\QA-Automation\Automation\exec\Automation_EXE\Automation

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\Automation_EXE -Update -DestinationPath C:\QA-Automation\Automation\exec\Automation
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\TestEnvironment -Update -DestinationPath C:\QA-Automation\Automation\exec\TestEnvironment
powershell Compress-Archive -literalpath "C:\QA-Automation\Automation\exec\TestEnvironment.zip", "C:\QA-Automation\Automation\exec\Automation.zip" -Update -DestinationPath C:\QA-Automation\Automation\exec\Automation_EXE.zip

echo Deleting the temp folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE

echo Deleting the temp .zip files.
DEL /F /Q C:\QA-Automation\Automation\exec\Automation.zip
DEL /F /Q C:\QA-Automation\Automation\exec\TestEnvironment.zip

pause