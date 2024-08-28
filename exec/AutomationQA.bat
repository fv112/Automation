@echo off
SETLOCAL 

REM Blue = Versão atual.
SET DIR_BLUE=C:\ProgramData\QA-Automation\Automation\Blue

REM Green = Nova versão.
SET DIR_GREEN=C:\ProgramData\QA-Automation-Files\Repository\Download

IF EXIST "%DIR_BLUE%\" (
    IF EXIST "%DIR_GREEN%\" (
        goto AmbosExistem
    ) ELSE (
        goto BlueExiste_Atual
    )
) ELSE (
    IF EXIST "%DIR_GREEN%\" (
         goto GreenExiste_Nova
    ) ELSE (
        goto NenhumExiste
    )
)

:AmbosExistem
echo Ambos os diretórios existem.
rmdir /S /Q "%DIR_BLUE%"

echo #############################################################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo "(English) This update will be delete your actual version inside the folder C:\ProgramData\QA-Automation. If you DO NOT want to continue close this window."
echo "(Português) Este update ira apagar a sua versão atual dentro da pasta C:\ProgramData\QA-Automation. Se NAO deseja continuar feche esta janela."
echo "(Español) Esta actualizacion eliminara su version actual dentro de la carpeta C:\ProgramData\QA-Automation. Si NO desea continuar, cierre esta ventana."
echo .
echo #############################################################################################################################################################

echo Creating the destination folder.
mkdir "C:\ProgramData\QA-Automation\Automation"

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path "%DIR_GREEN%"\Green.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\Automation.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

echo Move the Automation folder to Automation from _internal.
xcopy "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation\*" "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\" /E /H /C /I /Y
copy "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\README.md" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Move the file AutomationQA.bat to the Automation folder.
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\AutomationQA.bat" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Delete temporary files.
rmdir /S /Q "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation"
del "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\README.md"
del "C:\ProgramData\QA-Automation\Automation\Automation.zip"
del "C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip"
rmdir /S /Q "C:\ProgramData\QA-Automation-Files\Repository\Download"

echo Move the hash files used by the translation.
mkdir "C:\ProgramData\QA-Automation\Automation\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\en-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\es-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------

xcopy "%DIR_GREEN%" "%DIR_BLUE%" /E /H /C /I /Y
rmdir /S /Q "%DIR_GREEN%"
cd "C:\ProgramData\QA-Automation\Automation\Blue\Automation"
AutomationQA.exe
goto End

:GreenExiste_Nova
echo O diretório %DIR_GREEN% existe, mas o diretório %DIR_BLUE% não existe.

echo #############################################################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo "(English) This update will be delete your actual version inside the folder C:\ProgramData\QA-Automation. If you DO NOT want to continue close this window."
echo "(Português) Este update ira apagar a sua versão atual dentro da pasta C:\ProgramData\QA-Automation. Se NAO deseja continuar feche esta janela."
echo "(Español) Esta actualizacion eliminara su version actual dentro de la carpeta C:\ProgramData\QA-Automation. Si NO desea continuar, cierre esta ventana."
echo .
echo #############################################################################################################################################################

echo Creating the destination folder.
mkdir "C:\ProgramData\QA-Automation\Automation"

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path "%DIR_GREEN%"\Green.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\Automation.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

echo Move the Automation folder to Automation from _internal.
xcopy "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation\*" "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\" /E /H /C /I /Y
copy "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\README.md" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Move the file AutomationQA.bat to the Automation folder.
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\AutomationQA.bat" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Delete temporary files.
rmdir /S /Q "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation"
del "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\README.md"
del "C:\ProgramData\QA-Automation\Automation\Automation.zip"
del "C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip"
rmdir /S /Q "C:\ProgramData\QA-Automation-Files\Repository\Download"

echo Move the hash files used by the translation.
mkdir "C:\ProgramData\QA-Automation\Automation\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\en-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\es-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------

xcopy "%DIR_GREEN%" "%DIR_BLUE%" /E /H /C /I /Y
REN C:\ProgramData\QA-Automation\Automation\Green C:\ProgramData\QA-Automation\Automation\Blue
cd "C:\ProgramData\QA-Automation\Automation\Blue\Automation"
AutomationQA.exe
goto End

:BlueExiste_Atual
echo O diretório %DIR_BLUE% existe, mas o diretório %DIR_GREEN% não existe.
cd "C:\ProgramData\QA-Automation\Automation\Blue\Automation"
AutomationQA.exe
goto End

:NenhumExiste
echo Nenhum existe.
set "scriptPath=%~dp0"
set "scriptPath=%scriptPath:~0,-1%"

echo #############################################################################################################################################################
echo 		   				ATTENTION / ATENCAO / AVISO
echo "(English) This update will be delete your actual version inside the folder C:\ProgramData\QA-Automation. If you DO NOT want to continue close this window."
echo "(Português) Este update ira apagar a sua versão atual dentro da pasta C:\ProgramData\QA-Automation. Se NAO deseja continuar feche esta janela."
echo "(Español) Esta actualizacion eliminara su version actual dentro de la carpeta C:\ProgramData\QA-Automation. Si NO desea continuar, cierre esta ventana."
echo .
echo #############################################################################################################################################################

echo Creating the destination folder.
mkdir "C:\ProgramData\QA-Automation\Automation"

echo Unzip the Automation package and installing the new version.
powershell Expand-Archive -path %scriptPath%\Green.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

cd "C:\ProgramData\QA-Automation\Automation\"
powershell Expand-Archive -path C:\ProgramData\QA-Automation\Automation\Automation.zip -DestinationPath C:\ProgramData\QA-Automation\Automation\ -Force

echo Move the Automation folder to Automation from _internal.
xcopy "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation\*" "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\" /E /H /C /I /Y
copy "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\README.md" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Move the file AutomationQA.bat to the Automation folder.
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Automation\AutomationQA.bat" "C:\ProgramData\QA-Automation\Automation\Green\Automation"

echo Delete temporary files.
rmdir /S /Q "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\Automation"
del "C:\ProgramData\QA-Automation\Automation\Green\Automation\_internal\README.md"
del "C:\ProgramData\QA-Automation\Automation\Automation.zip"
del "C:\ProgramData\QA-Automation\Automation\TestEnvironment.zip"
rmdir /S /Q "C:\ProgramData\QA-Automation-Files\Repository\Download"

echo Move the hash files used by the translation.
mkdir "C:\ProgramData\QA-Automation\Automation\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\en-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"
move "C:\ProgramData\QA-Automation\Automation\Green\Automation\Repository\Hash\es-hash_dictionary.txt" "C:\ProgramData\QA-Automation-Files\Hash"

echo -----------------------------------------------------------------------------------------------------------------------
echo  New version installed.
echo -----------------------------------------------------------------------------------------------------------------------

xcopy C:\ProgramData\QA-Automation\Automation\Green C:\ProgramData\QA-Automation\Automation\Blue /E /H /C /I /Y
pause
rmdir /S /Q C:\ProgramData\QA-Automation\Automation\Green
cd "C:\ProgramData\QA-Automation\Automation\Blue\Automation"
AutomationQA.exe
goto End

:End
ENDLOCAL