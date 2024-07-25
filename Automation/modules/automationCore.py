import common_libs as Lib


class Main:

    def __init__(self, url):
        self.url = url
        self.connections = Lib.Con.Connections()

    def main(self):

        save_evidence = 'N'

        try:
            Lib.Aux.Main.deleteDirectory(self, directory=Lib.Aux.directories["Temp"])

            project_id, project_name = self.connections.getProjects()

            Lib.os.system('cls')

            while True:
                print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['SaveEvidenceMsg']['Msg']}"
                      f"{Lib.Aux.Textcolor.END}")
                evidence = input()
                if evidence.upper() in ['Y', 'S']:
                    save_evidence = True
                    break
                elif evidence.upper() in ['', 'N']:
                    save_evidence = False
                    break

            Lib.os.system('cls')

            test_case_id_list = self.connections.getTestCases(project_id=project_id)

            Main.startAutomation(self, project_id=project_id, project_name=project_name,
                                 test_case_id_list=test_case_id_list, save_evidence=save_evidence)

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorMain']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorMain"]['Msg'], value1=str(ex))

        finally:
            print(f"{Lib.Aux.Textcolor.BLUE}{Lib.Aux.otherConfigs['MsgFinishedExecution']['Msg']}{Lib.Aux.Textcolor.END}")

    # Execute the test case iterations.
    def startAutomation(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        project_name = kwargs.get('project_name')
        test_case_id_list = kwargs.get("test_case_id_list")
        save_evidence = kwargs.get("save_evidence")

        # Variables.
        duration = 0
        status = None
        testcase_status = None
        status_list = []

        try:
            # Complete name (if it is using the VPN).
            executed_by = Lib.win32net.NetUserGetInfo(Lib.win32net.NetGetAnyDCName(),
                                                      Lib.win32api.GetUserName(), 2)["full_name"]

        except:
            # Windows login (if it is not using the VPN).
            executed_by = Lib.Aux.get_display_name(self)

        try:

            for index, test_case_id in enumerate(test_case_id_list):
                status_ct_automation = 'Planned'

                # Inform the test case percentage already executed.
                Lib.Aux.Main.percentage(actual=index, total=len(test_case_id_list))

                # change_download_config: bool
                order_steps_list, name_testcase, steps_list, verbs_list, parameters1_list, parameters2_list = \
                    self.connections.startSteps(project_id=project_id, test_case_id=test_case_id)

                # Execution Initial time.
                initial_time = Lib.datetime.datetime.now()

                # Ask if it needs to save the evidence.
                if save_evidence:
                    status = "Not Completed"
                    # Create the TestSet folder.
                    test_set_path = Lib.os.path.join(Lib.Aux.directories["EvidenceFolder"],
                                                     Lib.Aux.otherConfigs["ETSName"] +
                                                     str(test_case_id) + " - " + name_testcase)

                    Lib.Aux.Main.createDirectory(path_folder=test_set_path)
                    Lib.shutil.rmtree(test_set_path)
                    Lib.os.makedirs(test_set_path)
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["EvidenceFolder"])
                else:
                    test_set_path = None
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["WarningEvidenceFolder"])

                Lib.Aux.Main.addLogs(message="NewSession",
                                     value="\nID: " + str(test_case_id) + " - TEST CASE: " + name_testcase +
                                           "\nPROJECT: " + project_name + "\n")

                print(f"{Lib.Aux.Textcolor.BOLD}{name_testcase}{Lib.Aux.Textcolor.END}")
                status, step_failed, take_picture_status =\
                    Main.executeStepByStep(self, order_steps_list=order_steps_list, steps_list=steps_list,
                                           verbs_list=verbs_list, test_set_path=test_set_path,
                                           save_evidence=save_evidence, parameters1_list=parameters1_list,
                                           parameters2_list=parameters2_list)

                # Set the list of iteration status for the test case.
                status_list.append(status)

                # If fail / abort in an iteration.
                if status == "Failed" and save_evidence:
                    Lib.Func.Main.verifyBrowser(self)

                elif status == "Aborted" and save_evidence:
                    Lib.Func.Main.verifyBrowser(self)
                    # status_ct_automation = 'Failed'
                # else:
                    # testcase_status = 'Closed'

                # Set the test case duration.
                duration = (
                    Lib.Aux.Main.convert_seconds_to_string(self, time_spent=(Lib.datetime.datetime.now()
                                                                             - initial_time).total_seconds()))

                # Verify in the list if the iteration status for the test case.
                if "Failed" in status_list:
                    status = "Failed"
                elif "Aborted" in status_list:
                    status = "Aborted"
                else:
                    status = "Passed"

                # If aborted do not create evidences.
                if save_evidence and status != 'Aborted':

                    print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.logs['SavingEvidence']['Msg']}{Lib.Aux.Textcolor.END}")

                    # Create an EST file.
                    word_path = Lib.Aux.directories["ESTFile"] + ' ' + Lib.Aux.otherConfigs["Language"] + '.docx'

                    est = Lib.Aux.Main.wordAddSteps(test_case_id=test_case_id,
                                                    name_testcase=name_testcase,
                                                    word_path=word_path,
                                                    steps_list=steps_list,
                                                    test_set_path=test_set_path,
                                                    step_failed=step_failed,
                                                    executed_by=executed_by,
                                                    take_picture_status=take_picture_status,
                                                    completed_date=str(Lib.datetime.datetime.now().
                                                                       strftime("%d/%m/%Y %H:%M")),
                                                    duration=duration)
                    pdf = Lib.Aux.Main.wordToPDF(path=est)

                    if est is None:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorEST"],
                                             value1=name_testcase)

                    if pdf is None:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorConvertPDF"],
                                             value1=name_testcase)

                    if (est is not None) and (pdf is not None):
                        # Add the evidence to the Run and the Test case.
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ConvertPDF"],
                                             value1=name_testcase)
                        # GitLab.AzureConnection.SaveEvidenceRun(project=project, test_run_id=test_run_id,
                        #                                       test_case_id_azure=test_case_id_azure,
                        #                                       evidence_folder=Lib.Aux.directories["EvidenceFolder"],
                        #                                       name_testcase=Lib.Aux.otherConfigs["ETSName"] + str(
                        #                                           test_case_id) + " - " + name_testcase,
                        #                                       cont_iteration=cont_iteration)

                        self.connections.SaveEvidenceTestCase(project_id=project_id,
                                                              test_case_id=test_case_id, status=status,
                                                              evidence_folder=Lib.Aux.directories["EvidenceFolder"],
                                                              name_testcase=Lib.Aux.otherConfigs["ETSName"] +
                                                                            str(test_case_id) + " - " + name_testcase)

                    # Clear the evidences prints.
                    Lib.Aux.Main.deleteFiles(file_path=test_set_path, extension="png")
                    Lib.Aux.Main.deleteFiles(file_path=test_set_path, extension="json")

                    # If there is file to download update to GitLab.
                    # if save_evidence and not status == "Aborted":
                    #     file_name = Lib.Aux.os.listdir(Lib.Aux.directories["DownloadFolder"])
                    #
                    #     status_ct_automation = "Planned"
                    #     testcase_status = "Design"
                    #     status = "Failed"
                    #     raise Exception
                    #     Lib.Aux.Main.deleteFiles(file_path=Lib.Aux.directories["DownloadFolder"], extension='*')

                    #### SOMENTE APÓS EXISTIR O TEST SUIT.
                    # if save_evidence:
                    #     # Update the status automation and test case status inside Test Case.
                    #     GitLab.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
                    #                                                 testcase_status=testcase_status,
                    #                                                 automation_status=status_ct_automation)

            # Inform the test case percentage already executed (100%).
            Lib.Aux.Main.percentage(actual=len(test_case_id_list), total=len(test_case_id_list))

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorStartAutomation']['Msg']}{Lib.Aux.Textcolor.END}",
                  str(ex))
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorStartAutomation"], value1=str(ex))

            #### SOMENTE APÓS EXISTIR O TEST SUIT.
            # GitLab.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
            #                                             testcase_status=testcase_status,
            #                                             automation_status=status_ct_automation)

        # Update the Run status.
        finally:
            # Clear the API variables.

            Lib.Aux.otherConfigs['API_Authorization'] = ''
            Lib.Aux.otherConfigs['API_Body'] = ''
            Lib.Aux.otherConfigs['API_Endpoint'] = ''
            Lib.Aux.otherConfigs['API_Headers'] = ''
            Lib.Aux.otherConfigs['API_Params'] = ''
            Lib.Aux.otherConfigs['API_Response'] = ''
            Lib.Aux.otherConfigs['API_Step'] = False
            Lib.Aux.Main.addLogs(message="EndExecution")

    # Execute the test case steps.
    def executeStepByStep(self, **kwargs):

        # kwargs variables.
        test_set_path = kwargs.get('test_set_path')
        order_steps_list = kwargs.get('order_steps_list')
        steps_list = kwargs.get('steps_list')
        verbs_list = kwargs.get('verbs_list')
        parameters1_list = kwargs.get('parameters1_list')
        parameters2_list = kwargs.get('parameters2_list')
        save_evidence = kwargs.get('save_evidence')

        # Variables.
        step_failed = None
        status_steps = []
        take_picture_status = None

        try:
            for index_oder, step_order in enumerate(order_steps_list):

                # Initialize the variables.
                verb = verbs_list[index_oder]
                parameters1 = parameters1_list[index_oder]
                parameters2 = parameters2_list[index_oder]
                step = steps_list[index_oder]

                # Don't execute the step with 'No' / 'Não'.
                if verb in ('"No"', '"Não"', '"No"'.replace('"', ''), '"Não"'.replace('"', '')):
                    verb = 'NoExecute'

                print(f"=+=" * 30)
                print(f"{Lib.Aux.otherConfigs['Step']['Msg']}: {step}")
                print(f"PARAM 1: {parameters1}")
                if parameters2 is not None:
                    print(f"PARAM 2: {parameters2}")

                # Execute the test step.
                Lib.Aux.otherConfigs['API_Step'] = False
                if parameters1 is None:
                    status_step = eval(Lib.Aux.verbs[verb]['Function'])(self)
                else:
                    status_step = eval(Lib.Aux.verbs[verb]['Function'])(self, verb=verb, parameters1=parameters1,
                                                                        parameters2=parameters2, step=step,
                                                                        api_action=verb,  num_of_steps=order_steps_list,
                                                                        actual_step=step_order)

                # Take the first step failed.
                if status_step == "Failed" and step_failed is None:
                    step_failed = step_order
                    status_steps.append("Failed")
                elif status_step == "Aborted" and step_failed is None:
                    step_failed = step_order
                    status_steps.append("Aborted")
                    return "Aborted", step_failed
                else:
                    status_steps.append("Passed")

                # Take the screenshot of each step, except to the NoExecute step OR API Step.
                if (verb not in ('NoExecute', 'Fechar', 'Cerrar', 'Close') and
                        Lib.Aux.otherConfigs['API_Step'] is False and
                        save_evidence):

                    # Image name file.
                    image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)

                    take_picture_status = Lib.Func.Main.takePicture(self, test_set_path=test_set_path,
                                                                    image_name=image_name)

                    if not take_picture_status:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

                elif Lib.Aux.otherConfigs['API_Step'] and save_evidence:
                    api_file_name = (Lib.Aux.otherConfigs["EvidenceNameAPI"] + str(step_order).zfill(2) +
                                     Lib.Aux.otherConfigs["EvidenceExtensionAPI"])
                    api_file = Lib.os.path.join(Lib.Aux.directories['EvidenceFolder'], test_set_path, api_file_name)

                    with open(api_file, 'w') as api_return:
                        tag = parameters1[:parameters1.find(':')]
                        if tag.upper() == "STATUS CODE":
                            api_return.write(Lib.Aux.otherConfigs['API_StatusCode'].__str__())
                        else:  # Normal response.
                            if (type(Lib.Aux.otherConfigs['API_Response']) is dict) and (
                                    Lib.Aux.otherConfigs['API_Response'].__len__() > 1):
                                for tag, value in Lib.Aux.otherConfigs['API_Response'].items():
                                    api_return.writelines(f"\nTAG AND NEW VALUE: {tag}\n")
                                    api_return.writelines(f"RESULT:{value}\n")
                                    api_return.writelines(f"-" * 120)
                            else:
                                api_return.write(Lib.Aux.otherConfigs['API_Response'].__str__())

            # Set the test case status.
            status_counter = Lib.Counter(status_steps)
            if status_counter['Failed'] != 0:
                status_ct = "Failed"
            else:
                status_ct = "Passed"

            return status_ct, step_failed, take_picture_status

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorExecuteStepByStep']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorExecuteStepByStep"], value1=str(ex))
