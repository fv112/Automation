import Automation.Automation.modules.automationAux as Aux
import Automation.Automation.modules.GitLabConnection as GitLab

instance = 'kantarware.visualstudio.com/'


class Main:

    def __init__(self):
        pass

    def main(self, **kwargs):
        try:
            # Variables.
            project = kwargs.get('project_id')
            project_name = kwargs.get('project_name') # Only for log.
            test_run_id = kwargs.get('test_run_id')
            id_test_case = kwargs.get('id_test_case')

            # Start generate evidence.
            Main.startGenerateEvidence(self, project=project, project_name=project_name,
                                       test_run_id=test_run_id.strip(), id_test_case=id_test_case)

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorMain']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.addLogs(Aux.logs["ErrorMain"], str(ex))
            ####exit(1)

        finally:
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['MsgFinishedEvidence']['Msg']}{Aux.Textcolor.END}")

    # Generate de manual evidence.
    def startGenerateEvidence(self, **kwargs):

        # kwargs arguments.
        project = kwargs.get('project')
        project_name = kwargs.get('project_name') # Only for log.
        test_run_id = kwargs.get('test_run_id')
        id_test_case = kwargs.get('id_test_case')

        status_ct_automation = 'Planned'
        workitem_status = None

        try:
            # Complete name (if it is using the VPN).
            full_name_run_evidence = (Aux.win32net.NetUserGetInfo(Aux.win32net.NetGetAnyDCName(),
                                                                  Aux.win32api.GetUserName(), 2))['full_name']
        except:
            # Windows login (if it is not using the VPN).
            full_name_run_evidence = Aux.Main.get_display_name(self)

        try:
            comment = None
            testset_path_manual = Aux.directories["EvidenceFolderManual"]
            Aux.Main.deleteDirectory(self, directory=testset_path_manual)
            Aux.Main.createDirectory(self, path_folder=testset_path_manual)

            # Execute the action to get the manual evidences.
            test_case_id_list, n_iterations_list, id_azure_list, n_test_case_list, failed_info_dict, \
            completed_date_list, full_name_run_test = (
                GitLab.GitLabConnection.manualEvidences(self, project=project, test_run_id=test_run_id,
                                                       id_test_case=id_test_case))

            for test_case_id in test_case_id_list:
                list_steps, name_testcase, summary, cont_steps, change_download_config = \
                    GitLab.GitLabConnection.startSteps(self, project=project, test_case_id=test_case_id)

                step_initial = 0
                n_iterations = n_iterations_list.pop(0)  # Get the number of the iterations for the test order.
                test_case_id_azure = id_azure_list.pop(0)
                n_test_case = n_test_case_list.pop(0)
                completed_date = completed_date_list.pop(0)

                # Create the TestSet folder.
                test_set_path = Aux.os.path.join(Aux.directories["EvidenceFolder"], Aux.otherConfigs["ETSName"] +
                                                 str(test_case_id) + " - " + name_testcase)

                if Aux.os.path.exists(test_set_path):
                    Aux.shutil.rmtree(test_set_path)
                Aux.os.makedirs(test_set_path)
                Aux.Main.addLogs(self, message="General", value=Aux.logs["EvidenceFolder"])
                Aux.Main.createDirectory(self, path_folder=test_set_path)

                print(f"{Aux.Textcolor.WARNING}{Aux.otherConfigs['GeneratingEvidence']['Msg']}"
                      f"{Aux.Textcolor.END}\n")

                # Create an EST file.
                word_path = Aux.os.path.join(Aux.os.getcwd(), Aux.directories["ESTFile"] + ' ' +
                                             Aux.otherConfigs["Language"] + '.docx')

                # Create evidence step by step per Iteration.
                for n_iteration in range(0, n_iterations):
                    n_print = 1
                    step_failed = 0

                    Aux.Main.addLogs(self, message="NewSession", value="\nID: " + str(test_case_id) + " - TEST CASE: " +
                                     name_testcase + " - ITERATION: " + str(n_iteration + 1) +
                                    "\nPROJECT: " + project_name + " - RUN ID: " + test_run_id + "\n")

                    # Verify status failed.
                    if failed_info_dict[test_case_id].__len__() != 0:
                        if failed_info_dict[test_case_id][n_iteration + 1].__len__() != 0:
                            step_failed = failed_info_dict[test_case_id][n_iteration + 1]['Step']
                            comment = failed_info_dict[test_case_id][n_iteration + 1]['Comment']
                            step_final = step_failed
                        else:
                            step_final = cont_steps
                    else:
                        step_final = cont_steps

                    # Move the prints to the correct folder and rename the evidences - Order by older first.
                    filenames = Aux.os.listdir(Aux.directories["EvidenceFolderManual"])
                    for filename in filenames:
                        if n_print > cont_steps: break
                        if (filename.endswith("png")) and \
                                (("CT" + str(n_test_case).zfill(2) + "-IT" + str(n_iteration + 1).zfill(2)) in
                                 filename):

                            file_newname = 'Screenshot_' + str(n_print).zfill(2) + '.png'

                            # Rename the prints and move to the correct Test Case folder.
                            Aux.os.rename(Aux.os.path.join(testset_path_manual, filename),
                                          Aux.os.path.join(testset_path_manual, file_newname))
                            Aux.shutil.move(Aux.os.path.join(testset_path_manual, file_newname), test_set_path)
                        n_print += 1
                    n_print = 0

                    est = Aux.Main.wordAddSteps(self, test_run_id=test_run_id, test_case_id=test_case_id,
                                                name_testcase=name_testcase + " - ITERATION " + str(n_iteration + 1),
                                                summary=summary, word_path=word_path, test_set_path=test_set_path,
                                                list_steps=list_steps[0:step_final],
                                                completed_date=completed_date, step_failed=step_failed,
                                                comment=comment, full_name_run_evidence=full_name_run_evidence,
                                                full_name_run_test=full_name_run_test)
                    if est is None:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorEST"],
                                         value1=name_testcase + " - ITERATION " + str(n_iteration + 1))

                        workitem_status = "Design"

                    pdf = Aux.Main.wordToPDF(self, path=est)
                    if pdf is None:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorConvertPDF"],
                                         value1=name_testcase + " - ITERATION " + str(n_iteration + 1))

                        workitem_status = "Design"

                    if (est is not None) and (pdf is not None):
                        # Add the evidence to the Run and the Test case.
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ConvertPDF"],
                                         value1=name_testcase + " - ITERATION " + str(n_iteration + 1))
                        GitLab.AzureConnection.SaveEvidenceRun(self, project=project, test_run_id=test_run_id,
                                                              test_case_id_azure=test_case_id_azure,
                                                              evidence_folder=Aux.directories["EvidenceFolder"],
                                                              name_testcase=Aux.otherConfigs["ETSName"] +
                                                              str(test_case_id) + " - " + name_testcase,
                                                              cont_iteration=n_iteration + 1)
                        GitLab.AzureConnection.SaveEvidenceTestCase(self, project=project, test_case_id=test_case_id,
                                                                   evidence_folder=Aux.directories["EvidenceFolder"],
                                                                   name_testcase=Aux.otherConfigs["ETSName"] +
                                                                   str(test_case_id) + " - " + name_testcase,
                                                                   cont_iteration=n_iteration + 1)

                        workitem_status = "Closed"

                        # Remove the items from the before iteration.
                        del list_steps[0: step_final]

                    # Clear the evidences prints.
                    Aux.Main.deleteFiles(self, file_path=test_set_path, extension="png")

                n_test_case += 1

            Aux.shutil.rmtree(testset_path_manual)

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorStartGenerateEvidence']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorStartGenerateEvidence"], value1=str(ex))
            ####exit(1)

        finally:
            # Update the status automation and test case status inside Test Case.
            GitLab.AzureConnection.UpdateStatusAutomated(self, project=project, test_case_id=test_case_id,
                                                        workitem_status=workitem_status,
                                                        automation_status=status_ct_automation)
