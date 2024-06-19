@echo off

echo Deleting the package older version.
DEL /F /Q C:\QA-Automation\Automation\exec\Automation_EXE.zip
DEL /F /Q C:\QA-Automation\Automation\exec\TestEnvironment.zip

REM ---------------------------------------------------------------------------------------------------------------------------------------------------------------

echo Generating CMD EXE file.
cd C:\QA-Automation\Automation\.venv\Scripts
python -m PyInstaller -y --icon C:\IBOPE\envAutomation\AutomacaoQA\Automation\images\Robot.ico C:\QA-Automation\Automation\AutomationQA_CMD.spec --clean --log-level=DEBUG

echo Save the .exe CMD file.
copy C:\QA-Automation\Automation\exec\Automation_EXE\AutomationCMD\AutomationQA.exe C:\QA-Automation\Automation\exec\Automation_EXE

echo Deleting all the CMD files and maintain only the AutomationQA.exe.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE\AutomationCMD

echo Creating the folder.
mkdir C:\QA-Automation\Automation\exec\Automation_EXE\AutomationCMD

REM ---------------------------------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell Compress-Archive -path C:\QA-Automation\Automation\exec\Automation_EXE -Update -DestinationPath C:\IBOPE\envAutomation\AutomacaoQA\exec\Automation

powershell Compress-Archive -path C:\QA-Automation\Automation\exec\TestEnvironment -Update -DestinationPath C:\QA-Automation\Automation\exec\TestEnvironment

powershell Compress-Archive -literalpath "C:\QA-Automation\Automation\exec\TestEnvironment.zip", "C:\QA-Automation\Automation\exec\Automation.zip" -Update -DestinationPath C:\QA-Automation\Automation\exec\Automation_EXE.zip

echo Deleting the temp folder.
rmdir /s /q C:\QA-Automation\Automation\exec\Automation_EXE
rmdir /s /q C:\QA-Automation\Automation\Scripts\build
rmdir /s /q C:\QA-Automation\Automation\Scripts\dist

echo Deleting the temp .zip files.
DEL /F /Q C:\QA-Automation\Automation\exec\Automation.zip
DEL /F /Q C:\QA-Automation\Automation\exec\TestEnvironment.zip



