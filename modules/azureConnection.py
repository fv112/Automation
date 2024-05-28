import json
import time
import xml.etree.ElementTree as eT
import requests
import base64
import socket
from operator import itemgetter

import modules.automationAux as Aux

instance = 'kantarware.visualstudio.com/'


class AzureConnection:

    def __init__(self):
        self.url = None

    # Start reading the information from Azure (API).
    def startRun(self, **kwargs):
        # Get the kwargs variables.
        project = kwargs.get("project")
        id_test_plan = kwargs.get("id_test_plan")
        id_test_suit = kwargs.get("id_test_suit")
        id_test_case = kwargs.get("test_case_id_list_all")

        test_case_id_list_all = []

        if project is None:
            # Projects list.
            project = AzureConnection.getProjects(self)
            # Test Plan list.
            id_test_plan = AzureConnection.getTestPlans(self, project=project)
            # Test Suit list.
            id_test_plan, id_test_suit, id_test_case = AzureConnection.getTestSuits(self, project=project,
                                                                                    id_test_plan=id_test_plan)

        # Get the test case id.
        test_case_id_list_all, point_id_list, test_suit = \
            AzureConnection.getTestCases(self, project=project, id_test_plan=id_test_plan, id_test_suit=id_test_suit,
                                         id_test_case=id_test_case)

        # Create the Test Run ID.
        test_run_id = \
            AzureConnection.createTestRunID(self, project=project, test_suit=test_suit, id_test_plan=id_test_plan,
                                            point_id_list=point_id_list)

        return project, test_case_id_list_all, test_run_id

    # Execute each step.
    def startSteps(self, **kwargs):

        # kwargs variables.
        project = kwargs.get('project')
        test_case_id = kwargs.get('test_case_id')

        # Execute each test case.
        request, name_testcase, summary = \
            AzureConnection.executeTestCase(self, project=project, test_case_id=test_case_id)
        # Load the test case steps.
        steps, cont_steps, change_download_config = \
            AzureConnection.getSteps(self, request=request, name_testcase=name_testcase)
        # Load the parameter from each test case.
        parameters = AzureConnection.getParameters(self, request=request)
        # Load the datas from each test case (Variables).
        variables = AzureConnection.getVariables(self, request=request, parameters=parameters)
        # Disjoint the variable from each step.
        datas = AzureConnection.sliceDatas(self, variables=variables, parameters=parameters, steps=steps)

        return datas, name_testcase, summary, cont_steps, change_download_config

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

            amount_test_case, id_azure, full_name_run_test = AzureConnection.getTestCaseRun(self, project=project,
                                                                                            test_run_id=test_run_id,
                                                                                            id_test_case=id_test_case)

            for n_test_case in range(0, amount_test_case):
                test_case_id, n_iterations, failed_info_dict, completed_date = \
                    AzureConnection.attachmentList(self, project=project, test_run_id=test_run_id,
                                                   n_test_case=n_test_case, failed_info_dict=failed_info_dict,
                                                   id_azure=id_azure)

                n_iterations_list.append(n_iterations)
                id_azure_list.append(id_azure)
                id_azure += 1
                test_case_id_list.append(test_case_id)
                n_test_case += 1
                n_test_case_list.append(n_test_case)
                completed_date_list.append(completed_date)

        except (TypeError, AttributeError):
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.otherConfigs['IDRunInvalid']['Msg']} "
                                                       f"'{test_run_id}'[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['IDRunInvalid']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['IDRunInvalid']['Msg']} '{test_run_id}'"
                  f"{Aux.Textcolor.END}")
            ###exit(1)

        else:
            return test_case_id_list, n_iterations_list, id_azure_list, n_test_case_list, failed_info_dict, \
                   completed_date_list, full_name_run_test

    # ===================================== Modules to extract info from Azure =========================================
    # Load the project list from KantarWare.
    def getProjects(self):
        projects_selected = 0

        try:
            # Variables.
            option = 1
            projects = []
            projects_ids = []
            # version = '6.1'

            self.url = 'https://sbs.t-systems.com.br/gitlab/api/v4/projects'

            # Execute the request from Azure.
            t = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if t.status_code == 200:

                # Filter some fields.
                json_str = json.dumps(t.json())
                resp = json.loads(json_str)
                if resp is not []:

                    for Projects_id in resp['id']:
                        projects.append(Projects_id['name'] + ' | ' + Projects_id['id'])
                        projects_ids.append(Projects_id)
                        option += 1
                    return projects

                else:
                    if Aux.otherConfigs['Interface']:
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorInstance']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorInstance']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorInstance']['Msg'])

            elif t.status_code == 401:
                text = Aux.regex.search('(?<=<title>).+?(?=</title>)', t.text, Aux.regex.DOTALL).group().strip()
                if text == 'Access Denied: The Personal Access Token used has expired.':
                    # Delete the token directory.
                    Aux.Main.deleteDirectory(self, directory=Aux.directories['TokensFile'])
                    Aux.Main.accessAzure(self)

                    print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['RunAgain']['Msg']}"
                          f"{Aux.Textcolor.UNDERLINE}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs['TokenExpired'])

            # If there is something written in your Tokens.txt file OR if token's size < token regular size.
            elif t.status_code == 203:
                Aux.Main.clean_token_file(self)
                Aux.Main.accessAzure(self)
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSaveToken'])

            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.UNDERLINE}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(t.status_code) + ' - getProjects')

        except ValueError:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['OptionInvalid']['Msg'])
            print(f"{Aux.Textcolor.FAIL}'{projects_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
                  f"{Aux.Textcolor.END}")
            ### exit(0)

        except AttributeError as e:  # When 'group' (text) doesn't exist.
            Aux.clean_token_file(self)
            Aux.accessAzure(self)

        except requests.exceptions.RequestException:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorConnection']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorConnection']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorConnection'])

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetProjects']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetProjects']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetProjects'], value1=str(e))
            ### exit(1)

    # Load the test plans.
    def getTestPlans(self, **kwargs):
        test_plan_selected = 0

        try:

            # Get the kwargs variables.
            project = kwargs.get("project")

            version = '5.1-preview.1'
            option = 1
            test_plans = []

            self.url = 'https://' + instance + project + '/_apis/testplan/plans?filterActivePlans=True&api-version=' \
                       + version

            # Execute the request from Azure.
            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if q.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)
                if resp['count'] != 0:

                    for testPlan_id in resp['value']:
                        test_plans.append(testPlan_id['name'] + '|' + str(testPlan_id['id']))
                        option += 1
                    return test_plans

                else:
                    if Aux.otherConfigs['Interface']:
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestPlan']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestPlan']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestPlan'])
                    ###exit(1)

            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                            value1='Status code: ' + str(q.status_code) +' - getTestPlans')

        except ValueError:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['OptionInvalid']['Msg'])
            print(f"{Aux.Textcolor.FAIL}'{test_plan_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
                  f"{Aux.Textcolor.END}")
            ###exit(0)

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestPlans']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestPlans']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestPlans'], value1=str(e))
            # exit(1)

    # Load the Test Suits.
    def getTestSuits(self, **kwargs):
        test_suit_selected = 0

        try:

            # Get the kwargs variables.
            project = kwargs.get("project")
            id_test_plan = kwargs.get("id_test_plan")

            version = '5.0'
            option = 1
            test_suit = []

            self.url = 'https://' + instance + project + '/_apis/test/plans/' + str(id_test_plan) + '/suites/' +\
                       '?api-version=' + version

            # Execute the request from Azure.
            r = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if r.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(r.json())
                resp = json.loads(json_str)
                if resp['count'] != 0:

                    for testSuit_id in resp['value']:
                        test_suit.append(testSuit_id['name'] + '|' + str(testSuit_id['id']))
                        option += 1
                    return test_suit

                else:
                    if Aux.otherConfigs['Interface']:
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestSuit']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestSuit']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestSuit'])

            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                            value1='Status code: ' + str(r.status_code) + ' - getTestSuits')

        except ValueError:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['OptionInvalid']['Msg'])
            print(f"{Aux.Textcolor.FAIL}'{test_suit_selected}' {Aux.otherConfigs['OptionInvalid']['Msg']}"
                  f"{Aux.Textcolor.END}")
            ###exit(0)

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestSuits']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestSuits']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestSuits'], value1=str(e))
            ###exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Load the test cases.
    def getTestCases(self, **kwargs):
        try:

            # kwargs variables.
            project = kwargs.get("project")
            id_test_plan = kwargs.get("id_test_plan")
            id_test_suit = kwargs.get("id_test_suit")
            id_test_case = kwargs.get("id_test_case")

            version = '6.1-preview.2'
            test_case_id_list = []
            point_id_list = []

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            if id_test_case is None:
                self.url = 'https://' + instance + project + '/_apis/testplan/plans/' + str(id_test_plan) + \
                      '/suites/' + str(id_test_suit) + '/TestCase?api-version=' + version
            else:  # Unique teste case.
                self.url = 'https://' + instance + project + '/_apis/testplan/plans/' + str(id_test_plan) + \
                      '/suites/' + str(id_test_suit) + '/TestPoint?testCaseId=' + str(id_test_case) + \
                      '&api-version=' + version

            # Execute the request from Azure.
            s = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if s.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(s.json())
                resp = json.loads(json_str)
                if resp['count'] != 0 and id_test_case is None:
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                            f"{Aux.otherConfigs['TestCaseList']['Msg']}[/color][/b]")
                    print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['TestCaseList']['Msg']}{Aux.Textcolor.END}")
                    for cont, testCase_id in enumerate(resp['value']):
                        if Aux.otherConfigs['Interface']:
                            screenRunning.write_message_on_console(
                                f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]" +
                                "[{0:02d}] ID: {1} Name: {2}".format
                                (cont + 1, testCase_id['workItem']['id'],
                                 testCase_id['workItem']['name'])+"[/color]")
                        print("[{0:02d}] ID: {1} Name: {2}".format(cont + 1, testCase_id['workItem']['id'],
                                                                   testCase_id['workItem']['name']))

                        test_case_id_list.append(testCase_id['workItem']['id'])
                        point_id_list.append(testCase_id['pointAssignments'][0]['id'])

                    test_suit = testCase_id['testSuite']['name']

                elif id_test_case != None:  # Unique test case.
                    testCase_id = resp['value'][0]
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.white.defaultvalue}]" +
                            "[{0:02d}] ID: {1} Name: {2}".format
                            (1, testCase_id['id'], testCase_id['testCaseReference']['name'])
                            + "[/color][/b]")

                    print("[{0:02d}] ID: {1} Name: {2}".format(1, testCase_id['id'],
                                                               testCase_id['testCaseReference']['name']))
                    test_case_id_list.append(testCase_id['testCaseReference']['id'])
                    point_id_list.append(testCase_id['id'])
                    test_suit = testCase_id['testSuite']['id']

                else:
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                            f"{Aux.logs['ErrorGetTestCase']['Msg']}[/color][/b]")
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestCase']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCase']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestCase'])
                    ###exit(1)

                return test_case_id_list, point_id_list, test_suit

            elif s.status_code == 401:
                # Delete the token directory.
                Aux.Main.deleteDirectory(self, directory=Aux.directories['TokensFile'])
                Aux.Main.accessAzure(self)

                print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['RunAgain']['Msg']}"
                      f"{Aux.Textcolor.UNDERLINE}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs['TokenExpired'])

            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                        f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(s.status_code) + ' - getTestCases')

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorGetTestCases']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestCases']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCases']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestCases'], value1=str(e))
            ###exit(1)

    # Get the test case name updated (If was changed after the executed the test case).
    def getTestCaseName(self, **kwargs):

        # kwargs variables.
        test_case_id = kwargs.get("test_case_id")
        project = kwargs.get("project")

        version = '6.0-preview.2'

        try:

            # Access screen running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
                       + version

            # Execute the Azure request.
            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if q.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                        f"{Aux.logs['GetTestCaseName']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['GetTestCaseName']['Msg']}"
                      f"{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetTestCaseName'], value1="GetTestCaseName")

                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)

                return resp['fields']['System.Title']  # Test case name.
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorGetTestCaseName']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['ErrorGetTestCaseName']['Msg']}"
                      f"{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestCaseName'], value1="GetTestCaseName")

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestCaseName']['Msg'])
            print('\033[31m' + Aux.logs['ErrorGetTestCaseName']['Msg'] + '\033[0;0m', e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestCaseName'], value1=str(e))
            ###exit(1)

    # Add the test cases in the Run.
    def createTestRunID(self, **kwargs):

        try:
            # kwargs variables.
            project = kwargs.get("project")
            test_suit = kwargs.get("test_suit")
            id_test_plan = kwargs.get("id_test_plan")
            point_id_list = kwargs.get("point_id_list", 0)

            version = '5.1-preview.3'

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            if Aux.otherConfigs['ReplaceEvidence']:
                # Add the test cases in the Run. (Use the Test Case PointID).
                self.url = 'https://' + instance + project + '/_apis/test/runs?api-version=' + version

                test_datas = {
                    "name": test_suit,
                    "priority": 1,
                    "plan": {
                        "id": id_test_plan,
                    },
                    "pointIds": point_id_list,
                    "Type": "Web",
                    "Automated": True
                }

                p = requests.post(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=test_datas, timeout=None)
                if p.status_code == 200:
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                            f"{Aux.otherConfigs['StatusTestCase']['Msg']}[/color][/b]")
                    print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['StatusTestCase']['Msg']}"
                          f"{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['StatusTestCase'], value1="createTestRun - TestRun")
                    # Filter some fields.
                    json_str = json.dumps(p.json())
                    resp = json.loads(json_str)
                    testrun_id = resp['id']

                    return testrun_id

                else:
                    if Aux.otherConfigs['Interface']:
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                value1='Status code: ' + str(p.status_code) + " - createTestRun - TestRun")
            else:
                return None

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorLoadTestRun']['Msg'])
            print('\033[31m' + Aux.logs['ErrorLoadTestRun']['Msg'] + '\033[0;0m', e + '- TestRun!')
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorLoadTestRun'], value1=str(e) + '- Run!')
            ###exit(1)

    # ===================================================== TEST CASE ==================================================
    # Execute the Test Case from Azure.
    def executeTestCase(self, **kwargs):
        try:
            # kwargs variables.
            project = kwargs.get("project")
            test_case_id = kwargs.get("test_case_id")

            version = '6.0-preview.2'
            name_testcase = ''
            summary = None

            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + \
                       '?$expand=All&api-version=' + version

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Execute the request from Azure.
            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if q.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.otherConfigs['RequestOK']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['RequestOK']['Msg']}{Aux.Textcolor.END}\n")
                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)
                name_testcase = resp['fields']['System.Title'].strip()

                if 'System.Description' in resp['fields']:
                    summary = Aux.Main.removeHTML(self, value=resp['fields']['System.Description'])
                else:
                    summary = Aux.otherConfigs['Summary']['Msg']
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ExecuteTestCase'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(q.status_code) + ' - executeTestCase')

            return q.json(), name_testcase, summary

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorExecuteTestCase']['Msg'])
            print('\033[31m' + Aux.logs['ErrorExecuteTestCase']['Msg'] + '\033[0;0m', e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorExecuteTestCase'], value1=str(e))
            ###exit(1)

    # Extract the steps from Test Case.
    def getSteps(self, **kwargs):

        try:
            # kwargs variables.
            request = kwargs.get("request")
            name_testcase = kwargs.get("name_testcase")

            xml_steps = request['fields']['Microsoft.VSTS.TCM.Steps']

            root = eT.fromstring(xml_steps)
            cont_steps = 0
            change_download_config: bool = False

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            steps = []

            for _ in root:
                # Remove HTML Tags from step.
                step = root[cont_steps][0].text
                step = Aux.Main.removeHTML(self, value=step)

                if (step.count('"') % 2 == 0) or step.split()[0].upper() in ('SAVE', 'SALVAR', 'GUARDAR'):

                    if step == '':
                        if Aux.otherConfigs['Interface']:
                            Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorEmptyLine']['Msg'])
                        print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorEmptyLine']['Msg']} {name_testcase}"
                              f"{Aux.Textcolor.END}")
                        Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorEmptyLine'], value1=name_testcase)
                        ###quit() #only the test with blank line.
                    steps.append(step)

                    # Verify if there is the save step to configure the browser.
                    if step.split()[0].upper() in ('SAVE', 'SALVAR', 'GUARDAR'):
                        change_download_config = True

                    cont_steps = cont_steps + 1

                else:
                    msgErro = ' STEP: ' + str(cont_steps + 1) + ' - TEST CASE: ' + name_testcase
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                            f"{Aux.logs['ErrorParameters']['Msg']}[/color][/b]")
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorParameters']['Msg'] + msgErro)
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorParameters']['Msg']} {msgErro}"
                          f"{Aux.Textcolor.END}")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorParameters'], value1=msgErro)
                    break
                    ### exit(1)

            Aux.Main.addLogs(self, message="General", value=Aux.logs['GetSteps'])

            return steps, cont_steps, change_download_config

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetSteps']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetSteps']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetSteps'], value1=str(e))
            ###exit(1)

    # Extract the parameters from the Test Case.
    def getParameters(self, **kwargs):

        try:
            # kwargs variables.
            request = kwargs.get("request")

            # In some cases the Test Case doesn't have variables.
            if 'Microsoft.VSTS.TCM.Parameters' in request['fields']:
                xml_parameters = request['fields']['Microsoft.VSTS.TCM.Parameters']

                root = eT.fromstring(xml_parameters)
                parameters = []

                for child in root.findall('param'):
                    parameters.append(child.get('name'))

                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetParameters'])
            else:
                parameters = None
            return parameters

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetParameters']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetParameters']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetParameters'], value1=str(e))
            ###exit(1)

    # Extract the variables from de Test Case.
    def getVariables(self, **kwargs):

        try:
            # kwargs variables.
            request = kwargs.get("request")
            parameters = kwargs.get("parameters")

            variables = []
            if parameters:
                xml_variables = request['fields']['Microsoft.VSTS.TCM.LocalDataSource']

                root = eT.fromstring(xml_variables)

                for child in root.findall('Table1'):
                    for x in parameters:
                        variables.append(child.find(x).text)

                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetVariables'])
            else:
                variables = None

            return variables

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetVariables']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetVariables']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetVariables'], value1=str(e))
            ###exit(1)

    # Dismember the variables from each test case.
    def sliceDatas(self, **kwargs):

        try:
            # kwargs variables.
            variables = kwargs.get("variables")
            parameters = kwargs.get("parameters")
            steps = kwargs.get("steps")

            if variables and parameters:
                # Variables.
                dic_test = {}
                datas = []
                cont_variable = 0

                # Amount of test cases.
                testcase_amount = int(len(variables) / len(parameters))
                # Create the dict with the tests and steps for each one.
                for num in range(1, testcase_amount + 1):
                    list_step = []
                    for cont, step_content in enumerate(steps, start=1):
                        list_step.append(step_content)
                        dic_test[num] = list_step

                # Variables x Parameters.
                for num in range(0, testcase_amount):
                    variables_param = {}
                    for cont, _ in enumerate(parameters):
                        variables_param[parameters[cont]] = variables[cont + cont_variable]
                    cont_variable = cont_variable + len(parameters)

                    # Create the dict to the variables.
                    # Each variable line is new interaction = test.
                    for step in steps:
                        if '@' in step:
                            num_of_at = step.count('@')
                            for num_at in range(0, num_of_at):
                                variable_no_at = Aux.regex.findall('"@([^"]*)"', step)[0]
                                variable = "@" + variable_no_at
                                if variables_param[variable_no_at] is None:
                                    if Aux.otherConfigs['Interface']:
                                        raise Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorLineEmpty']['Msg'])
                                    else:
                                        raise print(Aux.logs['ErrorLineEmpty']['Msg'])
                                else:
                                    step = Aux.regex.sub(variable, repr(variables_param[variable_no_at])[1:-1], step)
                            datas.append(step)
                        else:
                            datas.append(step)
            else:
                datas = steps

            Aux.Main.addLogs(self, message="General", value=Aux.logs['SliceDatas'])

            return datas

        # When there is no variable.
        except ZeroDivisionError:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorLineEmpty']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorLineEmpty']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorLineEmpty'])
            return steps

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorSliceDatas']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSliceDatas']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSliceDatas'], value1=str(e))
            ###exit(1)

    # ====================================== ISOLATE FUNCTIONS =========================================================
    # Get the Run info.
    def getInfoRun(self, **kwargs):

        try:

            # kwargs variables.
            project = kwargs.get("project")
            test_run_id = kwargs.get("test_run_id")
            test_case_id_azure = kwargs.get("test_case_id_azure")
            name_testcase = kwargs.get("name_testcase")
            cont_iteration = kwargs.get("cont_iteration")
            step = kwargs.get("step_failed")
            status_ct = kwargs.get("status_ct")

            version = '6.0-preview.6'
            new_comments = ''
            comments = ''
            old_comments = ''
            actual_comment = ''

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Get the actual Result comments.
            self.url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + '/results/' + \
                       str(test_case_id_azure) + '?api-version=' + version

            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if q.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['GetInfoRun']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['GetInfoRun']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetInfoRun'])

                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)
                if status_ct != "Passed":
                    # Comments from older iterations plus actual comments.
                    if 'comment' in resp:
                        old_comments = resp['comment'] + '\n\n'

                    actual_comment = "**TEST CASE FAILED - NAME:** " + name_testcase \
                                   + " - **ITERATION** :" + str(cont_iteration) + " - **STEP** : " \
                                   + str(step)

                    new_comments = old_comments + actual_comment

                # Comments from older iterations.
                elif 'comment' in resp:
                    new_comments = resp['comment'] + '\n\n'

                comments = comments + new_comments

                # Test executed by.
                full_name_run_test = resp['runBy']['displayName']

                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetInfoRun'])

                return comments, full_name_run_test, actual_comment

            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + " - getInfoRun")

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                # Access screen running.
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorGetInfoRun']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetInfoRun']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetInfoRun']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetInfoRun'], value1=str(e))
            ###exit(1)

    # Update the test cases in a Run.
    def updateTestCaseRun(self, **kwargs):

        # kwargs variables.
        project = kwargs.get("project")
        test_run_id = kwargs.get("test_run_id")
        test_case_id_azure = kwargs.get("test_case_id_azure")
        status_ct = kwargs.get("status_ct")
        duration = kwargs.get("duration")
        comments = kwargs.get("comments")

        try:
            version = '6.0'

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Get the actual Result comments.
            self.url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + \
                       '/results?api-version=' + version

            test_datas = {
                             "id": test_case_id_azure,
                             "state": "Completed",
                             "computerName": socket.gethostname(),
                             "outcome": status_ct,
                             "durationInMs": duration,
                             "comment": comments,
                         },

            p = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=test_datas, timeout=None)
            if p.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['UpdateTestCaseRun']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UpdateTestCaseRun']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['UpdateTestCaseRun'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'],
                                 value1='Status code: ' + str(p.status_code) + ' - UpdateTestCaseRun')

        except Exception as e:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorUpdateTestCaseRun']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorUpdateTestCaseRun']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUpdateTestCaseRun']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorUpdateTestCaseRun'], value1=str(e))
            ###exit(1)

    # Save the evidencess in the Run.
    def SaveEvidenceRun(self, **kwargs):

        try:

            # kwargs variables.
            project = kwargs.get("project")
            test_run_id = kwargs.get("test_run_id")
            test_case_id_azure = kwargs.get("test_case_id_azure")
            evidence_folder = kwargs.get("evidence_folder")
            name_testcase = kwargs.get("name_testcase")
            cont_iteration = kwargs.get("cont_iteration")

            version = '6.1-preview.1'

            self.url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + '/Results/' \
                       + str(test_case_id_azure) + '/attachments?api-version=' + version

            evidence_file = name_testcase + " - ITERATION " + str(cont_iteration) + ".pdf"

            with open(Aux.os.path.join(evidence_folder, name_testcase, evidence_file), "rb") as word_file:
                encoded_bytes = base64.b64encode(word_file.read())
                encoded_str = str(encoded_bytes, "utf-8")

            file_datas = {
                "stream": encoded_str,
                "fileName": "EST - " + evidence_file,
                "comment": "Evidence of the test case: " + name_testcase,
                "attachmentType": "GeneralAttachment"
            }

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            p = requests.post(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=file_datas, timeout=None)
            if p.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['SaveEvidenceRun']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveEvidenceRun']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['SaveEvidenceRun'], value1="SaveEvidenceRun")
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}"
                                                           f"[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + " - SaveEvidenceRun")

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorSaveEvidenceRun']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorSaveEvidenceRun']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveEvidenceRun']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSaveEvidenceRun'], value1=str(e))
            ###exit(1)

    # Update the evidence in the TestCase.
    def SaveEvidenceTestCase(self, **kwargs):

        # kwargs variables.
        project = kwargs.get("project")
        evidence_folder = kwargs.get("evidence_folder")
        test_case_id = kwargs.get("test_case_id")
        name_testcase = kwargs.get("name_testcase")
        cont_iteration = kwargs.get("cont_iteration")

        try:

            version = '5.1'

            evidence_file = name_testcase + " - ITERATION " + str(cont_iteration) + ".pdf"

            self.url = 'https://' + instance + project + '/_apis/wit/attachments?fileName=' + evidence_file + \
                       '&api-version=' + version

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            with open(Aux.os.path.join(evidence_folder, name_testcase, evidence_file), "rb") as pdf_file:
                data = pdf_file.read()

            headers = {'Content-Type': 'application/octet-stream'}

            p = requests.post(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], data=data, headers=headers,
                              timeout=None)
            if p.status_code == 201:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)
                idAttachment = resp['id']

                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['SaveEvidenceTestCaseID']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveEvidenceTestCaseID']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['SaveEvidenceTestCaseID'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}"
                                                           f"[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - SaveEvidenceTestCaseID')

            # ------------------------------------ Second API connection -----------------------------------------------
            """
            Function: Update the evidence inside the workitem (Azure).
    
            MS API Docs - Link:
            https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.1
            """

            version = '6.1-preview.3'

            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
                       + version

            headers = {'content-type': 'application/json-patch+json'}

            file_datas = [
                {
                    "op": "add",
                    "path": "/fields/System.History",
                    "value": "Adding the test evidence: " + evidence_file
                },
                {
                    "op": "add",
                    "path": "/relations/-",
                    "value": {
                        "rel": "AttachedFile",
                        "url": "https://kantarware.visualstudio.com/_apis/wit/attachments/" + idAttachment +
                               "?fileName=" + evidence_file,
                        "attributes": {
                            "comment": evidence_file
                        }
                    }
                }
            ]

            q = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=file_datas, headers=headers,
                               timeout=None)
            if q.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['SaveEvidenceTestCase']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveEvidenceTestCase']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['SaveEvidenceTestCase'])
            elif q.status_code in [500, 412]:
                AzureConnection._DownloadAttachment(self, project=project, test_case_id=test_case_id,
                                                    cont_iteration=cont_iteration, name_testcase=name_testcase)

                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['SaveEvidence100files']['Msg']}"
                                                           f"[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['SaveEvidence100files']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['SaveEvidence100files']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['SaveEvidence100files'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}"
                                                           f"[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - ' + str(q.text) + ' - SaveEvidenceTestCase')
        except Exception as e:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorSaveEvidenceTestCase']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorSaveEvidenceTestCase']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveEvidenceTestCase']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSaveEvidenceTestCase'], value1=str(e))
            ###exit(1)

    def UpdateStatusAutomated(self, **kwargs):
        """
        Function: Update the status the Automated Test Status.

        MS API Docs - Link:
        https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.1
        """
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            test_case_id = kwargs.get('test_case_id')
            automation_status = kwargs.get('automation_status')
            workitem_status = kwargs.get('workitem_status')

            version = '6.1-preview.3'

            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
                       + version

            headers = {'content-type': 'application/json-patch+json'}

            file_datas = [
                {
                    "op": "add",
                    "path": "/fields/System.History",
                    "value": "Update the automation status and Test Case status"
                },
                {
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.TCM.AutomationStatus",
                    "value": automation_status
                },
                {
                    "op": "add",
                    "path": "/fields/System.State",
                    "value": workitem_status
                }
            ]

            r = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=file_datas, headers=headers,
                               timeout=None)
            if r.status_code == 200:
                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    import AppAutomation
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.blue.defaultvalue}]"
                                                           f"{Aux.logs['UpdateStatusAutomated']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.BLUE}{Aux.logs['UpdateStatusAutomated']['Msg']}{Aux.Textcolor.END}")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['UpdateStatusAutomated'])
            else:
                raise Exception

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorUpdateStatusAutomated']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUpdateStatusAutomated']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorUpdateStatusAutomated'], 
                             value1='Status code: ' + str(r.status_code) + " - UpdateStatusAutomated")
            ###exit(1)

    # Download de attachments when there are more than 100 in a WIT and upload a .zip file.
    def _DownloadAttachment(self, **kwargs):
        try:
            # kwargs arguments.
            project = kwargs.get('project')
            test_case_id = kwargs.get('test_case_id')
            cont_iteration = kwargs.get('cont_iteration')
            name_testcase = kwargs.get('name_testcase')

            count_evidences = 1
            order = 0
            version = '6.0'
            evidence_folder = Aux.os.path.join(Aux.directories['EvidenceFolder'], name_testcase)
            relation_list = []
            order_list = []
            count_evidences_list = []
            relation_failed = ''
            order_failed = ''
            count_evidences_failed = ''

            Aux.Main.deleteDirectory(self, directory=evidence_folder)
            Aux.Main.deleteFiles(self, path_log=Aux.os.path.join(Aux.directories['EvidenceFolder']), extension='.zip',
                                 exact_file=name_testcase + '.zip')

            self.url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(test_case_id) + \
                       '&$expand=Relations&api-version=' + version

            r = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if r.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(r.json())
                resp = json.loads(json_str)
                rev_id = resp['value'][0]['rev']
                total = resp['value'][0]['relations'].__len__()

                for relation in resp['value'][0]['relations']:
                    order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed = \
                        AzureConnection._readRelation(self, project=project, total=total, test_case_id=test_case_id,
                                                      order=order, rev_id=rev_id, name_testcase=name_testcase,
                                                      count_evidences=count_evidences, relation=relation)

                    if relation_failed != None:
                        relation_list.append(relation_failed)
                        order_list.append(order_failed)
                        count_evidences_list.append(count_evidences_failed)

                # Sleep to try again.
                if relation_failed != None:
                    for seconds in range(1, 15):
                        time.sleep(1)
                        # Access Screen Running.
                        if Aux.otherConfigs['Interface']:
                            import AppAutomation
                            screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                            screenRunning.write_message_on_console(
                                f"[b][color={AppAutomation.KivyTextColor.blue.defaultvalue}]"
                                f"{Aux.logs['WaitTime']['Msg']} {seconds} / 15[/color][/b]")
                        print(f"{Aux.Textcolor.BLUE}{Aux.logs['WaitTime']['Msg']}{seconds} / 15{Aux.Textcolor.END}")

                # If any download fail.
                while relation_list.__len__() != 0:
                    for relation in relation_list:
                        order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed = \
                            AzureConnection._readRelation(self, name_testcase=name_testcase, order=order_list[0],
                                                          test_case_id=test_case_id, relation=relation,
                                                          total=count_evidences_list[-1], rev_id=rev_id,
                                                          project=project, count_evidences=count_evidences_list[0])

                        if relation_failed is None:
                            relation_list.pop(0)
                            order_list.pop(0)
                            count_evidences_list.pop(0)

                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    import AppAutomation
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['GenerateZIPFile']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.BLUE}{Aux.logs['GenerateZIPFile']['Msg']}{Aux.Textcolor.END}")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['GenerateZIPFile']['Msg'])
                Aux.shutil.make_archive(evidence_folder, 'zip', evidence_folder)

                AzureConnection.UploadDownloadFile(self, project=project, test_case_id=str(test_case_id),
                                                   evidence_folder=Aux.directories['EvidenceFolder'],
                                                   download_file_name=name_testcase + '.zip',
                                                   file_name=name_testcase + '.zip')

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorDownloadAttachment']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorDownloadAttachment']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorDownloadAttachment'], value1=str(e))
            ###exit(1)

    # Read the test case relation to upload the .zip file.
    def _readRelation(self, **kwargs):

        # kwargs arguments.
        project = kwargs.get('project')
        relation = kwargs.get('relation')
        rev_id = kwargs.get('rev_id')
        total = kwargs.get('total')
        order = kwargs.get('order')
        count_evidences = kwargs.get('count_evidences')
        name_testcase = kwargs.get('name_testcase')
        test_case_id = kwargs.get('test_case_id')

        # Variables.
        version = '6.0'
        relation_failed = None
        order_failed = None
        count_evidences_failed = None

        try:

            # Extract only if it a .pdf evidence.
            if relation['rel'] == 'AttachedFile' and relation['attributes']['name'].split('.')[-1] == 'pdf':
                date_time_folder = relation['attributes']['resourceCreatedDate'].replace(':', '.')
                id_point = relation['url'].split('/')[7]
                name = relation['attributes']['name']

                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    import AppAutomation
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['GenerateZIP']['Msg']} "
                                                           f"{count_evidences} / {total}[/color][/b]")
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['GenerateZIP']['Msg']} {count_evidences} / "
                      f"{total}{Aux.Textcolor.END}")

                Aux.Main.createDirectory(self, path_folder=Aux.os.path.join(Aux.directories['EvidenceFolder'], 
                                                                            name_testcase, date_time_folder))

                self.url = 'https://' + instance + project + '/_apis/wit/attachments/' + str(id_point) + \
                           '?api-version=' + version
                s = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=10)

                download = Aux.os.path.join(Aux.directories['EvidenceFolder'], name_testcase, date_time_folder, name)
                with open(download, 'wb') as f:
                    f.write(s.content)

                # Delete de .pdf files.
                if s.status_code == 200:
                    AzureConnection.DeleteDownloadFile(self, project=project, rev_id=rev_id,
                                                       test_case_id=str(test_case_id), order=order)
                rev_id += 1
            else:
                order += 1
            count_evidences += 1

        # If any download fail.
        except requests.ConnectionError:
            relation_failed = relation
            order_failed = order
            count_evidences_failed = count_evidences
            count_evidences += 1

        except Exception as e:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorDownloadAttachment']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorDownloadAttachment']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorDownloadAttachment']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorDownloadAttachment'], value1=str(e))
            ###exit(1)

        finally:
            return order, count_evidences, rev_id, relation_failed, order_failed, count_evidences_failed

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

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation

            # check if the download file already exist.
            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + \
                       '?$expand=all&api-version=' + version

            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)

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
                        AzureConnection.DeleteDownloadFile(self, project=project, rev_id=rev_id,
                                                           test_case_id=str(test_case_id), order=order)
                        rev_id += 1

                AzureConnection.UploadDownloadFile(self, project=project, evidence_folder=evidence_folder,
                                                   test_case_id=str(test_case_id),
                                                   download_file_name=download_file_name, file_name=file_name)

                if Aux.otherConfigs['Interface']:
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['CheckDownloadFile']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['CheckDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['CheckDownloadFile'])

            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - CheckDownloadFile')

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorCheckDownloadFile']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorCheckDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorCheckDownloadFile'], value1=str(e))
            ###exit(1)

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
            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + test_case_id + '?api-version=' \
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

            q = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=attachment_details,
                               headers=headers, timeout=None)

            if q.status_code == 200:
                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    import AppAutomation
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['DeleteDownloadFile']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['DeleteDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['DeleteDownloadFile'])
            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - DeleteDownloadFile')

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorDeleteDownloadFile']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorDeleteDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorDeleteDownloadFile'], value1=str(e))
            ###exit(1)

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

            if Aux.otherConfigs['Interface']:
                import AppAutomation

            self.url = 'https://' + instance + project + '/_apis/wit/attachments?fileName=' + str(file_name) + \
                       '&api-version=' + version

            with open(Aux.os.path.join(evidence_folder, file_name), "rb") as file:
                data = file.read()

            headers = {'Content-Type': 'application/octet-stream'}

            p = requests.post(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], data=data, headers=headers,
                              timeout=None)
            if p.status_code == 201:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)
                idAttachment = resp['id']
                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['UploadDownloadFileID']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UploadDownloadFileID']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['UploadDownloadFileID'])
            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - UploadDownloadFileID')

            # ------------------------------------ Second API conection ------------------------------------------------

            # Add the attachment in Azure.
            version = '6.1-preview.3'

            self.url = 'https://' + instance + project + '/_apis/wit/workitems/' + str(test_case_id) + '?api-version=' \
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

            q = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=file_datas, headers=headers,
                               timeout=None)
            if q.status_code == 200:
                # Access Screen Running.
                if Aux.otherConfigs['Interface']:
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['UploadDownloadFile']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UploadDownloadFile']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['UploadDownloadFile'])
            else:
                if Aux.otherConfigs['Interface']:
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - UploadDownloadFile')

        except Exception as e:
            if Aux.otherConfigs['Interface']:
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorUploadDownloadFile']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUploadDownloadFile']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorUploadDownloadFile'], value1=str(e))
            ###exit(1)

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

            self.url = 'https://' + instance + project + '/_apis/wit/workitems?ids=' + str(id_testcase) + \
                       '&$expand=all&api-version=' + version

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            p = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if p.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)

                for order in range(1, len(resp['value'][0]['relations'])):
                    download_name = resp['value'][0]['relations'][order]['attributes']['name']
                    test_name = resp['value'][0]['fields']['System.Title']

                    if any(x in download_name for x in list_names):
                        file_url = resp['value'][0]['relations'][order]['url']

                        r = requests.get(file_url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)

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

                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['SaveDownloadFileLocally']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['SaveDownloadFileLocally']['Msg']}"
                      f"{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['SaveDownloadFileLocally'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - ErrorSaveDownloadFileLocally')

            return test_name, id_testcase, sorted(list_files_baseline), sorted(list_files_new)

        except Exception as e:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                                                       f"{Aux.logs['ErrorSaveDownloadFileLocally']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorSaveDownloadFileLocally']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveDownloadFileLocally']['Msg']}"
                  f"{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSaveDownloadFileLocally'], value1=str(e))
            ###exit(1)

    # Update the Run.
    def updateRun(self, **kwargs):

        # kwargs variables:
        project = kwargs.get("project")
        test_run_id = kwargs.get("test_run_id")
        status_run = kwargs.get("status_run")

        try:

            version = '6.0-preview.3'

            self.url = 'https://' + instance + project + '/_apis/test/runs/' + str(test_run_id) + '?api-version=' + \
                       version

            test_datas = {
                "state": status_run,
            }

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            p = requests.patch(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], json=test_datas, timeout=None)
            if p.status_code == 200:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(
                        f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                        f"{Aux.logs['UpdateRun']['Msg']}[/color][/b]")
                print(f"{Aux.Textcolor.WARNING}{Aux.logs['UpdateRun']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['UpdateRun'])
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - updateRun')

        except Exception as e:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorUpdateRun']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorUpdateRun']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorUpdateRun']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorUpdateRun'], value1=str(e))
            ###exit(1)

    # ------------------------------------------------------------------------------------------------------------------
    # Functions to manual evidence.
    # ------------------------------------------------------------------------------------------------------------------
    # Get the number of test cases in Run.
    def getTestCaseRun(self, **kwargs):
        try:
            # kwargs variables.
            project = kwargs.get('project')
            test_run_id = kwargs.get('test_run_id')
            id_test_case = kwargs.get('id_test_case')

            version = '6.1-preview.6'
            id_azure = 100000

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation

            # Get the actual Result comments.
            self.url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + \
                       '/results?api-version=' + version

            p = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if p.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(p.json())
                resp = json.loads(json_str)
                amount_test_case = resp['count']

                # Test executed by.
                full_name_run_test = resp['value'][0]['runBy']['displayName']

                # If is a unique test case.
                if id_test_case != '':
                    for index in range(0, amount_test_case):
                        if resp['value'][index]['testCase']['id'] == id_test_case:
                            id_azure = resp['value'][index]['id']
                        amount_test_case = 1

            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(p.status_code) + ' - getTestCaseRun')

            if amount_test_case == 0:
                return None
            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                                                           f"{Aux.logs['GetTestCaseRun']['Msg']}[/color][/b]")

                print(f"{Aux.Textcolor.WARNING}{Aux.logs['GetTestCaseRun']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['GetTestCaseRun'])

                return amount_test_case, id_azure, full_name_run_test

        except Exception as e:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorGetTestCaseRun']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorGetTestCaseRun']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetTestCaseRun']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorGetTestCaseRun'], value1=str(e))
            exit(1)

    # Load the attachment list in Run Result.
    def attachmentList(self, **kwargs):
        try:
            version = '6.0'

            # kwargs variables.
            project = kwargs.get('project')
            n_test_case = kwargs.get('n_test_case')
            test_run_id = kwargs.get('test_run_id')
            failed_info_dict = kwargs.get('failed_info_dict')
            id_azure = kwargs.get('id_azure')

            # Using inside the function.
            list_id_manual_print = []
            list_step_status_manual = []
            list_num_print = []
            index = 0

            # Return values.
            failed_details = {}

            # Access screen running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            self.url = 'https://' + instance + project + '/_apis/test/Runs/' + str(test_run_id) + '/results/' + \
                       str(id_azure) + '/?detailsToInclude=iterations&?api-version=' + version

            # Execute the Azure request.
            q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)
            if q.status_code == 200:
                # Filter some fields.
                json_str = json.dumps(q.json())
                resp = json.loads(json_str)

                # Verify the test execution.
                if not resp['iterationDetails']:
                    if Aux.otherConfigs['Interface']:
                        Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['NoExecutions']['Msg'])
                        Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs['NoExecutions']['Msg'])
                    raise Exception(f"{Aux.Textcolor.FAIL}{Aux.logs['NoExecutions']['Msg']}{Aux.Textcolor.END}")

                # Verify the number of test cases.
                if resp['iterationDetails'] != 0:
                    test_case_id = resp['testCase']['id']
                    test_case_name = AzureConnection.getTestCaseName(self, project=project, test_case_id=test_case_id)

                    # Failed dictionary.
                    failed_info_dict[test_case_id] = {}

                    # Validate the testcase name.
                    if Aux.Main.validateTestName(self, name_testcase=test_case_name):
                        return test_case_id, None, failed_info_dict, None

                    # Verify the number of iteration for each test case.
                    n_iterations = len(resp['iterationDetails'])

                    for n_iteration in range(0, n_iterations):

                        failed_details[n_iteration + 1] = {}

                        # Verify the prints.
                        if not resp['iterationDetails'][n_iteration]['attachments']:
                            if Aux.otherConfigs['Interface']:
                                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['NoEvidences']['Msg'])
                            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['NoEvidences']['Msg']}"
                                  f"{Aux.Textcolor.END}")
                            Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs['NoEvidences'])
                            return None, None, None

                        if Aux.otherConfigs['Interface']:
                            screenRunning.write_message_on_console(
                                f"[b][color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                                f"{test_case_name}[/color][/b]")

                        print(f"{Aux.Textcolor.BOLD}{test_case_name}{Aux.Textcolor.END}")
                        attachments = resp['iterationDetails'][n_iteration]['attachments']
                        status_step = resp['iterationDetails'][n_iteration]['actionResults']
                        completed_date = resp['iterationDetails'][n_iteration]['startedDate']
                        for character in ('T', 'Z'):  # Remove letters.
                            completed_date = completed_date.replace(character, ' ')

                        # Remove the attachments are not print screen.
                        index = len(attachments)
                        while index > 0:
                            for word in ('html', 'json'):
                                if word in attachments[index - 1]['name']:
                                    attachments.pop(index - 1)
                            else:
                                index -= 1

                        num_prints = len(attachments)
                        for num_print in range(0, num_prints):
                            actionPath = attachments[num_print]['actionPath']
                            file_name = attachments[num_print]['name']
                            id_file = attachments[num_print]['id']

                            # Check the attachment and the status of the step.
                            for result, _ in enumerate(status_step):
                                if attachments[num_print]['actionPath'] == status_step[result]['actionPath']:
                                    status = status_step[result]['outcome']

                                    if 'Failed' in status_step[result]['outcome']:
                                        step_failed = result
                                        if 'errorMessage' in status_step[step_failed]:
                                            comment = status_step[step_failed]['errorMessage']
                                            failed_details[n_iteration + 1]['Step'] = step_failed
                                            failed_details[n_iteration + 1]['Comment'] = comment
                                            failed_info_dict[test_case_id] = failed_details
                                        else:
                                            comment = ''
                                    else:
                                        step_failed = 0
                                        comment = ''

                            list_id_manual_print.append([file_name, id_file, actionPath, status])

                        # Sorted by: order print by name.
                        for order, _ in enumerate(list_id_manual_print):
                            if '_' in list_id_manual_print[order][0]:  # Treat the filename save by LightShot.
                                list_id_manual_print[order][0] = \
                                    '0' + Aux.regex.search(r'\d+', list_id_manual_print[order][0]).group(0)
                                list_id_manual_print = sorted(list_id_manual_print)
                            else:  # Treat the filename save by Azure.
                                list_id_manual_print = sorted(list_id_manual_print)
                                list_id_manual_print[order][0] = '0' + str(order + 1)

                        # Get the first item from the tuple in list.
                        list_num_print = [int(first_item[0]) for first_item in list_id_manual_print]

                        AzureConnection.saveManualPrintScreen(self, project=project, list_num_print=list_num_print,
                                                              list_id_manual_print=list_id_manual_print,
                                                              n_test_case=n_test_case + 1, n_iteration=n_iteration + 1,
                                                              test_case_name=test_case_name,
                                                              completed_date=completed_date)

                        list_id_manual_print.clear()
                        list_num_print.clear()
                        list_step_status_manual.clear()

                    test_case_id = resp['testCase']['id']

                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.blue.defaultvalue}]"
                            f"{Aux.logs['AttachmentList']['Msg']}[/color][/b]")
                    print(f"{Aux.Textcolor.BLUE}{Aux.logs['AttachmentList']['Msg']}{Aux.Textcolor.END}")

                    return test_case_id, n_iterations, failed_info_dict, completed_date

            else:
                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                           f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                    Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                 value1='Status code: ' + str(q.status_code) + ' - attachmentList')

        except Exception as e:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorAttachmentList']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorAttachmentList']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorAttachmentList']['Msg']}{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorAttachmentList'], value1=str(e))
            ###exit(1)

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

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Saving by the attachment ID order.
            for index, id_manual_print in enumerate(list_id_manual_print):

                order = str(list_step_order[index])
                # Variable.
                step_order = str(order).zfill(2)

                file_name = 'CT' + str(n_test_case).zfill(2) + '-IT' + str(n_iteration).zfill(2) + '-' + \
                            Aux.otherConfigs["EvidenceName"] + step_order + Aux.otherConfigs["EvidenceExtension"]

                self.url = 'https://' + instance + project + '/_api/_testresult/DownloadAttachment?attachmentId=' + \
                           str(id_manual_print[1]) + '&api-version=' + version

                # Execute the Azure request.
                q = requests.get(self.url, auth=Aux.otherConfigs['HttpBasicAuth'], timeout=None)

                if q.status_code == 200:
                    evidence_image = Aux.os.path.join(Aux.directories['EvidenceFolderManual'], file_name)
                    with open(evidence_image, 'wb') as print_screen:
                        print_screen.write(q.content)

                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[u][color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                            f"{Aux.logs['SaveManualPrintScreen']['Msg']}[/u]" +
                            f" {test_case_name} ITERATION " +
                            f"{n_iteration} - Print {step_order}[/color]")

                    print(f"{Aux.Textcolor.UNDERLINE}{Aux.logs['SaveManualPrintScreen']['Msg']}{Aux.Textcolor.END} "
                          f"{test_case_name} ITERATION "
                          f"{n_iteration} - Print {step_order}")

                elif q.status_code == 401:
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                            f"{Aux.logs['ErrorToken']['Msg']}[/color][/b]")
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorToken']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorToken'],
                                     value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')

                else:
                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                            f"{Aux.logs['ErrorRequest']['Msg']}[/color][/b]")
                        Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorRequest']['Msg'])
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorRequest']['Msg']}{Aux.Textcolor.END}\n")
                    Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorRequest'], 
                                     value1='Status code: ' + str(q.status_code) + ' - saveManualPrintScreen')

        except Exception as e:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorSaveManualPrintScreen']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorSaveManualPrintScreen']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorSaveManualPrintScreen']['Msg']}"
                  f"{Aux.Textcolor.END}", e)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ErrorSaveManualPrintScreen'], value1=str(e))
            ###exit(1)

