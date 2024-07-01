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

echo Removing the latest version.
rmdir /s /q C:\QA-Automation

echo Creating the destination folder.
mkdir C:\QA-Automation\Automation

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path Automation_EXE.zip -DestinationPath C:\QA-Automation\Automation\ -Force

cd C:\QA-Automation\Automation\
powershell Expand-Archive -path TestEnvironment.zip -DestinationPath C:\QA-Automation\Automation\ -Force

cd C:\QA-Automation\Automation\
powershell Expand-Archive -path Automation.zip -DestinationPath C:\QA-Automation\Automation\ -Force

echo Move the file AutomationQA.exe to the AutomationCMD folder.
move C:\QA-Automation\Automation\Automation_EXE\Automation\AutomationQA.exe C:\QA-Automation\Automation\Automation_EXE\Automation

echo Move the Automation folder to outside from _internal.
move C:\QA-Automation\Automation\Automation_EXE\Automation\_internal\Automation C:\QA-Automation\Automation\Automation_EXE\Automation
move C:\QA-Automation\Automation\Automation_EXE\Automation\_internal\README.md C:\QA-Automation\Automation\Automation_EXE\Automation

echo Move the hash files used by the translation.
mkdir C:\QA-Automation\Automation\Hash
move C:\QA-Automation\Automation\Automation_EXE\Automation\Repository\Hash\en-hash_dictionary.txt C:\QA-Automation-Files\Hash
move C:\QA-Automation\Automation\Automation_EXE\Automation\Repository\Hash\es-hash_dictionary.txt C:\QA-Automation-Files\Hash

echo Deleting the temp .zip files.
DEL /F /Q C:\QA-Automation\Automation\Automation.zip
DEL /F /Q C:\QA-Automation\Automation\TestEnvironment.zip

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------


pause