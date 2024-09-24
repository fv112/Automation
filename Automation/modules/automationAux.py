import common_libs as Lib

verbs = None
logs = None
directories = None


# Colored the text.
class Textcolor:
    BLUE = '\033[1;34;47m'  # Blue
    HIGHLIGHT = '\033[7m'   # Highlight
    GREEN = '\033[32m'      # Green
    WARNING = '\033[93m'    # Yellow
    FAIL = '\033[91m'       # Red
    END = '\033[00m'        # End of line
    BOLD = '\033[1m'        # Bold
    UNDERLINE = '\033[4m'   # Underline


class Main:

    def __init__(self):
        pass

    # Validate test case name.
    def validate_test_name(self, **kwargs):

        # kwargs variables.
        name_testcase = kwargs.get("name_testcase")

        validation_status = None

        try:
            validation = Lib.regex.match(r'.*[\.@!#$%^&*<>?\\\/|\"}{:].*', name_testcase)
            if validation:
                print(f"{Textcolor.FAIL}{logs['ErrorSpecialCharacter']['Msg']} "
                      f"{otherConfigs['InvalidCharacter']} {Textcolor.END}")
                Main.add_logs(message="General", value=logs["ErrorSpecialCharacter"],
                              value1=f"{otherConfigs['InvalidCharacter']}")
                validation_status = True

            if len(name_testcase) >= 104:
                print(f"{Textcolor.FAIL}{logs['ErrorSizeName']['Msg']}{Textcolor.END}")
                Main.add_logs(message="General", value=logs["ErrorSizeName"])
                validation_status = True

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorTestCaseValidation']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorTestCaseValidation"], value1=str(ex))
            validation_status = False

        finally:
            return validation_status

    # Called to clean the file 'Tokens.txt'
    def clean_token_file(self):
        name = Lib.os.getlogin()
        file_path = Lib.os.path.join(directories["TokensFile"], 'Tokens.txt')
        file = open(file_path, 'w')
        file.close()

    # Get the Windows full name.
    def get_display_name(self):
        get_user_name_ex = Lib.ctypes.windll.secur32.GetUserNameExW
        name_display = 3

        size = Lib.ctypes.pointer(Lib.ctypes.c_ulong(0))
        get_user_name_ex(name_display, None, size)

        name_buffer = Lib.ctypes.create_unicode_buffer(size.contents.value)
        get_user_name_ex(name_display, name_buffer, size)

        return name_buffer.value

    # Set language.
    def set_language(**kwargs):
        try:
            # kwargs variables.
            language = kwargs.get('language')

            Main.load_configs(language='pt')  # Change to the Portuguese language.

            if language == 'pt_BR':
                print(f"{Textcolor.GREEN}{otherConfigs['NoTranslating']}{Textcolor.END}\n")
            elif language == 'en_US':
                need_translation, new_hash = Main.configure_language(language='en')
                if need_translation:
                    Main.translate_msg(language='en', new_hash=new_hash)  # Translation.
                else:
                    print(f"{Textcolor.GREEN}{otherConfigs['NoTranslating']}{Textcolor.END}\n")
                Main.load_configs(language='en')  # Change to the English language.
            else:  # es
                need_translation, new_hash = Main.configure_language(language='es')
                if need_translation:
                    Main.translate_msg(language='es', new_hash=new_hash)  # Translation.
                else:
                    print(f"{Textcolor.GREEN}{otherConfigs['NoTranslating']}{Textcolor.END}\n")
                Main.load_configs(language='es')  # Change to the Spanish language.

            # Variables.
            otherConfigs['Language'] = language

            Main.add_logs(message="General", value=logs["SetLanguage"])

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorSetLanguage']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="setLanguage", value=logs["ErrorSetLanguage"]['Msg'], value1=str(ex))

    # Ask and save the Token in a file.
    def save_token(**kwargs):
        try:
            # kwargs variables.
            file_path = kwargs.get("file_path")
            name = kwargs.get("name")

            TokenField.show_token_input(TokenField)
            TokenField.invalid_token_msg(TokenField)
            TokenField().run()
            otherConfigs['Token'] = TokenField().token_input_callback()

            print(otherConfigs['InvalidTokenMessage']['Msg'])
            otherConfigs['Token'] = input(otherConfigs['InformTokenPart1']['Msg'] + ' ' +
                                          otherConfigs['InformTokenPart2']['Msg'] + ' ' +
                                          directories['TokenExpiredUrl'] + ': ')

            token_file = open(file_path, 'a')
            token_file.write(str(name) + ',' + otherConfigs['Token'] + ',\n')
            token_file.close()
            Main.add_logs(message="General", value=logs["SaveToken"])

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorSaveToken']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorSaveToken"], value1=str(ex))

    # Create the directories.
    def create_directory(self, **kwargs):

        try:
            # kwargs variables.
            path = kwargs.get("path")

            if not Lib.os.path.exists(path):
                Lib.os.makedirs(path)
                return True
            else:
                # Clear the old logs and evidences (Older than 30 days).
                current_time = Lib.time.time()
                for item in Lib.os.listdir(path):

                    # Delete folders or files.
                    if Lib.os.path.isdir(Lib.os.path.join(directories['TestSetPath'], item)):
                        creation_time = Lib.os.path.getmtime(Lib.os.path.join(path, item))
                        if (current_time - creation_time) // (24 * 3600) >= 30:
                            Lib.shutil.rmtree(Lib.os.path.join(path, item), ignore_errors=True)
                            Main.add_logs(message="General", value=logs["DeleteFolder"],
                                          value1=path, value2=item)
                    else:
                        creation_time = Lib.os.path.getmtime(Lib.os.path.join(path, item))
                        if (current_time - creation_time) // (24 * 3600) >= 30:
                            Lib.os.remove(Lib.os.path.join(path, item))
                            Main.add_logs(message="General", value=logs["DeleteFile"],
                                          value1=Lib.os.path.join(path, item))

                return True

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorCreateDirectory']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorCreateDirectory"], value1=str(ex))

            return False

    # Delete the directories.
    def delete_directory(self, **kwargs):
        try:
            # kwargs variables.
            path_folder = kwargs.get('path_folder')

            if Lib.os.path.exists(path_folder):
                Lib.shutil.rmtree(path_folder)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorDeleteDirectory']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorDeleteDirectory"], value1=str(ex))

    # Add the screenshots in the Word file.
    def word_add_steps(**kwargs):

        try:
            # kwargs arguments.
            test_case_id = kwargs.get('test_case_id')
            name_testcase = kwargs.get('name_testcase')
            word_path = kwargs.get('word_path')
            steps_list = kwargs['steps_list']
            step_failed = int(kwargs.get('step_failed'))
            executed_by = kwargs.get('executed_by')
            completed_date = kwargs.get('completed_date')
            duration = kwargs.get('duration')

            # Variables.
            tag_paragraph = [
                {'pt_BR': 'Evidências dos passos', 'en_US': 'Evidence of the steps', 'es': 'Evidencia de los pasos'}
            ]
            image_path = ""
            path = []

            # Open the document.
            document = Lib.Document(word_path)
            # Search the correct paragraph.
            paragraph = Main.word_seach_text(document=document, text=tag_paragraph[0][otherConfigs['Language']])

            image_resize = True

            if paragraph is None:
                print('\033[31m' + '\n' + logs['ErrorWordFindParagraph']['Msg'] + '\033[0;0m')
                Main.add_logs(message="General", value=logs["ErrorWordFindParagraph"])
                return None

            # Add the info in the file.
            if not Main.word_add_info(document=document, test_case_id=test_case_id,
                                      name_testcase=name_testcase, step_number=len(steps_list), step_failed=step_failed,
                                      completed_date=completed_date, executed_by=executed_by, duration=duration):
                print('\033[31m' + '\n' + logs['ErrorWordSetCTInfo']['Msg'] + '\033[0;0m')
                Main.add_logs(message="General", value=logs["ErrorWordSetCTInfo"])

                return None

            # Read the test case steps and add them in the order.
            for step_order, step in enumerate(steps_list):

                step_order += 1

                verb = step.split()[0]
                # Don't execute the step with No / Não.
                if verb.upper() not in ('"NO"', '"NÃO"', '"NO"'.replace('"', ''),
                                        '"NÃO"'.replace('"', '')):

                    step = Main.replace_password_evidence(step=step)

                    paragraph = document.add_paragraph(
                        otherConfigs["StepName"] + " " + str(step_order) + " - " + step)
                    run_paragraph = paragraph.add_run()

                    if step_failed == step_order:
                        # Add the error message in the document.
                        paragraph = document.add_paragraph(otherConfigs['StepWithBug']['Msg'])
                        run_paragraph = paragraph.runs[0]
                        run_paragraph.font.color.rgb = Lib.RGBColor(*(255, 0, 0))
                        add_evidence = True
                    elif step_failed <= step_order and step_failed != 0:
                        # Add the error message in the document.
                        paragraph = document.add_paragraph(otherConfigs['StepWithPrevBug']['Msg'])
                        run_paragraph = paragraph.runs[0]
                        run_paragraph.font.color.rgb = Lib.RGBColor(*(255, 0, 0))
                        add_evidence = False
                    else:
                        add_evidence = True

                    # Last step or take_picture_status is true.
                    if verb not in ('Fechar', 'Cerrar', 'Close') and otherConfigs['Api_Step'] is False and add_evidence:
                        # Check the image size.
                        image_path = Lib.os.path.join(directories['TestSetPath'], otherConfigs["EvidenceName"] +
                                                      str(step_order).zfill(2) + otherConfigs["EvidenceExtension"])
                        image = Lib.ImageGrab.Image.open(image_path)

                        if image.size[0] <= 1500:
                            image_resize = False

                    if verb not in ('Fechar', 'Cerrar', 'Close') and otherConfigs['Api_Step'] is False:
                        # Resize the image if it is not full screen.
                        run_paragraph.add_break()
                        if image_resize:
                            # Change the print size.
                            run_paragraph.add_picture(image_path, width=eval(otherConfigs["EvidenceWidth"]),
                                                     height=eval(otherConfigs["EvidenceHeight"]))
                        else:
                            run_paragraph.add_picture(image_path, width=Lib.Inches(5))
                    elif otherConfigs['Api_Step'] and add_evidence:
                        api_evidence_step = None
                        api_file_name = (otherConfigs["EvidenceNameApi"] + str(step_order).zfill(2) +
                                         otherConfigs["EvidenceExtensionApi"])
                        api_file = Lib.os.path.join(directories['EvidenceFolder'], Lib.Aux.directories['TestSetPath'],
                                                    api_file_name)

                        with open(api_file, 'r') as api_evidence_file:
                            api_evidence_step = api_evidence_file.readlines()

                            if api_evidence_step.__len__() == 0:
                                paragraph = document.add_paragraph(otherConfigs['Api_NoResponseNeeded']['Msg'])
                                run_paragraph = paragraph.runs[0]
                                run_paragraph.bold = False
                            else:
                                for line in api_evidence_step:
                                    paragraph = document.add_paragraph(line)
                                    run_paragraph = paragraph.runs[0]
                                    run_paragraph.bold = False

                else:
                    paragraph = document.add_paragraph(otherConfigs["StepName"] + " " + str(step_order) + " - "
                                                       + otherConfigs["DisabledStep"]['Msg'])
                    run_paragraph = paragraph.add_run()

            # Save the file.
            if step_failed != 0:
                test_id = '[BUG] - ' + otherConfigs["ETSName"] + str(test_case_id)
            else:
                test_id = otherConfigs["ETSName"] + str(test_case_id)

            path.append(Lib.Aux.directories['TestSetPath'])
            path.append(test_id)
            path.append(str(name_testcase))
            path.append(otherConfigs["ETSExtension"])

            path = Lib.os.path.join(path[0], path[1]) + " - " + path[2] + path[3]
            document.save(path)

            return path

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorWordAddSteps']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorWordAddSteps"], value1=str(ex))

        return None

    # Replace the password in the evidence file.
    def replace_password_evidence(**kwargs):

        try:
            # kwargs variables.
            step = kwargs.get("step")

            if any(word in step.lower() for word in ['senha', 'contraseña', 'password']):
                password_string = Lib.regex.findall(r'"([^"]*)"', step)[1]
                step = step.replace(password_string, '*******')

            return step

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorReplacePasswordEvidence']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorReplacePasswordEvidence"], value1=str(ex))

    # Search the text in the file.
    def word_seach_text(**kwargs):

        try:
            # kwargs variables.
            document = kwargs.get("document")
            text = kwargs.get("text")

            for p in document.paragraphs:
                if p.text == text:
                    return p
        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorWordSearchText']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorWordSearchText"], value1=str(ex))

        return None

    # Add the test case info in the Word file.
    def word_add_info(**kwargs):

        # kwargs arguments.
        document = kwargs.get('document')
        test_case_id = kwargs.get('test_case_id')
        name_testcase = kwargs.get('name_testcase')
        step_number = kwargs.get('step_number')
        executed_by = kwargs.get('executed_by')
        completed_date = kwargs.get('completed_date')
        duration = kwargs.get('duration')
        step_failed = kwargs.get('step_failed')

        try:

            tag_language = [
                {'pt_BR': 'ID do Caso de Teste: ', 'en_US': 'Test Case ID: ', 'es': 'ID del Prueba: '},
                {'pt_BR': 'Caso de Teste: ', 'en_US': 'Test Case: ', 'es': 'Prueba: '},
                {'pt_BR': 'Teste executado por: ', 'en_US': 'Test executed by: ', 'es': 'Prueba realizada por: '},
                {'pt_BR': 'Evidência gerada por: ', 'en_US': 'Evidence generated by: ', 'es': 'Evidencia generada por: '},
                {'pt_BR': 'Data de Execução: ', 'en_US': 'Execution date: ', 'es': 'Fecha de ejecución: '},
                {'pt_BR': 'Total de passos: ', 'en_US': 'Total steps: ', 'es': 'Pasos totales: '},
                {'pt_BR': 'Duração da execução do teste: ', 'en_US': 'Test execution time: ', 'es': 'Tiempo de ejecución de la prueba: '},
                {'pt_BR': 'Falha no passo: ', 'en_US': 'Step failed: ', 'es': 'Paso fallido: '}
            ]

            # Test case GitLab ID.
            control = Main.word_seach_text(document=document, text=tag_language[0][otherConfigs['Language']])
            control.add_run(str(test_case_id)).bold = True

            # Test case name.
            control = Main.word_seach_text(document=document, text=tag_language[1][otherConfigs['Language']])
            control.add_run(name_testcase).bold = True

            # Executed by.
            control = Main.word_seach_text(document=document, text=tag_language[2][otherConfigs['Language']])
            control.add_run(executed_by).bold = True

            # Evidence generate by.
            control = Main.word_seach_text(document=document, text=tag_language[3][otherConfigs['Language']])
            control.add_run(executed_by).bold = True

            # Execution date.
            control = Main.word_seach_text(document=document, text=tag_language[4][otherConfigs['Language']])
            control.add_run(str(completed_date)).bold = True

            # Total steps.
            control = Main.word_seach_text(document=document, text=tag_language[5][otherConfigs['Language']])
            control.add_run(str(step_number)).bold = True

            # Test execution duration.
            control = Main.word_seach_text(document=document, text=tag_language[6][otherConfigs['Language']])
            control.add_run(duration).bold = True

            # Step failed.
            control = Main.word_seach_text(document=document, text=tag_language[7][otherConfigs['Language']])
            if step_failed != 0:
                control.add_run(str(step_failed)).bold = True
            else:
                control.add_run(otherConfigs['NoStepFailed']['Msg']).bold = True

            return True

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorWordAddInfo']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorWordAddInfo"], value1=str(ex))

            return False

    # Function to convert docx to pdf.
    def word_to_pdf(**kwargs):

        try:
            # kwargs variables.
            path = kwargs.get("path")

            word_format_pdf = 17

            # Initialize.
            Lib.pythoncom.CoInitialize()

            word = Lib.win.Dispatch('Word.Application')
            document = word.Documents.Open(path)

            pdf_path = path.replace("docx", "pdf")
            document.SaveAs(pdf_path, FileFormat=word_format_pdf)
            document.Close()

            word.Quit()

            return pdf_path

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorWordToPdf']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorWordToPdf"], value1=str(ex))
            return None

    # Delete files.
    def delete_files(**kwargs):

        try:
            # kwargs arguments.
            folder_path = kwargs.get('folder_path', '')
            extension = kwargs.get('extension')
            exact_file = kwargs.get('exact_file')

            # Delete all the files in a directory with the specific extension OR all if the extension is '*'.
            if Lib.os.path.exists(folder_path):
                files = Lib.os.listdir(folder_path)

                for item in files:
                    if item.endswith(extension) or extension == '*':
                        Lib.os.remove(Lib.os.path.join(folder_path, item))

            elif exact_file is not None:
                Lib.os.remove(exact_file)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorDeleteFiles']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorDeleteFiles"], value1=str(ex))

    # Add the log in the file.
    def add_logs(**kwargs):

        try:
            # kwargs variables.
            message = kwargs.get("message")
            value = kwargs.get("value")
            value1 = kwargs.get("value1")
            value2 = kwargs.get("value2")

            datetime_log: str = Lib.datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

            # Get the hostname.
            otherConfigs["ComputerName"] = Lib.socket.gethostname()
            hostname = otherConfigs["ComputerName"]
            # Get the datetime.
            date_log = str(Lib.datetime.datetime.now().strftime("%d.%m.%Y"))
            # Set the file name.
            path = Lib.os.path.join(directories["LogFolder"], hostname + " - " + date_log + ".log")

            if not Lib.os.path.isdir(directories["LogFolder"]):
                Main.create_directory(self, path=directories["LogFolder"])

            # Append the log file.
            with open(path, 'a+', encoding='utf-8') as log_file:
                if message == 'NewConfig':  # Set the first line.
                    log_file.write("\n " + "*" * 61 + datetime_log + "*" * 61 + "\n")
                    log_file.write("\nLOAD INFORMATION'S FROM GITLAB\n")
                elif message == 'NewSession':
                    log_file.write(str(value) + "\n")  # Test case name.
                    log_file.write("")
                elif message == 'General':
                    type_log = value['Type']
                    message_log = value['Msg']
                    local_log = value['Where']

                    # Alignment.
                    type_log = "{:<9}".format(type_log)

                    # Change the error origin if informed.
                    if value1 is not None and value2 is None:
                        msg_format = "{:<15}"
                        log_file.write(datetime_log + " - " + type_log + " - " + msg_format.format(message_log) + " - "
                                       + value1 + "\n")
                    elif value1 is not None and value2 is not None:
                        log_file.write(datetime_log + " - " + type_log + " - '" + value1 + "' " + message_log + " '" +
                                       value2 + "' - " + local_log + "\n")
                    else:
                        log_file.write(datetime_log + " - " + type_log + " - " + message_log + " - " + local_log + "\n")

                elif message == 'EndExecution':
                    log_file.write("\n " + "*" * 138 + "\n")
                else:
                    log_file.write(datetime_log + " - Log       - " + value + " " + " - " + str(value1) + "\n")

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorAddLog']['Msg']}{Textcolor.END}", str(ex))
            Main.add_logs(message="General", value=logs["ErrorAddLog"]['Msg'], value1=str(ex))

    # Remove the HTML from the string.
    def remove_html(**kwargs):

        try:
            # kwargs variables.
            value = kwargs.get("value")

            pattern = Lib.regex.compile('<.*?>')
            value = Lib.regex.sub(pattern, '', value).strip()

            value = value.replace('&nbsp;', ' ')
            value = value.replace('&lt;', '<')
            value = value.replace('&gt;', '>')

            return value

        except Exception as ex:

            print(f"{Textcolor.FAIL}{logs['ErrorRemoveHtml']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorRemoveHtml"]['Msg'], value1=str(ex))

    # Translate the messages.
    def translate_msg(**kwargs):
        try:
            # kwargs arguments.
            language = kwargs.get('language')
            new_hash = kwargs.get('new_hash')

            # Paths
            path_origin_yml = Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'configs', 'dictionary-pt.yml')
            path_translated_yml = Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'configs', 'dictionary-' +
                                                   language + '.yml')

            regex_pattern = Lib.regex.compile('(.*?,)(.*?,)(.*)')
            tag = 'Msg:'
            dots = ""

            if Lib.os.path.isfile(path_translated_yml):
                Main.delete_files(exact_file=path_translated_yml)

            with open(path_origin_yml, 'r') as yml_file:
                # print(f'{Textcolor.BLUE}{otherConfigs['WaitTranslate']['Msg']}{Textcolor.END}')
                lines = yml_file.readlines()
                for line in lines:
                    if tag in line:
                        with open(path_translated_yml, 'a', encoding='utf-8') as yml_new_file:
                            group_type = Lib.regex.match(regex_pattern, line).group(1)
                            group_msg = Lib.regex.match(regex_pattern, line).group(2)
                            msg_translated = Lib.GoogleTranslator(source='pt', target=language).\
                                translate((group_msg[len(tag) + 1:len(group_msg) - 1]).strip())
                            group_where = Lib.regex.match(regex_pattern, line).group(3)
                            yml_new_file.write(f'{group_type}{tag} {msg_translated},{group_where}\n')
                    else:
                        with open(path_translated_yml, 'a') as yml_new_file:
                            yml_new_file.write(f'{line}')
                    dots += "."
                    Lib.os.system('cls')
                    Lib.sys.stdout.write(f"\r{Textcolor.BLUE}{otherConfigs['WaitTranslate']['Msg']}{Textcolor.END} {dots}")
                    Lib.sys.stdout.flush()

            Main.save_hash(new_hash=new_hash, path_part=language)
            print(f"{Textcolor.GREEN}{otherConfigs['TranslateMessage']}{Textcolor.END}")

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorTranslateMessage']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorTranslateMessage"], value1=str(ex))

    def checkNewVersion(self):

        try:
            Main.add_logs(message="General", value=logs["ReleaseNotes"],
                          value1=f'\nActual version: {self.version_local} \nNew version:    {self.version_distributed}')

            zip_file = Lib.Aux.Main.verify_file(path=Lib.Aux.directories['DownloadFolder'], extension='.zip',
                                                msg_not_found=Lib.Aux.otherConfigs['DownloadFinished']['Msg'],
                                                msg_found=Lib.Aux.otherConfigs['DownloadingFile']['Msg'])

            if self.version_distributed > self.version_local and not zip_file:
                print("#" * 100)
                print(f"   {otherConfigs['NewVersionAvailableTitle']['Msg']}")
                print("#" * 100)

                while True:
                    option = input(f"{Textcolor.BOLD}{Textcolor.HIGHLIGHT}"
                                   f"{otherConfigs['NewVersionAvailable1']['Msg']}{Textcolor.END}\n"
                                   f"{Textcolor.BOLD}{Textcolor.HIGHLIGHT}{otherConfigs['NewVersionAvailable2']['Msg']}"
                                   f"{Textcolor.END}{Textcolor.END}")
                    if option.upper() in ['Y', 'S']:
                        install = True
                        break
                    elif option.upper() in ['', 'N']:
                        install = False
                        break

                if install:
                    Main.delete_directory(self, path_folder=directories['DownloadFolder'])
                    Main.create_directory(self, path=directories['DownloadFolder'])

                    output_file = Lib.os.path.join(directories['DownloadFolder'], 'Green.zip')
                    print('---> ' + output_file)

                    response = Lib.requests.get(otherConfigs['GitLabPackage'] + 'Green.zip', verify=False)
                    if response.status_code == 200:
                        with open(output_file, 'wb') as file:
                            file.write(response.content)
                        print(f"{logs['DownloadPackageCompleted']['Msg']}: {output_file}")
                        Main.add_logs(message="General", value=logs["DownloadPackageCompleted"],
                                      value1=str(output_file))

                    else:
                        print(f"{logs['ErrorDownloadUpdate']['Msg']}: {response.status_code}")
                        Main.add_logs(message="General", value=logs["ErrorDownloadUpdate"],
                                      value1=str(response.status_code))

                    print("-" * 30)
                    Main.add_logs(message="General", value=logs["InstallNewVersion"],
                                  value1=str(self.version_distributed))
                    print("-" * 30)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorCheckNewVersion']['Msg']}{Textcolor.END}", str(ex))
            Main.add_logs(message="General", value=logs["ErrorCheckNewVersion"], value1=str(ex))

    # Configure the language for the automation.
    def configure_language(**kwargs):
        try:
            need_translation = False
            language = kwargs.get('language')

            path_file = Lib.os.path.join(Lib.os.getcwd(), directories["ConfigFolder"], 'dictionary-pt.yml')
            new_hash = Main.generate_hash(path_file=path_file)
            actual_hash = Main.read_hash(directory=directories["HashFolder"], language=language,
                                         actual_file='hash_dictionary.txt')

            if new_hash != actual_hash:
                need_translation = True

            return need_translation, new_hash

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorConfigureLanguage']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorConfigureLanguage"], value1=str(ex))

    # Generate the hash for a file.
    def generate_hash(**kwargs):
        try:
            # kwargs arguments.
            path_file = kwargs.get('path_file')

            BLOCKSIZE = 65536
            hasher = Lib.hashlib.sha1()
            with open(path_file, 'rb') as target_file:
                buffer = target_file.read(BLOCKSIZE)
                while len(buffer) > 0:
                    hasher.update(buffer)
                    buffer = target_file.read(BLOCKSIZE)

            return hasher.hexdigest()

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorGenerateHash']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorGenerateHash"], value1=str(ex))

    # Read the hash in a file.
    def read_hash(**kwargs):
        try:
            # kwargs arguments.
            directory = kwargs.get('directory')
            language = kwargs.get('language')
            actual_file = kwargs.get('actual_file')

            file_read = Lib.os.path.join(directory, language + '-' + actual_file)

            if Lib.os.path.exists(file_read):

                with open(file_read, 'r') as file:
                    content = file.readline()
            else:
                content = None

            return content

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorReadHash']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorReadHash"], value1=str(ex))

    # Save the hash in a file.
    def save_hash(**kwargs):
        try:
            # kwargs arguments.
            new_hash = kwargs.get('new_hash')
            path_part = kwargs.get('path_part')

            # Variables.
            hash_file_path = Lib.os.path.join(directories["HashFolder"], path_part + '-hash_dictionary.txt')

            if not Lib.os.path.exists(directories['HashFolder']):
                Main.create_directory(self, path=directories['HashFolder'])
            with open(hash_file_path, 'w') as hash_file:
                hash_file.write(new_hash)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorSaveHash']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorSaveHash"], value1=str(ex))

    def read_html_content(self):

        try:

            git_url_readme = directories['GitUrlReadme']

            response = Lib.requests.get(git_url_readme, verify=False).text
            soup = Lib.BeautifulSoup(response, 'html.parser').contents

            return soup

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorReadHTMLContent']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorReadHTMLContent"], value1=str(ex))

    # Load the configuration file.
    def load_configs(**kwargs):

        # kwargs parameters.
        language = kwargs.get('language')

        try:
            global verbs, logs, directories, otherConfigs, searchForAttribute, searchForComponent

            # yml path.
            path = Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'configs', 'dictionary-' + language + '.yml')
            if not Lib.os.path.exists(path):  # For the exe file.
                path = Lib.os.path.join(Lib.os.getcwd(), 'configs', 'dictionary-' + language + '.yml')

            with open(path, encoding='utf-8') as configFile:
                config = Lib.yaml.safe_load(configFile)

            # Add the sections.
            verbs = config['verbs']
            logs = config['logs']
            directories = config['directories']
            otherConfigs = config['otherConfigs']
            searchForAttribute = config["searchForAttribute"]
            searchForComponent = config["searchForComponent"]

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorLoadConfigs']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorLoadConfigs"], value1=str(ex))

    # Calculate the percentage of execution.
    def percentage(**kwargs):
        try:
            # kwargs parameters.
            actual_number = kwargs.get('actual')
            total = kwargs.get('total')

            # line = "*" * 12
            percentage = "{0:.2f}".format((actual_number / total) * 100)

            print(f"{Textcolor.BLUE}{' '}"
                  f"{otherConfigs['Percentage']['Msg']}"
                  f"{' '}{Textcolor.UNDERLINE}{percentage}{'%'}{' '}{Textcolor.END}"
                  f"{Textcolor.BLUE}{Textcolor.END}\n")

            Main.add_logs(message="General", value=logs["Percentage"])

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorPercentage']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorPercentage"], value1=str(ex))

    # Verify if the file exist.
    def verify_file(**kwargs):

        try:
            # kwargs parameters.
            path = kwargs.get('path')
            extension = kwargs.get('extension')
            msg_not_found = kwargs.get('msg_not_found')
            msg_found = kwargs.get('msg_found')

            files = Lib.os.listdir(path)
            for file in files:
                if file.endswith(extension):
                    print(f"{Textcolor.GREEN}{msg_found}{Textcolor.END}")
                    return True
                else:
                    print(f"{Textcolor.GREEN}{msg_not_found}{Textcolor.END}")
                    return False

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorVerifyFile']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorVerifyFile"], value1=str(ex))

    # Compare files using Beyond Compare.
    def compare_beyond_compare(**kwargs):
        try:
            # kwargs parameters.
            baseline = kwargs.get('baseline')
            new_file = kwargs.get('new_file')
            test_name = kwargs.get('test_name')

            baseline = Lib.os.path.join(directories['CompareDownloadFolder'], test_name, baseline)
            new_file = Lib.os.path.join(directories['CompareDownloadFolder'], test_name, new_file)

            # Update the Settings.
            Lib.subprocess.Popen([directories['BeyondCompare'], directories['BeyondCompareSettings'], '/silent'])

            file_session = Main._checkSessionBCFile(baseline=baseline)

            # Open the session.
            Lib.subprocess.Popen([directories['BeyondCompare'], file_session, '/silent'])

            # Disable the mouse.
            pyautogui.FAILSAFE = False

            # Open the file (Left).
            time.sleep(10)
            pyautogui.hotkey('ctrl', 'o', interval=.5)
            pyautogui.typewrite(baseline)
            pyautogui.hotkey('Enter', interval=.5)

            pyautogui.press('tab', interval=.5)

            # Open the file (Right).
            pyautogui.hotkey('ctrl', 'o', interval=.5)
            pyautogui.typewrite(new_file)
            pyautogui.hotkey('Enter', interval=.5)

            # Enable the edit option.
            pyautogui.press('f2', interval=.5)

            # Disable the mouse.
            pyautogui.FAILSAFE = True

            while Main.checkProcess(process='BCompare.exe'):
                time.sleep(1)

            print(f"{Textcolor.GREEN}{test_name} - {logs['CompareFile']['Msg']}{Textcolor.END}")

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorCompareFile']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorCompareFile"], value1=str(ex))

    # Check if the test case is a Desktop test case.
    def _check_desktop_tc(**kwargs):

        # kwargs variable.
        list_steps = kwargs.get("list_steps")

        desktop_tc = False

        for cont, _ in enumerate(otherConfigs['DesktopFunctions']):
            if any(otherConfigs['DesktopFunctions'][cont] in desktop_verb for desktop_verb in list_steps):
                desktop_tc = True

        return desktop_tc

    # Inform the updates.
    def releaseNotes(**kwargs):

        try:
            # kwargs variables.
            path = kwargs.get('path')
            readme = kwargs.get('readme')

            release_infos = []
            version_int = 0
            date_version = []
            version = None

            if path:
                readme = open(path, 'r', encoding='utf-8')

            for line in readme:
                if 'Version' in line.__str__() and version_int == 0:
                    version = Lib.regex.findall(r'\*\*Version (.*?)\*\*', line)
                    version_int = int(version[0].replace(".", ""))

                if '<em>' in line.__str__():
                    date_version = Lib.regex.findall(r'<em>(.*?)</em>', line.__str__(), Lib.regex.DOTALL)
                if ': - ' in line.__str__():
                    release_infos.append(Lib.regex.findall(r' - (.*?)\.', line.__str__(), Lib.regex.DOTALL)[0])
                if '#' in line:
                    break

            return version_int, version[0], date_version[0], release_infos

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorReleaseNotes']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorReleaseNotes"], value1=str(ex))

    # Validate content inside JSON content.
    def find_content_json(self, **kwargs):

        # kwargs variable.
        param = kwargs.get("param")
        tag = kwargs.get("tag")

        validation = False

        try:
            response = otherConfigs['Api_Response']

            if 'message' in response:  # Simple message.
                param1 = Lib.regex.search(r'(?<=\:\")(.*?)(?=\"})', param)
                if param1.group(0) == response['message']:
                    otherConfigs['JsonValidate'] = otherConfigs['JsonValidateSuccess']['Msg']
                    return "Passed"
                else:
                    print(f"{Textcolor.FAIL}{logs['ErrorValidationApi']['Msg']}{Textcolor.END}")
                    Main.add_logs(message="General", value=logs["ErrorValidationAPI"])
                    otherConfigs['JsonValidate'] = otherConfigs['JsonValidateFailed']['Msg']
                    return "Failed"
            else:
                # Tag's validation.
                for dict_id, _ in enumerate(response):
                    if str(response[dict_id][tag]) == str(param):
                        validation = (validation or True)
                    else:
                        validation = (validation or False)

                    if validation:
                        otherConfigs['JsonValidate'] = otherConfigs['JsonValidateSuccess']['Msg']
                        return "Passed"
                    else:
                        print(f"{Textcolor.FAIL}{logs['ErrorValidationApi']['Msg']}{Textcolor.END}")
                        Main.add_logs(message="General", value=logs["ErrorValidationApi"])
                        otherConfigs['JsonValidate'] = otherConfigs['JsonValidateFailed']['Msg']
                        return "Failed"

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorFindContentApi']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorFindContentApi"], value1=str(ex))

            return "Failed"

    def convert_seconds_to_string(self, **kwargs):

        # kwargs variable.
        time_spent = kwargs.get("time_spent",0)

        minutes = int(time_spent // 60)
        remaining_seconds = time_spent % 60

        return f"{minutes:02}:{remaining_seconds:06.3f}"

    def validate_selection(**kwargs):

        # kwargs variables.
        input_data = kwargs.get("input_data")
        search_list = kwargs.get("search_list")

        try:
            if input_data in search_list:
                return True
            else:
                raise ValueError

        except ValueError:
            return False

    def validate_variations(self, **kwargs):

        # kwargs variables.
        variation = kwargs.get('variation')

        if variation in ['(CHECKED)', '(ACTIVE)', '(#VALUE)', '(#TITLE)', '(#HREF)', '(#CLASS)', '(VISIBLE)',
                         '(ENABLE)']:
            return True
        else:
            return False


"""---------------------------------------------------------------------------------------------------------------------
CLASS: API Schema
GOAL: Validate the Schema using the schema from the swagger page and generate other content type for each tag.
PROCESS: 
1) Read the schema from swagger page;
2) Generate different content type for each tag;
3) Run the validate schem to check each tag.
---------------------------------------------------------------------------------------------------------------------"""


class ApiSchema:

    def __init__(self, swagger_link):
        self.swagger_link = swagger_link
        self.swagger_file = 'swagger.json'
        self.resolved_schema = None

    def api_check(self):

        try:

            Main.create_directory(self, path=directories['SwaggerFolder'])

            # Download the swagger file.
            Lib.subprocess.run(
                ['curl', '-o', Lib.os.path.join(directories['SwaggerFolder'], self.swagger_file), self.swagger_link])

            swagger_data = ApiSchema.load_swagger(self, Lib.os.path.join(directories['SwaggerFolder'],
                                                                         self.swagger_file))
            # Generate fake data to the data types
            ApiSchema.extract_jsonschema_relevant_data(self, swagger_data)

            print(f"{Textcolor.WARNING}{otherConfigs['Api_ExtractInfo']['Msg']} {self.swagger_file}{Textcolor.END}")

            with open(Lib.os.path.join(directories['SwaggerFolder'], self.swagger_file), 'r', encoding='utf-8') as file:
                schema = Lib.json.load(file)

            # Enable the field to be possible validate one by one.
            for key, value in schema.items():
                if schema[key]['additionalProperties'] is False:
                    schema[key]['additionalProperties'] = True

            with open(Lib.os.path.join(directories['SwaggerFolder'], self.swagger_file), 'w', encoding='utf-8') as file:
                Lib.json.dump(schema, file, ensure_ascii=False, indent=2)

            # Generate and print the fake data.
            for definition_name, definition_schema in schema.items():
                data_list = ApiSchema.generate_data(self, definition_schema, schema)
                print(f"Data for '{definition_name}' tag:")
                for self.json_fake_data in data_list:
                    print(Lib.json.dumps(self.json_fake_data, indent=2))
                print("-" * 80)

            # Link between each fake info and the right tag. (Only to validate the schema response)
            # self.resolved_schema = {k: ApiSchema.resolve_refs(self, v, schema) for k, v in schema.items()}
            #
            # for key, values in data.items():
            #     for value in values:
            #         print(f"TAG: {key} / VALUE: {value} \n")
            #         json_fake_data = {key: value}
            #         ApiSchema.run_validation(self, json_data)
            #
            #     print("-" * 90)

            Main.delete_files(folder_path=directories['SwaggerFolder'], extension='*')

            return self.json_fake_data

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorApiCheck']['Msg']}{Textcolor.END}", str(ex))
            Main.add_logs(message="General", value=logs["ErrorApiCheck"], value1=str(ex))

    def load_swagger(self, file_path):

        try:
            with open(file_path, 'r') as f:
                return Lib.json.load(f)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorLoadSwagger']['Msg']}{Textcolor.END}", str(ex))
            Main.add_logs(message="General", value=logs["ErrorLoadSwagger"], value1=str(ex))

    def extract_jsonschema_relevant_data(self, swagger_data):

        try:
            if 'definitions' in swagger_data:
                relevant_data = swagger_data['definitions']
            elif 'components' in swagger_data and 'schemas' in swagger_data['components']:
                relevant_data = swagger_data['components']['schemas']
            else:
                relevant_data = {}

            with open(Lib.os.path.join(directories['SwaggerFolder'], self.swagger_file), 'w') as f:
                Lib.json.dump(relevant_data, f, indent=2)

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorExtractJson']['Msg']}{Textcolor.END}", str(ex))
            Main.add_logs(message="General", value=logs["ErrorExtractJson"], value1=str(ex))

    # Generate fake data.
    def generate_data(self, schema, definitions):
        if 'type' not in schema:
            return None
        data = []

        fake = Lib.Faker()

        # Generate different content type.
        def add_variations(base_type, value):

            try:
                if base_type == 'string':
                    data.extend([
                        value,  # Original value
                        fake.random_int(),  # Integer variation
                        fake.pyfloat(left_digits=5, right_digits=2),  # Float variation
                        fake.boolean()  # Boolean variation
                    ])
                elif base_type == 'integer':
                    data.extend([
                        value,  # Original value
                        fake.word(),  # String variation
                        fake.pyfloat(left_digits=5, right_digits=2),  # Float variation
                        fake.boolean()  # Boolean variation
                    ])
                elif base_type == 'number':
                    data.extend([
                        value,  # Original value
                        fake.word(),  # String variation
                        fake.random_int(),  # Integer variation
                        fake.boolean()  # Boolean variation
                    ])
                elif base_type == 'boolean':
                    data.extend([
                        value,  # Original value
                        fake.word(),  # String variation
                        fake.random_int(),  # Integer variation
                        fake.pyfloat(left_digits=5, right_digits=2)  # Float variation
                    ])

            except Exception as ex:
                print(f"{Textcolor.FAIL}{logs['ErrorAddJsonVariation']['Msg']} - {ex}{Textcolor.END}")
                Main.add_logs(message="General", value=logs["ErrorAddJsonVariation"], value1=str(ex))

        # Generate based on schema info.
        if schema['type'] == 'string':
            value = fake.word() if not (schema.get('nullable', False) and Lib.random.choice([True, False])) else None
            add_variations('string', value)
        elif schema['type'] == 'number':
            value = fake.pyfloat(left_digits=5, right_digits=2) if not (schema.get('nullable', False) and
                                                                        Lib.random.choice([True, False])) else None
            add_variations('number', value)
        elif schema['type'] == 'integer':
            value = fake.random_int() if not (schema.get('nullable', False) and Lib.random.choice([True, False])) \
                else None
            add_variations('integer', value)
        elif schema['type'] == 'boolean':
            value = fake.boolean() if not (schema.get('nullable', False) and Lib.random.choice([True, False])) else None
            add_variations('boolean', value)
        elif schema['type'] == 'array':
            if not (schema.get('nullable', False) and Lib.random.choice([True, False])):
                array_data = [generate_data(self, schema['items'], definitions) for _ in range(3)]
                if array_data not in data:
                    data.append(array_data)
        elif schema['type'] == 'object':
            if not (schema.get('nullable', False) and Lib.random.choice([True, False])):
                obj = {}
                for prop, prop_schema in schema.get('properties', {}).items():
                    if '$ref' in prop_schema:
                        ref = prop_schema['$ref'].split('/')[-1]
                        obj[prop] = ApiSchema.generate_data(self, definitions[ref], definitions)
                    else:
                        obj[prop] = ApiSchema.generate_data(self, prop_schema, definitions)
                if obj not in data:
                    data.append(obj)
        return data

    # Read the schema references.
    def resolve_refs(self, schema, definitions):

        try:

            if isinstance(schema, dict):
                if '$ref' in schema:
                    ref = schema['$ref'].split('/')[-1]
                    return ApiSchema.resolve_refs(self, definitions[ref], definitions)
                else:
                    return {k: ApiSchema.resolve_refs(self, v, definitions) for k, v in schema.items()}
            elif isinstance(schema, list):
                return [ApiSchema.resolve_refs(self, item, definitions) for item in schema]
            else:
                return schema

        except Exception as ex:
            print(f"{Textcolor.FAIL}{logs['ErrorResolvedReference']['Msg']} - {ex}{Textcolor.END}")
            Main.add_logs(message="General", value=logs["ErrorResolvedReference"], value1=str(ex))

    def run_validation(self, json_data):  ### (Only to validate the schema response)
        errors = []
        try:
            for schema_item in self.resolved_schema.keys():
                validate(instance=json_data, schema=self.resolved_schema[schema_item])
            # print("JSON valid.")
            # validation_status = False

        except ValidationError as e:
            print(f"JSON invalid: Variable {type(e.instance)} {e.message}")
            errors.append(e.message)
            # validation_status = True

        return errors, validation_status
