import common_libs as Lib

url = 'https://sbs.t-systems.com.br/gitlab/api/v4/'

Lib.urllib3.disable_warnings()


class Connections:

    def __init__(self):
        pass

    # Execute each step.
    def start_steps(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get('project_id')
        test_case_id = kwargs.get('test_case_id')

        # Execute each test case.
        name_testcase, step_block, web_url = self.execute_test_case(project_id=project_id, test_case_id=test_case_id)

        # Load the test case steps.
        steps_list, order_steps_list = self.get_steps(step_block=step_block)
        verbs_list, parameters1_list, parameters2_list = self.slice_datas(steps_list=steps_list)

        return order_steps_list, name_testcase, steps_list, verbs_list, parameters1_list, parameters2_list, web_url

    # Read the print screen from each step.
    # def manualEvidences(self, **kwargs):
    #
    #     try:
    #         # kwargs variables.
    #         project = kwargs.get('project')
    #         test_run_id = kwargs.get('test_run_id')
    #         id_test_case = kwargs.get('id_test_case')
    #
    #         test_case_id_list = []
    #         n_iterations_list = []
    #         id_azure_list = []
    #         n_test_case_list = []
    #         completed_date_list = []
    #         failed_info_dict = {}
    #         n_test_case = 0
    #
    #         amount_test_case, id_azure, full_name_run_test = self.getTestCaseRun(self, project=project,
    #                                                                                     test_run_id=test_run_id,
    #                                                                                     id_test_case=id_test_case)
    #
    #         for n_test_case in range(0, amount_test_case):
    #             test_case_id, n_iterations, failed_info_dict, completed_date = self.attachmentList(
    #                 self, project=project, test_run_id=test_run_id, n_test_case=n_test_case,
    #                 failed_info_dict=failed_info_dict, id_azure=id_azure)
    #
    #             n_iterations_list.append(n_iterations)
    #             id_azure_list.append(id_azure)
    #             id_azure += 1
    #             test_case_id_list.append(test_case_id)
    #             n_test_case += 1
    #             n_test_case_list.append(n_test_case)
    #             completed_date_list.append(completed_date)
    #
    #     except (TypeError, AttributeError):
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['IDRunInvalid']['Msg']} '{test_run_id}'"
    #               f"{Lib.Aux.Textcolor.END}")
    #         #exit(1)
    #
    #     else:
    #         return test_case_id_list, n_iterations_list, id_azure_list, n_test_case_list, failed_info_dict, \
    #                completed_date_list, full_name_run_test

    # ===================================== Modules to extract info from GitLab ========================================
    # Load the project list from GitLab.
    def get_projects(self, **kwargs):

        # Kwargs variables.
        project_id = kwargs.get('project_id', None)

        projects_dic = {}
        resp = []

        try:
            if project_id is None:
                new_url = url + 'projects?topic=QA-Automation'
            else:  # command line.
                new_url = url + 'projects/' + str(project_id) + '?topic=QA-Automation'

            t = Lib.requests.get(new_url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]},
                                 verify=False)

            if t.status_code == 200:
                # Filter some fields.
                json_str = Lib.json.dumps(t.json())
                resp = Lib.json.loads(json_str)
            elif t.status_code == 401:
                print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['RunAgain']['Msg']}"
                      f"{Lib.Aux.Textcolor.UNDERLINE}\n")
                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorTokenExpired'])

            else:
                print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.UNDERLINE}\n")
                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorRequest'],
                                      value1='Status code: ' + str(t.status_code) + ' - getProjects')

            # Menu.
            if resp is not [] and project_id is None:

                table = Lib.PrettyTable(['PROJECT ID', 'PROJECT'])
                table.align['PROJECT'] = 'l'

                for order in range(0, resp.__len__()):
                    table.add_row([str(resp[order]['id']), str(resp[order]['name'])])
                    projects_dic[resp[order]['id']] = str(resp[order]['name'])

                table.set_style(Lib.DOUBLE_BORDER)
                print(table.get_string(sortby="PROJECT"))

                project_list = [str(project_id) for project_id in list(projects_dic.keys())]

                while True:
                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['InformProject']['Msg']}"
                          f"{Lib.Aux.Textcolor.END}\n")
                    project_selected = input()
                    if Lib.Aux.Main.validate_selection(input_data=project_selected, search_list=project_list):
                        break

                project_name = projects_dic[int(project_selected)]
                return project_selected, project_name

            # Command line.
            elif resp is not [] and project_id is not None:

                # Filter some fields.
                json_str = Lib.json.dumps(t.json())
                resp = Lib.json.loads(json_str)
                if resp is not []:
                    return project_id, resp['name'],

            else:
                raise Exception(Lib.Aux.logs['ErrorGetProjects']['Msg'])

        except Lib.requests.exceptions.RequestException:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorConnection']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorConnection'])

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetProjects']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorGetProjects'], value1=str(ex))
            # exit(1)

    # Load the test plans.
    # def getTestPlans(self, **kwargs):
    #     test_plan_selected = 0
    #
    #     try:
    #
    #         # Get the kwargs variables.
    #         project = kwargs.get("project")
        #
        #     version = '5.1-preview.1'
        #     option = 1
        #     test_plans = []
        #
        #     url = 'https://' + instance + project + '/_apis/testplan/plans?filterActivePlans=True&api-version=' \
        #                + version
        #
        #     # Execute the request from Azure.
        #     q = requests.get(url, auth=Lib.Aux.otherConfigs['HttpBasicAuth'], verify=False)
        #     if q.status_code == 200:
        #         # Filter some fields.
        #         json_str = json.dumps(q.json())
        #         resp = json.loads(json_str)
        #         if resp['count'] != 0:
        #
        #             for testPlan_id in resp['value']:
        #                 test_plans.append(testPlan_id['name'] + '|' + str(testPlan_id['id']))
        #                 option += 1
        #             return test_plans
        #
        #         else:
        #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestPlan']['Msg']}{Lib.Aux.Textcolor.END}\n")
        #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorGetTestPlan'])
        #             #exit(1)
        #
        #     else:
        #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
        #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
        #                     value1='Status code: ' + str(q.status_code) +' - getTestPlans')
        #
        # except ValueError:
        #     print(f"{Lib.Aux.Textcolor.FAIL}'{test_plan_selected}' {Lib.Aux.otherConfigs['OptionInvalid']['Msg']}"
        #           f"{Lib.Aux.Textcolor.END}")
        #     #exit(0)

        #     return 0
        #
        # except Exception as e:
        #     print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestPlans']['Msg']}{Lib.Aux.Textcolor.END}", e)
        #     Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorGetTestPlans'], value1=str(e))
        #     # #exit(1)

    # Load the Test Suits.
    # def getTestSuits(self, **kwargs):
    #     test_suit_selected = 0
    #
    #     try:
    #
    #         # Get the kwargs variables.
    #         project = kwargs.get("project")
    #         id_test_plan = kwargs.get("id_test_plan")

            # version = '5.0'
            # option = 1
            # test_suit = []
            #
            # url = 'https://' + instance + project + '/_apis/test/plans/' + str(id_test_plan) + '/suites/' +\
            #            '?api-version=' + version
            #
            # # Execute the request from Azure.
            # r = requests.get(url, auth=Lib.Aux.otherConfigs['HttpBasicAuth'], verify=False)
            # if r.status_code == 200:
            #     # Filter some fields.
            #     json_str = json.dumps(r.json())
            #     resp = json.loads(json_str)
            #     if resp['count'] != 0:
            #
            #         for testSuit_id in resp['value']:
            #             test_suit.append(testSuit_id['name'] + '|' + str(testSuit_id['id']))
            #             option += 1
            #         return test_suit
            #
            #     else:
            #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestSuit']['Msg']}{Lib.Aux.Textcolor.END}\n")
            #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorGetTestSuit'])
            #
            # else:
            #     print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
            #     Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
            #                 value1='Status code: ' + str(r.status_code) + ' - getTestSuits')
        #     return 0, 0
        #
        # except ValueError:
        #     print(f"{Lib.Aux.Textcolor.FAIL}'{test_suit_selected}' {Lib.Aux.otherConfigs['OptionInvalid']['Msg']}"
        #           f"{Lib.Aux.Textcolor.END}")
        #     #exit(0)
        #
        # except Exception as e:
        #     print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestSuits']['Msg']}{Lib.Aux.Textcolor.END}", e)
        #     Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorGetTestSuits'], value1=str(e))
        #     #exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Load the test cases.

    def get_test_cases(self, **kwargs):

        try:

            # kwargs variables.
            project_id = kwargs.get("project_id")
            isolated_tc = kwargs.get("isolated_tc")
            id_test_case = kwargs.get("id_test_case")

            # Variables.
            test_case_id_list = []
            page = 1

            new_url = url + 'projects/' + str(project_id) + ('/issues?labels=Test%20case&per_page=100&page=' + str(page)
                                                             + '&not[labels]=Execution::Only%20Manual')

            s = Lib.requests.get(new_url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]},
                                 verify=False)

            while True:
                if s.status_code == 200:
                    # Filter some fields.
                    json_str = Lib.json.dumps(s.json())
                    resp = Lib.json.loads(json_str)
                    page += 1
                    if 'next' not in resp or resp['next'] is None:
                        break
                elif s.status_code == 401:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['RunAgain']['Msg']}"
                          f"{Lib.Aux.Textcolor.UNDERLINE}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.otherConfigs['TokenExpired'])
                    raise Exception

                else:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorRequest'],
                                          value1='Status code: ' + str(s.status_code) + ' - getTestCases')
                    raise Exception

            table = Lib.PrettyTable(["STATUS", "ORDER", "TEST CASE ID", "TEST CASE"])
            table.align['STATUS'] = 'l'
            table.align['TEST CASE'] = 'l'

            if resp.__len__() != 0:
                for id_test, testCase_id in enumerate(resp):
                    actual_status = [status for status in testCase_id['labels'] if 'Status' in status]

                    if not actual_status:
                        status = "Not Run"
                    else:
                        status = actual_status[0].replace('Status::', '')

                    if status == 'Failed':
                        status = f"{Lib.Aux.Textcolor.FAIL}{status}{Lib.Aux.Textcolor.END}"
                    elif status == 'Passed':
                        status = f"{Lib.Aux.Textcolor.GREEN}{status}{Lib.Aux.Textcolor.END}"
                    elif status == 'Blocked':
                        status = f"{Lib.Aux.Textcolor.BLUE}{status}{Lib.Aux.Textcolor.END}"
                    elif status == 'Aborted':
                        status = f"{Lib.Aux.Textcolor.WARNING}{status}{Lib.Aux.Textcolor.END}"

                    table.add_row([status, id_test + 1, str(testCase_id['iid']), testCase_id['title']])
                    test_case_id_list.append(testCase_id['iid'])

                while isolated_tc is None:
                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['AskCt']['Msg']}"
                          f"{Lib.Aux.Textcolor.END} ")
                    isolated_tc = input()
                    if Lib.Aux.Main.validate_selection(input_data=isolated_tc.upper(),
                                                       search_list=['Y', 'S', 'N', '']):
                        break

                print(
                    f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['TestCaseList']['Msg']}"
                    f"{Lib.Aux.Textcolor.END}")
                table.set_style(Lib.DOUBLE_BORDER)
                print(table)

                if isolated_tc.upper() != 'I':  # Only info.

                    test_case_list = [str(testcase_id) for testcase_id in test_case_id_list]

                    if isolated_tc.upper() in ['Y', 'S', ''] and id_test_case == 0:
                        while True:
                            print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['ChooseTestCase']['Msg']}"
                                  f"{Lib.Aux.Textcolor.END} ")
                            id_test_case = input()
                            if Lib.Aux.Main.validate_selection(input_data=id_test_case, search_list=test_case_list):
                                test_case_id_list.clear()
                                test_case_id_list.append(int(id_test_case))
                                break
                    elif isolated_tc.upper() in ['Y', 'S', ''] and id_test_case != 0:
                        if Lib.Aux.Main.validate_selection(input_data=id_test_case, search_list=test_case_list):
                            test_case_id_list.clear()
                            test_case_id_list.append(int(id_test_case))
                    elif isolated_tc.upper() in ['N', 'n']:  # Not add a new test case if 'N' is informed.
                        pass
                    else:
                        test_case_id_list.append(id_test_case)

            else:
                print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestCase']['Msg']}{Lib.Aux.Textcolor.END}\n")
                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorGetTestCase'])
                raise Exception

            return test_case_id_list

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetTestCases']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorGetTestCases'],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            # exit(1)

    # ===================================================== TEST CASE ==================================================
    # Execute the Test Case from GitLab.
    def execute_test_case(self, **kwargs):
        try:
            # kwargs variables.
            project_id = kwargs.get("project_id")
            test_case_id = kwargs.get("test_case_id")

            name_testcase = ''
            step_block = ''
            web_url = ''

            new_url = (url + 'projects/' + str(project_id) + '/issues?iids[]=' + str(test_case_id))

            # Execute the request from Azure.
            q = Lib.requests.get(new_url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]},
                                 verify=False)
            if q.status_code == 200:
                print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['RequestOK']['Msg']}{Lib.Aux.Textcolor.END}\n")
                # Filter some fields.
                json_str = Lib.json.dumps(q.json())
                resp = Lib.json.loads(json_str)
                name_testcase = resp[0]['title']
                step_block = resp[0]['description']
                web_url = resp[0]['web_url']

                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ExecuteTestCase'])
            else:
                print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorRequest'],
                                      value1='Status code: ' + str(q.status_code) + ' - executeTestCase')

            return name_testcase, step_block, web_url

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorExecuteTestCase']['Msg']}{Lib.Aux.Textcolor.END} - {ex}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorExecuteTestCase'], value1=str(ex))
            # exit(1)

    # Extract the steps from Test Case.
    def get_steps(self, **kwargs):

        try:
            # Variables.
            order_steps_list = []
            steps_list = []

            # kwargs variables.
            step_block = kwargs.get("step_block")

            steps = step_block.splitlines()
            for order_steps, step in enumerate(steps):
                order_steps_list.append(order_steps + 1)
                steps_list.append(step)

            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['GetSteps'])

            return steps_list, order_steps_list

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorGetSteps']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorGetSteps'], value1=str(ex))
            # exit(1)

    # Dismember the variables from each test case.
    def slice_datas(self, **kwargs):

        try:
            # Variables.
            verbs_list = []
            parameters1_list = []
            parameters2_list = []

            # kwargs variables.
            steps_list = kwargs.get("steps_list")

            for step in steps_list:
                verbs_list.append(step[:step.index(" ")])

            for step in steps_list:
                count_character = step.count('\"')
                if count_character == 0:
                    parameters1_list.append(None)
                    parameters2_list.append(None)
                elif count_character == 2:
                    parameters1_list.append(Lib.regex.findall(r'"([^"]*)"', step)[0])
                    parameters2_list.append(None)
                elif count_character == 4:
                    parameters1_list.append(Lib.regex.findall(r'"([^"]*)"', step)[0])
                    parameters2_list.append(Lib.regex.findall(r'"([^"]*)"', step)[1])
                elif count_character > 4:  # API content.
                    parameters1_list.append(step[step.find("\"")+1:-1])
                    parameters2_list.append(None)

            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['SliceDatas'])

            return verbs_list, parameters1_list, parameters2_list

        # When there is no variable.
        except ZeroDivisionError:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorLineEmpty']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorLineEmpty'])

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorSliceDatas']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorSliceDatas'], value1=str(ex))

    def update_labels(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        test_case_id = kwargs.get("test_case_id")
        status_ct = 'Status::' + kwargs.get("status_ct")

        update_data = None

        try:

            new_url = url + 'projects/' + str(project_id) + '/issues/' + str(test_case_id)

            q = Lib.requests.get(new_url, verify=False,
                                 headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["BearerUpload"]})
            if q.status_code == 200:
                issue_data = q.json()
                current_labels = issue_data.get("labels", [])

                for remove_item in ['Status', 'Execution']:
                    current_labels = [item for item in current_labels if remove_item not in item]

                if status_ct not in current_labels:
                    current_labels.append(status_ct)
                current_labels.append('Execution::Automated')

                update_data = {
                    "labels": ",".join(current_labels)
                }

            s = Lib.requests.put(new_url, data=update_data, verify=False,
                                 headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["BearerUpload"]})

            if q.status_code == 200 and s.status_code == 200:
                print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['UpdateLabels']['Msg']}"
                      f"{Lib.Aux.Textcolor.END}\n")
                Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['UpdateLabels'])
            else:
                raise Exception(f"Status code Get labels: {q.status_code} / Update labels: {s.status_code}")

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorUpdateLabels']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorUpdateLabels'], value1=str(ex))

    # Upload the evidence in the TestCase.
    def upload_file_git_token(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        name_testcase = kwargs.get("name_testcase")
        status_ct = kwargs.get("status_ct")
        file_type = kwargs.get("file_type")

        status_name_testcase = None
        file_path_list = []
        file_url_list = []
        files_list = []

        try:

            new_url = (url + 'projects/' + str(project_id) + '/uploads')

            if file_type == 'tc':
                if status_ct == 'Failed':
                    status_name_testcase = '[BUG] - ' + name_testcase
                else:
                    status_name_testcase = name_testcase

                file_path_list.append(Lib.os.path.join(Lib.Aux.directories['TestSetPath'],
                                                       status_name_testcase) + ".pdf")

            elif file_type == 'download_file':
                files_list = Lib.os.listdir(Lib.Aux.directories['DownloadFolder'])

                for cont, file_path in enumerate(files_list):
                    file_path_list.append(Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], files_list[cont]))

            for file_path in file_path_list:

                file_binary = {'file': open(file_path, 'rb')}

                with open(file_path, 'rb'):
                    q = Lib.requests.post(new_url, headers={'Authorization': 'Bearer ' +
                                                                             Lib.Aux.otherConfigs["BearerUpload"]},
                                          files=file_binary, verify=False)

                if q.status_code == 201:
                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['UploadFileGitToken']['Msg']}"
                          f"{Lib.Aux.Textcolor.END}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['UploadFileGitToken'])

                    # Filter some fields.
                    json_str = Lib.json.dumps(q.json())
                    resp = Lib.json.loads(json_str)
                    file_url_list.append(resp['url'])

                else:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorRequest'],
                                          value1='Status code: ' + str(q.status_code) + ' - ' + str(
                                              q.text) + ' - UploadFileGitToken')

            return file_url_list, file_path_list, status_name_testcase

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorUploadFileGitToken']['Msg']} - {ex}"
                  f"{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorUploadFileGitToken'], value1=str(ex))

    def upload_file_git(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        test_case_id = kwargs.get("test_case_id")
        status_name_testcase = kwargs.get('status_name_testcase', '')
        file_url_list = kwargs.get('file_url_list')
        file_path_list = kwargs.get('file_path_list')

        try:
            if file_path_list.__len__() != 0:
                path = Lib.regex.search(r'^(.*\\)[^\\]+\.\w+$', file_path_list[0]).group(1)
                if file_path_list.count == Lib.os.listdir(path):
                    raise Exception(Lib.Aux.logs['ErrorUploadFileAmount']['Msg'])
            else:
                raise Exception(Lib.Aux.logs['ErrorUploadFileAmount']['Msg'])

            new_url = (url + 'projects/' + str(project_id) + '/issues/' + str(test_case_id) + '/notes')

            for cont, file_path in enumerate(file_path_list):

                if status_name_testcase == '':
                    file_url = file_url_list[cont].replace("file", status_name_testcase + ".pdf")

                    body = {
                        "body": "[" + status_name_testcase + "](" + file_url + ")"
                    }
                else:
                    file = Lib.regex.search(r'([^\\]+)\.\w+$', file_path_list[cont]).group(0)
                    body = {
                        "body": "[" + file + "](" + file_url_list[cont] + ")"
                    }

                p = Lib.requests.post(
                    new_url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["BearerUpload"]}, data=body,
                    verify=False)

                if p.status_code == 201:
                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['UploadFileGit']['Msg']}"
                          f"{Lib.Aux.Textcolor.END}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['UploadFileGit'])

                else:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
                    Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorRequest'],
                                          value1='Status code: ' + str(p.status_code) + ' - ' + str(
                                              p.text) + ' - UploadFileGit')

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorUploadFileGit']['Msg']} - {ex}"
                  f"{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorUploadFileGit'], value1=str(ex))

    def send_request(self, **kwargs):

        api_action = kwargs.get("api_action")
        headers = kwargs.get("headers")
        body = kwargs.get("body")
        fake_info = kwargs.get("fake_info", False)

        try:
            if Lib.Aux.otherConfigs['Api_Authorization'] != '':
                headers = {'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Api_Headers"],
                           'Content-Type': 'application/json'
                           }

            if 'Basic' in Lib.Aux.otherConfigs['Api_Headers']:
                headers = {
                    'Basic': Lib.Aux.otherConfigs['Api_Headers'][Lib.Aux.otherConfigs['Api_Headers'].find(':') + 1:],
                    'Content-Type': 'application/json'
                }
            elif 'Bearer' in Lib.Aux.otherConfigs['Api_Headers']:
                headers = {'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Api_Headers"],
                           'Content-Type': 'application/json'}
            else:
                headers = Lib.json.loads(Lib.regex.search(r'{(.*?)}', headers).group(0))
                headers['Content-Type'] = 'application/json'

            for endpoint in Lib.Aux.otherConfigs['Api_Endpoints']:

                if api_action.upper() == "DELETE":
                    api_result = Lib.requests.delete(endpoint, headers=headers)
                elif api_action.upper() == "POST":
                    api_result = Lib.requests.post(endpoint, headers=headers, data=body, verify=False)
                elif api_action.upper() == "PUT":
                    api_result = Lib.requests.put(endpoint, headers=headers)
                else:  # api_action.upper() == "GET":
                    api_result = Lib.requests.get(endpoint, data=Lib.json.dumps(body), verify=False,
                                                  params=Lib.Aux.otherConfigs['Api_Params'], headers=headers)

                if api_action.upper() in ['GET', 'POST', 'DELETE', 'PUT']:
                    Lib.Aux.otherConfigs['Api_StatusCode'] = api_result.status_code
                    resp = Lib.json.loads(api_result.text)
                    if resp is not []:
                        Lib.Aux.otherConfigs['Api_Response'] = resp

                    if fake_info and api_result.status_code == 400:
                        return resp, "Failed"
                    elif api_result.status_code == 400:
                        # The status code should be verified in the Response command.
                        return resp, "Passed"
                    elif api_result.status_code == 200:
                        return resp, "Passed"

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorSendRequest']['Msg']} - {ex}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs['ErrorSendRequest'], value1=str(ex))

            return None, "Failed"

    # def UpdateStatusAutomated(self, **kwargs):
    #
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         test_case_id = kwargs.get('test_case_id')
    #         automation_status = kwargs.get('automation_status')
    #         workitem_status = kwargs.get('workitem_status')
    #
    #         version = '6.1-preview.3'
    #
    #         url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
    #                    + version
    #
    #         headers = {'content-type': 'application/json-patch+json'}
    #
    #         file_datas = [
    #             {
    #                 "op": "add",
    #                 "path": "/fields/System.History",
    #                 "value": "Update the automation status and Test Case status"
    #             },
    #             {
    #                 "op": "add",
    #                 "path": "/fields/Microsoft.VSTS.TCM.AutomationStatus",
    #                 "value": automation_status
    #             },
    #             {
    #                 "op": "add",
    #                 "path": "/fields/System.State",
    #                 "value": workitem_status
    #             }
    #         ]
    #
    #         # r = requests.patch(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, json=file_datas, headers=headers,
    #         #                    verify=False)
    #         if r.status_code == 200:
    #             print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.logs['UpdateStatusAutomated']['Msg']}{Lib.Aux.Textcolor.END}")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['UpdateStatusAutomated'])
    #         else:
    #             raise Exception
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorUpdateStatusAutomated']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorUpdateStatusAutomated'],
    #                          value1='Status code: ' + str(r.status_code) + " - UpdateStatusAutomated")
    #         #exit(1)

    # Download de attachments when there are more than 100 in a WIT and upload a .zip file.
    # def _DownloadAttachment(self, **kwargs):
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         test_case_id = kwargs.get('test_case_id')
    #         cont_iteration = kwargs.get('cont_iteration')
    #         name_testcase = kwargs.get('name_testcase')
    # 
    #         count_evidences = 1
    #         order = 0
    #         version = '6.0'
    #         evidence_folder = Lib.Aux.os.path.join(Lib.Aux.directories['EvidenceFolder'], name_testcase)
    #         relation_list = []
    #         order_list = []
    #         count_evidences_list = []
    #         relation_failed = ''
    #         order_failed = ''
    #         count_evidences_failed = ''
    # 
    #         Lib.Aux.Main.deleteDirectory(self, directory=evidence_folder)
    #         Lib.Aux.Main.deleteFiles(self, file_path=Lib.Aux.os.path.join(Lib.Aux.directories['EvidenceFolder']), extension='.zip',
    #                              exact_file=name_testcase + '.zip')
    # 
    #         url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(test_case_id) + \
    #                    '&$expand=Relations&api-version=' + version
    # 
    #         r = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, verify=False)
    #         if r.status_code == 200:
    #             # Filter some fields.
    #             json_str = json.dumps(r.json())
    #             resp = json.loads(json_str)
    #             rev_id = resp['value'][0]['rev']
    #             total = resp['value'][0]['relations'].__len__()
    # 
    #             for relation in resp['value'][0]['relations']:
    #                 order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed = \
    #                     GitLabConnection._readRelation(self, project=project, total=total, test_case_id=test_case_id,
    #                                                   order=order, rev_id=rev_id, name_testcase=name_testcase,
    #                                                   count_evidences=count_evidences, relation=relation)
    # 
    #                 if relation_failed != None:
    #                     relation_list.append(relation_failed)
    #                     order_list.append(order_failed)
    #                     count_evidences_list.append(count_evidences_failed)
    # 
    #             # Sleep to try again.
    #             if relation_failed != None:
    #                 for seconds in range(1, 15):
    #                     time.sleep(1)
    #                     print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.logs['WaitTime']['Msg']}{seconds} / 15{Lib.Aux.Textcolor.END}")
    # 
    #             # If any download fail.
    #             while relation_list.__len__() != 0:
    #                 for relation in relation_list:
    #                     order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed = \
    #                         GitLabConnection._readRelation(self, name_testcase=name_testcase, order=order_list[0],
    #                                                       test_case_id=test_case_id, relation=relation,
    #                                                       total=count_evidences_list[-1], rev_id=rev_id,
    #                                                       project=project, count_evidences=count_evidences_list[0])
    # 
    #                     if relation_failed is None:
    #                         relation_list.pop(0)
    #                         order_list.pop(0)
    #                         count_evidences_list.pop(0)
    # 
    #             print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.logs['GenerateZIPFile']['Msg']}{Lib.Aux.Textcolor.END}")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['GenerateZIPFile']['Msg'])
    #             Lib.Aux.shutil.make_archive(evidence_folder, 'zip', evidence_folder)
    # 
    #             GitLabConnection.UploadDownloadFile(self, project=project, test_case_id=str(test_case_id),
    #                                                evidence_folder=Lib.Aux.directories['EvidenceFolder'],
    #                                                download_file_name=name_testcase + '.zip',
    #                                                file_name=name_testcase + '.zip')
    # 
    #     except Exception as e:
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorDownloadAttachment'], value1=str(e))
    #         #exit(1)

    # Read the test case relation to upload the .zip file.
    # def _readRelation(self, **kwargs):
    #
    #     # kwargs arguments.
    #     project = kwargs.get('project')
    #     relation = kwargs.get('relation')
    #     rev_id = kwargs.get('rev_id')
    #     total = kwargs.get('total')
    #     order = kwargs.get('order')
    #     count_evidences = kwargs.get('count_evidences')
    #     name_testcase = kwargs.get('name_testcase')
    #     test_case_id = kwargs.get('test_case_id')
    #
    #     # Variables.
    #     version = '6.0'
    #     relation_failed = None
    #     order_failed = None
    #     count_evidences_failed = None
    #
    #     try:
    #
    #         # Extract only if it a .pdf evidence.
    #         if relation['rel'] == 'AttachedFile' and relation['attributes']['name'].split('.')[-1] == 'pdf':
    #             date_time_folder = relation['attributes']['resourceCreatedDate'].replace(':', '.')
    #             id_point = relation['url'].split('/')[7]
    #             name = relation['attributes']['name']
    #
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['GenerateZIP']['Msg']} {count_evidences} / "
    #                   f"{total}{Lib.Aux.Textcolor.END}")
    #
    #             Lib.Aux.Main.createDirectory(self, path_folder=Lib.Aux.os.path.join(Lib.Aux.directories['EvidenceFolder'],
    #                                                                         name_testcase, date_time_folder))
    #
    #             url = 'https://' + instance + project + '/_apis/wit/attachments/' + str(id_point) + \
    #                        '?api-version=' + version
    #             s = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, timeout=10)
    #
    #             download = Lib.Aux.os.path.join(Lib.Aux.directories['EvidenceFolder'], name_testcase, date_time_folder, name)
    #             with open(download, 'wb') as f:
    #                 f.write(s.content)
    #
    #             # Delete de .pdf files.
    #             if s.status_code == 200:
    #                 GitLabConnection.DeleteDownloadFile(self, project=project, rev_id=rev_id,
    #                                                    test_case_id=str(test_case_id), order=order)
    #             rev_id += 1
    #         else:
    #             order += 1
    #         count_evidences += 1
    #
    #     # If any download fail.
    #     except requests.ConnectionError:
    #         relation_failed = relation
    #         order_failed = order
    #         count_evidences_failed = count_evidences
    #         count_evidences += 1
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorDownloadAttachment']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorDownloadAttachment'], value1=str(e))
    #         #exit(1)
    #
    #     finally:
    #         return order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed

    # Check if the download Baseline exist or not.
    # def CheckDownloadFile(self, **kwargs):
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         test_case_id = kwargs.get('test_case_id')
    #         file_name = kwargs.get('file_name')
    #         evidence_folder = kwargs.get('evidence_folder')
    #         compare = kwargs.get('compare')
    #
    #         version = '6.0'
    #
    #         # check if the download file already exist.
    #         url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + \
    #                    '?$expand=all&api-version=' + version
    #
    #         q = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, verify=False)
    #
    #         if q.status_code == 200:
    #             flag_save_baseline = True
    #
    #             # Filter some fields.
    #             json_check = json.dumps(q.json())
    #             req = json.loads(json_check)
    #             rev_id = req['rev']
    #             for order in range(1, len(req['relations'])):
    #                 name_file_downloaded = req['relations'][order]['attributes']['name']
    #
    #                 if compare:  # For compare the files.
    #                     if name_file_downloaded == str(file_name):
    #                         flag_save_baseline = True
    #                         download_file_name = file_name
    #                 else:  # For execution
    #                     # Verify if the Baseline doesn't exist.
    #                     if name_file_downloaded == ('Baseline - ' + str(file_name)):
    #                         flag_save_baseline = False
    #
    #                     if flag_save_baseline:
    #                         download_file_name = 'Baseline - ' + file_name
    #                     else:
    #                         download_file_name = 'New - ' + file_name
    #
    #                 # Verify if the New file exists and delete for a new one OR replace the Baseline after compare.
    #                 if name_file_downloaded == 'New - ' + file_name or name_file_downloaded == str(file_name):
    #                     GitLabConnection.DeleteDownloadFile(self, project=project, rev_id=rev_id,
    #                                                        test_case_id=str(test_case_id), order=order)
    #                     rev_id += 1
    #
    #             GitLabConnection.UploadDownloadFile(self, project=project, evidence_folder=evidence_folder,
    #                                                test_case_id=str(test_case_id),
    #                                                download_file_name=download_file_name, file_name=file_name)
    #
    #             print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['CheckDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['CheckDownloadFile'])
    #
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(q.status_code) + ' - CheckDownloadFile')
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorCheckDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorCheckDownloadFile'], value1=str(e))
    #         #exit(1)
    #
    # # Delete the 'New' download file to the TestCase.
    # def DeleteDownloadFile(self, **kwargs):
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         rev_id = kwargs.get('rev_id')
    #         test_case_id = kwargs.get('test_case_id')
    #         order = kwargs.get('order')
    #
    #         version = '6.0'
    #
    #         # check if the download file already exist.
    #         url = 'https://' + instance + project + '/_apis/wit/workitems/' + test_case_id + '?api-version=' \
    #                    + version
    #
    #         headers = {'content-type': 'application/json-patch+json'}
    #
    #         attachment_details = [
    #             {
    #                 "op": "test",
    #                 "path": "/rev",
    #                 "value": rev_id,
    #             },
    #             {
    #                 "op": "remove",
    #                 "path": "/relations/" + str(order)
    #             }
    #         ]
    #
    #         # q = requests.patch(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, json=attachment_details,
    #         #                    headers=headers, verify=False)
    #
    #         if q.status_code == 200:
    #             print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['DeleteDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['DeleteDownloadFile'])
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(q.status_code) + ' - DeleteDownloadFile')
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorDeleteDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorDeleteDownloadFile'], value1=str(e))
    #         #exit(1)

    # Upload the download file in the TestCase.
    # def UploadDownloadFile(self, **kwargs):
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         evidence_folder = kwargs.get('evidence_folder')
    #         test_case_id = kwargs.get('test_case_id')
    #         file_name = kwargs.get('file_name')
    #         download_file_name = kwargs.get('download_file_name')
    #
    #         # Get the Attachment ID.
    #         version = '6.0'
    #
    #         url = 'https://' + instance + project + '/_apis/wit/attachments?fileName=' + str(file_name) + \
    #                    '&api-version=' + version
    #
    #         with open(Lib.Aux.os.path.join(evidence_folder, file_name), "rb") as file:
    #             data = file.read()
    #
    #         headers = {'Content-Type': 'application/octet-stream'}
    #
    #         # p = requests.post(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, data=data, headers=headers,
    #         #                   verify=False)
    #         if p.status_code == 201:
    #             # Filter some fields.
    #             json_str = json.dumps(p.json())
    #             resp = json.loads(json_str)
    #             idAttachment = resp['id']
    #             print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['UploadDownloadFileID']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['UploadDownloadFileID'])
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(p.status_code) + ' - UploadDownloadFileID')
    #
    #         # ------------------------------------ Second API conection ------------------------------------------------
    #
    #         # Add the attachment in Azure.
    #         version = '6.1-preview.3'
    #
    #         url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
    #                    + version
    #
    #         headers = {'content-type': 'application/json-patch+json'}
    #
    #         file_datas = [
    #             {
    #                 "op": "add",
    #                 "path": "/fields/System.History",
    #                 "value": "Download file: " + download_file_name
    #             },
    #             {
    #                 "op": "add",
    #                 "path": "/relations/-",
    #                 "value": {
    #                     "rel": "AttachedFile",
    #                     "url": "https://kantarware.visualstudio.com/_apis/wit/attachments/" + idAttachment +
    #                            "?fileName=" + download_file_name,
    #                     "attributes": {
    #                         "comment": download_file_name
    #                     }
    #                 }
    #             }
    #         ]
    #
    #         # q = requests.patch(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, json=file_datas, headers=headers,
    #         #                    verify=False)
    #         if q.status_code == 200:
    #             print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['UploadDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['UploadDownloadFile'])
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(q.status_code) + ' - UploadDownloadFile')
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorUploadDownloadFile']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorUploadDownloadFile'], value1=str(e))
    #         #exit(1)
    #
    # # Save the download file, from the test case locally.
    # def SaveDownloadFileLocally(self, **kwargs):
    #     try:
    #         # kwargs arguments.
    #         project = kwargs.get('project')
    #         id_testcase = kwargs.get('id_testcase')
    #
    #         list_names = ['Baseline -', 'New -']
    #         list_files_baseline = []
    #         list_files_new = []
    #
    #         # Get the Attachment ID.
    #         version = '6.0'
    #
    #         url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(id_testcase) + \
    #                    '&$expand=all&api-version=' + version
    #
    #         p = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, verify=False)
    #         if p.status_code == 200:
    #             # Filter some fields.
    #             json_str = json.dumps(p.json())
    #             resp = json.loads(json_str)
    #
    #             for order in range(1, len(resp['value'][0]['relations'])):
    #                 download_name = resp['value'][0]['relations'][order]['attributes']['name']
    #                 test_name = resp['value'][0]['fields']['System.Title']
    #
    #                 if any(x in download_name for x in list_names):
    #                     file_url = resp['value'][0]['relations'][order]['url']
    #
    #                     r = requests.get(file_url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, verify=False)
    #
    #                     # Create the Compare directory.
    #                     Lib.Aux.Main.createDirectory(self,
    #                                              path_folder=Lib.Aux.os.path.join(Lib.Aux.directories['CompareDownloadFolder'],
    #                                                                           test_name))
    #
    #                     download = Lib.Aux.os.path.join(Lib.Aux.directories['CompareDownloadFolder'], test_name, download_name)
    #                     with open(download, 'wb') as file:
    #                         file.write(r.content)
    #
    #                     if list_names[0] in download_name:
    #                         list_files_baseline.append(download_name)
    #                     else:
    #                         list_files_new.append(download_name)
    #
    #             print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['SaveDownloadFileLocally']['Msg']}"
    #                   f"{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['SaveDownloadFileLocally'])
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(p.status_code) + ' - ErrorSaveDownloadFileLocally')
    #
    #         return test_name, id_testcase, sorted(list_files_baseline), sorted(list_files_new)
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorSaveDownloadFileLocally']['Msg']}"
    #               f"{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorSaveDownloadFileLocally'], value1=str(e))
    #         #exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Functions to manual evidence.
    # ------------------------------------------------------------------------------------------------------------------
        # Load the attachment list in Run Result.
    # def attachmentList(self, **kwargs):
    #     try:
    #         version = '6.0'
    #
    #         # kwargs variables.
    #         project = kwargs.get('project')
    #         n_test_case = kwargs.get('n_test_case')
    #         test_run_id = kwargs.get('test_run_id')
    #         failed_info_dict = kwargs.get('failed_info_dict')
    #         id_azure = kwargs.get('id_azure')
    #
    #         # Using inside the function.
    #         list_id_manual_print = []
    #         list_step_status_manual = []
    #         list_num_print = []
    #         index = 0
    #
    #         # Return values.
    #         failed_details = {}
    #
    #         url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + '/results/' + \
    #                    str(id_azure) + '/?detailsToInclude=iterations&?api-version=' + version
    #
    #         # Execute the Azure request.
    #         q = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]}, verify=False)
    #         if q.status_code == 200:
    #             # Filter some fields.
    #             json_str = json.dumps(q.json())
    #             resp = json.loads(json_str)
    #
    #             # Verify the test execution.
    #             # if not resp['iterationDetails']:
    #             #     raise Exception(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['NoExecutions']['Msg']}{Lib.Aux.Textcolor.END}")
    #
    #             # Verify the number of test cases.
    #             # if resp['iterationDetails'] != 0:
    #             test_case_id = resp['testCase']['id']
    #             test_case_name = GitLabConnection.getTestCaseName(self, project=project, test_case_id=test_case_id)
    #
    #             # Failed dictionary.
    #             failed_info_dict[test_case_id] = {}
    #
    #                 # Validate the testcase name.
    #                 # if Lib.Aux.Main.validateTestName(self, name_testcase=test_case_name):
    #                 #     return test_case_id, None, failed_info_dict, None
    #
    #                 # Verify the number of iteration for each test case.
    #                 # n_iterations = len(resp['iterationDetails'])
    #
    #                 # for n_iteration in range(0, n_iterations):
    #                 #
    #                 #     failed_details[n_iteration + 1] = {}
    #                 #
    #                 #     # Verify the prints.
    #                 #     if not resp['iterationDetails'][n_iteration]['attachments']:
    #                 #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['NoEvidences']['Msg']}"
    #                 #               f"{Lib.Aux.Textcolor.END}")
    #                 #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.otherConfigs['NoEvidences'])
    #                 #         return None, None, None
    #                 #
    #                 #     print(f"{Lib.Aux.Textcolor.BOLD}{test_case_name}{Lib.Aux.Textcolor.END}")
    #                 #     attachments = resp['iterationDetails'][n_iteration]['attachments']
    #                 #     status_step = resp['iterationDetails'][n_iteration]['actionResults']
    #                 #     completed_date = resp['iterationDetails'][n_iteration]['startedDate']
    #                 #     for character in ('T', 'Z'):  # Remove letters.
    #                 #         completed_date = completed_date.replace(character, ' ')
    #                 #
    #                 #     # Remove the attachments are not print screen.
    #                 #     index = len(attachments)
    #                 #     while index > 0:
    #                 #         for word in ('html', 'json'):
    #                 #             if word in attachments[index - 1]['name']:
    #                 #                 attachments.pop(index - 1)
    #                 #         else:
    #                 #             index -= 1
    #                 #
    #                 #     num_prints = len(attachments)
    #                 #     for num_print in range(0, num_prints):
    #                 #         actionPath = attachments[num_print]['actionPath']
    #                 #         file_name = attachments[num_print]['name']
    #                 #         id_file = attachments[num_print]['id']
    #                 #
    #                 #         # Check the attachment and the status of the step.
    #                 #         for result, _ in enumerate(status_step):
    #                 #             if attachments[num_print]['actionPath'] == status_step[result]['actionPath']:
    #                 #                 status = status_step[result]['outcome']
    #                 #
    #                 #                 if 'Failed' in status_step[result]['outcome']:
    #                 #                     step_failed = result
    #                 #                     if 'errorMessage' in status_step[step_failed]:
    #                 #                         comment = status_step[step_failed]['errorMessage']
    #                 #                         failed_details[n_iteration + 1]['Step'] = step_failed
    #                 #                         failed_details[n_iteration + 1]['Comment'] = comment
    #                 #                         failed_info_dict[test_case_id] = failed_details
    #                 #                     else:
    #                 #                         comment = ''
    #                 #                 else:
    #                 #                     step_failed = 0
    #                 #                     comment = ''
    #                 #
    #                 #         list_id_manual_print.append([file_name, id_file, actionPath, status])
    #                 #
    #                 #     # Sorted by: order print by name.
    #                 #     for order, _ in enumerate(list_id_manual_print):
    #                 #         if '_' in list_id_manual_print[order][0]:  # Treat the filename save by LightShot.
    #                 #             list_id_manual_print[order][0] = \
    #                 #                 '0' + Lib.Aux.regex.search(r'\d+', list_id_manual_print[order][0]).group(0)
    #                 #             list_id_manual_print = sorted(list_id_manual_print)
    #                 #         else:  # Treat the filename save by Azure.
    #                 #             list_id_manual_print = sorted(list_id_manual_print)
    #                 #             list_id_manual_print[order][0] = '0' + str(order + 1)
    #                 #
    #                 #     # Get the first item from the tuple in list.
    #                 #     list_num_print = [int(first_item[0]) for first_item in list_id_manual_print]
    #                 #
    #                 #     GitLabConnection.saveManualPrintScreen(self, project=project, list_num_print=list_num_print,
    #                 #                                           list_id_manual_print=list_id_manual_print,
    #                 #                                           n_test_case=n_test_case + 1, n_iteration=n_iteration + 1,
    #                 #                                           test_case_name=test_case_name,
    #                 #                                           completed_date=completed_date)
    #                 #
    #                 #     list_id_manual_print.clear()
    #                 #     list_num_print.clear()
    #                 #     list_step_status_manual.clear()
    #
    #             test_case_id = resp['testCase']['id']
    #
    #             print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.logs['AttachmentList']['Msg']}{Lib.Aux.Textcolor.END}")
    #
    #             # return test_case_id, n_iterations, failed_info_dict, completed_date
    #         else:
    #             print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #             Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(q.status_code) + ' - attachmentList')
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorAttachmentList']['Msg']}{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorAttachmentList'], value1=str(e))
    #         #exit(1)

    # Save the images locally.
    # def saveManualPrintScreen(self, **kwargs):
    #     try:
    #
    #         version = '6.0'
    #
    #         # kwargs arguments.
    #         list_id_manual_print = kwargs.get('list_id_manual_print')
    #         project = kwargs.get('project')
    #         list_step_order = kwargs.get('list_num_print')
    #         n_test_case = kwargs.get('n_test_case')
    #         n_iteration = kwargs.get('n_iteration')
    #         test_case_name = kwargs.get('test_case_name')
    #
    #         # Saving by the attachment ID order.
    #         for index, id_manual_print in enumerate(list_id_manual_print):
    #
    #             order = str(list_step_order[index])
    #             # Variable.
    #             step_order = str(order).zfill(2)
    #
    #             file_name = 'CT' + str(n_test_case).zfill(2) + '-IT' + str(n_iteration).zfill(2) + '-' + \
    #                         Lib.Aux.otherConfigs["EvidenceName"] + step_order + Lib.Aux.otherConfigs["EvidenceExtension"]
    #
    #             url = 'https://' + instance + project + '/_api/_testresult/DownloadAttachment?attachmentId=' + \
    #                        str(id_manual_print[1]) + '&api-version=' + version
    #
    #             # Execute the Azure request.
    #             q = requests.get(url, headers={'Authorization': 'Bearer ' + Lib.Aux.otherConfigs["Bearer"]},
    #                              verify=False)
    #
    #             if q.status_code == 200:
    #                 evidence_image = Lib.Aux.os.path.join(Lib.Aux.directories['EvidenceFolderManual'], file_name)
    #                 with open(evidence_image, 'wb') as print_screen:
    #                     print_screen.write(q.content)
    #
    #                 print(f"{Lib.Aux.Textcolor.UNDERLINE}{Lib.Aux.logs['SaveManualPrintScreen']['Msg']}{Lib.Aux.Textcolor.END} "
    #                       f"{test_case_name} ITERATION "
    #                       f"{n_iteration} - Print {step_order}")
    #
    #             elif q.status_code == 401:
    #                 print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorToken']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #                 Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorToken'],
    #                                  value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')
    #
    #             else:
    #                 print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequest']['Msg']}{Lib.Aux.Textcolor.END}\n")
    #                 Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorRequest'],
    #                                  value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')
    #
    #     except Exception as e:
    #         print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorSaveManualPrintScreen']['Msg']}"
    #               f"{Lib.Aux.Textcolor.END}", e)
    #         Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ErrorSaveManualPrintScreen'], value1=str(e))
    #         #exit(1)
