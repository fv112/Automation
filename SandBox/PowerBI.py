import requests
import pandas as pd
import urllib3

urllib3.disable_warnings()

frames = []


def _connection(**kwargs):

    # kwargs variable.
    url = kwargs.get('url')
    headers = kwargs.get('headers')

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code != 200:
        print("Erro ao listar os bugs.")

    return response

# ----------------------------------------------------------------------------------------------------------------------

url1 = "https://sbs.t-systems.com.br/gitlab/api/v4/projects?topic=QA-Automation"

headers = {
    "Authorization": "Bearer rrkae8z2EMv_kfxXdCD-"
}

response_project = _connection(url=url1, headers=headers)

if response_project.status_code == 200:

    # page = 1

    data_project = response_project.json()

    for _, project_id in enumerate(data_project):
        print(f"Bugs do projeto '{project_id['name']}' listado com sucesso")
        page = 1
        while True:
            url2 = ('https://sbs.t-systems.com.br/gitlab/api/v4/projects/' + str(project_id['id']) +
                    '/issues?label=[%27phase::Code%20Review%27,%27phase::QA%27,%27phase::'
                    'UAT%27,%27phase::Production%20Issue%27]&per_page=1000&page=' + str(page))

            response_ct = _connection(url=url2, headers=headers)

            if response_ct.status_code == 200:
                data_ct = response_ct.json()
                df = pd.DataFrame(data_ct)

                if not df.empty:
                    print(f"Page {page}\n")
                    frames.append(df)
                else:
                    print(f"Page {page}\n")
                    frames = [df.dropna(how='all', axis=1) for df in frames if not df.empty]
                    df_final = pd.concat(frames, ignore_index=True)
                    print(df_final)
                    break

                page += 1
            else:
                print(f"Erro ao ler os casos de teste: {response_ct.status_code}")

    else:
        print(f"Erro ao ler os projetos: {response_project.status_code}")
