# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
block_cipher = None

# Variables.
OUTPUT_DIR = "C:\\QA-Automation\\Automation\\exec\\Green"

# Create the folder to save the token.
if not os.path.exists(os.path.join(OUTPUT_DIR)):
    os.makedirs(OUTPUT_DIR)

PyInstaller.config.CONF['distpath'] = OUTPUT_DIR

# Create the Command Line executable.
command = Analysis([
            'C:\\QA-Automation\\Automation\\AppAutomation.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\automationAux.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\automationCore.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\automationFunc.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\connections.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\common_libs.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\automaticCompareFiles.py',
            'C:\\QA-Automation\\Automation\\Automation\\modules\\generateManualEvidence.py'
            ],
            pathex=[],
            binaries=None,
            datas=[
			('C:\\QA-Automation\\Automation\\README.md','Automation'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Robot.ico', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Robot.png', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Unavailable.jpg', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-en.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-es.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-pt.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\Notepad_Theme_Log_Automation.xml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - en_US.docx','Automation\\evidence'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - es.docx','Automation\\evidence'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - pt_BR.docx','Automation\\evidence'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\automaticCompareFiles.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\automationAux.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\automationCore.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\automationFunc.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\common_libs.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\connections.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\Automation\\modules\\generateManualEvidence.py','Automation\\modules'),
            ('C:\\QA-Automation\\Automation\\exec\\AutomationQA.bat','Automation')
            ],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher)

command.excludedimports=[]

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
            icon='C:\\QA-Automation\\Automation\\Automation\\images\\Robot.ico')

coll = COLLECT(exe, Tree('C:\\QA-Automation\\Automation\\Automation\\modules'),
                command.binaries,
                command.zipfiles,
                command.datas,
                strip=False,
                upx=False,
                name='Automation',
                icon='C:\\QA-Automation\\Automation\\Automation\\images\\Robot.ico')