# class GitHubConnection:
#
#     def __init__(self):
#         self.url = None
#
#     # Check for Updates.
#     def check_Updates(self):
#
#         self.URL = 'https://' + token_GitHub + '@raw.githubusercontent.com/AutomacaoITQC/AutomacaoQA/master/version.txt'
#
#         headers = {
#             'Authorization': f'token {token_GitHub}',
#             'Accept': 'application/vnd.github.v4+raw'
#         }
#
#         try:
#             from AppAutomation import UpdateField
#             update = UpdateField()
#
#             response = requests.get(self.URL, headers=headers)
#
#             if response.status_code == 200:
#                 GitHubVersion = response.text
#
#                 # If the GitHub version is latest than local version.
#                 if float(GitHubVersion) > float(LocalVersion):
#                     update.show_Update_input()
#                     update.run()
#
#                 else:
#                     print('Não há atualizações disponíveis')
#                     #update.no_updates_available()
#                     #update.run()
#
#             else:
#                 print('Não foi possível verificar atualizações!')
#                 update.could_not_check_for_updates_msg()
#                 update.run()
#
#         except Exception as error:
#             print('Erro: ' + str(error))
#
#     # Check for Updates
#     def download_Updates(self):
#
#         from AppAutomation import UpdateField
#
#         update = UpdateField()
#
#         headers = {
#             'Authorization': f'token {token_GitHub}',
#             'Accept': 'application/vnd.github.v4+raw'
#         }
#
#         try:
#             # diretório de download
#             DOWNLOAD_DIR = 'C:\ibope\Repository\TEMP'
#             LINK_DOWNLOAD = 'https://' + token_GitHub + '@raw.githubusercontent.com/AutomacaoITQC/AutomacaoQA/master/exec/Automation_EXE.zip'
#             local_filename = LINK_DOWNLOAD.split('/')[-1]
#
#             # download Atualização
#             with requests.get(LINK_DOWNLOAD, stream=True, headers=headers) as r:
#                 if r.status_code == 200:
#                     with open(DOWNLOAD_DIR + '\\' + local_filename, 'wb') as f:
#                         shutil.copyfileobj(r.raw, f)
#                         print('DOWNLOAD COMPLETO DA ATUALIZAÇÃO!')
#
#                 else:
#                     print('FALHA AO BAIXAR A VERSÃO')
#                     update.download_update_fail_msg()
#                     update.run()
#
#             LINK_DOWNLOAD_BAT = 'https://' + token_GitHub + '@raw.githubusercontent.com/AutomacaoITQC/AutomacaoQA/master/exec/Install.bat'
#             local_filename = LINK_DOWNLOAD_BAT.split('/')[-1]
#
#             # download BAT da Atualização
#             with requests.get(LINK_DOWNLOAD_BAT, stream=True, headers=headers) as r:
#                 if r.status_code == 200:
#
#                     with open(DOWNLOAD_DIR + '\\' + local_filename, 'wb') as f:
#                         shutil.copyfileobj(r.raw, f)
#                         print('DOWNLOAD COMPLETO DA BAT!')
#
#                 else:
#                     print('FALHA AO BAIXAR A BAT DE INSTALAÇÃO DA VERSÃO')
#                     update.download_update_fail_msg()
#                     update.run()
#
#             #update.download_update_completed_msg()
#             #update.run()
#
#             #instalar Atualização
#             #install_Update(self)
#
#         except Exception as error:
#             print('Erro: ' + str(error))
#
#     def install_Update(self):
#         subprocess.call([r'C:\ibope\Repository\TEMP\Install.bat'])
