@echo off
echo ########################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo.                                                                                                                                                         
echo (English) This update will be delete your actual version inside the folder C:\IBOPE\envAutomation. If you DO NOT want to continue close this window.     
echo.                                                                                                                                                            
echo (Portugues) Este update ira apagar a sua versao atual dentro da pasta C:\IBOPE\envAutomation. Se NAO deseja continuar feche esta janela.                   
echo.                                                                                                                                                             
echo (Espanol) Esta actualizacion eliminara su version actual dentro de la carpeta C:\IBOPE\envAutomation. Si NO desea continuar, cierre esta ventana.        
echo.                                                                                                                                                             
echo ########################################################################################################################

pause

echo Removing the lastest version.
rmdir /s /q C:\Temp\envAutomation
rmdir /s /q C:\Temp\Repository\Hash

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path Automation_EXE.zip -DestinationPath C:\Temp\envAutomation\AutomacaoQA\exec\ -Force

cd C:\Temp\envAutomation\AutomacaoQA\exec
powershell Expand-Archive -path Automation.zip -DestinationPath C:\Temp\envAutomation\AutomacaoQA\exec\ -Force

cd C:\Temp\envAutomation\AutomacaoQA\exec
powershell Expand-Archive -path TestEnvironment.zip -DestinationPath C:\Temp\envAutomation\AutomacaoQA\exec\ -Force

echo Copy the automation files from the interface package.
xcopy /e /y C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\Automation C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD

echo Move the file AutomationQA.exe to the AutomationCMD folder.
move C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationQA.exe C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD

echo Move the hash files used by the translation.
mkdir C:\Temp\Repository\Automation\Hash
move C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\Automation\Repository\Hash\en-hash_dictionary.txt C:\Temp\Repository\Automation\Hash
move C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\Automation\Repository\Hash\es-hash_dictionary.txt C:\Temp\Repository\Automation\Hash
rmdir /s /q C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\Automation\Repository
rmdir /s /q C:\Temp\envAutomation\AutomacaoQA\exec\Automation_EXE\AutomationCMD\Repository

echo Deleting the temp .zip files.
DEL /F /Q C:\Temp\envAutomation\AutomacaoQA\exec\Automation.zip
DEL /F /Q C:\Temp\envAutomation\AutomacaoQA\exec\TestEnvironment.zip

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------
pause