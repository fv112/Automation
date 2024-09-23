import common_libs as Lib

class Main:

    def __init__(self):
        pass

    def main(self, **kwargs):
        try:
            # Variables.
            project = kwargs.get('project_id')
            project_name = kwargs.get('project_name')  # Only for log.
            test_run_id = kwargs.get('test_run_id')
            id_test_case = kwargs.get('id_test_case')

            # Start generate evidence.
            Main.startGenerateEvidence(self, project=project, project_name=project_name,
                                       test_run_id=test_run_id.strip(), id_test_case=id_test_case)

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorMain']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.addLogs(Lib.Aux.logs["ErrorMain"], str(ex))
            ####exit(1)

        finally:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.otherConfigs['MsgFinishedEvidence']['Msg']}{Lib.Aux.Textcolor.END}")

    #Generate de manual evidence.
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
            full_name_run_evidence = (Lib.Aux.win32net.NetUserGetInfo(Lib.Aux.win32net.NetGetAnyDCName(),
                                                                  Lib.Aux.win32api.GetUserName(), 2))['full_name']
        except:
            # Windows login (if it is not using the VPN).
            full_name_run_evidence = Lib.Aux.Main.get_display_name(self)

        try:
            comment = None
            testset_path_manual = Lib.Aux.directories["EvidenceFolderManual"]
            Lib.Aux.Main.delete_directory(self, directory=testset_path_manual)
            Lib.Aux.Main.create_directory(self, path=testset_path_manual)

            # Execute the action to get the manual evidences.
            test_case_id_list, n_iterations_list, id_azure_list, n_test_case_list, failed_info_dict, \
            completed_date_list, full_name_run_test = (
                GitLab.Connections.manualEvidences(self, project=project, test_run_id=test_run_id,
                                                   id_test_case=id_test_case))

            for test_case_id in test_case_id_list:
                list_steps, name_testcase, summary, cont_steps, change_download_config = \
                    GitLab.Connections.start_steps(self, project=project, test_case_id=test_case_id)

                step_initial = 0
                n_iterations = n_iterations_list.pop(0)  # Get the number of the iterations for the test order.
                test_case_id_azure = id_azure_list.pop(0)
                n_test_case = n_test_case_list.pop(0)
                completed_date = completed_date_list.pop(0)

                # Create the TestSet folder.
                test_set_path = Lib.Aux.os.path.join(Lib.Aux.directories["EvidenceFolder"], Lib.Aux.otherConfigs["ETSName"] +
                                                 str(test_case_id) + " - " + name_testcase)

                if Lib.Aux.os.path.exists(test_set_path):
                    Lib.Aux.shutil.rmtree(test_set_path)
                Lib.Aux.os.makedirs(test_set_path)
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["EvidenceFolder"])
                Lib.Aux.Main.create_directory(self, path=test_set_path)

                print(f"{Lib.Aux.Textcolor.WARNING}{Lib.Aux.otherConfigs['GeneratingEvidence']['Msg']}"
                      f"{Lib.Aux.Textcolor.END}\n")

                # Create an EST file.
                word_path = Lib.Aux.os.path.join(Lib.Aux.os.getcwd(), Lib.Aux.directories["ESTFile"] + ' ' +
                                             Lib.Aux.otherConfigs["Language"] + '.docx')

                # Create evidence step by step per Iteration.
                for n_iteration in range(0, n_iterations):
                    n_print = 1
                    step_failed = 0

                    Lib.Aux.Main.add_logs(message="NewSession", value="\nID: " + str(test_case_id) + " - TEST CASE: " +
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
                    filenames = Lib.Aux.os.listdir(Lib.Aux.directories["EvidenceFolderManual"])
                    for filename in filenames:
                        if n_print > cont_steps: break
                        if (filename.endswith("png")) and \
                                (("CT" + str(n_test_case).zfill(2) + "-IT" + str(n_iteration + 1).zfill(2)) in
                                 filename):

                            file_newname = 'Screenshot_' + str(n_print).zfill(2) + '.png'

                            # Rename the prints and move to the correct Test Case folder.
                            Lib.Aux.os.rename(Lib.Aux.os.path.join(testset_path_manual, filename),
                                          Lib.Aux.os.path.join(testset_path_manual, file_newname))
                            Lib.Aux.shutil.move(Lib.Aux.os.path.join(testset_path_manual, file_newname), test_set_path)
                        n_print += 1
                    n_print = 0

                    est = Lib.Aux.Main.word_add_steps(self, test_run_id=test_run_id, test_case_id=test_case_id,
                                                      name_testcase=name_testcase + " - ITERATION " + str(n_iteration + 1),
                                                      summary=summary, word_path=word_path, test_set_path=test_set_path,
                                                      list_steps=list_steps[0:step_final],
                                                      completed_date=completed_date, step_failed=step_failed,
                                                      comment=comment, full_name_run_evidence=full_name_run_evidence,
                                                      full_name_run_test=full_name_run_test)
                    if est is None:
                        Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs["ErrorEST"],
                                              value1=name_testcase + " - ITERATION " + str(n_iteration + 1))

                        workitem_status = "Design"

                    pdf = Lib.Aux.Main.word_to_pdf(self, path=est)
                    if pdf is None:
                        Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs["ErrorConvertPDF"],
                                              value1=name_testcase + " - ITERATION " + str(n_iteration + 1))

                        workitem_status = "Design"

                    if (est is not None) and (pdf is not None):
                        # Add the evidence to the Run and the Test case.
                        Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs["ConvertPDF"],
                                              value1=name_testcase + " - ITERATION " + str(n_iteration + 1))
                        self.connections.SaveEvidenceRun(self, project=project, test_run_id=test_run_id,
                                                              test_case_id_azure=test_case_id_azure,
                                                              evidence_folder=Lib.Aux.directories["EvidenceFolder"],
                                                              name_testcase=Lib.Aux.otherConfigs["ETSName"] +
                                                              str(test_case_id) + " - " + name_testcase,
                                                              cont_iteration=n_iteration + 1)
                        self.connections.SaveEvidenceTestCase(self, project=project, test_case_id=test_case_id,
                                                                   evidence_folder=Lib.Aux.directories["EvidenceFolder"],
                                                                   name_testcase=Lib.Aux.otherConfigs["ETSName"] +
                                                                   str(test_case_id) + " - " + name_testcase,
                                                                   cont_iteration=n_iteration + 1)

                        workitem_status = "Closed"

                        # Remove the items from the before iteration.
                        del list_steps[0: step_final]

                    # Clear the evidences prints.
                    Lib.Aux.Main.delete_files(self, file_path=test_set_path, extension="png")

                n_test_case += 1

            Lib.Aux.shutil.rmtree(testset_path_manual)

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorStartGenerateEvidence']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.add_logs(self, message="General", value=Lib.Aux.logs["ErrorStartGenerateEvidence"], value1=str(ex))
            ####exit(1)

        finally:
            # Update the status automation and test case status inside Test Case.
            GitLab.AzureConnection.UpdateStatusAutomated(self, project=project, test_case_id=test_case_id,
                                                        workitem_status=workitem_status,
                                                        automation_status=status_ct_automation)

