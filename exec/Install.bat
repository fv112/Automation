@echo off
echo ########################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo.                                                                                                                                                         
echo (English) This update will be delete your actual version inside the folder C:\QA-Automation. If you DO NOT want to continue close this window.
echo.                                                                                                                                                            
echo (Português) Este update ira apagar a sua versão atual dentro da pasta C:\QA-Automation. Se NAO deseja continuar feche esta janela.
echo.                                                                                                                                                             
echo (Español) Esta actualizacion eliminara su version actual dentro de la carpeta C:\QA-Automation. Si NO desea continuar, cierre esta ventana.
echo.                                                                                                                                                             
echo ########################################################################################################################

pause

echo Removing the latest version.
rmdir /s /q C:\Temp\envAutomation
rmdir /s /q C:\Temp\Repository\Hash

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path Automation_EXE.zip -DestinationPath C:\QA-Automation\Automation\exec\ -Force

cd C:\QA-Automation\Automation\exec
powershell Expand-Archive -path Automation.zip -DestinationPath C:\QA-Automation\Automation\exec\ -Force

cd cd C:\QA-Automation\Automation\exec
powershell Expand-Archive -path TestEnvironment.zip -DestinationPath cd C:\QA-Automation\Automation\exec\ -Force

echo Move the file AutomationQA.exe to the AutomationCMD folder.
move cd C:\QA-Automation\Automation\exec\exec\Automation_EXE\AutomationQA.exe cd C:\QA-Automation\Automation\exec\Automation_EXE\AutomationCMD

echo Move the hash files used by the translation.
mkdir cd C:\QA-Automation\Automation\Hash
move C:\QA-Automation\Automation\exec\Automation_EXE\Automation\Repository\Hash\en-hash_dictionary.txt C:\QA-Automation-Files\Hash
move C:\QA-Automation\Automation\exec\Automation_EXE\Automation\Repository\Hash\es-hash_dictionary.txt C:\QA-Automation-Files\Hash
rmdir /s /q C:\QA-Automation-Files\Repository
rmdir /s /q C:\QA-Automation-Files\Repository

echo Deleting the temp .zip files.
DEL /F /Q C:\QA-Automation\Automation\exec\Automation.zip
DEL /F /Q C:\QA-Automation\Automation\exec\TestEnvironment.zip

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------
pause