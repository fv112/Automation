import common_libs as Lib

driver = None


class Main:

    def __init__(self):
        self.connections = Lib.Con.Connections()

    # Function to search the element using the option above.
    def findElement(self, **kwargs):

        # kwargs variables.
        parameters1 = kwargs.get('parameters1')

        color = kwargs.get('color', 'blue')

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

        for tag in search_list:

            try:
                driver.implicitly_wait(1)

                new_element = driver.find_element(tag, parameters1)

                if new_element is not None:
                    # Set element focus.
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_element)

                    Main.highlight(self, new_element=new_element, effect_time=1, color=color, border=3)

                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FindElement"], parameters1=tag,
                                         parameters2=parameters1)

                    return new_element

            except Lib.NoSuchElementException:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["WarningFindElement"], parameters1=tag,
                                     parameters2=parameters1)

    # ---------------------- Action Elements ----------------------
    # Fill the fields.
    def fillField(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.clear()

            if parameters2.upper() not in ('VAZIO', 'VACÍO', 'EMPTY'):
                element_field.send_keys(parameters2)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["FillField"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorFillField"], parameters1=str(ex))

            return "Failed"

    # Don't execute the step.
    def noExecute(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')

        try:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["NoExecute"], parameters1="'" + step + "'")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorNoExecute"],
                                 parameters1="'" + step + "' - " + str(ex))
            return "Failed"

    # Execute a MS-DOS command line.
    def execute(self, **kwargs):

        path = ""

        try:
            # kwargs arguments.
            path = kwargs.get('parameters1')

            Lib.Aux.os.system('start "" "' + path + '"')

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Execute"], parameters1="'" + path + "'")

            return path, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorExecute"],
                                 parameters1="'" + path + "' - " + str(ex))
            return "Failed"

    # Click in an element.
    def click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.click()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Click"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorClick"], parameters1=str(ex))
            return "Failed"

    # Double click.
    def doubleClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.click()
            element_field.click()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["DoubleClick"])

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDoubleClick"], parameters1=str(ex))
            return "Failed"

    # Right click (mouse).
    def rightClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            actions = Lib.ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1)

            actions.context_click(element_field)
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["RightClick"])

            return "Passed"
        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRightClick"], parameters1=str(ex))
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
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDragDrop"], parameters1=str(ex))
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

            actions = Lib.ActionChains(driver)
            element_field1 = Main.findElement(self, parameters1=parameters1)
            element_field2 = Main.findElement(self, parameters1=parameters2)

            actions.drag_and_drop(element_field2, element_field1)
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["DragDropToElement"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorDragDropToElement"], parameters1=str(ex))
            return "Failed"

    # Type keyboard key.
    def pressButton(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')

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

            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["PressButton"],
                                 parameters1=parameters1 + " - " + str(parameters2) + "x")

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorPressButton"],
                                 parameters1=parameters1 + " - " + str(ex))
            return "Failed"

    # Mouse Over.
    def mouseOver(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:

            actions = Lib.ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1)

            actions.move_to_element(element_field)  # Worked with XPath.
            actions.perform()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["MouseOver"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorMouseOver"], parameters1=str(ex))

            return "Failed"

    # Wait.
    def wait(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            Lib.time.sleep(int(parameters1))

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Wait"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorWait"], parameters1=str(ex))

            return "Failed"

    # Select DropDownList.
    def selectDropDownList(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            element_field = Lib.Select(Main.findElement(self, parameters1=parameters1))

            element_field.select_by_visible_text(parameters2)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["SelectDropDownList"], parameters1=parameters2)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorSelectDropDownList"], parameters1=str(ex))

            return "Failed"

    # Get the text from an elements.
    def getText(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            obtained_text = Main.findElement(self, parameters1=parameters1, color="green").text

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
                            Main.findElement(self, parameters1=parameters1, color="green")
                            return textFound.contents[0], "Passed"
                        else:
                            return Lib.Aux.logs["ErrorGetText"]["Msg"], "Failed"
            else:
                return obtained_text, "Passed"

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetText"])

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetText"], parameters1=str(ex))

            return Lib.Aux.logs["ErrorGetText"]['Msg'], "Failed"

    @staticmethod
    def openNewTab():
        try:

            driver.execute_script("window.open('', '_blank')")

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["OpenNewTab"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenNewTab"], parameters1=str(ex))

            return "Failed"

    # Get current url
    @staticmethod
    def getURL():
        try:

            url = driver.current_url
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetURL"])

            return url, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetURL"], parameters1=str(ex))

            return None, "Failed"

    # get Title
    @staticmethod
    def getTitle():

        try:

            title = driver.title
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetTitle"])

            return title, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetTitle"], parameters1=str(ex))

            return None, "Failed"

    # Back Page
    @staticmethod
    def backPage():

        try:

            driver.back()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["BackPage"])

            return driver, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorBackPage"], parameters1=str(ex))

            return "Failed"

    # Back Page.
    @staticmethod
    def forwardPage():

        try:

            driver.forward()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ForwardPage"])

            return driver, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorForwardPage"], parameters1=str(ex))

            return "Failed"

    # Gets the attribute of an element (can be value, title or href).
    def getAttribute(self, **kwargs):

        # kwargs arguments.
        element = kwargs.get('element')
        parameters1 = kwargs.get('parameters1')
        parameters2 = kwargs.get('parameters2')

        obtained_attribute = ''
        text_found = None

        try:

            if '(#value)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1)
                text_found = page.get_attribute('value')

            elif '(#title)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1)
                text_found = page.get_attribute('title')

            elif '(#href)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1)
                text_found = page.get_attribute('href')

            elif '(#class)' in parameters2:
                page = Main.findElement(self, parameters1=parameters1)
                text_found = page.get_attribute('class')

            else:
                raise "Tag not correct."

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetAttribute"])

            return text_found, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetAttribute"], parameters1=str(ex))

            return text_found, "Failed"

    def getQuantityElements(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        search_list = (
            Lib.By.ID,
            Lib.By.NAME,
            Lib.By.XPATH,
            Lib.By.CSS_SELECTOR,
            Lib.By.CLASS_NAME,
            Lib.By.TAG_NAME,
            Lib.By.LINK_TEXT,
            Lib.By.PARTIAL_LINK_TEXT
        )

        x = 0

        for tag in search_list:

            try:

                driver.implicitly_wait(3)
                new_element = driver.find_elements(tag, parameters1)
                elements = len(new_element)

                if elements > 0:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["GetQuantityElements"], parameters1=tag,
                                         parameters2=parameters1)
                    return elements, "Passed"

                elif x > 8:
                    return elements, "Passed"

                x += 1

            except Lib.NoSuchElementException:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorGetQuantityElements"], parameters1=tag,
                                     parameters2=parameters1)
                return None, "Failed"

    # Scroll Page
    def scrollPage(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            driver.execute_script('window.scrollTo(0, ' + parameters1 + ')')
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ScrollPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorScrollPage"], parameters1=str(ex))

            return "Failed"

    # Refresh Page
    def refreshPage(self):
        try:

            driver.refresh()
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["RefreshPage"])

            return driver, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRefreshPage"], parameters1=str(ex))

            return "Failed"

    # Checks whether the element is inactive.
    def isEnable(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        status_element = None

        try:
            status_element = Main.findElement(self, parameters1=parameters1).is_enabled()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsEnable"])

            return status_element, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsEnable"], parameters1=str(ex))
            return status_element, "Failed"

    # Checks whether the element is visible.
    def isDisplayed(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        status_element = None

        try:
            status_element = Main.findElement(self, parameters1=parameters1).is_displayed()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsDisplayed"])

            return status_element, "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsDisplayed"], parameters1=str(ex))

            return status_element, "Failed"

    # Checks whether a checkbox or radio button is selected (returns True or False)
    def isSelected(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:

            status_element = Main.findElement(self, parameters1=parameters1).is_selected()

            if status_element:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["IsSelected"])
                return "True", "Passed"
            else:
                return "False", "Failed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorIsSelected"], parameters1=str(ex))
            return "False", "Failed"

    # Validate data (With * validate the partial text).
    def validateData(self, **kwargs):
        try:
            # kwargs arguments.
            alert = kwargs.get('alert')
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            if alert != 'AlertScreen':

                # Get the title page.
                if '(title)' in parameters1:
                    text_found, status = Main.getTitle()
                    parameters2 = parameters1.replace('(title)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the URL from the address bar (getURL).
                elif '(url)' in parameters1:
                    text_found, status = Main.getURL()
                    parameters2 = parameters1.replace('(url)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])

                        parameters2 = parameters1.replace('(url)', '')
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check a part of the text was found.
                elif '*' in parameters2:  # Check part of the text.
                    text_found, status = Main.getText(self, parameters1=parameters1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if parameters2.replace('*', '') in text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is active or inactive.
                elif '(?)' in parameters2:
                    text_found, status = Main.isEnable(self, parameters1=parameters1)
                    text_found = str(text_found)
                    parameters2 = parameters2.replace('(?)', '')

                    if text_found == parameters2:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is visible to the user.
                elif '($)' in parameters2:
                    text_found, status = Main.isDisplayed(self, parameters1=parameters1)
                    text_found = str(text_found)
                    parameters2 = parameters2.replace('($)', '')

                    if text_found == parameters2:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether a checkbox or radio button is selected.
                elif '(.)' in parameters2:
                    text_found, status = Main.isSelected(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(.)', '')

                    if str(text_found) == parameters2:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if data is not available.
                elif '(!=)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(!=)', ' - ')

                    if parameters2 not in str(text_found):
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if the data is available.
                elif '(!)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(!)', '')

                    if parameters2 in str(text_found):
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check some attributes.
                elif ('(#title)' in parameters2 or '(#href)' in parameters2 or '(#value)' in parameters2 or '(#class)'
                      in parameters2):
                    text_found, status = Main.getAttribute(self, parameters1=parameters1, parameters2=parameters2)
                    parameters2 = parameters2.replace('(#title)', '')
                    parameters2 = parameters2.replace('(#href)', '')
                    parameters2 = parameters2.replace('(#value)', '')
                    parameters2 = parameters2.replace('(#class)', '')

                    if parameters2 == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the amount of elements. # ---> OK.
                elif '<' and '>' in parameters2:
                    text_found, status = Main.getQuantityElements(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('<', '')
                    parameters2 = parameters2.replace('>', '')

                    if int(parameters2) == text_found:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"
                        text_found = str(text_found)

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"
                        text_found = str(text_found)

                # Validates that the text obtained from the page is the same as the expected text.
                else:
                    text_found, status = Main.getText(self, parameters1=parameters1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if text_found == parameters2:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                        status = "Failed"

            else:  # If Alert Element.
                alert = driver.switch_to.alert()
                text_found = alert.text

                if parameters2 == text_found:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ValidateData"])
                    status = "Passed"

                else:
                    Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorValidateData"])
                    status = "Failed"

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataExpected'],
                                 value1=parameters2)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs['ValidateDataObtained'],
                                 value1=text_found)

            return status

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorFunctionValidateData"], parameters1=str(ex))
            return "Failed"

    # Alter (Verify iFrame or Windows).
    def alter(self, **kwargs):
        try:

            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            if parameters1 is None:
                Main.alterWindow(self)

            elif parameters1.upper() == 'IFRAME':
                Main.alterFrame(self, parameters2=parameters2)

            elif parameters1.upper() == 'ALERT':
                Main.alterAlertOK(self)

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlter"], parameters1=str(ex))
            return "Failed"

    # Alter window.
    def alterWindow(self):
        try:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterWindow"], parameters1=str(ex))
            return "Failed"

    # Alter IFrame.
    def alterFrame(self, **kwargs):
        try:
            # kwargs arguments.
            parameters2 = kwargs.get('parameters2')

            # Store iframe web element
            iframe = Main.findElement(self, parameters1=parameters2)

            # switch to selected iframe
            driver.switch_to.frame(iframe)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterIframe"], parameters1=str(ex))
            return "Failed"

    # Alter Alert and Click OK.
    def alterAlertOK(self):
        try:

            alert = driver.switch_to.alert
            alert.accept()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["AlterAlert"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorAlterAlert"], parameters1=str(ex))
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
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnDefault"], parameters1=str(ex))
            return "Failed"

    # Return to window.
    def returnWindow(self):
        try:
            driver.switch_to.window(driver.window_handles[0])

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ReturnWindow"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnWindow"], parameters1=str(ex))
            return "Failed"

    # Return to default.
    def returnFrame(self):
        try:

            driver.switch_to.default_content()

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ReturnIframe"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorReturnIframe"], parameters1=str(ex))
            return "Failed"

    # Choose an option in a browser alert screen.
    def inform(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            wait = Lib.WebDriverWait(driver, timeout=2)
            alert = wait.until(lambda d: d.switch_to.alert)

            # Validate de Alert content (Text).
            if parameters2 is not None:
                status = Main.validateData(self, alert='AlertScreen', parameters1=alert.text, parameters2=parameters2)

            # Actions inside de Alert.
            if parameters1.upper() in ("OK", "ACEPTAR"):
                alert.accept()
                Lib.time.sleep(3)

            elif parameters1.upper() in ("CANCELAR", "CANCEL"):
                alert.dismiss()
                Lib.time.sleep(3)

            else:  # Fill the Alert textbox.
                alert.send_keys(parameters1)
                Lib.time.sleep(3)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["Inform"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorInform"], parameters1=str(ex))
            return "Failed"

    # Function to create the browser object.
    def openBrowser(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            enable_cookie = kwargs.get('enable_cookie')

            global driver

            # Configure before open the browser.
            if parameters1.upper() in ("CHROME", "GOOGLE", "GOOGLE CHROME"):
                # Disable the Chrome logs in the .bat file and alter the download folder.
                preferences = {
                    "download.default_directory": Lib.Aux.directories['DownloadFolderTemp'],
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
                options = Lib.webdriver.ChromeOptions()

                # If cookies are enabled.
                if enable_cookie:
                    options.add_argument('--profile-directory=Default')
                    options.add_argument('--user-data-dir=' + Lib.Aux.directories["Temp"] + 'CHROME')

                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("prefs", preferences)

                driver = Lib.webdriver.Chrome(service=Lib.ChromeService(Lib.ChromeDriverManager().install()),
                                              options=options)

            # Configure before open the browser.
            elif parameters1.upper() in ("MOZILLA", "FIREFOX"):
                profile = Lib.webdriver.FirefoxProfile()
                profile.set_preference("browser.download.dir", Lib.Aux.directories['DownloadFolderTemp'])
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.panel.shown", True)
                profile.set_preference("marionette.actors.enabled", False)
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

                preferences = {
                    "download.default_directory": Lib.Aux.directories['DownloadFolderTemp'],
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                }
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_experimental_option("prefs", preferences)
                driver = Lib.webdriver.Edge(service=Lib.EdgeService(Lib.EdgeChromiumDriverManager().install()), options=options)

            else:
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"])
                return "Failed"

            Lib.Aux.otherConfigs['Browser'] = parameters1
            driver.maximize_window()
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
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenBrowser"], parameters1=str(ex))

            return "Failed"

    # Verify is the browser is still opened.
    def verifyBrowser(self):

        try:
            if driver.current_url:
                driver.close()

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorVerifyBrowser"], parameters1=str(ex))
            return "Failed"

    # Close (windows or the whole browser).
    def close(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            if parameters1 is None:  # If none was informed = Close Windows.
                driver.close()
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["CloseWindow"])
            else:  # If something was informed = Close Browser.
                driver.quit()
                Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["CloseBrowser"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorClose"], parameters1=str(ex))
            return "Failed"

    # Open page address.
    def openPage(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            driver.get(parameters1)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["OpenPage"])

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorOpenPage"], parameters1=str(ex))

            return "Failed"

    # Highlight the component during the execution.
    def highlight(self, **kwargs):

        try:
            # kwargs variables.
            new_element = kwargs.get('new_element')
            effect_time = kwargs.get('effect_time')
            color = kwargs.get('color')
            border = kwargs.get('border')

            def apply_style(style):
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", new_element, style)

            original_style = new_element.get_attribute('style')
            apply_style("border: {0}px solid {1};".format(border, color))
            Lib.time.sleep(effect_time)
            apply_style(original_style)

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorHighLight"], parameters1=str(ex))

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
            Lib.Aux.pyautogui.typewrite(Lib.Aux.directories['DownloadFolderTemp'])
            Lib.Aux.pyautogui.typewrite(['enter', 'tab', 'enter'], interval=.2)

            # Do not ask after finish the download.
            Lib.Aux.pyautogui.typewrite(['tab', 'space', 'esc'], interval=.2)

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ConfigureSavePath"])

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorConfigureSavePath"], parameters1=str(ex))
            return "Failed"

    # Save the file locally.
    def saveFile(self, **kwargs):

        cont_iteration = kwargs.get("cont_iteration")

        try:
            Lib.Aux.time.sleep(5)
            while True:
                # The file found means it is still downloading.
                if Lib.Aux.Main.verifyFile(self, path=Lib.Aux.directories['DownloadFolderTemp'], extension='crdownload',
                                           msg_not_found=Lib.Aux.otherConfigs['DownloadFinished']['Msg'],
                                           msg_found=Lib.Aux.otherConfigs['DownloadingFile']['Msg']):
                    Lib.time.sleep(1)
                    continue
                else:
                    # Rename de file.
                    files = Lib.os.listdir(Lib.Aux.directories['DownloadFolderTemp'])
                    for file in files:
                        new_name = 'IT' + str(cont_iteration).zfill(2) + ' - ' + file
                        Lib.os.rename(Lib.os.path.join(Lib.Aux.directories['DownloadFolderTemp'], file),
                                      Lib.os.path.join(Lib.Aux.directories['DownloadFolderTemp'], new_name))
                        Lib.shutil.move(Lib.os.path.join(Lib.Aux.directories['DownloadFolderTemp'], new_name),
                                        Lib.os.path.join(Lib.Aux.directories['DownloadFolder'], new_name))
                    break

            return "Passed"

        except Exception as ex:
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorSaveFile"], parameters1=str(ex))
            return "Failed"

    # Save the screenshots.
    def takePicture(self, **kwargs):

        # kwargs variables:
        test_set_path = kwargs.get("test_set_path")
        image_name = kwargs.get("image_name")

        try:
            # Alert print screen.
            if Lib.ec.alert_is_present()(driver):
                Lib.time.sleep(1)
                Lib.shutil.copyfile(Lib.os.path.join(Lib.Aux.os.getcwd(), 'Automation', 'images',
                                                     Lib.Aux.directories['UnavailablePrint']),
                                    test_set_path + "\\" + image_name + ".png")

            else:
                driver.save_screenshot(test_set_path + "\\" + image_name + ".png")

            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["TakePicture"])

            return True

        except AttributeError or Lib.requests.exceptions.RequestException or Lib.requests.exceptions.RetryError:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}{Lib.Aux.Textcolor.END}")
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorTakePicture"])

            return False

        except Exception as ex:
            print(f"{Lib.Aux.Textcolor.FAIL}{Lib.Aux.logs['ErrorTakePicture']['Msg']}{Lib.Aux.Textcolor.END}", ex)
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorTakePicture"])

            return False

# --------------------------------------------- API Functions ----------------------------------------------------------
    def request_api(self, **kwargs):

        # kwargs variables:
        parameters1 = kwargs.get("parameters1")
        api_action = kwargs.get("api_action")
        num_of_steps = kwargs.get("num_of_steps")
        actual_step = kwargs.get("actual_step")

        # Variables
        Lib.Aux.otherConfigs['API_Step'] = True
        api_status_final = True
        error_msg_list = {}

        try:
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
                    if num_of_steps.__len__() != actual_step:
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
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorRequestAPI"])

            return "Failed"

    def responseAPI(self, **kwargs):

        # kwargs variables:
        parameters1 = kwargs.get("parameters1")
        find_content = None
        status_code = None
        schema = None

        Lib.Aux.otherConfigs['API_Step'] = True

        try:
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
            Lib.Aux.Main.addLogs(message="General", value=Lib.Aux.logs["ErrorResponseAPI"])

            return "Failed"
