@echo off

REM Set the fullpath file path.
setlocal
set "scriptPath=%~dp0"
set "scriptPath=%scriptPath:~0,-1%"

echo ########################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo.                                                                                                                                                         
echo (English) This update will be delete your actual version inside the folder C:\ProgramData\QA-Automation. If you DO NOT want to continue close this window.
echo.                                                                                                                                                            
echo (Português) Este update ira apagar a sua versão atual dentro da pasta C:\ProgramData\QA-Automation. Se NAO deseja continuar feche esta janela.
echo.                                                                                                                                                             
echo (Español) Esta actualizacion eliminara su version actual dentro de la carpeta C:\ProgramData\QA-Automation. Si NO desea continuar, cierre esta ventana.
echo.                                                                                                                                                             
echo ########################################################################################################################

echo Creating the destination folder.
mkdir C:\ProgramData\QA-Automation\Automation

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path  %scriptPath%\Automation_EXE.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd C:\ProgramData\QA-Automation\Automation\
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd C:\ProgramData\QA-Automation\Automation\
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\Automation.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

echo Move the Automation folder to Automation from _internal.
xcopy C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\_internal\Automation\* C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\ /E /H /C /I /Y
copy C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\_internal\README.md C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation

echo Move the file AutomationQA.exe to the AutomationCMD folder.
move C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\AutomationQA.exe C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation

REM echo Move the file AutomationQA.exe to the AutomationCMD folder.
REM mkdir C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\modules
REM move C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\_internal\common_libs.py C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\modules

echo Delete temporary files.
rmdir /S /Q C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\_internal\Automation
del C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\_internal\README.md

echo Move the hash files used by the translation.
mkdir C:\ProgramData\QA-Automation\Automation\Hash
move C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\Repository\Hash\en-hash_dictionary.txt C:\ProgramData\QA-Automation-Files\Hash
move C:\ProgramData\QA-Automation\Automation\Automation_EXE\Automation\Repository\Hash\es-hash_dictionary.txt C:\ProgramData\QA-Automation-Files\Hash

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------