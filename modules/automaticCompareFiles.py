import modules.automationAux as Aux
import modules.azureConnection as Azure


class Main:

    def __init__(self):
        pass

    def main(self, **kwargs):
        try:
            # Kwargs variables.
            project_id = kwargs.get('project_id')
            id_test_plan = kwargs.get('id_test_plan')
            id_test_suit = kwargs.get('id_test_suit')
            test_case_id_list_all = kwargs.get('test_case_id_list_all')

            list_files_baseline = []    # 'Baseline' files - In this order.
            list_files_new = []         # 'New' files - In this order.

            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                import AppAutomation
                screenRunning = AppAutomation.AppAutomation.get_running_app().root.get_screen('Running')

            # Start the automation.
            project, test_case_id_list, test_run_id = \
                Azure.AzureConnection.startRun(self, project=project_id, id_test_plan=id_test_plan,
                                               id_test_suit=id_test_suit, test_case_id_list_all=test_case_id_list_all)

            for id_testcase in test_case_id_list:
                test_name, id_testcase, list_files_baseline, list_files_new = \
                    Azure.AzureConnection.SaveDownloadFileLocally(self, project=project, id_testcase=id_testcase)

                # Compare 'Baseline' file to 'New' file -> Iteration counts.
                for _ in range(0, len(list_files_baseline)):

                    # Generate a hash for the actual baseline file.
                    path_file = Aux.os.path.join(Aux.directories['CompareDownloadFolder'], test_name,
                                                 list_files_baseline[0])
                    baseline_actual_hash = Aux.Main.generateHash(self, path_file=path_file)

                    Aux.Main.compareBeyondCompare(self, test_name=test_name, baseline=list_files_baseline[0],
                                                  new_file=list_files_new[0])

                    # Generate a hash for the new baseline file.
                    new_actual_hash = Aux.Main.generateHash(self, path_file=path_file)

                    # Compare hash and update the new baseline to Azure.
                    if baseline_actual_hash != new_actual_hash:
                        Azure.AzureConnection.CheckDownloadFile(self, project=project, test_case_id=str(id_testcase),
                                                                evidence_folder=Aux.os.path.join(
                                                                    Aux.directories['CompareDownloadFolder'], test_name)
                                                                , file_name=list_files_baseline[0],
                                                                download_file_name=list_files_baseline[0], compare=True)

                    list_files_baseline.pop(0)
                    list_files_new.pop(0)

            # Delete the Compare_Download_Temp directory.
            Aux.Main.deleteDirectory(self, directory=Aux.directories['DownloadFolderTemp'])

        except Exception as ex:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.red.defautlvalue}]"
                                                       f"{Aux.logs['ErrorMain']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorMain']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorMain']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorMain"], value1=str(ex))
            ###exit(1)

        finally:
            # Access Screen Running.
            if Aux.otherConfigs['Interface']:
                screenRunning.write_message_on_console(f"[b][color={AppAutomation.KivyTextColor.orange.defaultvalue}]"
                                                       f"{Aux.otherConfigs['MsgFinishedCompare']['Msg']}[/color][/b]")
                Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['MsgFinishedCompare']['Msg'])
                Aux.MDDialogAppTest().show_mddialog()
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['MsgFinishedCompare']['Msg']}{Aux.Textcolor.END}")

