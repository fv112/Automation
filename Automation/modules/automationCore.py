import time

import common_libs as Lib


class Main:

    def __init__(self, url):
        self.url = url
        self.connections = Lib.Con.Connections()

    def main(self, **kwargs):

        try:
            # kwargs variables.
            project_id = kwargs.get('project_id', None)
            isolated_tc = kwargs.get('isolated_tc', None)
            id_test_case = kwargs.get('id_test_case', 0)
            save_evidence = kwargs.get('save_evidence', None)

            test_case_id_list = []

            Lib.Aux.Main.delete_directory(self, path_folder=Lib.Aux.directories['TestSetPath'])

            project_id, project_name = self.connections.get_projects(project_id=project_id)

            Lib.os.system('cls')

            while save_evidence is None:
                evidence = input(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['SaveEvidenceMsg']['Msg']}"
                                 f"{Lib.Aux.Textcolor.END}")
                if evidence.upper() in ['Y', 'S'] or save_evidence:
                    save_evidence = True
                    break
                elif evidence.upper() in ['', 'N']:
                    save_evidence = False
                    break

            Lib.os.system('cls')

            test_case_id_list = self.connections.get_test_cases(project_id=project_id, isolated_tc=isolated_tc,
                                                                id_test_case=id_test_case)

            Main.start_automation(self, project_id=project_id, project_name=project_name,
                                  test_case_id_list=test_case_id_list, save_evidence=save_evidence)

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorMain']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorMain"],
                                  value1=str(ex))

        finally:
            print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.otherConfigs['MsgFinishedExecution']['Msg']}"
                  f"{Lib.Aux.Textcolor.END}")

    # Execute the test case iterations.
    def start_automation(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        project_name = kwargs.get('project_name')
        test_case_id_list = kwargs.get("test_case_id_list")
        save_evidence = kwargs.get("save_evidence")

        # Variables.
        duration = 0
        test_list_status = []

        try:
            # Complete name (if it is using the VPN).
            executed_by = Lib.win32net.NetUserGetInfo(Lib.win32net.NetGetAnyDCName(),
                                                      Lib.win32api.GetUserName(), 2)["full_name"]

        except:
            # Windows login (if it is not using the VPN).
            executed_by = Lib.Aux.Main.get_display_name(self)

        try:

            for index, test_case_id in enumerate(test_case_id_list):
                status_ct = 'Not Run'
                Lib.Aux.otherConfigs['Api_Step'] = False

                # Inform the test case percentage already executed.
                Lib.Aux.Main.percentage(actual=index, total=len(test_case_id_list))

                order_steps_list, name_testcase, steps_list, verbs_list, parameters1_list, parameters2_list = \
                    self.connections.start_steps(project_id=project_id, test_case_id=test_case_id)

                # Execution Initial time.
                initial_time = Lib.datetime.datetime.now()

                # Ask if it needs to save the evidence.
                if save_evidence:
                    Lib.Aux.directories['TestSetPath'] = Lib.os.path.join(Lib.Aux.directories["EvidenceFolder"],
                                                                          Lib.Aux.otherConfigs["ETSName"] +
                                                                          str(test_case_id) + " - " + name_testcase)

                    # Clear the evidences.
                    Lib.Aux.Main.delete_files(folder_path=Lib.Aux.directories['TestSetPath'], extension="png")
                    Lib.Aux.Main.delete_files(folder_path=Lib.Aux.directories['TestSetPath'], extension="json")

                    Lib.Aux.Main.delete_directory(self, path_folder=Lib.Aux.directories['TestSetPath'])

                    Lib.Aux.Main.create_directory(self, path=Lib.Aux.directories['TestSetPath'])

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["EvidenceFolder"])

                else:
                    Lib.Aux.directories['TestSetPath'] = None
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["WarningEvidenceFolder"])

                Lib.Aux.Main.add_logs(message="NewSession",
                                      value="\nPROJECT: " + project_name + "\n"
                                            "\nID: " + str(test_case_id) + " - TEST CASE: " + name_testcase + "\n")

                # Validate the testcase name.
                if Lib.Aux.Main.validate_test_name(self, name_testcase=name_testcase):
                    continue

                print(f"{Lib.Aux.Textcolor.BOLD}{name_testcase}{Lib.Aux.Textcolor.END}")

                status_ct, step_failed = \
                    Main.execute_step_by_step(self, order_steps_list=order_steps_list, steps_list=steps_list,
                                              verbs_list=verbs_list,
                                              save_evidence=save_evidence, parameters1_list=parameters1_list,
                                              parameters2_list=parameters2_list)

                # Set the list of iteration status for the test case.
                test_list_status.append(status_ct)

                # If fail / abort in an iteration.
                if status_ct == "Failed" and save_evidence:
                    Lib.Func.Main.verify_browser(self)

                elif status_ct == "Aborted" and save_evidence:
                    Lib.Func.Main.verify_browser(self)

                # Set the test case duration.
                duration = (
                    Lib.Aux.Main.convert_seconds_to_string(
                        self, time_spent=(Lib.datetime.datetime.now() - initial_time).total_seconds()))

                # Verify test case list and update the test plan list.
                if "Failed" in test_list_status:
                    plan_status = "Failed"
                elif "Aborted" in test_list_status:
                    plan_status = "Aborted"
                else:
                    plan_status = "Passed"

                # If aborted do not create evidences.
                if save_evidence and status_ct != 'Aborted':

                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['SavingEvidence']['Msg']}{Lib.Aux.Textcolor.END}")

                    # Create an EST file.
                    word_path = (Lib.os.path.join(Lib.os.getcwd(), Lib.Aux.directories["ESTFile"])
                                 + ' ' + Lib.Aux.otherConfigs["Language"] + '.docx')

                    est = Lib.Aux.Main.word_add_steps(test_case_id=test_case_id,
                                                      name_testcase=name_testcase,
                                                      word_path=word_path,
                                                      steps_list=steps_list,
                                                      step_failed=step_failed,
                                                      executed_by=executed_by,
                                                      completed_date=str(Lib.datetime.datetime.now().strftime(
                                                          "%d/%m/%Y %H:%M:%S")),
                                                      duration=duration)
                    pdf = Lib.Aux.Main.word_to_pdf(path=est)

                    if est is None:
                        status_ct = "Aborted"
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorEST"],
                                              value1=name_testcase)

                    if pdf is None:
                        status_ct = "Aborted"
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorConvertPDF"],
                                              value1=name_testcase)

                    if (est is not None) and (pdf is not None):

                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ConvertPDF"],
                                              value1=name_testcase)

                        file_url_list, file_path_list, status_name_testcase = (
                            self.connections.upload_file_git_token(project_id=project_id, test_case_id=test_case_id,
                                                                   status_ct=status_ct, file_type='tc',
                                                                   name_testcase=Lib.Aux.otherConfigs["ETSName"] + str(
                                                                       test_case_id) + " - " + name_testcase))

                        self.connections.upload_file_git(project_id=project_id, file_url_list=file_url_list,
                                                         test_case_id=test_case_id, file_path_list=file_path_list,
                                                         status_name_testcase=status_name_testcase)

                        Lib.Aux.Main.delete_files(folder_path=Lib.Aux.directories['TestSetPath'], extension="png")
                        Lib.Aux.Main.delete_files(folder_path=Lib.Aux.directories['TestSetPath'], extension="json")

                    #### SOMENTE APÓS EXISTIR O TEST SUIT.
                    # if save_evidence:
                    #     # Update the status automation and test case status inside Test Case.
                    #     GitLab.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
                    #                                                 testcase_status=testcase_status,
                    #                                                 automation_status=status_ct_automation)

                    verbs_list = [verb.upper() for verb in verbs_list]
                    if any(item in verbs_list for item in ['GUARDAR', 'SALVAR', 'SAVE']):
                        file_url_list, file_path_list, status_name_testcase = (
                            self.connections.upload_file_git_token(project_id=project_id, test_case_id=test_case_id,
                                                                   status_ct=status_ct, file_type='download_file',
                                                                   name_testcase=Lib.Aux.otherConfigs["ETSName"] + str(
                                                                       test_case_id) + " - " + name_testcase)
                        )

                        self.connections.upload_file_git(project_id=project_id, file_url_list=file_url_list,
                                                         test_case_id=test_case_id, file_path_list=file_path_list,
                                                         status_name_testcase=status_name_testcase)

                self.connections.update_labels(project_id=project_id, test_case_id=test_case_id,
                                               status_ct=status_ct)

            # Inform the test case percentage already executed (100%).
            Lib.Aux.Main.percentage(actual=len(test_case_id_list), total=len(test_case_id_list))

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorStartAutomation']['Msg']} - {ex.msg[0]}"
                  f"{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorStartAutomation"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))

            #### SOMENTE APÓS EXISTIR O TEST SUIT.
            # GitLab.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
            #                                             testcase_status=testcase_status,
            #                                             automation_status=status_ct_automation)

        # Update the Run status.
        finally:
            # Clear the API variables.
            Lib.Aux.otherConfigs['Api_Authorization'] = ''
            Lib.Aux.otherConfigs['Api_Body'] = ''
            Lib.Aux.otherConfigs['Api_Endpoint'] = ''
            Lib.Aux.otherConfigs['Api_Headers'] = ''
            Lib.Aux.otherConfigs['Api_Params'] = ''
            Lib.Aux.otherConfigs['Api_Response'] = ''
            Lib.Aux.otherConfigs['Api_Step'] = False
            Lib.Aux.Main.add_logs(message="EndExecution")
            test_list_status.clear()

    # Execute the test case steps.
    def execute_step_by_step(self, **kwargs):

        # kwargs variables.
        order_steps_list = kwargs.get('order_steps_list')
        steps_list = kwargs.get('steps_list')
        verbs_list = kwargs.get('verbs_list')
        parameters1_list = kwargs.get('parameters1_list')
        parameters2_list = kwargs.get('parameters2_list')
        save_evidence = kwargs.get('save_evidence')

        # Variables.
        step_failed = 0
        status_steps = []
        step_order = None
        status_ct = 'Not Run'

        try:
            Lib.Aux.Main.delete_files(folder_path=Lib.Aux.directories['DownloadFolder'], extension='*')

            for index_oder, step_order in enumerate(order_steps_list):

                # Initialize the variables.
                verb = verbs_list[index_oder]
                parameters1 = parameters1_list[index_oder]
                parameters2 = parameters2_list[index_oder]
                step = steps_list[index_oder]

                # Don't execute the step with 'No' / 'Não'.
                if verb.upper() in ('"NO"', '"NÃO"', '"NO"'.replace('"', ''),
                                    '"NÃO"'.replace('"', '')):
                    verb = 'NoExecute'

                print(f"=+=" * 30)
                print(f"{Lib.Aux.otherConfigs['Step']['Msg']}: {step}")
                print(f"PARAM 1: {parameters1}")
                if parameters2 is not None:
                    print(f"PARAM 2: {parameters2}")

                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["StepBlank"])
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["Step"], value1=step_order.__str__())

                if Lib.Counter(status_steps)['Failed'] != 0:
                    status_steps.append("Not Run")
                    print(f"STEP STATUS: {Lib.Aux.Textcolor.WARNING}NOT RUN{Lib.Aux.Textcolor.END}")
                else:
                    status_step = (
                        eval(Lib.Aux.verbs[verb]['Function'])(self, verb=verb, parameters1=parameters1,
                                                              parameters2=parameters2, step=step, api_action=verb,
                                                              num_of_steps=order_steps_list, step_order=step_order,
                                                              save_evidence=save_evidence))

                    if status_step.upper() == "FAILED" and step_failed == 0:
                        step_failed = step_order
                        color_init = Lib.Aux.Textcolor.FAIL
                        status_steps.append("Failed")
                    elif status_step.upper() == "ABORTED" and step_failed == 0:
                        step_failed = step_order
                        status_steps.append("Aborted")
                        color_init = Lib.Aux.Textcolor.WARNING
                        return "Aborted", step_failed
                    else:
                        status_steps.append("Passed")
                        color_init = Lib.Aux.Textcolor.GREEN

                    print(f"STEP STATUS: {color_init}{status_step.upper()}{Lib.Aux.Textcolor.END}")

                    if Lib.Aux.otherConfigs['Api_Step'] is False and status_step != 'Passed':
                        image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)
                        take_picture_status = Lib.Func.Main.take_picture(self, image_name=image_name)
                        if not take_picture_status:
                            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

                    if Lib.Aux.otherConfigs['Api_Step'] and save_evidence:
                        api_file_name = (Lib.Aux.otherConfigs["EvidenceNameApi"] + str(step_order).zfill(2) +
                                         Lib.Aux.otherConfigs["EvidenceExtensionApi"])
                        api_file = Lib.os.path.join(Lib.Aux.directories['EvidenceFolder'],
                                                    Lib.Aux.directories['TestSetPath'], api_file_name)

                        with open(api_file, 'w') as api_return:
                            tag = parameters1[:parameters1.find(':')]
                            if tag.upper() == "STATUS CODE":
                                api_return.write(Lib.Aux.otherConfigs['Api_StatusCode'].__str__())
                            else:  # Normal response.
                                if (type(Lib.Aux.otherConfigs['Api_Response']) is dict) and (
                                        Lib.Aux.otherConfigs['Api_Response'].__len__() > 1):
                                    for tag, value in Lib.Aux.otherConfigs['Api_Response'].items():
                                        api_return.writelines(f"\nTAG AND NEW VALUE: {tag}\n")
                                        api_return.writelines(f"RESULT:{value}\n")
                                        api_return.writelines(f"-" * 120)
                                else:
                                    api_return.write(Lib.Aux.otherConfigs['Api_Response'].__str__())

            # Set the test case status.
            if Lib.Counter(status_steps)['Failed'] != 0:
                status_ct = "Failed"
            else:
                status_ct = "Passed"

            return status_ct, step_failed

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorExecuteStepByStep']['Msg']} - {ex.msg[0]}"
                  f"{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorExecuteStepByStep"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))

            return status_ct, step_order
