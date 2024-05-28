# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
block_cipher = None

# Variables.
OUTPUT_DIR = "C:\\IBOPE\\envAutomation\\AutomacaoQA\exec\\Automation_EXE"

# Create the folder to save the token.
if not os.path.exists(os.path.join(OUTPUT_DIR)):
    os.makedirs(OUTPUT_DIR)

PyInstaller.config.CONF['distpath'] = OUTPUT_DIR

# Create the Command Line executable.
command = Analysis([
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\AppAutomationCMD.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\automaticCompareFiles.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\automationAux.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\automationFunc.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\automatizationCore_Azure.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\azureConnection.py',
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules\\generateManualEvidence.py'
            ],
            pathex=[],
            binaries=None,
            datas=[
			('C:\\IBOPE\\envAutomation\\AutomacaoQA\\README.md','.'),
			('C:\IBOPE\\Repository\\Automation\Hash\\en-hash_dictionary.txt', 'Repository\\Hash'),
			('C:\IBOPE\\Repository\\Automation\Hash\\es-hash_dictionary.txt', 'Repository\\Hash'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.ico', 'Automation\\images'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.png', 'Automation\\images'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Unavailable.jpg', 'Automation\\images'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\configs\\dictionary-en.yml','Automation\\configs'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\configs\\dictionary-es.yml','Automation\\configs'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\configs\\dictionary-pt.yml','Automation\\configs'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\configs\\Settings.bcpkg','Automation\\configs'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\drivers\\Chrome32Bits.exe','Automation\\drivers'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\drivers\\Firefox64Bits.exe','Automation\\drivers'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\drivers\\IE32bits.exe','Automation\\drivers'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\drivers\\MSEdge64Bits.exe','Automation\\drivers'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\drivers\\MSEdgeLegacy-v16.exe','Automation\\drivers'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\evidence\\ETS - en_US.docx','Automation\\evidence'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\evidence\\ETS - es.docx','Automation\\evidence'),
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\evidence\\ETS - pt_BR.docx','Automation\\evidence')
            ],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher)

command.excludedimports=['kviy', 'kivymd']

pyz = PYZ(command.pure, command.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
            command.scripts,
            [],
            exclude_binaries=True,
            name='AutomationQA',
            debug=True,
            bootloader_ignore_signals=False,
            strip=False,
            upx=False,
            console=True, # True = Enable the command line in background to debug.
            icon='C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.ico')

coll = COLLECT(exe, Tree('C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules'),
                command.binaries,
                command.zipfiles,
                command.datas,
                strip=False,
                upx=False,
                name='AutomationCMD',
                icon='C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.ico')