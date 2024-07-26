import os.path
import sys

sys.path.append(os.path.abspath(''))
import common_libs as Lib


class Update:

    def __init__(self):
        # Lib.Aux.Main.setLanguage(language='pt_BR')

        self.git_url_package = 'https://github.com/fv112/Automation/tree/CommandLine/exec/Automation_EXE.zip'
        self.git_url_install = 'https://github.com/fv112/Automation/tree/CommandLine/exec/Install.bat'
        self.git_url_readme = 'https://raw.githubusercontent.com/fv112/Automation/CommandLine/README.md'

        self.readme_content = self.read_html_content()

        self.version_actual, _, _ = Lib.Aux.Main.releaseNotes(readme=self.readme_content)
        path = Lib.os.path.join(Lib.os.path.dirname(Lib.os.path.realpath(__file__)), 'README.md')
        self.version_distributed, _, _ = Lib.Aux.Main.releaseNotes(path=path)

        Update.check(self)

    def read_html_content(self):

        response = Lib.requests.get(self.git_url_readme, verify=False).text
        soup = Lib.BeautifulSoup(response, 'html.parser').contents

        return soup

    def check(self):
        if self.version_distributed > self.version_actual:
            print("Nova versão disponível")

            if not os.path.exists(Lib.Aux.directories['DownloadFolder']):
                os.makedirs(Lib.Aux.directories['DownloadFolder'])

            output_filepath = os.path.join(Lib.Aux.directories['DownloadFolder'], 'Automation_EXE.zip')
            ### Falta colocar o installer também.

            response = Lib.requests.get('https://github.com/fv112/Automation/tree/CommandLine/exec/Automation_EXE.zip')
            if response.status_code == 200:
                with open(output_filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Arquivo baixado com sucesso: {output_filepath}")
            else:
                print(f"Falha ao baixar o arquivo: {response.status_code}")

        else:
            print("Versão mais atual já instalada")


if __name__ == "__main__":
    run = Update()
