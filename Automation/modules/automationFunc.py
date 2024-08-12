import common_libs as Lib

driver = None


class Main:

    def __init__(self):
        self.connections = Lib.Con.Connections()

    # Function to search the element using the option above.
    def findElement(self, **kwargs):

        # kwargs variables.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')
        several = kwargs.get('several', False)
        color = kwargs.get('color', 'blue')

        new_element = None

        search_list = [
            Lib.By.ID,
            Lib.By.NAME,
            Lib.By.XPATH,
            Lib.By.CSS_SELECTOR,
            Lib.By.CLASS_NAME,
            Lib.By.TAG_NAME,
            Lib.By.LINK_TEXT,
            Lib.By.PARTIAL_LINK_TEXT
        ]

        if parameters1 == 'full_screen' or parameters1 == 'Alert':
            Main.highlight(self, new_element=parameters1, color=color, border=3, several=several,
                           save_evidence=save_evidence, step=step, step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FindElement"], value1='full_screen')

        else:

            for tag in search_list:

                try:
                    driver.implicitly_wait(3)

                    if several:  # Check the quantity of elements.
                        new_elements = driver.find_elements(tag, parameters1)

                        if new_elements:

                            for element in new_elements:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

                                Main.highlight(self, new_element=element, color=color, border=3, several=several,
                                               save_evidence=save_evidence, step=step, step_order=step_order)

                                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FindElement"], value1=tag,
                                                     value2=parameters1)

                            return new_elements

                    else:
                        new_element = driver.find_element(tag, parameters1)

                        if new_element is not None:
                            # Set element focus.
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_element)

                            Main.highlight(self, new_element=new_element, color=color, border=3, several=several,
                                           save_evidence=save_evidence, step=step, step_order=step_order)

                            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FindElement"], value1=tag,
                                                 value2=parameters1)

                            return new_element

                except Lib.NoSuchElementException:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["WarningFindElement"], value1=tag,
                                         value2=parameters1)

                # finally:
                #
                #     return new_element

    # -------------------------------------------- Action Elements -----------------------------------------------------
    def fillField(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.clear()

            if parameters2.upper() not in ('VAZIO', 'VACÍO', 'EMPTY'):
                element_field.send_keys(parameters2)

            _ = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FillField"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorFillField"], value1=str(ex))

            return "Failed"

    # Don't execute the step.
    def noExecute(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')

        try:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["NoExecute"], value1="'" + step + "'")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorNoExecute"],
                                 value1="'" + step + "' - " + str(ex))
            return "Failed"

    # Execute a MS-DOS command line.
    def execute(self, **kwargs):

        path = ""

        try:
            # kwargs arguments.
            path = kwargs.get('parameters1')

            Lib.Aux.os.system('start "" "' + path + '"')

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Execute"], value1="'" + path + "'")

            return path, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorExecute"],
                                 value1="'" + path + "' - " + str(ex))
            return "Failed"

    # Click in an element.
    def click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            element_field = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                             step_order=step_order)
            element_field.click()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Click"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorClick"], value1=str(ex))
            return "Failed"

    # Double click.
    def doubleClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            element_field = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                             step_order=step_order)
            element_field.click()
            element_field.click()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["DoubleClick"])

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDoubleClick"], value1=str(ex))
            return "Failed"

    # Right click (mouse).
    def rightClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            actions = Lib.ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                             step_order=step_order)

            actions.context_click(element_field)
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["RightClick"])

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRightClick"], value1=str(ex))
            return "Failed"

    # Drag and drop.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """

    def dragDrop(self, **kwargs):
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

            #actions.drag_and_drop_by_offset(element_field, int(positionx) * 10, int(positiony) * 10)
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['DragDrop'])

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDragDrop"], value1=str(ex))
            return "Failed"

    # Drag and drop to the other component.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """
    def dragDropToElement(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            actions = Lib.ActionChains(driver)
            element_field1 = Main.findElement(self, parameters1=parameters1)
            element_field2 = Main.findElement(self, parameters1=parameters2, save_evidence=save_evidence, step=step,
                                              step_order=step_order)

            actions.drag_and_drop(element_field2, element_field1)
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["DragDropToElement"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDragDropToElement"], value1=str(ex))
            return "Failed"

    # Type keyboard key.
    def pressButton(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

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
                    Lib.Aux.time.sleep(.2)
                    actions.send_keys(parameters1.upper().rsplit('+')[1].strip())
                    Lib.Aux.time.sleep(.2)
                    actions.key_up(Lib.Keys.CONTROL)
            elif parameters1.upper().__contains__('ALT'):
                for _ in range(parameters2):
                    actions.key_down(Lib.Keys.ALT)
                    Lib.Aux.time.sleep(.2)
                    actions.send_keys(parameters1.upper().rsplit('+')[1].strip())
                    Lib.Aux.time.sleep(.2)
                    actions.key_up(Lib.Keys.ALT)

            _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["PressButton"],
                                 value1=parameters1 + " - " + str(parameters2) + "x")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorPressButton"],
                                 value1=parameters1 + " - " + str(ex))
            return "Failed"

    # Mouse Over.
    def mouseOver(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            actions = Lib.ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                             step_order=step_order)

            actions.move_to_element(element_field)  # Worked with XPath.
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["MouseOver"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorMouseOver"], value1=str(ex))

            return "Failed"

    # Wait.
    def wait(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.time.sleep(int(parameters1))

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Wait"], value1=parameters1)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorWait"], value1=str(ex))

            return "Failed"

    def selectDropDownList(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            # Only to highlight and take picture.
            # _ = Main.findElement(self, parameters1='parameters1', save_evidence=save_evidence, step=step,
            #                      step_order=step_order)

            element_field = Lib.Select(Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence,
                                                        step=step, step_order=step_order))

            element_field.select_by_visible_text(parameters2)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["SelectDropDownList"], value1=parameters1,
                                 value2=parameters2)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorSelectDropDownList"] + " - " + str(ex),
                                 value1=parameters1, value2=parameters2)

            return "Failed"

    # Get the text from an elements.
    def getText(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            obtained_text = Main.findElement(self, parameters1=parameters1, color="green", save_evidence=save_evidence,
                                             step=step, step_order=step_order).text

            if obtained_text is None:
                headers = {'User-Agent': Lib.Aux.otherConfigs['Agent']}
                content = Lib.Aux.request.get(driver.current_url, headers=headers).content
                soup = Lib.BeautifulSoup(content, 'html.parser')

                for tag in Lib.Aux.searchForAttribute:
                    for component in Lib.Aux.searchForComponent:
                        table = soup.findAll(Lib.Aux.searchForComponent[component],
                                             attrs={Lib.Aux.searchForAttribute[tag]: parameters1})
                        for textFound in table:
                            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetText"])
                            Main.findElement(self, parameters1=parameters1, color="green", save_evidence=save_evidence,
                                             step=step, step_order=step_order)
                            return textFound.contents[0], "Passed"
                        else:
                            return Lib.Aux.logs["ErrorGetText"]["Msg"], "Failed"
            else:
                return obtained_text, "Passed"

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetText"])

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetText"], value1=str(ex))

            return Lib.Aux.logs["ErrorGetText"]['Msg'], "Failed"

    def openNewTab(self, **kwargs):
        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.execute_script("window.open('', '_blank')")

            _ = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["OpenNewTab"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenNewTab"], value1=str(ex))

            return "Failed"

    # Get current url
    def getURL(self, **kwargs):

        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            url = driver.current_url

            _ = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetURL"])

            return url, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetURL"], value1=str(ex))

            return None, "Failed"

    # get Title
    def getTitle(self, **kwargs):

        # kwargs arguments.
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:

            title = driver.title

            _ = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetTitle"])

            return title, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetTitle"], value1=str(ex))

            return None, "Failed"

    # Back Page
    def backPage(self, **kwargs):

        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.back()
            _ = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["BackPage"])

            return driver, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorBackPage"], value1=str(ex))

            return "Failed"

    # Back Page.
    def forwardPage(self, **kwargs):

        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.forward()
            _ = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ForwardPage"])

            return driver, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorForwardPage"], value1=str(ex))

            return "Failed"

    # Gets the attribute of an element (can be value, title or href).
    def getAttribute(self, **kwargs):

        text_found = None

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            if '(#value)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                        step_order=step_order)
                text_found = page.get_attribute('value')

            elif '(#title)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                        step_order=step_order)
                text_found = page.get_attribute('title')

            elif '(#href)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                        step_order=step_order)
                text_found = page.get_attribute('href')

            elif '(#class)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                        step_order=step_order)
                text_found = page.get_attribute('class')

            else:
                raise "Tag not correct."

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetAttribute"])

            return text_found, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetAttribute"], value1=str(ex))

            return text_found, "Failed"

    def getQuantityElements(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        save_evidence = kwargs.get('save_evidence')
        step = kwargs.get('step')
        step_order = kwargs.get('step_order')

        try:
        #     search_list = (
        #         Lib.By.ID,
        #         Lib.By.NAME,
        #         Lib.By.XPATH,
        #         Lib.By.CSS_SELECTOR,
        #         Lib.By.CLASS_NAME,
        #         Lib.By.TAG_NAME,
        #         Lib.By.LINK_TEXT,
        #         Lib.By.PARTIAL_LINK_TEXT
        #     )
        #
        #     x = count_elements = 0
        #
        #     for tag in search_list:

            new_elements = 0

                #driver.implicitly_wait(3)
                #new_element = driver.find_elements(tag, parameters1)
            new_element = Main.findElement(self, parameters1=parameters1, color="yellow", save_evidence=save_evidence,
                                           step=step, step_order=step_order, several=True)

            new_elements = len(new_element)


            # elif x > 8:
            #     return elements, "Passed"

            if new_elements > 0:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetQuantityElements"],
                                     value1=str(new_elements), value2=parameters1)

                return new_elements, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"], value1=str(ex),
                                 value2=parameters1)

            return None, "Failed"

    # Scroll Page
    def scrollPage(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.execute_script('window.scrollTo(0, ' + parameters1 + ')')

            status_element = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            # Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ScrollPage"])

            if status_element is not None:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ScrollPage"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorScrollPage"], value1=str(ex))

            return "Failed"

    def refreshPage(self, **kwargs):

        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.refresh()
            status_element = Main.findElement(self, parameters1='full_screen', color="blue", save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["RefreshPage"])

            # return driver, "Passed"

            if status_element is not None:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["RefreshPage"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRefreshPage"], value1=str(ex))

            return "Failed"

    # Checks whether the element is inactive.
    def isEnable(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status_element = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                              step_order=step_order).is_enabled()

            if status_element is not None:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsEnable"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsEnable"], value1=str(ex))

            return "Failed"

    # Checks whether the element is visible.
    def isDisplayed(self, **kwargs):

        # status_element = None

        try:

            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status_element = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                              step_order=step_order).is_displayed()

            if status_element is not None:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsDisplayed"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"], value1=str(ex))

            return "Failed"

    # Checks whether a checkbox or radio button is selected (returns True or False)
    def isSelected(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            status_element = Main.findElement(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                              step_order=step_order).is_selected()

            if status_element is not None:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsSelected"])
                return "Passed"
            else:
                return "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsSelected"], value1=str(ex))
            return "Failed"

    # Validate data (With * validate the partial text).
    def validateData(self, **kwargs):

        try:
            # kwargs arguments.
            alert = kwargs.get('alert')
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            if alert != 'AlertScreen':

                # Get the title page.
                if '(title)' in parameters1:
                    text_found, status = Main.getTitle(self, save_evidence=save_evidence, step=step,
                                                       step_order=step_order)
                    parameters2 = parameters1.replace('(title)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetTitle"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetTitle"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Get the URL from the address bar (getURL).
                elif '(url)' in parameters1:
                    text_found, status = Main.getURL(self, save_evidence=save_evidence, step=step,
                                                     step_order=step_order)
                    parameters2 = parameters1.replace('(url)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetURL"])

                        parameters2 = parameters1.replace('(url)', '')
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetURL"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Check a part of the text was found.
                elif '*' in parameters2:  # Check part of the text.
                    text_found, status = Main.getText(self, parameters1=parameters1, save_evidence=save_evidence,
                                                      step=step, step_order=step_order)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if parameters2.replace('*', '') in text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetTextPart"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetTextPart"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Checks whether the element is active or inactive.
                elif '(?)' in parameters2:
                    status = Main.isEnable(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                           step_order=step_order)
                    # text_found = str(text_found)
                    # parameters2 = parameters2.replace('(?)', '')

                    if status == "Passed":
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsEnable"])
                        # status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsEnable"])
                        status = "Failed"

                # Checks whether the element is visible to the user.
                elif '($)' in parameters2:
                    status = Main.isDisplayed(self, value1=parameters1, save_evidence=save_evidence, step=step,
                                              step_order=step_order)
                    # text_found = str(text_found)
                    # parameters2 = parameters2.replace('($)', '')

                    if status == "Passed":
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsDisplayed"])
                        # status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"])
                        # status = "Failed"

                # Checks whether a checkbox or radio button is selected.
                elif '(.)' in parameters2:
                    status = Main.isSelected(self, parameters1=parameters1, save_evidence=save_evidence, step=step,
                                             step_order=step_order)

                    # parameters2 = parameters2.replace('(.)', '')

                    if status == "Passed":
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsSelected"])
                        # status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsSelected"])
                        status = "Failed"

                # Checks if data is not available.
                elif '(!=)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1, save_evidence=save_evidence,
                                                      step=step, step_order=step_order)
                    parameters2 = parameters2.replace('(!=)', ' - ')

                    if parameters2 not in str(text_found):
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Checks if the data is available.
                elif '(!)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1, save_evidence=save_evidence,
                                                      step=step, step_order=step_order)
                    parameters2 = parameters2.replace('(!)', '')

                    if parameters2 in str(text_found):
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Available"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAvailable"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Check some attributes.
                elif ('(#title)' in parameters2 or '(#href)' in parameters2 or '(#value)' in parameters2 or '(#class)'
                      in parameters2):
                    text_found, status = Main.getAttribute(self, parameters1=parameters1, parameters2=parameters2,
                                                           save_evidence=save_evidence, step=step,
                                                           step_order=step_order)
                    parameters2 = parameters2.replace('(#title)', '')
                    parameters2 = parameters2.replace('(#href)', '')
                    parameters2 = parameters2.replace('(#value)', '')
                    parameters2 = parameters2.replace('(#class)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetAttribute"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetAttribute"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Get the amount of elements.
                elif '<' and '>' in parameters2:
                    text_found, status = Main.getQuantityElements(self, parameters1=parameters1, step=step,
                                                                  save_evidence=save_evidence, step_order=step_order)
                    parameters2 = parameters2.replace('<', '')
                    parameters2 = parameters2.replace('>', '')

                    if int(parameters2) == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetQuantityElements"])
                        status = "Passed"
                        text_found = str(text_found)

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"])
                        status = "Failed"
                        text_found = str(text_found)

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

                # Validates that the text obtained from the page is the same as the expected text.
                else:
                    text_found, status = Main.getText(self, parameters1=parameters1, save_evidence=save_evidence,
                                                      step=step, step_order=step_order)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if text_found == parameters2:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                         value1=str(parameters2))
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                         value1=str(text_found))

            else:  # If Alert Element.
                wait = Lib.WebDriverWait(driver, timeout=2)
                alert = wait.until(lambda driver: driver.switch_to.alert)

                text_found = alert.text

                if parameters2 == text_found:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                    status = "Passed"

                else:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                    status = "Failed"

                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                     value1=str(parameters2))
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                     value1=str(text_found))

            return status

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorFunctionValidateData"], value1=str(ex))
            return "Failed"

    # Alter (Verify iFrame or Windows).
    def alter(self, **kwargs):

        try:

            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            if parameters1 is None:
                Main.alterWindow(self, save_evidence=save_evidence, step=step, step_order=step_order)

            elif parameters1.upper() == 'IFRAME':
                Main.alterFrame(self, parameters2=parameters2, save_evidence=save_evidence, step=step,
                                step_order=step_order)

            elif parameters1.upper() == 'ALERT':
                Main.alterAlertOK(self)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlter"], value1=str(ex))
            return "Failed"

    # Alter window.
    def alterWindow(self, **kwargs):

        try:
            # kwargs arguments.
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            for handle in driver.window_handles:
                driver.switch_to.window(handle)

            _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterWindow"], value1=str(ex))
            return "Failed"

    # Alter IFrame.
    def alterFrame(self, **kwargs):

        try:
            # kwargs arguments.
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            # Store iframe web element
            iframe = Main.findElement(self, parameters1=parameters2, save_evidence=save_evidence, step=step,
                                      step_order=step_order)

            # switch to selected iframe
            driver.switch_to.frame(iframe)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterIframe"], value1=str(ex))
            return "Failed"

    # Alter Alert and Click OK.
    def alterAlertOK(self):
        try:

            alert = driver.switch_to.alert
            alert.accept()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterAlert"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterAlert"], value1=str(ex))
            return "Failed"

    # Return to default.
    def returnDefault(self, **kwargs):

        try:

            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            if parameters1 is None:
                Main.returnWindow(self)

            elif parameters1.upper() == 'IFRAME':

                Main.returnFrame(self)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ReturnDefault"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnDefault"], value1=str(ex))
            return "Failed"

    # Return to window.
    def returnWindow(self):
        try:
            driver.switch_to.window(driver.window_handles[0])

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ReturnWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnWindow"], value1=str(ex))
            return "Failed"

    # Return to default.
    def returnFrame(self):

        try:

            driver.switch_to.default_content()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ReturnIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnIframe"], value1=str(ex))
            return "Failed"

    # Choose an option in a browser alert screen.
    def inform(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            wait = Lib.WebDriverWait(driver, timeout=2)
            alert = wait.until(lambda driver: driver.switch_to.alert)

            # Validate de Alert content (Text).
            if parameters1 is not None:
                _ = Main.validateData(self, alert='AlertScreen', parameters1=parameters1, parameters2=alert.text)
                _ = Main.findElement(self, parameters1='Alert', save_evidence=save_evidence, step=step,
                                     step_order=step_order)

            # Actions inside de Alert.
            if parameters2.upper() in ("OK", "ACEPTAR"):
                alert.accept()
                Lib.time.sleep(3)

            elif parameters2.upper() in ("CANCELAR", "CANCEL"):
                alert.dismiss()
                Lib.time.sleep(3)

            elif parameters2.upper() is not None:  # Fill the Alert textbox.
                # wait = Lib.WebDriverWait(driver, 10)
                # alert = wait.until(Lib.ec.alert_is_present())
                # alert = driver.switch_to.alert
                alert.send_keys(parameters2)
                # actions = Lib.ActionChains(driver)
                # actions.send_keys(parameters2).perform()
                alert.accept()
                Lib.time.sleep(3)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Inform"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorInform"], value1=str(ex))
            return "Failed"

    # Function to create the browser object.
    def openBrowser(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            enable_cookie = kwargs.get('enable_cookie')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            global driver

            # Configure before open the browser.
            if parameters1.upper() in ("CHROME", "GOOGLE", "GOOGLE CHROME"):
                # Disable the Chrome logs in the .bat file and alter the download folder.
                preferences = {
                    "download.default_directory": Lib.Aux.directories['DownloadFolder'],
                    "download.prompt_for_download": False
                    # "download.directory_upgrade": True,
                    # "safebrowsing.enabled": True,
                    # "credentials_enable_service": False,
                    # "profile.password_manager_enabled": False
                }
                options = Lib.webdriver.ChromeOptions()

                # If cookies are enabled.
                if enable_cookie:
                    options.add_argument('--profile-directory=Default')
                    options.add_argument('--user-data-dir=' + Lib.Aux.directories["Temp"] + 'CHROME')
                    # options.add_argument("--log-level=3")
                    options.add_argument("--homepage=" + Lib.Aux.otherConfigs['HomePage'])

                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("prefs", preferences)

                driver = Lib.webdriver.Chrome(service=Lib.ChromeService(Lib.ChromeDriverManager().install()),
                                              options=options)

            # Configure before open the browser.
            elif parameters1.upper() in ("MOZILLA", "FIREFOX"):
                profile = Lib.webdriver.FirefoxProfile()
                profile.set_preference("browser.download.dir", Lib.Aux.directories['DownloadFolder'])
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.panel.shown", True)
                profile.set_preference("marionette.actors.enabled", False)
                profile.set_preference("browser.startup.homepage", Lib.Aux.otherConfigs['HomePage'])
                profile.set_preference("browser.startup.page", 1)  # 1 = Home page
                mime_types = [
                    'text/plain',
                    'application/vnd.ms-excel',
                    'text/csv',
                    'application/csv',
                    'text/comma-separated-values',
                    'application/download',
                    'application/octet-stream',
                    'binary/octet-stream',
                    'application/binary',
                    'application/x-unknown',
                    'multipart/x-zip',
                    'application/zip',
                    'application/zip-compressed',
                    'application/x-zip-compressed']
                profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))

                driver = Lib.webdriver.Firefox(service=Lib.FirefoxService(Lib.GeckoDriverManager().install()))

            # Configure before open the browser.
            elif parameters1.upper() in "EDGE":  # Edge Chromium.

                options = Lib.webdriver.EdgeOptions()

                options.use_chromium = True
                options.ensure_clean_session = True  # Set blank user.
                options.add_argument("-inprivate")

                # If Cookies are enabled.
                if enable_cookie:
                    options.add_argument('--profile-directory=Default')
                    options.add_argument('--user-data-dir=' + Lib.Aux.directories["Temp"] + 'EDGE_CHROMIUM')
                    options.add_argument('--homepage=' + Lib.Aux.directories["HomePage"])

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
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"])
                return "Failed"

            Lib.Aux.otherConfigs['Browser'] = parameters1
            driver.maximize_window()

            _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Main.openPage(self, parameters1=Lib.Aux.otherConfigs["HomePage"])

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["OpenBrowser"])

            # Set the page load timeout (receive in minutes from interface).
            driver.set_page_load_timeout(int(Lib.Aux.otherConfigs['TimeoutSession']) * 60)

            return "Passed"

        except Lib.requests.exceptions.RequestException:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorFindBrowser']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorFindBrowser"])

            return "Failed"

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorOpenBrowser']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"], value1=str(ex))

            return "Failed"

    # Verify is the browser is still opened.
    def verifyBrowser(self):

        try:
            if driver.current_url:
                driver.close()

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorVerifyBrowser"], value1=str(ex))

            return "Failed"

    # Close (windows or the whole browser).
    def close(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            if parameters1 is None:  # If none was informed = Close Windows.
                driver.quit()
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["CloseBrowser"])
            else:  # If something was informed = Close Browser.
                driver.close()
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["CloseWindow"])
                Main.alterWindow(self, save_evidence=save_evidence, step=step, step_order=step_order)

            # _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
            #                      step_order=step_order)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorClose"], value1=str(ex))
            return "Failed"

    # Open page address.
    def openPage(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')

            driver.get(parameters1)
            _ = Main.findElement(self, parameters1='full_screen', save_evidence=save_evidence, step=step,
                                 step_order=step_order)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["OpenPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenPage"], value1=str(ex))

            return "Failed"

    # Highlight the component during the execution.
    def highlight(self, **kwargs):

        try:
            # kwargs variables.
            new_element = kwargs.get('new_element')
            # effect_time = kwargs.get('effect_time')
            color = kwargs.get('color')
            border = kwargs.get('border')
            save_evidence = kwargs.get('save_evidence')
            step = kwargs.get('step')
            step_order = kwargs.get('step_order')
            several = kwargs.get('several', False)

            image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)

            if save_evidence and new_element == 'Alert':
                # Alert print screen.
                wait = Lib.WebDriverWait(driver, 1)
                if wait.until(lambda driver: driver.switch_to.alert):
                    # if Lib.ec.alert_is_present()(driver):
                    Lib.shutil.copyfile(Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'images',
                                                         Lib.Aux.directories['UnavailablePrint']),
                                        Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")

            # else:
        # except Lib.NoAlertPresentException:

            # driver.save_screenshot(Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")

            # Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["TakePicture"])

            elif save_evidence and new_element != 'full_screen':
                def apply_style(style):
                    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", new_element, style)

                original_style = new_element.get_attribute('style')
                apply_style("border: {0}px solid {1};".format(border, color))
                Lib.time.sleep(1)

                # Take picture.
                # image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)
                # take_picture_status = Lib.Func.Main.takePicture(self, test_set_path=Lib.Aux.directories['TestSetPath'],
                #                                                 image_name=image_name)
                take_picture_status = Lib.Func.Main.takePicture(self, image_name=image_name)
                if not take_picture_status:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

                if several is False:
                    apply_style(original_style)

            elif save_evidence and new_element == 'full_screen':
                highlight_script = """
                var highlight = document.createElement('div');
                highlight.setAttribute('id', 'highlight');
                highlight.setAttribute('style', 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(255, 255, 0, 0.5); z-index: 999999; pointer-events: none;');
                document.body.appendChild(highlight);
                """
                driver.execute_script(highlight_script)
                driver.execute_script(
                    "var highlight = document.getElementById('highlight'); if (highlight) highlight.remove();")

                # Take picture.
                image_name = Lib.Aux.otherConfigs["EvidenceName"] + str(step_order).zfill(2)
                # take_picture_status = Lib.Func.Main.takePicture(self, test_set_path=Lib.Aux.directories['TestSetPath'],
                #                                                 image_name=image_name)
                take_picture_status = Lib.Func.Main.takePicture(self, image_name=image_name)
                if not take_picture_status:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorScreenshot"], value1=step)

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorHighLight"], value1=str(ex))

    # Configure the save path - Only Edge Legacy.
    @staticmethod
    def _configureSavePath():

        try:
            # Keyboard press Alt+x and open the browser Configuration.
            Lib.Aux.pyautogui.keyDown('alt')
            Lib.Aux.time.sleep(.2)
            Lib.Aux.pyautogui.keyDown('x')
            Lib.Aux.time.sleep(.2)
            Lib.Aux.pyautogui.keyUp('alt')

            # Navigate to the browser download folder.
            Lib.Aux.pyautogui.typewrite(['up', 'Enter', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab',
                                     'enter', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'Enter'], interval=.2)

            # Type the new path.
            Lib.Aux.time.sleep(2)
            Lib.Aux.pyautogui.typewrite(Lib.Aux.directories['DownloadFolder'])
            Lib.Aux.pyautogui.typewrite(['enter', 'tab', 'enter'], interval=.2)

            # Do not ask after finish the download.
            Lib.Aux.pyautogui.typewrite(['tab', 'space', 'esc'], interval=.2)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ConfigureSavePath"])

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorConfigureSavePath"], value1=str(ex))
            return "Failed"

    # Save the file locally.
    def saveFile(self, **kwargs):

        try:
            cont_iteration = kwargs.get("cont_iteration")

            Lib.Aux.time.sleep(5)

            while True:
                # The file found means it is still downloading.
                if Lib.Aux.Main.verifyFile(self, path=Lib.Aux.directories['DownloadFolder'], extension='crdownload',
                                           msg_not_found=Lib.Aux.otherConfigs['DownloadFinished']['Msg'],
                                           msg_found=Lib.Aux.otherConfigs['DownloadingFile']['Msg']):
                    Lib.time.sleep(1)
                    continue
                else:
                    # Rename de file.
                    files = Lib.os.listdir(Lib.Aux.directories['DownloadFolder'])
                    for file in files:
                        new_name = 'IT' + str(cont_iteration).zfill(2) + ' - ' + file
                        Lib.os.rename(Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], file),
                                      Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name))
                        Lib.shutil.move(Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name),
                                        Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name))
                    break

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorSaveFile"], value1=str(ex))
            return "Failed"

    # Save the screenshots.
    def takePicture(self, **kwargs):

        try:
            # kwargs variables:
            # test_set_path = kwargs.get("test_set_path")
            image_name = kwargs.get("image_name")

            # Alert print screen.
        #     wait = Lib.WebDriverWait(driver, 1)
        #     if wait.until(lambda driver: driver.switch_to.alert):
        #     # if Lib.ec.alert_is_present()(driver):
        #         Lib.shutil.copyfile(Lib.os.path.join(Lib.os.getcwd(), 'Automation', 'images',
        #                                              Lib.Aux.directories['UnavailablePrint']),
        #                             Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")
        #
        # except Lib.NoAlertPresentException:

            driver.save_screenshot(Lib.Aux.directories['TestSetPath'] + "\\" + image_name + ".png")

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["TakePicture"])

            return True

        except AttributeError or Lib.requests.exceptions.RequestException or Lib.requests.exceptions.RetryError:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorTakePicture"])

            return False

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorTakePicture"], value1=str(ex))

            return False

