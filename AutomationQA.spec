# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
block_cipher = None

# Variables.
OUTPUT_DIR = "C:\\QA-Automation\\Automation\\exec\\Automation_EXE"

# Create the folder to save the token.
if not os.path.exists(os.path.join(OUTPUT_DIR)):
    os.makedirs(OUTPUT_DIR)

PyInstaller.config.CONF['distpath'] = OUTPUT_DIR

# Create the Command Line executable.
command = Analysis([
            'C:\\QA-Automation\\Automation\\modules\\automationAux.py',
            'C:\\QA-Automation\\Automation\\modules\\automationFunc.py',
            'C:\\QA-Automation\\Automation\\modules\\automatizationCore_Azure.py',
            'C:\\QA-Automation\\Automation\\modules\\azureConnection.py',
            'C:\\QA-Automation\\Automation\\modules\\generateManualEvidence.py'
            ],
            pathex=[],
            binaries=None,
            datas=[
			('C:\\QA-Automation\\Automation\\README.md','.'),
			('C:\\QA-Automation-Files\\Repository\\Automation\\Hash\\en-hash_dictionary.txt', 'Repository\\Hash'),
			('C:\\QA-Automation-Files\\Repository\\Automation\\Hash\\es-hash_dictionary.txt', 'Repository\\Hash'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Robot.ico', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Robot.png', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\images\\Unavailable.jpg', 'Automation\\images'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-en.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-es.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\dictionary-pt.yml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\configs\\Notepad_Theme_Log_Automation.xml','Automation\\configs'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - en_US.docx','Automation\\evidence'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - es.docx','Automation\\evidence'),
            ('C:\\QA-Automation\\Automation\\Automation\\evidence\\ETS - pt_BR.docx','Automation\\evidence')
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

coll = COLLECT(exe, Tree('C:\\QA-Automation\\Automation\\modules'),
                command.binaries,
                command.zipfiles,
                command.datas,
                strip=False,
                upx=False,
                name='AutomationCMD',
                icon='C:\\QA-Automation\\Automation\\Automation\\images\\Robot.ico')