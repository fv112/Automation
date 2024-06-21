@echo off

echo Deleting the package older version.
REM DEL /F /Q C:\QA-Automation\Automation\Temp\Automation_EXE.zip
REM DEL /F /Q C:\QA-Automation\Automation\Temp\TestEnvironment.zip

REM echo Deleting the temp folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Temp

REM echo Deleting all the CMD files and maintain only the AutomationQA.exe.
REM rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE

REM --------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\Automation\.venv\Scripts
python -m PyInstaller -y C:\QA-Automation\Automation\AutomationQA.spec --clean --log-level=DEBUG 

REM echo Save the .exe CMD file.
REM copy C:\QA-Automation\Automation\exec\Automation_EXE\Automation\AutomationQA.exe C:\QA-Automation\Automation\exec\Automation_EXE

REM echo Move from _internal folder to Automation.
REM robocopy /E /MOV C:\QA-Automation\Automation\exec\Automation_EXE\Automation\_internal\ C:\QA-Automation\Automation\exec\Automation_EXE\Automation\

REM echo Deleting the _internal folder.
REM rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE\Automation\_internal

REM echo Deleting the AutomationQA.exe file.
REM DEL /F /Q C:\QA-Automation\Automation\exec\AutomationQA.exe

REM --------------------------------------------------------------------------------------------------------------------------------------

REM echo Creating the folder.
REM mkdir C:\QA-Automation\Automation\exec\Automation_EXE\Automation

echo Creating zip files.
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\Automation_EXE -Update -DestinationPath C:\QA-Automation\Automation\exec\Temp\Automation
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\TestEnvironment -Update -DestinationPath C:\QA-Automation\Automation\exec\Temp\TestEnvironment
powershell Compress-Archive -literalpath "C:\QA-Automation\Automation\exec\TestEnvironment.zip", "C:\QA-Automation\Automation\exec\Automation.zip" -Update -DestinationPath C:\QA-Automation\Automation\exec\Temp\Automation_EXE.zip

echo Deleting the temp folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Temp

echo Deleting the temp .zip files.
DEL /F /Q C:\QA-Automation\Automation\exec\Temp\Automation.zip
DEL /F /Q C:\QA-Automation\Automation\exec\Temp\TestEnvironment.zip

pause