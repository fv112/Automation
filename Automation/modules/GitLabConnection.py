import json
import os.path
import requests
import urllib3
from prettytable import PrettyTable

import Automation.modules.automationAux as Aux

url = 'https://sbs.t-systems.com.br/gitlab/api/v4/'

urllib3.disable_warnings()


class GitLabConnection:

    def __init__(self, url):
        pass

    # Start reading the information from Azure (API).
    # def startRun(self):
    #     # # Get the kwargs variables.
    #     # project = kwargs.get("project")
    #     # id_test_plan = kwargs.get("id_test_plan")
    #     # id_test_suit = kwargs.get("id_test_suit")
    #     # id_test_case = kwargs.get("test_case_id_list_all")
    #
    #     test_case_id_list_all = []
    #
    #     # if project is None:
    #
    #     # Projects list.
    #     project = GitLabConnection.getProjects(self)
    #     # Test Plan list.
    #     # id_test_plan = GitLabConnection.getTestPlans(self, project=project)
    #     # Test Suit list.
    #     # id_test_plan, id_test_suit = GitLabConnection.getTestSuits(self, project=project, id_test_plan=id_test_plan)
    #
    #     # Get the test case id.
    #     test_case_id_list_all, test_suit = \
    #         GitLabConnection.getTestCases(self, project=project, id_test_plan=id_test_plan, id_test_suit=id_test_suit,
    #                                      id_test_case=id_test_case)
    #
    #     # Create the Test Run ID.
    #     # test_run_id = \
    #     #     GitLabConnection.createTestRunID(self, project=project, test_suit=test_suit, id_test_plan=id_test_plan)
    #
    #     return project, test_case_id_list_all

    # Execute each step.
    def startSteps(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get('project_id')
        test_case_id = kwargs.get('test_case_id')

        # Execute each test case.
        name_testcase, step_block = GitLabConnection.executeTestCase(self, project_id=project_id,
                                                                     test_case_id=test_case_id)

        # Load the test case steps.
        steps_list, order_steps_list = GitLabConnection.getSteps(self, step_block=step_block)
        verbs_list, parameters1_list, parameters2_list = GitLabConnection.sliceDatas(self, steps_list=steps_list)

        return order_steps_list, name_testcase, steps_list, verbs_list, parameters1_list, parameters2_list

    # Read the print screen from each step.
    def manualEvidences(self, **kwargs):

        try:
            # kwargs variables.
            project = kwargs.get('project')
            test_run_id = kwargs.get('test_run_id')
            id_test_case = kwargs.get('id_test_case')

            test_case_id_list = []
            n_iterations_list = []
            id_azure_list = []
            n_test_case_list = []
            completed_date_list = []
            failed_info_dict = {}
            n_test_case = 0

            amount_test_case, id_azure, full_name_run_test = GitLabConnection.getTestCaseRun(self, project=project,
                                                                                            test_run_id=test_run_id,
                                                                                            id_test_case=id_test_case)

            for n_test_case in range(0, amount_test_case):
                test_case_id, n_iterations, failed_info_dict, completed_date = GitLabConnection.attachmentList(
                    self, project=project, test_run_id=test_run_id, n_test_case=n_test_case,
                    failed_info_dict=failed_info_dict, id_azure=id_azure)

                n_iterations_list.append(n_iterations)
                id_azure_list.append(id_azure)
                id_azure += 1
                test_case_id_list.append(test_case_id)
                n_test_case += 1
                n_test_case_list.append(n_test_case)
                completed_date_list.append(completed_date)

        except (TypeError, AttributeError):
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['IDRunInvalid']['Msg']} '{test_run_id}'"
                  f"{Aux.Textcolor.END}")
            #exit(1)

        else:
            return test_case_id_list, n_iterations_list, id_azure_list, n_test_case_list, failed_info_dict, \
                   completed_date_list, full_name_run_test

    # ===================================== Modules to extract info from GitLab ========================================
    # Load the project list from GitLab.
    def getProjects(self):

        projects_dic = {}
        project_selected = ''

        try:

            new_url = url + 'projects?topic=QA-Automation'

            t = requests.get(new_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
            if t.status_code == 200:

                # Filter some fields.
                json_str = json.dumps(t.json())
                resp = json.loads(json_str)
                if resp is not []:

                    table = PrettyTable(['PROJECT ID', 'PROJECT'])

                    for order in range(0, resp.__len__()):
                        table.add_row([str(resp[order]['id']), str(resp[order]['name'])])
                        projects_dic[resp[order]['id']] = str(resp[order]['name'])

                    print(table.get_string(sortby="PROJECT ID"))
                    print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['InformProject']['Msg']}{Aux.Textcolor.END}\n")

                    project_selected = input()
                    project_name = projects_dic[int(project_selected)]
                    return project_selected, project_name
                else:
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorInstance']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(message="General", value=Aux.logs['ErrorInstance']['Msg'])

            elif t.status_code == 401:
                # text = Aux.regex.search('(?<=<title>).+?(?=</title>)', t.text, Aux.regex.DOTALL).group().strip()
                print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['RunAgain']['Msg']}"
                      f"{Aux.Textcolor.UNDERLINE}\n")
                Aux.Main.addLogs(message="General", value=Aux.otherConfigs['TokenExpired'])

            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.UNDERLINE}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(t.status_code) + ' - getProjects')

        except ValueError:
            print(f"{Aux.Textcolor.FAIL}'{project_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
                  f"{Aux.Textcolor.END}")
            #exit(1)

        except requests.exceptions.RequestException:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorConnection']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorConnection'])

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetProjects']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetProjects'], value1=str(e))
            #exit(1)

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
        #     q = requests.get(url, auth=Aux.otherConfigs['HttpBasicAuth'], verify=False)
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
        #             print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestPlan']['Msg']}{Aux.Textcolor.END}\n")
        #             Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestPlan'])
        #             #exit(1)
        #
        #     else:
        #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
        #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
        #                     value1='Status code: ' + str(q.status_code) +' - getTestPlans')
        #
        # except ValueError:
        #     print(f"{Aux.Textcolor.FAIL}'{test_plan_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
        #           f"{Aux.Textcolor.END}")
        #     #exit(0)

        #     return 0
        #
        # except Exception as e:
        #     print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestPlans']['Msg']}{Aux.Textcolor.END}", e)
        #     Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestPlans'], value1=str(e))
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
            # r = requests.get(url, auth=Aux.otherConfigs['HttpBasicAuth'], verify=False)
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
            #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestSuit']['Msg']}{Aux.Textcolor.END}\n")
            #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestSuit'])
            #
            # else:
            #     print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
            #     Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
            #                 value1='Status code: ' + str(r.status_code) + ' - getTestSuits')
        #     return 0, 0
        #
        # except ValueError:
        #     print(f"{Aux.Textcolor.FAIL}'{test_suit_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
        #           f"{Aux.Textcolor.END}")
        #     #exit(0)
        #
        # except Exception as e:
        #     print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestSuits']['Msg']}{Aux.Textcolor.END}", e)
        #     Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestSuits'], value1=str(e))
        #     #exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Load the test cases.
    def getTestCases(self, **kwargs):
        try:

            # kwargs variables.
            project_id = kwargs.get("project_id")

            # Variables.
            test_case_id_list = []

            new_url = url + 'projects/' + str(project_id) + '/issues?labels=Test%20case'

            # Execute the request from Azure.
            s = requests.get(new_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
            if s.status_code == 200:

                table = PrettyTable(['ORDER', 'TEST CASE ID', 'TEST CASE'])

                # Filter some fields.
                json_str = json.dumps(s.json())
                resp = json.loads(json_str)
                if resp.__len__() != 0:
                    for id_test, testCase_id in enumerate(resp):
                        table.add_row([id_test + 1, str(testCase_id['iid']), testCase_id['title']])
                        test_case_id_list.append(testCase_id['iid'])

                    isolated_tc = None

                    while True:
                        if isolated_tc not in ["Y", "N"]:
                            print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['AskCT']['Msg']}{Aux.Textcolor.END}\n")
                            isolated_tc = input().upper()
                            os.system('cls')
                            if isolated_tc.upper() in ["Y", "S"]:
                                print(
                                    f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['TestCaseList']['Msg']}{Aux.Textcolor.END}")
                                print(table)
                                print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['ChooseTestCase']['Msg']}{Aux.Textcolor.END}\n")
                                tc_id = int(input())
                                test_case_id_list.clear()
                                test_case_id_list.append(int(tc_id))
                                break
                            else:
                                break
                        else:
                            print("Invalid option. Try again!")

                else:
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCase']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestCase'])
                    #exit(1)

                return test_case_id_list

            elif s.status_code == 401:
                print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['RunAgain']['Msg']}"
                      f"{Aux.Textcolor.UNDERLINE}\n")
                Aux.Main.addLogs(message="General", value=Aux.otherConfigs['TokenExpired'])

            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(s.status_code) + ' - getTestCases')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCases']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestCases'], value1=str(e))
            #exit(1)

    # ===================================================== TEST CASE ==================================================
    # Execute the Test Case from Azure.
    def executeTestCase(self, **kwargs):
        try:
            # kwargs variables.
            project_id = kwargs.get("project_id")
            test_case_id = kwargs.get("test_case_id")

            name_testcase = ''
            step_block = ''

            new_url = (url + 'projects/' + str(project_id) + '/issues?iids[]=' + str(test_case_id))

            # Execute the request from Azure.
            q = requests.get(new_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
            if q.status_code == 200:
                print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['RequestOK']['Msg']}{Aux.Textcolor.END}\n")
                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)
                name_testcase = resp[0]['title']
                step_block = resp[0]['description']

                Aux.Main.addLogs(message="General", value=Aux.logs['ExecuteTestCase'])
            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(q.status_code) + ' - executeTestCase')

            return name_testcase, step_block

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorExecuteTestCase']['Msg']}{Aux.Textcolor.END} - {e}")
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorExecuteTestCase'], value1=str(e))
            #exit(1)

    # Extract the steps from Test Case.
    def getSteps(self, **kwargs):

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

            Aux.Main.addLogs(message="General", value=Aux.logs['GetSteps'])

            return steps_list, order_steps_list

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetSteps']['Msg']}{Aux.Textcolor.END} - {e}")
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetSteps'], value1=str(e))
            #exit(1)

    # Dismember the variables from each test case.
    def sliceDatas(self, **kwargs):

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
                if count_character == 2:
                    parameters1_list.append(Aux.re.findall(r'"([^"]*)"', step)[0])
                    parameters2_list.append(None)
                elif count_character == 4:
                    parameters1_list.append(Aux.re.findall(r'"([^"]*)"', step)[0])
                    parameters2_list.append(Aux.re.findall(r'"([^"]*)"', step)[1])
                elif count_character > 4:  # API content.
                    parameters1_list.append(step[step.find("\"")+1:-1])
                    parameters2_list.append(None)

            Aux.Main.addLogs(message="General", value=Aux.logs['SliceDatas'])

            return verbs_list, parameters1_list, parameters2_list

        # When there is no variable.
        except ZeroDivisionError:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorLineEmpty']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorLineEmpty'])

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSliceDatas']['Msg']}{Aux.Textcolor.END} - {e}")
            Aux.Main.addLogs( message="General", value=Aux.logs['ErrorSliceDatas'], value1=str(e))
            #exit(1)

    # Update the evidence in the TestCase.
    def SaveEvidenceTestCase(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        evidence_folder = kwargs.get("evidence_folder")
        test_case_id = kwargs.get("test_case_id")
        name_testcase = kwargs.get("name_testcase")
        status = kwargs.get("status")

        file_url = None

        try:

            # Get Token.
            new_url = (url + 'projects/' + str(project_id) + '/uploads')

            if status == 'Failed':
                status_name_testcase = '[BUG] - ' + name_testcase
            else:
                status_name_testcase = name_testcase

            file = os.path.join(evidence_folder, name_testcase, status_name_testcase) + ".pdf"

            files = {'file': open(file, 'rb')}

            with open(file, 'rb') as f:
                q = requests.post(new_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["BearerUpload"]},
                                  files=files, verify=False)

            if q.status_code == 201:
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveEvidenceTestCaseUpload']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['SaveEvidenceTestCaseUpload'])

                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)
                file_url = resp['url']

            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - ' + str(q.text) + 
                                        ' - SaveEvidenceTestCase - GetToken')
                #exit(1)

            new_url = (url + 'projects/' + str(project_id) + '/issues/' + str(test_case_id) + '/notes')

            # Upload file.
            file_url = file_url.replace("file", status_name_testcase + ".pdf")

            body = {
                "body": "[" + status_name_testcase + "](" + file_url + ")"
            }

            p = requests.post(new_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["BearerUpload"]},
                              data=body, verify=False)

            if p.status_code == 201:
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveEvidenceTestCase']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['SaveEvidenceTestCase'])

            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(p.status_code) + ' - ' + str(p.text) +
                                        ' - SaveEvidenceTestCase - Upload File')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveEvidenceTestCase']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorSaveEvidenceTestCase'], value1=str(e))
            #exit(1)

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
    #         # r = requests.patch(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, json=file_datas, headers=headers,
    #         #                    verify=False)
    #         if r.status_code == 200:
    #             print(f"{Aux.Textcolor.BLUE}{Aux.logs['UpdateStatusAutomated']['Msg']}{Aux.Textcolor.END}")
    #             Aux.Main.addLogs(message="General", value=Aux.logs['UpdateStatusAutomated'])
    #         else:
    #             raise Exception
    #
    #     except Exception as e:
    #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUpdateStatusAutomated']['Msg']}{Aux.Textcolor.END}", e)
    #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorUpdateStatusAutomated'],
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
    #         evidence_folder = Aux.os.path.join(Aux.directories['EvidenceFolder'], name_testcase)
    #         relation_list = []
    #         order_list = []
    #         count_evidences_list = []
    #         relation_failed = ''
    #         order_failed = ''
    #         count_evidences_failed = ''
    # 
    #         Aux.Main.deleteDirectory(self, directory=evidence_folder)
    #         Aux.Main.deleteFiles(self, path_log=Aux.os.path.join(Aux.directories['EvidenceFolder']), extension='.zip',
    #                              exact_file=name_testcase + '.zip')
    # 
    #         url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(test_case_id) + \
    #                    '&$expand=Relations&api-version=' + version
    # 
    #         r = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
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
    #                     print(f"{Aux.Textcolor.BLUE}{Aux.logs['WaitTime']['Msg']}{seconds} / 15{Aux.Textcolor.END}")
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
    #             print(f"{Aux.Textcolor.BLUE}{Aux.logs['GenerateZIPFile']['Msg']}{Aux.Textcolor.END}")
    #             Aux.Main.addLogs(message="General", value=Aux.logs['GenerateZIPFile']['Msg'])
    #             Aux.shutil.make_archive(evidence_folder, 'zip', evidence_folder)
    # 
    #             GitLabConnection.UploadDownloadFile(self, project=project, test_case_id=str(test_case_id),
    #                                                evidence_folder=Aux.directories['EvidenceFolder'],
    #                                                download_file_name=name_testcase + '.zip',
    #                                                file_name=name_testcase + '.zip')
    # 
    #     except Exception as e:
    #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorDownloadAttachment'], value1=str(e))
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
    #             print(f"{Aux.Textcolor.FAIL}{Aux.logs['GenerateZIP']['Msg']} {count_evidences} / "
    #                   f"{total}{Aux.Textcolor.END}")
    #
    #             Aux.Main.createDirectory(self, path_folder=Aux.os.path.join(Aux.directories['EvidenceFolder'],
    #                                                                         name_testcase, date_time_folder))
    #
    #             url = 'https://' + instance + project + '/_apis/wit/attachments/' + str(id_point) + \
    #                        '?api-version=' + version
    #             s = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, timeout=10)
    #
    #             download = Aux.os.path.join(Aux.directories['EvidenceFolder'], name_testcase, date_time_folder, name)
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
    #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorDownloadAttachment']['Msg']}{Aux.Textcolor.END}", e)
    #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorDownloadAttachment'], value1=str(e))
    #         #exit(1)
    #
    #     finally:
    #         return order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed

    # Check if the download Baseline exist or not.
    def CheckDownloadFile(self, **kwargs):
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            test_case_id = kwargs.get('test_case_id')
            file_name = kwargs.get('file_name')
            evidence_folder = kwargs.get('evidence_folder')
            compare = kwargs.get('compare')

            version = '6.0'

            # check if the download file already exist.
            url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + \
                       '?$expand=all&api-version=' + version

            q = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)

            if q.status_code == 200:
                flag_save_baseline = True

                # Filter some fields.
                json_check = json.dumps(q.json())
                req = json.loads(json_check)
                rev_id = req['rev']
                for order in range(1, len(req['relations'])):
                    name_file_downloaded = req['relations'][order]['attributes']['name']

                    if compare:  # For compare the files.
                        if name_file_downloaded == str(file_name):
                            flag_save_baseline = True
                            download_file_name = file_name
                    else:  # For execution
                        # Verify if the Baseline doesn't exist.
                        if name_file_downloaded == ('Baseline - ' + str(file_name)):
                            flag_save_baseline = False

                        if flag_save_baseline:
                            download_file_name = 'Baseline - ' + file_name
                        else:
                            download_file_name = 'New - ' + file_name

                    # Verify if the New file exists and delete for a new one OR replace the Baseline after compare.
                    if name_file_downloaded == 'New - ' + file_name or name_file_downloaded == str(file_name):
                        GitLabConnection.DeleteDownloadFile(self, project=project, rev_id=rev_id,
                                                           test_case_id=str(test_case_id), order=order)
                        rev_id += 1

                GitLabConnection.UploadDownloadFile(self, project=project, evidence_folder=evidence_folder,
                                                   test_case_id=str(test_case_id),
                                                   download_file_name=download_file_name, file_name=file_name)

                print(f"{Aux.Textcolor.WARNING}{Aux.logs['CheckDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['CheckDownloadFile'])

            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - CheckDownloadFile')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorCheckDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorCheckDownloadFile'], value1=str(e))
            #exit(1)

    # Delete the 'New' download file to the TestCase.
    def DeleteDownloadFile(self, **kwargs):
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            rev_id = kwargs.get('rev_id')
            test_case_id = kwargs.get('test_case_id')
            order = kwargs.get('order')

            version = '6.0'

            # check if the download file already exist.
            url = 'https://' + instance + project + '/_apis/wit/workitems/' + test_case_id + '?api-version=' \
                       + version

            headers = {'content-type': 'application/json-patch+json'}

            attachment_details = [
                {
                    "op": "test",
                    "path": "/rev",
                    "value": rev_id,
                },
                {
                    "op": "remove",
                    "path": "/relations/" + str(order)
                }
            ]

            # q = requests.patch(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, json=attachment_details,
            #                    headers=headers, verify=False)

            if q.status_code == 200:
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['DeleteDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['DeleteDownloadFile'])
            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - DeleteDownloadFile')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorDeleteDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorDeleteDownloadFile'], value1=str(e))
            #exit(1)

    # Upload the download file in the TestCase.
    def UploadDownloadFile(self, **kwargs):
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            evidence_folder = kwargs.get('evidence_folder')
            test_case_id = kwargs.get('test_case_id')
            file_name = kwargs.get('file_name')
            download_file_name = kwargs.get('download_file_name')

            # Get the Attachment ID.
            version = '6.0'

            url = 'https://' + instance + project + '/_apis/wit/attachments?fileName=' + str(file_name) + \
                       '&api-version=' + version

            with open(Aux.os.path.join(evidence_folder, file_name), "rb") as file:
                data = file.read()

            headers = {'Content-Type': 'application/octet-stream'}

            # p = requests.post(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, data=data, headers=headers,
            #                   verify=False)
            if p.status_code == 201:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)
                idAttachment = resp['id']
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UploadDownloadFileID']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['UploadDownloadFileID'])
            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - UploadDownloadFileID')

            # ------------------------------------ Second API conection ------------------------------------------------

            # Add the attachment in Azure.
            version = '6.1-preview.3'

            url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
                       + version

            headers = {'content-type': 'application/json-patch+json'}

            file_datas = [
                {
                    "op": "add",
                    "path": "/fields/System.History",
                    "value": "Download file: " + download_file_name
                },
                {
                    "op": "add",
                    "path": "/relations/-",
                    "value": {
                        "rel": "AttachedFile",
                        "url": "https://kantarware.visualstudio.com/_apis/wit/attachments/" + idAttachment +
                               "?fileName=" + download_file_name,
                        "attributes": {
                            "comment": download_file_name
                        }
                    }
                }
            ]

            # q = requests.patch(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, json=file_datas, headers=headers,
            #                    verify=False)
            if q.status_code == 200:
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UploadDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['UploadDownloadFile'])
            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - UploadDownloadFile')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUploadDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorUploadDownloadFile'], value1=str(e))
            #exit(1)

    # Save the download file, from the test case locally.
    def SaveDownloadFileLocally(self, **kwargs):
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            id_testcase = kwargs.get('id_testcase')

            list_names = ['Baseline -', 'New -']
            list_files_baseline = []
            list_files_new = []

            # Get the Attachment ID.
            version = '6.0'

            url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(id_testcase) + \
                       '&$expand=all&api-version=' + version

            p = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
            if p.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)

                for order in range(1, len(resp['value'][0]['relations'])):
                    download_name = resp['value'][0]['relations'][order]['attributes']['name']
                    test_name = resp['value'][0]['fields']['System.Title']

                    if any(x in download_name for x in list_names):
                        file_url = resp['value'][0]['relations'][order]['url']

                        r = requests.get(file_url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)

                        # Create the Compare directory.
                        Aux.Main.createDirectory(self,
                                                 path_folder=Aux.os.path.join(Aux.directories['CompareDownloadFolder'],
                                                                              test_name))

                        download = Aux.os.path.join(Aux.directories['CompareDownloadFolder'], test_name, download_name)
                        with open(download, 'wb') as file:
                            file.write(r.content)

                        if list_names[0] in download_name:
                            list_files_baseline.append(download_name)
                        else:
                            list_files_new.append(download_name)

                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveDownloadFileLocally']['Msg']}"
                      f"{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['SaveDownloadFileLocally'])
            else:
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - ErrorSaveDownloadFileLocally')

            return test_name, id_testcase, sorted(list_files_baseline), sorted(list_files_new)

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveDownloadFileLocally']['Msg']}"
                  f"{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorSaveDownloadFileLocally'], value1=str(e))
            #exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Functions to manual evidence.
    # ------------------------------------------------------------------------------------------------------------------
    # Get the number of test cases in Run.
    # def getTestCaseRun(self, **kwargs):
    #     try:
    #         # kwargs variables.
    #         project = kwargs.get('project')
    #         test_run_id = kwargs.get('test_run_id')
    #         id_test_case = kwargs.get('id_test_case')
    #
    #         version = '6.1-preview.6'
    #         id_azure = 100000
    #
    #         # Get the actual Result comments.
    #         url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + \
    #                    '/results?api-version=' + version
    #
    #         p = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
    #         if p.status_code == 200:
    #             # Filter some fields.
    #             json_str = json.dumps(p.json())
    #             resp = json.loads(json_str)
    #             amount_test_case = resp['count']
    #
    #             # Test executed by.
    #             full_name_run_test = resp['value'][0]['runBy']['displayName']
    #
    #             # If is a unique test case.
    #             if id_test_case != '':
    #                 for index in range(0, amount_test_case):
    #                     if resp['value'][index]['testCase']['id'] == id_test_case:
    #                         id_azure = resp['value'][index]['id']
    #                     amount_test_case = 1
    #
    #         else:
    #             print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
    #             Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(p.status_code) + ' - getTestCaseRun')
    #
    #         if amount_test_case == 0:
    #             return None
    #         else:
    #             print(f"{Aux.Textcolor.WARNING}{Aux.logs['GetTestCaseRun']['Msg']}{Aux.Textcolor.END}\n")
    #             Aux.Main.addLogs(message="General", value=Aux.logs['GetTestCaseRun'])
    #
    #             return amount_test_case, id_azure, full_name_run_test
    #
    #     except Exception as e:
    #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCaseRun']['Msg']}{Aux.Textcolor.END}", e)
    #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorGetTestCaseRun'], value1=str(e))
    #         #exit(1)

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
    #         q = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]}, verify=False)
    #         if q.status_code == 200:
    #             # Filter some fields.
    #             json_str = json.dumps(q.json())
    #             resp = json.loads(json_str)
    #
    #             # Verify the test execution.
    #             # if not resp['iterationDetails']:
    #             #     raise Exception(f"{Aux.Textcolor.FAIL}{Aux.logs['NoExecutions']['Msg']}{Aux.Textcolor.END}")
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
    #                 # if Aux.Main.validateTestName(self, name_testcase=test_case_name):
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
    #                 #         print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['NoEvidences']['Msg']}"
    #                 #               f"{Aux.Textcolor.END}")
    #                 #         Aux.Main.addLogs(message="General", value=Aux.otherConfigs['NoEvidences'])
    #                 #         return None, None, None
    #                 #
    #                 #     print(f"{Aux.Textcolor.BOLD}{test_case_name}{Aux.Textcolor.END}")
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
    #                 #                 '0' + Aux.regex.search(r'\d+', list_id_manual_print[order][0]).group(0)
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
    #             print(f"{Aux.Textcolor.BLUE}{Aux.logs['AttachmentList']['Msg']}{Aux.Textcolor.END}")
    #
    #             # return test_case_id, n_iterations, failed_info_dict, completed_date
    #         else:
    #             print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
    #             Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'],
    #                              value1='Status code: ' + str(q.status_code) + ' - attachmentList')
    #
    #     except Exception as e:
    #         print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorAttachmentList']['Msg']}{Aux.Textcolor.END}", e)
    #         Aux.Main.addLogs(message="General", value=Aux.logs['ErrorAttachmentList'], value1=str(e))
    #         #exit(1)

    # Save the images locally.
    def saveManualPrintScreen(self, **kwargs):
        try:

            version = '6.0'

            # kwargs arguments.
            list_id_manual_print = kwargs.get('list_id_manual_print')
            project = kwargs.get('project')
            list_step_order = kwargs.get('list_num_print')
            n_test_case = kwargs.get('n_test_case')
            n_iteration = kwargs.get('n_iteration')
            test_case_name = kwargs.get('test_case_name')

            # Saving by the attachment ID order.
            for index, id_manual_print in enumerate(list_id_manual_print):

                order = str(list_step_order[index])
                # Variable.
                step_order = str(order).zfill(2)

                file_name = 'CT' + str(n_test_case).zfill(2) + '-IT' + str(n_iteration).zfill(2) + '-' + \
                            Aux.otherConfigs["EvidenceName"] + step_order + Aux.otherConfigs["EvidenceExtension"]

                url = 'https://' + instance + project + '/_api/_testresult/DownloadAttachment?attachmentId=' + \
                           str(id_manual_print[1]) + '&api-version=' + version

                # Execute the Azure request.
                q = requests.get(url, headers={'Authorization': 'Bearer ' + Aux.otherConfigs["Bearer"]},
                                 verify=False)

                if q.status_code == 200:
                    evidence_image = Aux.os.path.join(Aux.directories['EvidenceFolderManual'], file_name)
                    with open(evidence_image, 'wb') as print_screen:
                        print_screen.write(q.content)

                    print(f"{Aux.Textcolor.UNDERLINE}{Aux.logs['SaveManualPrintScreen']['Msg']}{Aux.Textcolor.END} "
                          f"{test_case_name} ITERATION "
                          f"{n_iteration} - Print {step_order}")

                elif q.status_code == 401:
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorToken']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(message="General", value=Aux.logs['ErrorToken'],
                                     value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')

                else:
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(message="General", value=Aux.logs['ErrorRequest'], 
                                     value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')

        except Exception as e:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveManualPrintScreen']['Msg']}"
                  f"{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(message="General", value=Aux.logs['ErrorSaveManualPrintScreen'], value1=str(e))
            #exit(1)
