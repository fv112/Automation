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

        # Load the Windows DLL's to inform the computer language.
        windll = Lib.ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()

        # Load the correct file according the language.
        language = Lib.locale.windows_locale[windll.GetUserDefaultUILanguage()]

        if 'es' in language:
            language = language[:2]  # Any spanish language.

        # For debug.
        ### language = 'es'     ### For test.
        ### language = 'en_US'  ### For test.
        ### language = 'pt_BR'  ### For test.

        Lib.Aux.Main.setLanguage(language=language)

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

        # With arguments.
        if sys.argv.__len__() > 1:

            self.cmdHelp()

            # Minimize the Python screen (command line).
            # minimize = Lib.GetForegroundWindow()
            # Lib.ShowWindow(minimize, Lib.win32con.SW_MINIMIZE)

            self.project = None
            self.test_case_id = None
            self.isolated_test_case = None
            self.save_evidence = None

            # Split the command line parameters.
            options, args = Lib.getopt(sys.argv[1:], "p:i:t:s:",
                                       ["project", "isolated_test_case", "test_case_id", "save_evidence"])

            print(options)

            for name, value in options:
                if name in ['-p']:  # Project.
                    self.project = value
                elif name in ['-i']:  # Isolated test case.
                    self.isolated_test_case = value
                elif name in ['-t']:  # Test case id.
                    self.test_case_id = value
                elif name in ['-s']:  # Save evidence.
                    self.save_evidence = value

            print(f'Project:               {self.project}\n'
                  f'Isolated Test case:    {self.isolated_test_case}\n'
                  f'Test Case ID:          {self.test_case_id}\n'
                  f'Save evidence:         {self.save_evidence}\n'
                  )

            app_core.main(project_id=self.project, isolated_tc=self.isolated_test_case, id_test_case=self.test_case_id,
                          save_evidence=self.save_evidence)

        # NO arguments.
        else:
            app_core.main()

    @staticmethod
    def cmdHelp():

        os.system('cls')

        parser = Lib.argparse.ArgumentParser(prog='AutomationQA', prefix_chars='-+', conflict_handler='resolve',
                                             formatter_class=Lib.argparse.RawDescriptionHelpFormatter,
                                             description=Lib.textwrap.dedent(
                                                 '''Please check the parameters below:
                                                 --------------------------------
                                                 project   - Mandatory to inform the project source.
                                                 isolated  - Mandatory to run one test case or the whole test suit.
                                                 ID test case - Mandatory when the isolated is equal to "YES".
                                                 save evidence - Mandatory to inform if it is necessary to save the evidence.
                                                 '''))
        default = parser.add_argument_group('default')
        default.add_argument('-p', type=int, help='Inform the project ID.', required=True)
        default.add_argument('-i', choices=['Y/S', 'N'], help='Test Case isolated', required=True)
        default.add_argument('-t', type=int, help='Inform the test case ID.', required=True)
        default.add_argument('-e', type=int, help='Save the necessity to generate the evidence.', required=True)


if __name__ == "__main__":
    run = AutomationQA()
