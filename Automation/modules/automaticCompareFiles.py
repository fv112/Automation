import common_libs as Lib


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

            # Start the automation.
            project, test_case_id_list, test_run_id = (
                Lib.Con.startRun(self, project=project_id, id_test_plan=id_test_plan,
                                 id_test_suit=id_test_suit, test_case_id_list_all=test_case_id_list_all))

            for id_testcase in test_case_id_list:
                test_name, id_testcase, list_files_baseline, list_files_new = \
                    Lib.Con.SaveDownloadFileLocally(self, project=project, id_testcase=id_testcase)

                # Compare 'Baseline' file to 'New' file -> Iteration counts.
                for _ in range(0, len(list_files_baseline)):

                    # Generate a hash for the actual baseline file.
                    path_file = Lib.Aux.os.path.join(Lib.Aux.directories['CompareDownloadFolder'], test_name,
                                                 list_files_baseline[0])
                    baseline_actual_hash = Lib.Aux.Main.generateHash(self, path_file=path_file)

                    Lib.Aux.Main.compareBeyondCompare(self, test_name=test_name, baseline=list_files_baseline[0],
                                                  new_file=list_files_new[0])

                    # Generate a hash for the new baseline file.
                    new_actual_hash = Lib.Aux.Main.generateHash(self, path_file=path_file)

                    # Compare hash and update the new baseline to GitLab.
                    if baseline_actual_hash != new_actual_hash:
                        Lib.Con.CheckDownloadFile(self, project=project, test_case_id=str(id_testcase),
                                                  evidence_folder=Lib.Aux.os.path.join(
                                                      Lib.Aux.directories['CompareDownloadFolder'], test_name)
                                                  , file_name=list_files_baseline[0],
                                                  download_file_name=list_files_baseline[0], compare=True)

                    list_files_baseline.pop(0)
                    list_files_new.pop(0)

            # Delete the Compare_Download_Temp directory.
            Lib.Aux.Main.deleteDirectory(self, directory=Lib.Aux.directories['DownloadFolderTemp'])

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorMain']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.addLogs(self, message="General", value=Lib.Aux.logs["ErrorMain"], value1=str(ex))

        finally:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['MsgFinishedCompare']['Msg']}{Lib.Aux.Textcolor.END}")
