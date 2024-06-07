import modules.automationAux as Aux
import modules.automationFunc as Func
import modules.azureConnection as Azure


class Main:

    def __init__(self):
        self.main()

    def main(self):
        try:
            # Clear the temp files.
            Aux.Main.deleteDirectory(directory=Aux.directories["Temp"])

            project_id, project_name = Azure.AzureConnection.getProjects(self)

            test_case_id_list = Azure.AzureConnection.getTestCases(self, project_id=project_id)

            Main.startAutomation(self, project_id=project_id, project_name=project_name,
                                 test_case_id_list=test_case_id_list)

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorMain']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorMain"]['Msg'], value1=str(ex))

        finally:
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['MsgFinishedEvidence']['Msg']}{Aux.Textcolor.END}")

    # Execute the test case iterations.
    def startAutomation(self, **kwargs):

        # kwargs variables.
        project_id = kwargs.get("project_id")
        project_name = kwargs.get('project_name')  # Only for log.
        test_case_id_list = kwargs.get("test_case_id_list")
        # test_run_id = kwargs.get("test_run_id")
        # id_test_plan = kwargs.get("id_test_plan")  # Only for log.
        # id_test_suit = kwargs.get("id_test_suit")  # Only for log.

        # Variables.
        duration = 0
        status = None
        save_evidence = True
        status_ct_automation = None
        # comments = None
        testcase_status = None
        # full_name_run_test = None
        # actual_comment = None
        status_list = []

        try:
            # Complete name (if it is using the VPN).
            full_name_run_evidence = Aux.win32net.NetUserGetInfo(Aux.win32net.NetGetAnyDCName(),
                                                                 Aux.win32api.GetUserName(), 2)["full_name"]
        except:
            # Windows login (if it is not using the VPN).
            full_name_run_evidence = Aux.Main.get_display_name(self)

        try:
            if Aux.otherConfigs['ReplaceEvidence']:
                save_evidence = True

            for index, test_case_id in enumerate(test_case_id_list):
                status_ct_automation = 'Planned'

                # Inform the test case percentage already executed.
                Aux.Main.percentage(actual=index, total=len(test_case_id_list))

                change_download_config: bool
                order_steps_list, name_testcase, steps_list, verbs_list, parameters1_list, parameters2_list = \
                    Azure.AzureConnection.startSteps(self, project_id=project_id, test_case_id=test_case_id)
                total_steps = len(order_steps_list)
                # total_iteration = int(total_steps / cont_steps) + 1
                # step_initial = 0
                # step_final = cont_steps

                # Execution Initial time.
                initial_time = Aux.datetime.datetime.now()

                # Validate the testcase name.
                # if Aux.Main.validateTestName(name_testcase=name_testcase):
                #     # test_case_id_azure += 1
                #     continue

                # Ask if it needs to save the evidence.
                if save_evidence:
                    status = "Not Completed"
                    # Create the TestSet folder.
                    test_set_path = Aux.os.path.join(Aux.directories["EvidenceFolder"], Aux.otherConfigs["ETSName"] +
                                                     str(test_case_id) + " - " + name_testcase)

                    Aux.Main.createDirectory(path_folder=test_set_path)
                    Aux.shutil.rmtree(test_set_path)
                    Aux.os.makedirs(test_set_path)
                    Aux.Main.addLogs(message="General", value=Aux.logs["EvidenceFolder"])
                else:
                    test_set_path = None
                    Aux.Main.addLogs(message="General", value=Aux.logs["WarningEvidenceFolder"])

                # Execute step by step per Iteration.
                # for cont_iteration in range(1, total_steps):

                Aux.Main.addLogs(message="NewSession",
                                 value="\nID: " + str(test_case_id) + " - TEST CASE: " + name_testcase +
                                       "\nPROJECT: " + project_name + "\n")

                print(f"{Aux.Textcolor.BOLD}{name_testcase}{Aux.Textcolor.END}")
                status, step_failed, save_evidence, take_picture_status =\
                    Main.executeStepByStep(self, order_steps_list=order_steps_list, name_testcase=name_testcase,
                                           steps_list=steps_list, verbs_list=verbs_list, test_set_path=test_set_path,
                                           parameters1_list=parameters1_list, parameters2_list=parameters2_list)

                # Set the list of iteration status for the test case.
                status_list.append(status)

                # If fail / abort in an iteration.
                if status == "Failed" and save_evidence:
                    Func.Main.verifyBrowser(self)
                    # comments, full_name_run_test, actual_comment = \
                    #     Azure.AzureConnection.getInfoRun(project=project, test_run_id=test_run_id,
                    #                                      test_case_id_azure=test_case_id_azure,
                    #                                      name_testcase=name_testcase, status_ct=status,
                    #                                      cont_iteration=cont_iteration, step_failed=step_failed)
                    # testcase_status = 'Design'

                elif status == "Aborted" and save_evidence:
                    Func.Main.verifyBrowser(self)
                    # comments = Aux.otherConfigs['DownloadingFileIE']['Msg']
                    status_ct_automation = 'Failed'
                    # testcase_status = 'Design'

                elif save_evidence:
                    # comments, full_name_run_test, actual_comment = \
                    #     Azure.AzureConnection.getInfoRun(project=project, test_run_id=test_run_id,
                    #                                      test_case_id_azure=test_case_id_azure,
                    #                                      name_testcase=name_testcase, status_ct=status,
                    #                                      cont_iteration=cont_iteration, step_failed=step_failed)
                    testcase_status = 'Closed'

                else:
                    comments = None

                # Set the test case duration.
                duration = Aux.datetime.datetime.now() - initial_time
                duration = int(duration.total_seconds() * 1000)

                # Verify in the list if the iteration status for the test case.
                if "Failed" in status_list:
                    status = "Failed"
                elif "Aborted" in status_list:
                    status = "Aborted"
                else:
                    status = "Passed"

                # Process to generate the evidences and save to Azure.
                # if save_evidence:
                #     # Update the test case inside the Run.
                #     Azure.AzureConnection.updateTestCaseRun(project=project, test_run_id=test_run_id,
                #                                             test_case_id_azure=test_case_id_azure, status_ct=status,
                #                                             duration=duration, comments=comments)
                #     print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['GeneratingEvidence']['Msg']}"
                #           f"{Aux.Textcolor.END}\n")

                # If aborted do not create evidences.
                if save_evidence and status != 'Aborted':
                    # Create an EST file.
                    word_path = Aux.directories["ESTFile"] + ' ' + Aux.otherConfigs["Language"] + '.docx'

                    est = Aux.Main.wordAddSteps(test_case_id=test_case_id,
                                                name_testcase=name_testcase,
                                                word_path=word_path,
                                                steps_list=steps_list,
                                                test_set_path=test_set_path,
                                                step_failed=step_failed,
                                                take_picture_status=take_picture_status,
                                                completed_date=str(Aux.datetime.datetime.now().
                                                                   strftime("%d/%m/%Y %H:%M")))
                    pdf = Aux.Main.wordToPDF(path=est)

                    if est is None:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorEST"],
                                         value1=name_testcase)

                    if pdf is None:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorConvertPDF"],
                                         value1=name_testcase)

                    if (est is not None) and (pdf is not None):
                        # Add the evidence to the Run and the Test case.
                        Aux.Main.addLogs(message="General", value=Aux.logs["ConvertPDF"],
                                         value1=name_testcase)
                        Azure.AzureConnection.SaveEvidenceRun(project=project, test_run_id=test_run_id,
                                                              test_case_id_azure=test_case_id_azure,
                                                              evidence_folder=Aux.directories["EvidenceFolder"],
                                                              name_testcase=Aux.otherConfigs["ETSName"] + str(
                                                                  test_case_id) + " - " + name_testcase,
                                                              cont_iteration=cont_iteration)
                        Azure.AzureConnection.SaveEvidenceTestCase(project=project, test_case_id=test_case_id,
                                                                   evidence_folder=Aux.directories["EvidenceFolder"]
                                                                   , name_testcase=Aux.otherConfigs["ETSName"] +
                                                                   str(test_case_id) + " - " + name_testcase,
                                                                   cont_iteration=cont_iteration)

                    # Clear the evidences prints.
                    Aux.Main.deleteFiles(path_log=test_set_path, extension="png")

                    # If there is file to download update to Azure.
                    if change_download_config and save_evidence and not status == "Aborted":
                        file_name = Aux.os.listdir(Aux.directories["DownloadFolder"])
                        if file_name:  # Check if the file was download.
                            Azure.AzureConnection.CheckDownloadFile(project=project, test_case_id=str(test_case_id),
                                                                    file_name=file_name[0], compare=False,
                                                                    evidence_folder=Aux.directories["DownloadFolder"])
                        else:
                            status_ct_automation = "Planned"
                            testcase_status = "Design"
                            status = "Failed"
                            # comments = Aux.logs["ErrorDownload"]["Msg"]
                            raise Exception
                        Aux.Main.deleteFiles(path_log=Aux.directories["DownloadFolder"], extension='*')

                    # Variables.
                    # step_initial = step_final
                    # step_final = step_final + cont_steps

                    if save_evidence:
                        # Update the status automation and test case status inside Test Case.
                        Azure.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
                                                                    testcase_status=testcase_status,
                                                                    automation_status=status_ct_automation)

                test_case_id_azure += 1

            # Inform the test case percentage already executed (100%).
            Aux.Main.percentage(actual=len(test_case_id_list), total=len(test_case_id_list))

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorStartAutomation']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorStartAutomation"], value1=str(ex))

            Azure.AzureConnection.UpdateStatusAutomated(project=project, test_case_id=test_case_id,
                                                        testcase_status=testcase_status,
                                                        automation_status=status_ct_automation)

        # Update the Run status.
        finally:
            # if Aux.otherConfigs["ReplaceEvidence"]:
            #     Azure.AzureConnection.updateRun(project=project, test_run_id=test_run_id, status_run="Completed")
            Aux.Main.addLogs(message="EndExecution")

    # Execute the test case steps.
    def executeStepByStep(self, **kwargs):

        # kwargs variables.
        # list_steps = kwargs.get('list_steps')
        # step_initial = kwargs.get('step_initial', None)
        # step_final = kwargs.get('step_final', None)
        # change_download_config = kwargs.get('change_download_config', False)
        # cont_iteration = kwargs.get('cont_iteration', 0)
        test_set_path = kwargs.get('test_set_path')
        # enable_cookie = kwargs.get('enable_cookie')
        order_steps_list = kwargs.get('order_steps_list')
        name_testcase = kwargs.get('name_testcase')
        steps_list = kwargs.get('steps_list')
        verbs_list = kwargs.get('verbs_list')
        parameters1_list = kwargs.get('parameters1_list')
        parameters2_list = kwargs.get('parameters2_list')

        # Variables.
        element = None
        step_order = 1
        step_failed = None
        status_steps = []
        save_evidence = True
        take_picture_status = None

        try:
            for index_oder, step_order in enumerate(order_steps_list):
                # # Initialize the variables.
                # value1 = None
                # value2 = None
                verb = verbs_list[index_oder]
                parameters1 = parameters1_list[index_oder]
                parameters2 = parameters2_list[index_oder]
                step = steps_list[index_oder]

                # Don't execute the step with 'No' / 'Não'.
                if verb in ('"No"', '"Não"', '"No"'.replace('"', ''), '"Não"'.replace('"', '')):
                    verb = 'NoExecute'
                    # pattern = Aux.regex.compile('(?:"Não"|"No")')
                    # step = Aux.regex.sub(pattern, '', step).strip()
                # else:
                #     pattern = Aux.regex.compile('(?:"Sim"|"Si"|"Yes")')
                #     step = Aux.regex.sub(pattern, '', step).strip()
                #     verb = step.split()[0]

                # if step.count('"') >= 3:  # More than one parameter.
                #     value1 = step.split('"')[1]
                #     value2 = step.split('"')[3]
                # elif step.count('"') == 2:  # One parameter.
                #     value1 = step.split('"')[1]

                print(f"{Aux.otherConfigs['Step']['Msg']}: {step}")
                print(f"{Aux.otherConfigs['Verb']['Msg']}: {verb}")
                print(f"PARAM 1: {parameters1}")
                if parameters2 is not None:
                    print(f"PARAM 2: {parameters2}")
                print(f"=+=" * 30)

                # Execute the test step.
                if parameters1 is None:
                    status_step = eval(Aux.verbs[verb]['Function'])(self)
                else:
                    status_step = eval(Aux.verbs[verb]['Function'])(self, verb=verb, parameters1=parameters1,
                                                                    parameters2=parameters2)

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

                # Take the screenshot of each step, except to the NoExecute step.
                if Aux.otherConfigs["ReplaceEvidence"] and verb not in ('NoExecute', 'Fechar', 'Cerrar', 'Close'):

                    # Image name file.
                    image_name = Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)

                    take_picture_status = Func.Main.takePicture(self, test_set_path=test_set_path,
                                                                image_name=image_name, verb=verb, list_steps=steps_list)

                    if not take_picture_status:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorScreenshot"], value1=step)

                # step_order += 1

            # Set the test case status.
            status_counter = Aux.Counter(status_steps)
            if status_counter['Failed'] != 0:
                status_ct = "Failed"
            else:
                status_ct = "Passed"

            return status_ct, step_failed, save_evidence, take_picture_status

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorExecuteStepByStep']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorExecuteStepByStep"], value1=str(ex))