# --------------------------------------------- API Functions ----------------------------------------------------------
    def request_api(self, **kwargs):

        try:
            # kwargs variables:
            parameters1 = kwargs.get("parameters1")
            api_action = kwargs.get("api_action")
            num_of_steps = kwargs.get("num_of_steps")
            step_order = kwargs.get("step_order")

            # Variables
            Lib.Aux.otherConfigs['API_Step'] = True
            api_status_final = True
            error_msg_list = {}

            if parameters1.upper() != 'SUBMIT':
                tag = parameters1[:parameters1.find(':')]
                if tag.upper() == 'ENDPOINT':
                    Lib.Aux.otherConfigs['API_Endpoint'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'AUTHORIZATION':
                    Lib.Aux.otherConfigs['API_Authorization'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'HEADERS':
                    Lib.Aux.otherConfigs['API_Headers'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'BODY':
                    Lib.Aux.otherConfigs['API_Body'] = (parameters1[parameters1.find(':') + 1:parameters1.rfind('\"')]
                                                    .strip())
                elif tag.upper() == 'PARAMS':
                    Lib.Aux.otherConfigs['API_Params'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == "SCHEMA":
                    if num_of_steps.__len__() != step_order:
                        raise Exception(Lib.Aux.logs['ErrorAPISchema']['Msg'])

                    if Lib.Aux.otherConfigs['API_Body']:
                        dict_body = Lib.ast.literal_eval(Lib.Aux.otherConfigs['API_Body'])
                    else:
                        print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorAPIBodyMissing']['Msg']}"
                              f"{Lib.Aux.Textcolor.END}")
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAPIBodyMissing"])
                        raise TypeError(Lib.Aux.logs['ErrorAPIBodyMissing']['Msg'])
                    json_data = Lib.Aux.ApiSchema(parameters1[parameters1.find(':') + 1:].strip())
                    json_fake_data = json_data.api_check()

                    for tag in json_fake_data.keys():
                        for fake_order, _ in enumerate(json_fake_data[tag]):
                            dict_body[tag] = json_fake_data[tag][fake_order]

                            # Run the API request.
                            error_msg = (
                                self.connections.send_request(api_action=api_action,
                                                              headers=Lib.Aux.otherConfigs['API_Headers'],
                                                              body=dict_body))

                            error_msg_list[tag + ' -> ' + str(dict_body[tag])] = error_msg

                            if Lib.Aux.otherConfigs['API_StatusCode'] == 400:
                                api_status = True
                            else:
                                api_status = False

                            api_status_final = (api_status_final and api_status)

                    Lib.Aux.otherConfigs['API_Response'] = error_msg_list

                    if api_status_final:
                        return "Passed"
                    else:
                        return "Failed"

                if Lib.Aux.otherConfigs['API_Endpoint'] is None:
                    print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorAPIMissingInfo']['Msg']}"
                          f"{Lib.Aux.Textcolor.END}")
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAPIMissingInfo"])
                    raise TypeError(Lib.Aux.logs['ErrorAPIMissingInfo']['Msg'])
            else:
                # Run the API request.
                Lib.Aux.otherConfigs['API_Response'] = (
                    self.connections.send_request(api_action=api_action,
                                                  headers=Lib.Aux.otherConfigs['API_Headers'],
                                                  body=Lib.Aux.otherConfigs['API_Body']))

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorRequestAPI']['Msg']}{Lib.Aux.Textcolor.END}", str(ex))
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRequestAPI"], value1=str(ex))

            return "Failed"

    def responseAPI(self, **kwargs):


        try:
            # kwargs variables:
            parameters1 = kwargs.get("parameters1")
            find_content = None
            status_code = None
            schema = None

            Lib.Aux.otherConfigs['API_Step'] = True

            tag = parameters1[:parameters1.find(':')]
            param = parameters1[parameters1.find(':') + 1:]

            # Status Code.
            if tag.upper() == "STATUS CODE" and int(param) == Lib.Aux.otherConfigs['API_StatusCode']:
                status_code = "Passed"
            elif tag.upper() == "STATUS CODE" and int(param) != Lib.Aux.otherConfigs['API_StatusCode']:
                status_code = "Failed"
            else:  # tag.upper() != "STATUS CODE":
                find_content = Lib.Aux.Main.find_content_json(self, tag=tag, param=param)

            if status_code == "Passed" or find_content == "Passed" or schema == "Passed":
                return "Passed"
            else:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorResponseAPI"],
                                     value1=f"Expected: {tag} - Result {param}")
                return "Failed"

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorResponseAPI']['Msg']}{Lib.Aux.Textcolor.END}", str(ex))
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorResponseAPI"], value1=str(ex))

            return "Failed"
