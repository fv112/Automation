import modules.automationAux as Aux
import modules.automationFunc as Func
import modules.azureConnection as Azure


class Main:

    def __init__(self):
        pass

    def main(self, **kwargs):
        try:
            # Variables.
            test_case_id_list = []
            project = kwargs.get('project_id')
            project_name = kwargs.get('project_name') # Only for log.
            id_test_plan = kwargs.get('id_test_plan')
            id_test_suit = kwargs.get('id_test_suit')
            test_case_id_list_all = kwargs.get('test_case_id_list_all')
            enable_cookie = kwargs.get('cookie')
            Aux.otherConfigs['ReplaceEvidence'] = kwargs.get('evidence')
            Aux.otherConfigs['TimeoutSession'] = kwargs.get('timeout')

            if enable_cookie:
                Aux.otherConfigs['FlagEnableCookie'] = True
            else:
                Aux.otherConfigs['FlagEnableCookie'] = False
            if test_case_id_list_all == '': test_case_id_list_all = None

            # Clear the temp files.
            Aux.Main.deleteDirectory(self, directory=Aux.directories["Temp"])

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Start the automation.
            project, test_case_id_list, test_run_id = \
                Azure.AzureConnection.startRun(self, project=project, id_test_plan=id_test_plan,
                                               id_test_suit=id_test_suit, test_case_id_list_all=test_case_id_list_all)

            Main.startAutomation(self, project=project, project_name=project_name, id_test_plan=id_test_plan,
                                 id_test_suit=id_test_suit, test_case_id_list=test_case_id_list,
                                 test_run_id=test_run_id)

        except IndexError as e:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['IndexError']['Msg']}[/color][/b]")

        except Exception as ex:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorMain']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorMain']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorMain']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorMain"]['Msg'], value1=str(ex))

        finally:
            # Access screen running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.orange.defaultvalue}]"
                                                       f"{Aux.otherConfigs['MsgFinishedEvidence']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['MsgFinishedExecution']['Msg'])
                Aux.MDDialogAppTest().show_mddialog()
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['MsgFinishedEvidence']['Msg']}{Aux.Textcolor.END}")

    # Execute the test case iterations.
    def startAutomation(self, **kwargs):

        # kwargs variables.
        project = kwargs.get("project")
        project_name = kwargs.get('project_name')  # Only for log.
        test_case_id_list = kwargs.get("test_case_id_list")
        test_run_id = kwargs.get("test_run_id")
        id_test_plan = kwargs.get("id_test_plan") # Only for log.
        id_test_suit = kwargs.get("id_test_suit") # Only for log.

        # Variables.
        duration = 0
        status = None
        save_evidence = False
        status_ct_automation = None
        comments = None
        workitem_status = None
        full_name_run_test = None
        actual_comment = None
        status_list = []

        # Access Screen Running.
        if Aux.otherConfigs['Interface']:
            import AppAutomation
            screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

        try:
            # Complete name (if it is using the VPN).
            full_name_run_evidence = Aux.win32net.NetUserGetInfo(Aux.win32net.NetGetAnyDCName(),
                                                                 Aux.win32api.GetUserName(), 2)["full_name"]
        except:
            # Windows login (if it is not using the VPN).
            full_name_run_evidence = Aux.Main.get_display_name(self)

        try:
            test_case_id_azure = 100000

            if Aux.otherConfigs['ReplaceEvidence']:
                save_evidence = True

            for index, test_case_id in enumerate(test_case_id_list):
                status_ct_automation = 'Planned'

                # Inform the test case percentage already executed.
                Aux.Main.percentage(self, actual=index, total=len(test_case_id_list))

                change_download_config: bool
                list_steps, name_testcase, summary, cont_steps, change_download_config = \
                    Azure.AzureConnection.startSteps(self, project=project, test_case_id=test_case_id)
                total_steps = len(list_steps)
                total_iteration = int(total_steps / cont_steps) + 1
                step_initial = 0
                step_final = cont_steps

                # Execution Initial time.
                initial_time = Aux.datetime.datetime.now()

                # Validate the testcase name.
                if Aux.Main.validateTestName(self, name_testcase=name_testcase):
                    test_case_id_azure += 1
                    continue

                # Ask if it needs to save the evidence.
                if save_evidence:
                    status = "Not Completed"
                    # Create the TestSet folder.
                    test_set_path = Aux.os.path.join(Aux.directories["EvidenceFolder"], Aux.otherConfigs["ETSName"] +
                                                     str(test_case_id) + " - " + name_testcase)

                    Aux.Main.createDirectory(self, path_folder=test_set_path)
                    Aux.shutil.rmtree(test_set_path)
                    Aux.os.makedirs(test_set_path)
                    Aux.Main.addLogs(self, message="General", value=Aux.logs["EvidenceFolder"])
                else:
                    test_set_path = None
                    Aux.Main.addLogs(self, message="General", value=Aux.logs["WarningEvidenceFolder"])

                # Execute step by step per Iteration.
                for cont_iteration in range(1, total_iteration):

                    Aux.Main.addLogs(self, message="NewSession",
                                     value="\nID: " + str(test_case_id) + " - TEST CASE: " +
                                           name_testcase + " - ITERATION: " + str(cont_iteration) +
                                           "\nPROJECT: " + project_name + " - TEST PLAN: " + id_test_plan +
                                           " - TEST SUIT: " + id_test_suit + " - RUN ID: " + str(test_run_id) + "\n")

                    if Aux.otherConfigs['Interface']:
                        screenRunning.write_message_on_console(
                            f"[b][color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                            f"{name_testcase}[/color][/b]")
                    print(f"{Aux.Textcolor.BOLD}{name_testcase}{Aux.Textcolor.END}")
                    status, step_failed, save_evidence, take_picture_status = \
                        Main.executeStepByStep(self, list_steps=list_steps, test_set_path=test_set_path,
                                               step_initial=step_initial, step_final=step_final,
                                               change_download_config=change_download_config,
                                               cont_iteration=cont_iteration,
                                               enable_cookie=Aux.otherConfigs['FlagEnableCookie'])

                    # Set the list of iteration status for the test case.
                    status_list.append(status)

                    # If fail / abort in an iteration.
                    if status == "Failed" and save_evidence:
                        Func.Main.verifyBrowser(self)
                        comments, full_name_run_test, actual_comment = \
                            Azure.AzureConnection.getInfoRun(self, project=project, test_run_id=test_run_id,
                                                             test_case_id_azure=test_case_id_azure,
                                                             name_testcase=name_testcase, status_ct=status,
                                                             cont_iteration=cont_iteration, step_failed=step_failed)
                        workitem_status = 'Design'

                    elif status == "Aborted" and save_evidence:
                        Func.Main.verifyBrowser(self)
                        comments = Aux.otherConfigs['DownloadingFileIE']['Msg']
                        status_ct_automation = 'Planned'
                        workitem_status = 'Design'

                    elif save_evidence:
                        comments, full_name_run_test, actual_comment = \
                            Azure.AzureConnection.getInfoRun(self, project=project, test_run_id=test_run_id,
                                                             test_case_id_azure=test_case_id_azure,
                                                             name_testcase=name_testcase, status_ct=status,
                                                             cont_iteration=cont_iteration, step_failed=step_failed)
                        workitem_status = 'Closed'

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
                    if save_evidence:
                        # Update the test case inside the Run.
                        Azure.AzureConnection.updateTestCaseRun(self, project=project, test_run_id=test_run_id,
                                                                test_case_id_azure=test_case_id_azure, status_ct=status,
                                                                duration=duration, comments=comments)
                        if Aux.otherConfigs['Interface']:
                            screenRunning.write_message_on_console(
                                f"[b][color={AppAutomation.KivyTextColor.yellow.defaultvalue}]"
                                f"{Aux.otherConfigs['GeneratingEvidence']['Msg']}[/color]"
                                f"[/b]")
                        print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['GeneratingEvidence']['Msg']}"
                              f"{Aux.Textcolor.END}\n")

                    # If aborted do not create evidences.
                    if save_evidence and status != 'Aborted':
                        # Create an EST file.
                        word_path = Aux.directories["ESTFile"] + ' ' + Aux.otherConfigs["Language"] + '.docx'

                        est = Aux.Main.wordAddSteps(self, test_run_id=test_run_id, test_case_id=test_case_id,
                                                    name_testcase=name_testcase + " - ITERATION " + str(cont_iteration),
                                                    summary=summary, word_path=word_path, test_set_path=test_set_path,
                                                    list_steps=list_steps[step_initial:step_final],
                                                    step_failed=step_failed, comments=actual_comment,
                                                    full_name_run_evidence=full_name_run_evidence,
                                                    full_name_run_test=full_name_run_test,
                                                    take_picture_status=take_picture_status,
                                                    completed_date=str(Aux.datetime.datetime.now().
                                                                       strftime("%d/%m/%Y %H:%M")))
                        pdf = Aux.Main.wordToPDF(self, path=est)

                        if est is None:
                            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorEST"],
                                             value1=name_testcase + " - ITERATION " + str(cont_iteration))

                        if pdf is None:
                            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorConvertPDF"],
                                             value1=name_testcase + " - ITERATION " + str(cont_iteration))

                        if (est is not None) and (pdf is not None):
                            # Add the evidence to the Run and the Test case.
                            Aux.Main.addLogs(self, message="General", value=Aux.logs["ConvertPDF"],
                                             value1=name_testcase + " - ITERATION " + str(cont_iteration))
                            Azure.AzureConnection.SaveEvidenceRun(self, project=project, test_run_id=test_run_id,
                                                                  test_case_id_azure=test_case_id_azure,
                                                                  evidence_folder=Aux.directories["EvidenceFolder"],
                                                                  name_testcase=Aux.otherConfigs["ETSName"] + str(
                                                                      test_case_id) + " - " + name_testcase,
                                                                  cont_iteration=cont_iteration)
                            Azure.AzureConnection.SaveEvidenceTestCase(self, project=project, test_case_id=test_case_id,
                                                                       evidence_folder=Aux.directories["EvidenceFolder"]
                                                                       , name_testcase=Aux.otherConfigs["ETSName"] +
                                                                       str(test_case_id) + " - " + name_testcase,
                                                                       cont_iteration=cont_iteration)

                        # Clear the evidences prints.
                        Aux.Main.deleteFiles(self, path_log=test_set_path, extension="png")

                    # If there is file to download update to Azure.
                    if change_download_config and save_evidence and not status == "Aborted":
                        file_name = Aux.os.listdir(Aux.directories["DownloadFolder"])
                        if file_name:  # Check if the file was download.
                            Azure.AzureConnection.CheckDownloadFile(self, project=project, test_case_id=str(test_case_id),
                                                                    file_name=file_name[0], compare=False,
                                                                    evidence_folder=Aux.directories["DownloadFolder"])
                        else:
                            status_ct_automation = "Planned"
                            workitem_status = "Design"
                            status = "Failed"
                            comments = Aux.logs["ErrorDownload"]["Msg"]
                            raise Exception
                        Aux.Main.deleteFiles(self, path_log=Aux.directories["DownloadFolder"], extension='*')

                    # Variables.
                    step_initial = step_final
                    step_final = step_final + cont_steps

                    if save_evidence:
                        # Update the status automation and test case status inside Test Case.
                        Azure.AzureConnection.UpdateStatusAutomated(self, project=project, test_case_id=test_case_id,
                                                                    workitem_status=workitem_status,
                                                                    automation_status=status_ct_automation)

                test_case_id_azure += 1

            # Inform the test case percentage already executed (100%).
            Aux.Main.percentage(self, actual=len(test_case_id_list), total=len(test_case_id_list))

        except Exception as ex:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorStartAutomation']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorStartAutomation']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorStartAutomation']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorStartAutomation"], value1=str(ex))

            Azure.AzureConnection.UpdateStatusAutomated(self, project=project, test_case_id=test_case_id,
                                                        workitem_status=workitem_status,
                                                        automation_status=status_ct_automation)
            Azure.AzureConnection.updateTestCaseRun(self, project=project, test_run_id=test_run_id, status_ct=status,
                                                    test_case_id_azure=test_case_id_azure, duration=duration,
                                                    comments=comments)
            Azure.AzureConnection.updateRun(self, project=project, test_run_id=test_run_id, status_run="Aborted")

        # Update the Run status.
        finally:
            if Aux.otherConfigs["ReplaceEvidence"]:
                Azure.AzureConnection.updateRun(self, project=project, test_run_id=test_run_id, status_run="Completed")
            Aux.Main.addLogs(self, message="EndExecution")

    # Execute the test case steps.
    def executeStepByStep(self, **kwargs):

        # kwargs variables.
        list_steps = kwargs.get('list_steps')
        step_initial = kwargs.get('step_initial', None)
        step_final = kwargs.get('step_final', None)
        change_download_config = kwargs.get('change_download_config', False)
        cont_iteration = kwargs.get('cont_iteration', 0)
        test_set_path = kwargs.get('test_set_path')
        enable_cookie = kwargs.get('enable_cookie')

        # Variables.
        element = None
        step_order = 1
        step_failed = None
        status_steps = []
        save_evidence= True
        take_picture_status = None

        # Access Screen Running.
        if Aux.otherConfigs['Interface']:
            import AppAutomation
            screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

        try:
            for step in list_steps[step_initial:step_final]:
                # Initialize the variables.
                value1 = None
                value2 = None

                verb = step.split()[0]
                # Don't execute the step with 'No' / 'Não'.
                if verb in ('"No"', '"Não"', '"No"'.replace('"', ''), '"Não"'.replace('"', '')):
                    verb = 'NoExecute'
                    pattern = Aux.regex.compile('(?:"Não"|"No")')
                    step = Aux.regex.sub(pattern, '', step).strip()
                else:
                    pattern = Aux.regex.compile('(?:"Sim"|"Si"|"Yes")')
                    step = Aux.regex.sub(pattern, '', step).strip()
                    verb = step.split()[0]

                if step.count('"') >= 3:  # More than one parameter.
                    value1 = step.split('"')[1]
                    value2 = step.split('"')[3]
                elif step.count('"') == 2:  # One parameter.
                    value1 = step.split('"')[1]

                if Aux.otherConfigs['Interface']:
                    screenRunning.write_message_on_console(f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                                                           f"{Aux.otherConfigs['Step']['Msg']}: {step}[/color]")
                    screenRunning.write_message_on_console(f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                                                           f"{Aux.otherConfigs['Verb']['Msg']}: {verb}[/color]")
                    screenRunning.write_message_on_console(f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                                                           f"PARAM 1: {value1}[/color]")
                    screenRunning.write_message_on_console(f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]"
                                                           f"PARAM 2: {value2}[/color]")
                    screenRunning.write_message_on_console(f"[color={AppAutomation.KivyTextColor.white.defaultvalue}]" +
                                                           f"{('=+=' * 20)}" + "[/color]")

                print(f"{Aux.otherConfigs['Step']['Msg']}: {step}")
                print(f"{Aux.otherConfigs['Verb']['Msg']}: {verb}")
                print(f"PARAM 1: {value1}")
                print(f"PARAM 2: {value2}")
                print(f"=+=" * 30)

                # Execute the test step.
                if value1 is None:
                    status_step = eval(Aux.verbs[verb]['Function'])(self)
                else:
                    status_step = eval(Aux.verbs[verb]['Function'])(self, value1=value1, value2=value2,
                                                                    step=step,cont_iteration=cont_iteration,
                                                                    change_download_config=change_download_config,
                                                                    enable_cookie=enable_cookie, list_steps=list_steps)

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
                    imagename = Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)

                    take_picture_status = Func.Main.takePicture(self, test_set_path=test_set_path,
                                                                image_name=imagename, verb=verb, list_steps=list_steps)

                    if not take_picture_status:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorScreenshot"], value1=step)

                step_order += 1

            # Set the test case status.
            status_counter = Aux.Counter(status_steps)
            if status_counter['Failed'] != 0:
                status_ct = "Failed"
            else:
                status_ct = "Passed"

            return status_ct, step_failed, save_evidence, take_picture_status

        except Exception as ex:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defaultvalue}]"
                                                       f"{Aux.logs['ErrorExecuteStepByStep']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorExecuteStepByStep']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorExecuteStepByStep']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorExecuteStepByStep"], value1=str(ex))
