import common_libs as Lib


driver = None
step = None
step_order = None


class Main:

    def __init__(self):
        self.connections = Lib.Con.Connections()

    def find_component(self, **kwargs):

        # kwargs variables.
        parameters1 = kwargs.get('parameters1')
        several = kwargs.get('several', False)
        checked_status = kwargs.get('checked_status', None)     # Only for IsEnable validation.

        search_list = [
            Lib.By.ID,
            Lib.By.NAME,
            Lib.By.XPATH,
            Lib.By.CSS_SELECTOR,
            Lib.By.CLASS_NAME,
            Lib.By.LINK_TEXT,
            Lib.By.PARTIAL_LINK_TEXT,
            Lib.By.TAG_NAME,
            'Not found'
        ]

        element_field = None
        elements_fields = None

        for tag in search_list:

            try:

                if several:
                    elements_fields = driver.find_elements(tag, parameters1)
                    if elements_fields:
                        return "Passed", tag, elements_fields

                else:
                    element_field = driver.find_element(tag, parameters1)
                    if element_field:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["FindComponent"],
                                              value1=tag + ":" + parameters1)
                        return "Passed", tag, element_field

            except Exception as ex:
                if tag == 'Not found' and checked_status is None:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorFindComponent"])
                    return "Aborted", tag, element_field
                elif tag == 'Not found' and checked_status is not None:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["WarningFindComponent"],
                                          value1=tag + ' - ' + parameters1,
                                          value2=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
                    return "Passed", tag, element_field
                else:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["WarningFindComponent"],
                                          value1=tag + ' - ' + parameters1,
                                          value2=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))

    # -------------------------------------------- Action Elements -----------------------------------------------------
    def fill_field(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            element_field.clear()

            if parameters2.upper() not in ('VAZIO', 'VACÍO', 'EMPTY'):
                element_field.send_keys(parameters2)

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, tag=tag)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["FillField"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorFillField"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Don't execute the step.
    def no_execute(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')

        try:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["NoExecute"], value1="'" + step + "'")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorNoExecute"],
                                  value1="'" + step + "' - " + str(ex))
            return "Failed"

    # Execute a MS-DOS command line.
    def execute(self, **kwargs):

        path = ""

        try:
            # kwargs arguments.
            path = kwargs.get('parameters1')

            Lib.Aux.os.system('start "" "' + path + '"')

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["Execute"], value1="'" + path + "'")

            return path, "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorExecute"],
                                  value1="'" + path + "' - " + str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Click in an element.
    def click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step, step_order=step_order,
                           tag=tag)
            element_field.click()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["Click"], value1=parameters1)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorClick"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Double click.
    def double_click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step, step_order=step_order,
                           tag=tag)
            Lib.ActionChains(driver).double_click(element_field).perform()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["DoubleClick"], value1=parameters1)

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorDoubleClick"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Right click (mouse).
    def right_click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            actions = Lib.ActionChains(driver)
            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step, step_order=step_order,
                           tag=tag)

            actions.context_click(element_field)
            actions.perform()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["RightClick"], value1=parameters1)

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorRightClick"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Drag and drop.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """

    def drag_drop(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            actions = Lib.ActionChains(driver)

            positions = parameters2.split(":")
            positionx = positions[0]
            positionx = positionx[1:]  # Only the numeric number.
            positiony = positions[1]
            positiony = positiony[1:]  # Only the numeric number.

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order)

            #actions.drag_and_drop_by_offset(element_field, int(positionx) * 10, int(positiony) * 10)
            actions.perform()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['DragDrop'], value1=parameters1)

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorDragDrop"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Drag and drop to the other component.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """
    def drag_drop_to_element(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            actions = Lib.ActionChains(driver)
            _, tag1, element_field1 = Main.find_component(self, parameters1=parameters1)

            if element_field1 is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, tag=tag1)
            _, tag2, element_field2 = Main.find_component(self, parameters1=parameters2)

            if element_field2 is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters2, step=step, step_order=step_order, tag=tag2)

            actions.drag_and_drop(element_field2, element_field1)
            actions.perform()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["DragDropToElement"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorDragDropToElement"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Type keyboard key.
    def press_button(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:
            if parameters2 is None:
                parameters2 = 1
            parameters1 = str(parameters1)
            parameters2 = int(parameters2)

            actions = Lib.ActionChains(driver)

            if parameters1.upper() == 'RETURN' or parameters1.upper() == 'ENTER':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.RETURN)
            elif parameters1.upper() == 'UP':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.UP)
            elif parameters1.upper() == 'PAGE UP':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.PAGE_UP)
            elif parameters1.upper() == 'DOWN':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.DOWN)
            elif parameters1.upper() == 'PAGE DOWN':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.PAGE_DOWN)
            elif parameters1.upper() == 'LEFT':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.LEFT)
            elif parameters1.upper() == 'RIGHT':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.RIGHT)
            elif parameters1.upper() == 'TAB':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.TAB)
            elif parameters1.upper() == 'SPACE':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.SPACE)
            elif parameters1.upper() == 'BACKSPACE':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.BACKSPACE)
            elif parameters1.upper() == 'DELETE':
                for _ in range(parameters2): actions.send_keys(Lib.Keys.DELETE)
            # Alt or Ctrl + <any other key>.
            elif parameters1.upper().__contains__('CTRL'):
                for _ in range(parameters2):
                    actions.key_down(Lib.Keys.CONTROL)
                    Lib.time.sleep(.2)
                    actions.send_keys(parameters1.upper().rsplit('+')[1].strip())
                    Lib.time.sleep(.2)
                    actions.key_up(Lib.Keys.CONTROL)
            elif parameters1.upper().__contains__('ALT'):
                for _ in range(parameters2):
                    actions.key_down(Lib.Keys.ALT)
                    Lib.time.sleep(.2)
                    actions.send_keys(parameters1.upper().rsplit('+')[1].strip())
                    Lib.time.sleep(.2)
                    actions.key_up(Lib.Keys.ALT)

            actions.perform()

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["PressButton"],
                                  value1=parameters1 + " - " + str(parameters2) + "x")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorPressButton"],
                                  value1=parameters1 + " - " + str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Mouse Over.
    def mouse_over(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            actions = Lib.ActionChains(driver)
            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, tag=tag)

            actions.move_to_element(element_field)  # Worked with XPath.
            actions.perform()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["MouseOver"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorMouseOver"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    def wait(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')
            save_evidence = kwargs.get('save_evidence')

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.time.sleep(int(parameters1))

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["Wait"], value1=parameters1)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorWait"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    def select_drop_down_list(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            element = Lib.Select(element_field)

            if status == 'Failed':
                raise Exception

            try:
                element.select_by_visible_text(parameters2)

                Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                               step_order=step_order, tag=tag)

                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["SelectDropDownList"],
                                      value1=parameters1, value2=parameters2)
            except Lib.NoSuchElementException:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["NoSelectDropDownList"])

            return "Passed"

        except Lib.NoSuchElementException as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorSelectDropDownList"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Get the text from an elements.
    def get_text(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return Lib.Aux.logs["ErrorGetText"]['Msg'], "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, color="green", tag=tag)

            if status == "Failed":
                raise Exception

            if element_field.text is None:
                headers = {'User-Agent': Lib.Aux.otherConfigs['Agent']}
                content = Lib.Aux.request.get(driver.current_url, headers=headers).content
                soup = Lib.BeautifulSoup(content, 'html.parser')

                for tag in Lib.Aux.searchForAttribute:
                    for component in Lib.Aux.searchForComponent:
                        table = soup.findAll(Lib.Aux.searchForComponent[component],
                                             attrs={Lib.Aux.searchForAttribute[tag]: parameters1})
                        for textFound in table:
                            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetText"])
                            Main.find_component(self, parameters1=parameters1, save_evidence=save_evidence,
                                                color="green")
                            return textFound.contents[0], "Passed"
                        else:
                            return Lib.Aux.logs["ErrorGetText"]["Msg"], "Failed"
            else:
                return element_field.text, "Passed"

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetText"])

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetText"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return Lib.Aux.logs["ErrorGetText"]['Msg'], "Failed"

    def open_new_tab(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
            driver.execute_script("window.open('', '_blank')")

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["OpenNewTab"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorOpenNewTab"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Get current url
    def get_url(self, **kwargs):

        # kwargs arguments.
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
            url = driver.current_url

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order, color='green',
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetUrl"])

            return url, "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetUrl"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return None, "Failed"

    # get Title
    def get_title(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:

            title = driver.title

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order, color='green',
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetTitle"])

            return title, "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetTitle"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return None, "Failed"

    # Back Page
    def back_page(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:
            driver.back()
            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["BackPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorBackPage"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Back Page.
    def forward_page(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:
            driver.forward()
            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ForwardPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorForwardPage"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Gets the attribute of an element (can be value, title or href).
    def get_attribute(self, **kwargs):

        text_found = None

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            if '(#value)' in parameters2:
                status, tag, elements_fields = Main.find_component(self, parameters1=parameters1)
                text_found = elements_fields.get_attribute('value')

            elif '(#title)' in parameters2:
                status, tag, elements_fields = Main.find_component(self, parameters1=parameters1)
                text_found = elements_fields.get_attribute('title')

            elif '(#href)' in parameters2:
                status, tag, elements_fields = Main.find_component(self, parameters1=parameters1)
                text_found = elements_fields.get_attribute('href')

            elif '(#class)' in parameters2:
                status, tag, elements_fields = Main.find_component(self, parameters1=parameters1)
                text_found = elements_fields.get_attribute('class')

            else:
                raise "Tag not correct."

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, color='green', tag=tag)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetAttribute"])

            return text_found, "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetAttribute"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return text_found, "Failed"

    def get_quantity_elements(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
            new_elements = 0
            original_style = None

            status, tag, elements_fields = Main.find_component(self, parameters1=parameters1, several=True)
            if elements_fields is None:
                return "0", "Aborted"

            if status == 'Passed':
                for _, new_element in enumerate(elements_fields):
                    original_style = new_element.get_attribute('style')
                    Main.highlight(self, parameters1=new_element, step=step, step_order=step_order, tag=tag,
                                   several=True, color='yellow', save_evidence=save_evidence)

                for _, new_element in enumerate(elements_fields):
                    Main.apply_style(new_element, original_style)

            if int(parameters2) == len(elements_fields):
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetQuantityElements"],
                                      value1=str(len(elements_fields)), value2=parameters1)

                return len(elements_fields), "Passed"
            else:
                Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                               save_evidence=save_evidence)

                raise AttributeError(str(len(elements_fields)))

        except AttributeError as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"],
                                  value1=str(ex), value2=parameters1)

            return str(len(elements_fields)), "Failed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=parameters1)

            return str(len(elements_fields)), "Failed"

    def scroll_page(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            driver.execute_script('window.scrollTo(0, ' + parameters1 + ')')

            element_field = Main.find_component(self, parameters1=parameters1)
            if element_field is None:
                return "Aborted"
            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order)

            if element_field is not None:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ScrollPage"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorScrollPage"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    def refresh_page(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:

            driver.refresh()
            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["RefreshPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorRefreshPage"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Checks whether the element is inactive.
    def is_enable(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        checked_status = kwargs.get('checked_status')

        try:

            status, tag, elements_fields = (
                Main.find_component(self, parameters1=parameters1, checked_status=checked_status))

            if elements_fields is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, color='green', tag=tag)

            if elements_fields.is_enabled() == checked_status:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsEnable"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsEnable"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Checks whether the element is visible.
    def is_displayed(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        checked_status = kwargs.get('checked_status')

        try:

            status, tag, element_field = Main.find_component(self, parameters1=parameters1, checked_status=checked_status)

            if element_field:
                Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                               step_order=step_order, color='green', tag=tag)

                if element_field.is_displayed() == checked_status:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsDisplayed"])
                    return "Passed"
                else:
                    return "Failed"

            if element_field is None and checked_status is False:
                Main.highlight(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                               step_order=step_order, color='green', tag=tag)

                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsDisplayedNo"])
                return "Passed"

            else:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"])
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Checks whether a checkbox or radio button is selected (returns True or False)
    def is_selected(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        checked_status = kwargs.get('checked_status')

        try:

            status, tag, element_field = Main.find_component(self, parameters1=parameters1)

            if element_field is None:
                return "Aborted"

            Main.highlight(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                           step_order=step_order, color='green', tag=tag)

            if element_field.is_selected() == checked_status:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsSelected"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsSelected"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Validate data (With * validate the partial text).
    def validate_data(self, **kwargs):

        # kwargs arguments.
        alert = kwargs.get('alert')
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            if alert != 'AlertScreen':

                # Get the title page.
                if '(TITLE)' in parameters1.upper():
                    text_found, status = Main.get_title(self, save_evidence=save_evidence, step=step,
                                                        step_order=step_order)
                    parameters2 = parameters1.replace('(title)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetTitle"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetTitle"])
                        status = "Failed"

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(text_found))

                # Get the URL from the address bar (get_url).
                elif '(URL)' in parameters1.upper():
                    text_found, status = Main.get_url(self, save_evidence=save_evidence, step=step,
                                                      step_order=step_order)
                    parameters2 = parameters1.replace('(url)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetUrl"])

                        status = "Passed"

                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetURL"])
                        status = "Failed"

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(text_found))

                # Check a part of the text was found.
                elif '*' in parameters2:  # Check part of the text.
                    text_found, status = Main.get_text(self, parameters1=parameters1, save_evidence=save_evidence,
                                                       step=step, step_order=step_order)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if parameters2.replace('*', '') in text_found:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetTextPart"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetTextPart"])
                        status = "Failed"

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(text_found))

                # Checks whether the element is active or inactive.
                elif parameters2.upper() in ['(INACTIVE)', '(ACTIVE)']:

                    checked_status = Lib.Aux.Main.validate_variations(self, variation=parameters2.upper())

                    status = Main.is_enable(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                            step_order=step_order, checked_status=checked_status)

                    if status == "Passed":
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsEnable"])
                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsEnable"])
                        status = "Failed"

                # Checks whether the element is visible to the user.
                elif parameters2.upper() in ['(VISIBLE)', '(INVISIBLE)']:

                    checked_status = Lib.Aux.Main.validate_variations(self, variation=parameters2.upper())

                    status = Main.is_displayed(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                               step_order=step_order, checked_status=checked_status)

                    if status == "Passed":
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsDisplayed"])
                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"])

                # Checks whether a checkbox or radio button is selected.
                elif parameters2.upper() in ['(CHECKED)', '(UNCHECKED)']:

                    checked_status = Lib.Aux.Main.validate_variations(self, variation=parameters2.upper())

                    status = Main.is_selected(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                              step_order=step_order, checked_status=checked_status)

                    if status == "Passed":
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["IsSelected"])
                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorIsSelected"])
                        status = "Failed"

                # Check some attributes.
                elif any(found in parameters2.upper() for found in ['(#TITLE)', '(#HREF)', '(#VALUE)', '(#CLASS)']):

                    text_found, status = Main.get_attribute(self, parameters1=parameters1, save_evidence=save_evidence,
                                                            parameters2=parameters2, step=step, step_order=step_order)

                    parameters2 = parameters2.replace('(#title)', '')
                    parameters2 = parameters2.replace('(#href)', '')
                    parameters2 = parameters2.replace('(#value)', '')
                    parameters2 = parameters2.replace('(#class)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetAttribute"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetAttribute"])
                        status = "Failed"

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(text_found))

                # Get the amount of elements.
                elif '<' and '>' in parameters2:
                    parameters2 = parameters2.replace('<', '')
                    parameters2 = parameters2.replace('>', '')

                    n_elements, status = Main.get_quantity_elements(self, parameters1=parameters1, step=step,
                                                                    parameters2=parameters2, step_order=step_order,
                                                                    save_evidence=save_evidence)

                    if status == 'Passed':
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["GetQuantityElements"])
                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"])

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(n_elements))

                # Validates that the text obtained from the page is the same as the expected text.
                else:
                    text_found, status = Main.get_text(self, parameters1=parameters1, save_evidence=save_evidence,
                                                       step=step, step_order=step_order)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if text_found == parameters2:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                          value1=str(parameters2))
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                          value1=str(text_found))

            else:  # If Alert Element.
                wait = Lib.WebDriverWait(driver, timeout=2)
                alert = wait.until(lambda driver: driver.switch_to.alert)

                text_found = alert.text

                if parameters1 == text_found:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ValidateData"])
                    status = "Passed"

                else:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                    status = "Failed"

                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                      value1=str(parameters1))
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                      value1=str(text_found))

            return status

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorFunctionValidateData"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Alter (Verify iFrame or Windows).
    def alter(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            if parameters1 is None:
                Main.alter_window(self, save_evidence=save_evidence, step=step, step_order=step_order)

            elif parameters1.upper() == 'IFRAME':
                Main.alter_frame(self, parameters2=parameters2, save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            elif parameters1.upper() == 'ALERT':
                Main.alter_alert_ok(self, save_evidence=save_evidence)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorAlter"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Alter window.
    def alter_window(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        save_evidence = kwargs.get('save_evidence')

        try:

            if driver.window_handles.__len__() > 0:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["AlterWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorAlterWindow"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Alter IFrame.
    def alter_frame(self, **kwargs):

        # kwargs arguments.
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            _, _, iframe = Main.find_component(self, parameters1=parameters2, save_evidence=save_evidence, step=step,
                                               step_order=step_order)

            # switch to selected iframe
            driver.switch_to.frame(iframe)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["AlterIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorAlterIframe"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Alter Alert and Click OK.
    def alter_alert_ok(self, **kwargs):

        # kwargs arguments.
        save_evidence = kwargs.get('save_evidence')

        try:

            alert = driver.switch_to.alert
            alert.accept()

            Main.highlight(self, parameters1='Alert', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["AlterAlert"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorAlterAlert"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Return to default.
    def return_default(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:

            if parameters1 is None:
                Main.return_window(self)

            elif parameters1.upper() == 'IFRAME':

                Main.return_frame(self)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ReturnDefault"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorReturnDefault"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Return to window.
    def return_window(self):

        try:
            driver.switch_to.window(driver.window_handles[0])

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ReturnWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorReturnWindow"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Return to default.
    def return_frame(self):

        try:

            driver.switch_to.default_content()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ReturnIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorReturnIframe"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Choose an option in a browser alert screen.
    def inform(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            wait = Lib.WebDriverWait(driver, timeout=2)
            alert = wait.until(lambda driver: driver.switch_to.alert)

            # Validate de Alert content (Text).
            if parameters1 is not None:
                status = Main.validate_data(self, alert='AlertScreen', parameters1=parameters1, parameters2=alert.text)
                Main.highlight(self, parameters1='Alert', step=step, step_order=step_order, save_evidence=save_evidence)

            # Actions inside de Alert.
            if parameters2.upper() in ("OK", "ACEPTAR"):
                alert.accept()

            elif parameters2.upper() in ("CANCELAR", "CANCEL"):
                alert.dismiss()

            elif parameters2.upper() is not None:  # Fill the Alert textbox.
                alert.send_keys(parameters2)
                alert.accept()

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["Inform"])

            return status

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorInform"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Function to create the browser object.
    def open_browser(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            global driver

            if parameters2 is None:
                parameters2 = ''

            # Configure before open the browser.
            if parameters1.upper() in ("CHROME", "GOOGLE", "GOOGLE CHROME"):

                preferences = {
                    "download.default_directory": Lib.Aux.directories['DownloadFolder'],
                    "download.prompt_for_download": False,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "download.directory_upgrade": True
                }
                options = Lib.webdriver.ChromeOptions()

                # If cookies are enabled.
                if parameters2.upper() == 'COOKIE':
                    options.add_argument("--disable-cache")

                options.add_argument('--profile-directory=Default')
                options.add_argument('--user-data-dir=' + Lib.Aux.directories["Temp"] + 'CHROME')
                options.add_argument("--homepage=" + Lib.Aux.otherConfigs['HomePage'])
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("prefs", preferences)

                if parameters2.upper() == '(INVISIBLE)':
                    options.add_argument("--headless")

                driver = Lib.webdriver.Chrome(service=Lib.ChromeService(Lib.ChromeDriverManager().install()),
                                              options=options)

            # Configure before open the browser.
            elif parameters1.upper() in ("MOZILLA", "FIREFOX"):

                options = Lib.webdriver.FirefoxOptions()

                # No cache.
                options.set_preference("browser.cache.disk.enable", False)
                options.set_preference("browser.cache.memory.enable", False)
                options.set_preference("browser.cache.offline.enable", False)
                options.set_preference("network.http.use-cache", False)

                options.set_preference("browser.download.folderList", 2)
                options.set_preference("browser.download.dir", Lib.Aux.directories['DownloadFolder'])
                options.set_preference("browser.download.manager.showWhenStarting", False)
                options.set_preference("browser.download.panel.shown", True)
                options.set_preference("marionette.actors.enabled", False)
                options.set_preference("browser.startup.homepage", Lib.Aux.otherConfigs['HomePage'])
                options.set_preference("browser.startup.page", 1)  # 1 = Home page

                if parameters2.upper() == '(INVISIBLE)':
                    options.headless = True

                driver = Lib.webdriver.Firefox(service=Lib.FirefoxService(Lib.GeckoDriverManager().install()),
                                               options=options)

            # Configure before open the browser.
            elif parameters1.upper() in "EDGE":  # Edge Chromium.

                options = Lib.webdriver.EdgeOptions()

                options.use_chromium = True
                options.ensure_clean_session = True  # Set blank user.
                options.add_argument("-inprivate")
                options.add_argument('--homepage-url=' + Lib.Aux.otherConfigs["HomePage"])
                options.add_argument('--user-data-dir=' + Lib.Aux.directories["Temp"] + 'EDGE_CHROMIUM')

                # If Cookies are enabled.
                if parameters2.upper() == 'COOKIE':
                    options.add_argument('--profile-directory=Default')

                # Cache config.
                options.add_argument("--disable-cache")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-application-cache")
                options.add_argument("--disk-cache-size=0")

                if parameters2.upper() == '(INVISIBLE)':
                    options.add_argument("--headless")
                    options.add_argument("disable-gpu")
                    options.add_argument('--allow-running-insecure-content')
                    options.add_argument('--ignore-certificate-errors')

                preferences = {
                    "download.default_directory": Lib.Aux.directories['DownloadFolder'],
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                }

                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_experimental_option("prefs", preferences)
                driver = Lib.webdriver.Edge(service=Lib.EdgeService(Lib.EdgeChromiumDriverManager().install()),
                                            options=options)

            else:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"])
                return "Failed"

            Lib.Aux.otherConfigs['Browser'] = parameters1
            driver.maximize_window()

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["OpenBrowser"])

            # Set the page load timeout (receive in minutes from interface).
            driver.set_page_load_timeout(int(Lib.Aux.otherConfigs['TimeoutSession']) * 60)



            return "Passed"

        except Lib.requests.exceptions.RequestException:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorFindBrowser']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorFindBrowser"])

            return "Failed"

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorOpenBrowser']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    # Verify is the browser is still opened.
    def verify_browser(self):

        try:
            check_title = None
            while check_title == driver.title:
                driver.close()

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorVerifyBrowser']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorVerifyBrowser"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

    # Close (windows or the whole browser).
    def close(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
            if parameters1 is None:  # If none was informed = Close Windows.
                driver.close()
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["CloseBrowser"])
                Main.alter_window(self, save_evidence=save_evidence, step=step, step_order=step_order)
            else:  # If something was informed = Close Browser.
                driver.quit()
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["CloseWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorClose"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')
            return "Failed"

    # Open page address.
    def open_page(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.get(parameters1)
            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["OpenPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorOpenPage"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    def apply_style(new_element, style):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", new_element, style)

    # Highlight the component during the execution.
    def highlight(self, **kwargs):

        try:
            # kwargs variables.
            parameters1 = kwargs.get('parameters1')
            color = kwargs.get('color', 'blue')
            border = kwargs.get('border', 3)
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')
            tag = kwargs.get('tag')
            several = kwargs.get('several', False)

            image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)

            if save_evidence and parameters1 == 'Alert':
                # Alert print screen.
                wait = Lib.WebDriverWait(driver, 1)
                if wait.until(lambda driver: driver.switch_to.alert):
                    Lib.shutil.copyfile(Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'images',
                                                         Lib.Aux.directories['UnavailablePrint']),
                                        Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")

            elif save_evidence and parameters1 != 'full_screen':

                if several is False:
                    new_element = Lib.WebDriverWait(driver, 59).until(Lib.ec.visibility_of_element_located
                                                                      ((tag, parameters1)))

                    original_style = new_element.get_attribute('style')
                else:
                    new_element = parameters1

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_element)

                Main.apply_style(new_element, "border: {0}px solid {1};".format(border, color))
                Lib.time.sleep(1)

                take_picture_status = Lib.Func.Main.take_picture(self, image_name=image_name)

                if several is False:
                    Main.apply_style(new_element, original_style)

                if not take_picture_status:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

            elif save_evidence and parameters1 == 'full_screen':
                highlight_script = "var highlight = document.createElement('div'); highlight.setAttribute('id', 'highlight'); highlight.setAttribute('style', 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(255, 255, 0, 0.5); z-index: 999999; pointer-events: none;'); document.body.appendChild(highlight);"
                driver.execute_script(highlight_script)
                driver.execute_script("var highlight = document.getElementById('highlight'); if (highlight) highlight.remove();")

                # Take picture.
                image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)
                take_picture_status = Lib.Func.Main.take_picture(self, image_name=image_name)
                if not take_picture_status:
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorHighLight"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]),
                                  value2=f' Step order: {step_order} / Step: {step}')

    # Save the file locally.
    def save_file(self, **kwargs):

        try:
            # kwargs variables:
            step_order = kwargs.get("step_order")
            step = kwargs.get('step')
            save_evidence = kwargs.get('save_evidence')

            Lib.time.sleep(5)
            cont = 1

            while True:
                # The file found means it is still downloading.
                if Lib.Aux.Main.verify_file(path=Lib.Aux.directories['DownloadFolder'], extension='crdownload',
                                            msg_not_found=Lib.Aux.otherConfigs['DownloadFinished']['Msg'],
                                            msg_found=Lib.Aux.otherConfigs['DownloadingFile']['Msg']):
                    Lib.time.sleep(1)
                    continue
                else:
                    #     # Rename de file.
                    #     files = Lib.os.listdir(Lib.Aux.directories['DownloadFolder'])
                    #     for file in files:
                    #         new_name = file + ' - ' + cont.__str__()
                    #         Lib.os.rename(Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], file),
                    #                       Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name))
                    #         Lib.shutil.move(Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name),
                    #                         Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name))
                    break

            Main.highlight(self, parameters1='full_screen', step=step, step_order=step_order,
                           save_evidence=save_evidence)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["SaveFile"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorSaveFile"],
                                  value1=str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            return "Failed"

    # Save the screenshots.
    def take_picture(self, **kwargs):

        try:
            # kwargs variables:
            image_name = kwargs.get("image_name")

            driver.save_screenshot(Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["TakePicture"])

            return True

        except AttributeError or Lib.requests.exceptions.RequestException or Lib.requests.exceptions.RetryError:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}"
                  f"{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorTakePicture"])

            return False

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}{Lib.Aux.Textcolor.END}",
                  str(Lib.regex.split(r'\.|\n', ex.msg)[0]))
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorTakePicture"], value1=str(ex),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return False

# --------------------------------------------- API Functions ----------------------------------------------------------
    def request_api(self, **kwargs):

        # kwargs variables:
        parameters1 = kwargs.get("parameters1")
        api_action = kwargs.get("api_action")
        num_of_steps = kwargs.get("num_of_steps")
        step_order = kwargs.get("step_order")
        step = kwargs.get('step')

        try:

            # Variables
            Lib.Aux.otherConfigs['Api_Step'] = True
            api_status_final = True
            error_msg_list = {}
            step_status = "Not Run"

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ApiLog"],
                                  value1=parameters1.upper())

            if parameters1.upper() != 'SUBMIT':
                tag = parameters1[:parameters1.find(':')]
                if tag.upper() == 'ENDPOINT':
                    Lib.Aux.otherConfigs['Api_Endpoint'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'AUTHORIZATION':
                    Lib.Aux.otherConfigs['Api_Authorization'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'HEADERS':
                    Lib.Aux.otherConfigs['Api_Headers'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'BODY':
                    Lib.Aux.otherConfigs['Api_Body'] = (parameters1[parameters1.find(':') + 1:parameters1.rfind('\"')]
                                                        .strip())
                elif tag.upper() == 'PARAMS':
                    Lib.Aux.otherConfigs['Api_Params'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == "SCHEMA":
                    if num_of_steps.__len__() != step_order:
                        raise Exception(Lib.Aux.logs['ErrorApiSchema']['Msg'])

                    if Lib.Aux.otherConfigs['Api_Body']:
                        dict_body = Lib.ast.literal_eval(Lib.Aux.otherConfigs['Api_Body'])
                    else:
                        print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorApiBodyMissing']['Msg']}"
                              f"{Lib.Aux.Textcolor.END}")
                        Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorApiBodyMissing"])
                        raise TypeError(Lib.Aux.logs['ErrorApiBodyMissing']['Msg'])
                    json_data = Lib.Aux.ApiSchema(parameters1[parameters1.find(':') + 1:].strip())
                    json_fake_data = json_data.api_check()

                    for tag in json_fake_data.keys():
                        for fake_order, _ in enumerate(json_fake_data[tag]):
                            dict_body[tag] = json_fake_data[tag][fake_order]

                            # Run the API request.
                            error_msg, step_status = (
                                self.connections.send_request(api_action=api_action,
                                                              headers=Lib.Aux.otherConfigs['Api_Headers'],
                                                              body=dict_body))

                            error_msg_list[tag + ' -> ' + str(dict_body[tag])] = error_msg

                            if step_status == 'Failed':
                                api_status = True
                            else:
                                api_status = False

                            api_status_final = (api_status_final and api_status)

                    Lib.Aux.otherConfigs['Api_Response'] = error_msg_list

                    if api_status_final:
                        return "Passed"
                    else:
                        return "Failed"

                if Lib.Aux.otherConfigs['Api_Endpoint'] is None:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorApiMissingInfo']['Msg']}"
                          f"{Lib.Aux.Textcolor.END}")
                    Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorApiMissingInfo"])
                    raise TypeError(Lib.Aux.logs['ErrorApiMissingInfo']['Msg'])
                else:
                    return "Passed"
            else:
                # Run the API request.
                Lib.Aux.otherConfigs['Api_Response'], step_status = (
                    self.connections.send_request(api_action=api_action,
                                                  headers=Lib.Aux.otherConfigs['Api_Headers'],
                                                  body=Lib.Aux.otherConfigs['Api_Body']))

                return step_status

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequestApi']['Msg']}{Lib.Aux.Textcolor.END}", str(ex))
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorRequestApi"], value1=str(ex),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"

    def response_api(self, **kwargs):

        try:
            # kwargs variables:
            parameters1 = kwargs.get("parameters1")
            step = kwargs.get("step")
            step_order = kwargs.get("step_order")
            find_content = None
            status_code = None
            schema = None

            Lib.Aux.otherConfigs['Api_Step'] = True

            tag = parameters1[:parameters1.find(':')]
            param = parameters1[parameters1.find(':') + 1:]

            # Status Code.
            if tag.upper() == "STATUS CODE" and int(param) == Lib.Aux.otherConfigs['Api_StatusCode']:
                status_code = "Passed"
            elif tag.upper() == "STATUS CODE" and int(param) != Lib.Aux.otherConfigs['Api_StatusCode']:
                status_code = "Failed"
            else:  # tag.upper() != "STATUS CODE":
                find_content = Lib.Aux.Main.find_content_json(self, tag=tag, param=param)

            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ApiLog"],
                                  value1=f"{tag.upper()} : {param.upper()}")

            if status_code == "Passed" or find_content == "Passed" or schema == "Passed":
                return "Passed"
            else:
                Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorResponseApi"],
                                      value1=f"Expected: {tag} - Result {param}")
                return "Failed"

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorResponseApi']['Msg']}{Lib.Aux.Textcolor.END}", str(ex))
            Lib.Aux.Main.add_logs(message="General", value=Lib.Aux.logs["ErrorResponseApi"], value1=str(ex),
                                  value2=f' Step order: {step_order} / Step: {step}')

            return "Failed"
