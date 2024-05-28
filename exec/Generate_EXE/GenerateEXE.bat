@echo off

echo Deleting the package older version.
DEL /F /Q C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE.zip
DEL /F /Q C:\ibope\envAutomation\AutomacaoQA\exec\TestEnvironment.zip

REM ---------------------------------------------------------------------------------------------------------------------------------------------------------------

echo Generating Interface EXE file.
cd C:\IBOPE\envAutomation\AutomacaoQA\Scripts
python -m PyInstaller -y --icon C:\IBOPE\envAutomation\AutomacaoQA\Automation\images\Robot.ico c:\IBOPE\envAutomation\AutomacaoQA\AutomationQA_Interface.spec --clean --log-level=DEBUG

echo Generating CMD EXE file.
cd C:\IBOPE\envAutomation\AutomacaoQA\Scripts
python -m PyInstaller -y --icon C:\IBOPE\envAutomation\AutomacaoQA\Automation\images\Robot.ico c:\IBOPE\envAutomation\AutomacaoQA\AutomationQA_CMD.spec --clean --log-level=DEBUG

echo Save the .exe CMD file.
copy C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD\AutomationQA.exe C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE

echo Deleting all the CMD files and maintain only the AutomationQA.exe.
rmdir /s /q C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD

echo Creating the folder.
mkdir C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD

REM ---------------------------------------------------------------------------------------------------------------------------------------------------------------

echo Creating zip files.
powershell Compress-Archive -path C:\IBOPE\envAutomation\AutomacaoQA\exec\Automation_EXE -Update -DestinationPath C:\IBOPE\envAutomation\AutomacaoQA\exec\Automation

powershell Compress-Archive -path C:\IBOPE\envAutomation\AutomacaoQA\exec\TestEnvironment -Update -DestinationPath C:\IBOPE\envAutomation\AutomacaoQA\exec\TestEnvironment

powershell Compress-Archive -literalpath "C:\IBOPE\envAutomation\AutomacaoQA\exec\TestEnvironment.zip", "C:\IBOPE\envAutomation\AutomacaoQA\exec\Automation.zip" -Update -DestinationPath C:\IBOPE\envAutomation\AutomacaoQA\exec\Automation_EXE.zip

echo Deleting the temp folder.
rmdir /s /q C:\ibope\envAutomation\AutomacaoQA\exec\Automation_EXE
rmdir /s /q C:\ibope\envAutomation\AutomacaoQA\Scripts\build
rmdir /s /q C:\ibope\envAutomation\AutomacaoQA\Scripts\dist

echo Deleting the temp .zip files.
DEL /F /Q C:\ibope\envAutomation\AutomacaoQA\exec\Automation.zip
DEL /F /Q C:\ibope\envAutomation\AutomacaoQA\exec\TestEnvironment.zip



