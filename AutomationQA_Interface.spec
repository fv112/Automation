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

# Create the Interface executable.
interface = Analysis([
            'C:\\IBOPE\\envAutomation\\AutomacaoQA\\AppAutomation.py',
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
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\AppAutomation.kv','.'),
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
            ('C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\configs\\Notepad_Theme_Log_Automation.xml','Automation\\configs'),
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
            hookspath=[kivymd_hooks_path],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher)

pyz = PYZ(interface.pure, interface.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
            interface.scripts,
            [],
            exclude_binaries=True,
            name='AutomationQA',
            debug=True,
            bootloader_ignore_signals=False,
            strip=False,
            upx=False,
            console=False, # False = Disable the command line in background to debug.
            icon='C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.ico')

coll = COLLECT(exe, Tree('C:\\IBOPE\\envAutomation\\AutomacaoQA\\modules'),
                interface.binaries,
                interface.zipfiles,
                interface.datas,
                *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
                strip=False,
                upx=False,
                name='Automation',
                icon='C:\\IBOPE\\envAutomation\\AutomacaoQA\\Automation\\images\\Robot.ico')