import os.path
import sys


for root, dirs, files in os.walk(os.getcwd()):
    if 'common_libs.py' in files:
        sys.path.append(os.path.abspath(root))
        break

import common_libs as Lib


class AutomationQA:

    def __init__(self):
        path = None
        Lib.Aux.Main.setLanguage(language='pt_BR')

        # ------ Check the version ----------
        # Git version.
        self.readme_content = Lib.Aux.Main.read_html_content(self)
        self.version_distributed, _, _, _ = Lib.Aux.Main.releaseNotes(readme=self.readme_content)

        for root, dirs, files in os.walk(os.getcwd()):
            if 'README.md' in files:
                path = os.path.join(os.path.abspath(root), 'README.md')
                break

        # Local version.
        self.version_local, _, _, _ = Lib.Aux.Main.releaseNotes(path=path)

        Lib.os.system('cls')

        Lib.Aux.Main.checkNewVersion(self)

        # ------ Run the menu ----------

        _, local_version, date_version, release_infos = Lib.Aux.Main.releaseNotes(path=path)

        print(f"{Lib.Aux.Textcolor.HIGHLIGHT}       Automation QA - Version: {local_version} - Date: {date_version}    "
              f"{Lib.Aux.Textcolor.END}")
        print(f"{Lib.Aux.Textcolor.BOLD}Release notes:{Lib.Aux.Textcolor.END}")
        for releaseInfo in release_infos:
            print(f"{releaseInfo}")
        print("")

        app_core = Lib.Core.Main(self)
        app_core.main()

    #     self.cmdHelp()
    #
    #     # Minimize the Python screen (command line).
    #     Minimize = win32gui.GetForegroundWindow()
    #     win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    #
    #     self.project = None
    #     self.test_case_id = None
    #     self.isolated_test_case = None
    #
    #     # Split the command line parameters.
    #     options, args = getopt.getopt(argv[1:], "p:i:t:",
    #                                   ["project",
    #                                    "isolated_test_case",
    #                                    "test_case_id"])
    #
    #     print(options)
    #
    #     for name, value in options:
    #         if name in ['-p']:  # Project.
    #             self.project = value
    #         elif name in ['-i']:  # Isolated test case.
    #             self.isolated_test_case = value
    #         elif name in ['-t']:  # Test case id.
    #             self.test_case_id = value
    #
    #     print(f' Project:               {self.project}\n',
    #           f' Isolated Test case:    {self.isolated_test_case}\n',
    #           f' Test Case ID:          {self.test_case_id}\n'
    #           )
    #
    #     # Read any language to load the directories and paths.
    #     Aux.Main.loadConfigs(self, language='pt_BR', interface=False)
    #
    #     # Create the log directory.
    #     Aux.Main.createDirectory(self, path_folder=Aux.directories['LogFolder'])
    #
    #     # Create the New Version directory.
    #     Aux.Main.createDirectory(self, path_folder=Aux.directories['UpdateFolder'])
    #
    #     # Create the export directory.
    #     Aux.Main.createDirectory(self, path_folder=Aux.directories['DownloadFolder'])
    #     Aux.Main.createDirectory(self, path_folder=Aux.directories['DownloadFolderTemp'])
    #
    #     # Clear the export folder, if already exist.
    #     Aux.Main.deleteFiles(self, file_path=Aux.directories['DownloadFolder'], extension='*')
    #     Aux.Main.deleteFiles(self, file_path=Aux.directories['DownloadFolderTemp'], extension='*')
    #
    #     # Load the Windows DLL's to inform the computer language.
    #     windll = ctypes.windll.kernel32
    #     windll.GetUserDefaultUILanguage()
    #
    #     # Load the correct file according the language.
    #     ###language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    #     ### language = 'es' ### For test.
    #     ### language = 'en_US' ### For test.
    #     language = 'pt_BR' ### For test.
    #
    #     if 'es' in language:
    #         language = language[:2]  # Any spanish language.
    #
    #     if language not in ('es', 'en_US', 'pt_BR'):
    #         print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['LanguageError']['Msg']}{Aux.Textcolor.END}")
    #         Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs["LanguageError"])
    #         #exit(1)
    #
    #     # Configure the languages.
    #     Aux.Main.setLanguage(self, language=language, interface=False)
    #
    #     # Language.
    #     Aux.otherConfigs['Language'] = language
    #
    #     # Request the token.
    #     Aux.Main.accessAzure(self)
    #
    # @staticmethod
    # def cmdHelp():
    #
    #     os.system('cls')
    #
    #     parser = argparse.ArgumentParser(prog='AutomationQA', prefix_chars='-+', conflict_handler='resolve',
    #                                      formatter_class=argparse.RawDescriptionHelpFormatter,
    #                                      description=textwrap.dedent('''\
    #                                                      Please check the parameters below:
    #                                                      --------------------------------
    #                                                          project   - Mandatory to inform the project source.
    #                                                          isolated  - Mandatory to run one test case or the whole test suit.
    #                                                          test case - Mandatory when the isolated is equal to "YES".
    #                                                      '''))
    #     default = parser.add_argument_group('default')
    #     default.add_argument('-p', type=int, help='Inform the project ID.', required=True)
    #     default.add_argument('-i', choices=['Y/S', 'N'], help='Test Case isolated')
    #     default.add_argument('-t', type=int, help='Inform the test case ID.')
    #
    #     args = parser.parse_args()
    #
    #     def execute_automation(self):
    #         from modules.automatizationCore_Azure import Main as Execute
    #
    #         try:
    #             Execute.main(self, project_id=self.project, project_name=self.project, id_test_plan=self.test_plan,
    #                          id_test_suit=self.test_suit,
    #                          test_case_id_list_all=self.test_case_id, evidence=self.save_evidence, cookie=self.run_id,
    #                          timeout=self.time_out)
    #
    #         except Exception as e:
    #             print(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'] + ' - ' + str(e))


if __name__ == "__main__":
    run = AutomationQA()
