import time

import requests
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from msedge.selenium_tools import Edge, EdgeOptions  # It is necessary to install the Edge in the PC.
from bs4 import BeautifulSoup

import modules.automationAux as Aux
import modules.azureConnection as Azure

driver = None


class Main:

    def __init__(self):
        pass

    # Function to search the element using the option above.
    def findElement(self, **kwargs):

        # kwargs variables.
        value1 = kwargs.get('value1')
        color = kwargs.get('color', 'blue')

        search_list = (
            By.ID,
            By.NAME,
            By.XPATH,
            By.CSS_SELECTOR,
            By.CLASS_NAME,
            By.TAG_NAME,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT
        )

        for tag in search_list:
            try:
                driver.implicitly_wait(3)
                newelement = driver.find_element(tag, value1)

                if newelement != None:
                    Main.highlight(self, newelement=newelement, effect_time=1, color=color, border=3)

                    Aux.Main.addLogs(self, message="General", value=Aux.logs["FindElement"], value1=tag, value2=value1)

                    return newelement

            except NoSuchElementException:
                Aux.Main.addLogs(self, message="General", value=Aux.logs["WarningFindElement"], value1=tag,
                                 value2=value1)

    # ---------------------- Action Elements ----------------------
    # Fill the fields.
    def fillField(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            element_field = Main.findElement(self, value1=value1)
            element_field.clear()

            if value2.upper() not in ('VAZIO', 'VACÍO', 'EMPTY'):
                element_field.send_keys(value2)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["FillField"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorFillField"], value1=str(ex))
            return "Failed"

    # Don't execute the step.
    def noExecute(self, **kwargs):
        try:
            # kwargs arguments.
            step = kwargs.get('step')
            Aux.Main.addLogs(self, message="General", value=Aux.logs["NoExecute"], value1="'" + step + "'")

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorNoExecute"], value1="'" + step + "' - " +
                                                                                               str(ex))
            return "Failed"

    # Execute a MS-DOS command line.
    def execute(self, **kwargs):
        try:
            # kwargs arguments.
            path = kwargs.get('value1')

            Aux.os.system('start "" "' + path + '"')

            Aux.Main.addLogs(self, message="General", value=Aux.logs["Execute"], value1="'" + path + "'")

            return path, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorExecute"], value1="'" + path + "' - " +
                                                                                             str(ex))
            return "Failed"

    # Click in an element.
    def click(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            element_field = Main.findElement(self, value1=value1)
            element_field.click()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["Click"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorClick"], value1=str(ex))
            return "Failed"

    # Double click.
    def doubleClick(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            element_field = Main.findElement(self, value1=value1)
            element_field.click()
            element_field.click()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["DoubleClick"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorDoubleClick"], value1=str(ex))
            return "Failed"

    # Right click (mouse).
    def rightClick(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            actions = ActionChains(driver)
            element_field = Main.findElement(self, value1=value1)

            actions.context_click(element_field)
            actions.perform()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["RightClick"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorRightClick"], value1=str(ex))
            return "Failed"

    # Drag and drop.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """
    def dragDrop(self, **kwargs):
        try:
            # kwargs arguments.

            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            actions = ActionChains(driver)
            source = Main.findElement(self, value1=value1)
            target = Main.findElement(self, value1=value2)

            positions = value2.split(":")
            positionx = positions[0]
            positionx = positionx[1:]  # Only the numeric number.
            positiony = positions[1]
            positiony = positiony[1:]  # Only the numeric number.

            actions.drag_and_drop_by_offset(element_field, int(positionx) * 10, int(positiony) * 10)
            actions.perform()

            Aux.Main.addLogs(self, message="General", value=Aux.logs['DragDrop'])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorDragDrop"], value1=str(ex))
            return "Failed"

    # Drag and drop to the other component.
    """
    COMMENT: ERROR IN THE SELENIUM ACTION.

    """
    def dragDropToElement(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            actions = ActionChains(driver)
            element_field1 = Main.findElement(self, value1=value1)
            element_field2 = Main.findElement(self, value1=value2)

            actions.drag_and_drop(element_field2, element_field1)
            actions.perform()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["DragDropToElement"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorDragDropToElement"], value1=str(ex))
            return "Failed"

    # Type keyboard key.
    def pressButton(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')
            list_steps = kwargs.get('list_steps')

            Desktop_TC = False

            if value2 is None:
                value2 = 1
            value2 = int(value2)
            value1 = str(value1)

            Desktop_TC = Aux.Main._checkDesktop_TC(self, list_steps=list_steps)

            if not Desktop_TC:
                actions = ActionChains(driver)

            if value1.upper() == 'RETURN' or value1.upper() == 'ENTER':
                for _ in range(value2): actions.send_keys(Keys.RETURN)
            elif value1.upper() == 'UP':
                for _ in range(value2): actions.send_keys(Keys.UP)
            elif value1.upper() == 'PAGE UP':
                for _ in range(value2): actions.send_keys(Keys.PAGE_UP)
            elif value1.upper() == 'DOWN':
                for _ in range(value2): actions.send_keys(Keys.DOWN)
            elif value1.upper() == 'PAGE DOWN':
                for _ in range(value2): actions.send_keys(Keys.PAGE_DOWN)
            elif value1.upper() == 'LEFT':
                for _ in range(value2): actions.send_keys(Keys.LEFT)
            elif value1.upper() == 'RIGHT':
                for _ in range(value2): actions.send_keys(Keys.RIGHT)
            elif value1.upper() == 'TAB':
                for _ in range(value2): actions.send_keys(Keys.TAB)
            elif value1.upper() == 'SPACE':
                for _ in range(value2): actions.send_keys(Keys.SPACE)
            elif value1.upper() == 'BACKSPACE':
                for _ in range(value2): actions.send_keys(Keys.BACKSPACE)
            elif value1.upper() == 'DELETE':
                for _ in range(value2): actions.send_keys(Keys.DELETE)
            # Alt or Ctrl + <any other key>.
            elif value1.upper().__contains__('CTRL') or value1.upper().__contains__('ALT'):
                for _ in range(value2):
                    Aux.pyautogui.keyDown(value1.upper().rsplit('+')[0])
                    Aux.time.sleep(.2)
                    Aux.pyautogui.keyDown(value1.upper().rsplit('+')[1])
                    Aux.time.sleep(.2)
                    Aux.pyautogui.keyUp(value1.upper().rsplit('+')[0])

            if not Desktop_TC:
                actions.perform()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["PressButton"],
                             value1=value1 + " - " + str(value2) + "x")

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorPressButton"],
                             value1=value1 + " - " + str(ex))
            return "Failed"

    # Mouse Over.
    def mouseOver(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            actions = ActionChains(driver)
            element_field = Main.findElement(self, value1=value1)

            actions.move_to_element(element_field)  # Funcionou com XPath
            actions.perform()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["MouseOver"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorMouseOver"], value1=str(ex))
            return "Failed"

    # Wait.
    def wait(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            Aux.time.sleep(int(value1))

            Aux.Main.addLogs(self, message="General", value=Aux.logs["Wait"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorWait"], value1=str(ex))
            return "Failed"

    # Select DropDownList.
    def selectDropDownList(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            element_field = Select(Main.findElement(self, value1=value1))

            element_field.select_by_visible_text(value2)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["SelectDropDownList"], value1=value2)

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorSelectDropDownList"], value1=str(ex))

            return "Failed"

    # Get the text from a elements.
    def getText(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            ObtainedText = Main.findElement(self, value1=value1, color="green").text

            if ObtainedText is None:
                headers = {'User-Agent': Aux.otherConfigs['Agent']}
                conteudo = Aux.request.get(driver.current_url, headers=headers).content
                soup = BeautifulSoup(conteudo, 'html.parser')

                for tag in Aux.searchForAttribute:
                    for component in Aux.searchForComponent:
                        table = soup.findAll(Aux.searchForComponent[component],
                                             attrs={Aux.searchForAttribute[tag]: value1})
                        for textFound in table:
                            Aux.Main.addLogs(self, message="General", value=Aux.logs["GetText"])
                            Main.findElement(self, value1=value1, color="green")
                            return textFound.contents[0], "Passed"
                        else:
                            return Aux.logs["ErrorGetText"]["Msg"], "Failed"
            else:
                return ObtainedText, "Passed"

            Aux.Main.addLogs(self, message="General", value=Aux.logs["GetText"])

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorGetText"])

            return Aux.logs["ErrorGetText"]['Msg'], "Failed"

    def openNewTab(self, **kwargs):
        try:

            driver.execute_script("window.open('', '_blank')")

            Aux.Main.addLogs(self, message="General", value=Aux.logs["OpenNewTab"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorOpenNewTab"], value1=str(ex))

            return "Failed"

    # Get current url
    def getURL(self):
        try:

            URL = driver.current_url
            Aux.Main.addLogs(self, message="General", value=Aux.logs["GetURL"])

            return URL, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorGetURL"], value1=str(ex))
            return None, "Failed"

    # get Title
    def getTitle(self):
        try:

            title = driver.title
            Aux.Main.addLogs(self, message="General", value=Aux.logs["GetTitle"])

            return title, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorGetTitle"], value1=str(ex))
            return None, "Failed"

    # Back Page
    def backPage(self):
        try:

            driver.back()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["BackPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorBackPage"], value1=str(ex))
            return "Failed"

    # Back Page.
    def forwardPage(self):
        try:

            driver.forward()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ForwardPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorForwardPage"], value1=str(ex))
            return "Failed"

    # Gets the attribute of an element (can be value, title or href).
    def getAttribute(self, **kwargs):

        try:
            # kwargs arguments.
            element = kwargs.get('element')
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            ObtainedAttribute = ''

            if '(#value)' in value2:
                page = Main.findElement(self, value1=value1)
                text_found = page.get_attribute('value')

            elif '(#title)' in value2:
                page = Main.findElement(self, value1=value1)
                text_found = page.get_attribute('title')

            elif '(#href)' in value2:
                page = Main.findElement(self, value1=value1)
                text_found = page.get_attribute('href')

            elif '(#class)' in value2:
                page = Main.findElement(self, value1=value1)
                text_found = page.get_attribute('class')

            else:
                raise "Tag not correct."

            Aux.Main.addLogs(self, message="General", value=Aux.logs["GetAttribute"])

            return text_found, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorGetAttribute"], value1=str(ex))
            return text_found, "Failed"

    def getQuantityElements(self, **kwargs):

        # kwargs arguments.
        value1 = kwargs.get('value1')

        search_list = (
            By.ID,
            By.NAME,
            By.XPATH,
            By.CSS_SELECTOR,
            By.CLASS_NAME,
            By.TAG_NAME,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT
        )

        x = 0

        for tag in search_list:

            try:

                driver.implicitly_wait(3)
                newelement = driver.find_elements(tag, value1)
                elements = len(newelement)

                if elements > 0:
                    Aux.Main.addLogs(self, message="General", value=Aux.logs["GetQuantityElements"], value1=tag,
                                     value2=value1)
                    return elements, "Passed"

                elif x > 8:
                    return elements, "Passed"

                x += 1

            except NoSuchElementException:
                Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorGetQuantityElements"], value1=tag,
                                 value2=value1)
                return None, "Failed"

    # Scroll Page
    def scrollPage(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            driver.execute_script('window.scrollTo(0, ' + value1 + ')')
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ScrollPage"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorScrollPage"], value1=str(ex))
            return "Failed"

    # Refresh Page
    def refreshPage(self):
        try:

            driver.refresh()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["RefreshPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorRefreshPage"], value1=str(ex))
            return "Failed"

    # Checks whether the element is inactive.
    def isEnable(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            statusElement = Main.findElement(self, value1=value1).is_enabled()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["IsEnable"])

            return statusElement, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorIsEnable"])
            return statusElement, "Failed"

    # Checks whether the element is visible.
    def isDisplayed(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            statusElement = Main.findElement(self, value1=value1).is_displayed()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["IsDisplayed"])

            return statusElement, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorIsDisplayed"], value1=str(ex))
            return statusElement, "Failed"

    # Checks whether a checkbox or radio button is selected (returns True or False)
    def isSelected(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            statusElement = Main.findElement(self, value1=value1).is_selected()

            if statusElement:
                Aux.Main.addLogs(self, message="General", value=Aux.logs["IsSelected"])
                return "True", "Passed"
            else:
                return "False", "Failed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorIsSelected"], value1=str(ex))
            return "False", "Failed"

    # Validade data (With * validate the partial text).
    def validateData(self, **kwargs):
        try:
            # kwargs arguments.
            alert = kwargs.get('alert')
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            if alert != 'AlertScreen':

                # Get the title page.
                if '(title)' in value1:
                    text_found, status = Main.getTitle(self)
                    value2 = value1.replace('(title)', '')

                    if value2 == text_found:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the URL from the adress bar (getURL).
                elif '(url)' in value1:
                    text_found, status = Main.getURL(self)
                    value2 = value1.replace('(url)', '')

                    if value2 == text_found:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])

                        value2 = value1.replace('(url)', '')
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check a part of the text was found.
                elif '*' in value2:  # If it only part of text.
                    text_found, status = Main.getText(self, value1=value1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if value2.replace('*', '') in text_found:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is active or inactive.
                elif '(?)' in value2:
                    text_found, status = Main.isEnable(self, value1=value1)
                    text_found = str(text_found)
                    value2 = value2.replace('(?)', '')

                    if text_found == value2:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is visible to the user.
                elif '($)' in value2:
                    text_found, status = Main.isDisplayed(self, value1=value1)
                    text_found = str(text_found)
                    value2 = value2.replace('($)', '')

                    if text_found == value2:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether a checkbox or radio button is selected.
                elif '(.)' in value2:
                    text_found, status = Main.isSelected(self, value1=value1)
                    value2 = value2.replace('(.)', '')

                    if str(text_found) == value2:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if data is not available.
                elif '(!=)' in value2:
                    text_found, status = Main.getText(self, value1=value1)
                    value2 = value2.replace('(!=)', ' - ')

                    if value2 not in str(text_found):
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if the data is available.
                elif '(!)' in value2:
                    text_found, status = Main.getText(self, value1=value1)
                    value2 = value2.replace('(!)', '')

                    if value2 in str(text_found):
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check some attributes.
                elif '(#title)' in value2 or '(#href)' in value2 or '(#value)' in value2 or '(#class)' in value2:
                    text_found, status = Main.getAttribute(self, value1=value1, value2=value2)
                    value2 = value2.replace('(#title)', '')
                    value2 = value2.replace('(#href)', '')
                    value2 = value2.replace('(#value)', '')
                    value2 = value2.replace('(#class)', '')

                    if value2 == text_found:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the amount of elements. # ---> OK.
                elif '<' and '>' in value2:
                    text_found, status = Main.getQuantityElements(self, value1=value1)
                    value2 = value2.replace('<', '')
                    value2 = value2.replace('>', '')

                    if int(value2) == text_found:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"
                        text_found = str(text_found)

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"
                        text_found = str(text_found)

                # Validates that the text obtained from the page is the same as the expected text.
                else:
                    text_found, status = Main.getText(self, value1=value1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if text_found == value2:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

            else:  # If Alert Element.
                alert = driver.switch_to_alert()
                text_found = alert.text

                if value2 == text_found:
                    Aux.Main.addLogs(self, message="General", value=Aux.logs["ValidateData"])
                    status = "Passed"

                else:
                    Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorValidateData"])
                    status = "Failed"

            Aux.Main.addLogs(self, message="General", value=Aux.logs['ValidateDataExpected'], value1=value2)
            Aux.Main.addLogs(self, message="General", value=Aux.logs['ValidateDataObtained'], value1=text_found)

            return status

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorFunctionValidateData"], value1=str(ex))
            return "Failed"

    # Alter (Verify iFrame or Windows).
    def alter(self, **kwargs):
        try:

            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            if value1 is None:
                Main.alterWindow(self)

            elif value1.upper() == 'IFRAME':
                Main.alterFrame(self, value2=value2)

            elif value1.upper() == 'ALERT':
                Main.alterAlertOK(self)

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorAlter"], value1=str(ex))
            return "Failed"

    # Alter window.
    def alterWindow(self, **kwargs):
        try:
            for handle in driver.window_handles:
                driver.switch_to_window(handle)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["AlterWindow"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorAlterWindow"], value1=str(ex))
            return "Failed"

    # Alter IFrame.
    def alterFrame(self, **kwargs):
        try:
            # kwargs arguments.
            value2 = kwargs.get('value2')

            # Store iframe web element
            iframe = Main.findElement(self, value1=value2)

            # switch to selected iframe
            driver.switch_to.frame(iframe)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["AlterIframe"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorAlterIframe"], value1=str(ex))
            return "Failed"

    # Alter Alert and Click OK.
    def alterAlertOK(self):
        try:

            alert = driver.switch_to.alert
            alert.accept()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["AlterAlert"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorAlterAlert"], value1=str(ex))
            return "Failed"

    # Return to default.
    def returnDefault(self, **kwargs):
        try:

            # kwargs arguments.
            value1 = kwargs.get('value1')

            if value1 is None:
                Main.returnWindow(self)

            elif value1.upper() == 'IFRAME':

                Main.returnFrame(self)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["ReturnDefault"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorReturnDefault"], value1=str(ex))
            return "Failed"

    # Return to window.
    def returnWindow(self):
        try:
            driver.switch_to.window(driver.window_handles[0])

            Aux.Main.addLogs(self, message="General", value=Aux.logs["ReturnWindow"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorReturnWindow"], value1=str(ex))
            return "Failed"

    # Return to default.
    def returnFrame(self):
        try:

            driver.switch_to.default_content()

            Aux.Main.addLogs(self, message="General", value=Aux.logs["ReturnIframe"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorReturnIframe"], value1=str(ex))
            return "Failed"

    # Choose an option in a browser alert screen.
    def inform(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            value2 = kwargs.get('value2')

            alert = driver.switch_to_alert()

            # Validate de Alert content (Text).
            if value2 != None:
                status = Main.validateData(self, alert='AlertScreen', value1=alert.text, value2=value2)

            # Actions inside de Alert.
            if value1.upper() in ("OK", "ACEPTAR"):
                alert.accept()
                time.sleep(3)

            elif value1.upper() in ("CANCELAR", "CANCEL"):
                alert.dismiss()
                time.sleep(3)

            else:  # Fill the Alert textbox.
                alert.send_keys(value1)
                time.sleep(3)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["Inform"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorInform"], value1=str(ex))
            return "Failed"

    # Function to create the browser object.
    def openBrowser(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')
            change_download_config = kwargs.get('change_download_config')
            enable_cookie = kwargs.get('enable_cookie')

            global driver

            # Configure before open the browser.
            if value1.upper() in ("CHROME", "GOOGLE", "GOOGLE CHROME"):
                # Disable the Chrome logs in the .bat file and alter the download folder.
                preferences = {
                    "download.default_directory": Aux.directories['DownloadFolderTemp'],
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
                options = webdriver.ChromeOptions()

                # If cookies are enabled.
                if enable_cookie:
                    options.add_argument('--profile-directory=Default')
                    options.add_argument('--user-data-dir=' + Aux.directories["Temp"] + 'CHROME')

                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("prefs", preferences)
                driver = webdriver.Chrome(Aux.directories["WebDriverChrome"], chrome_options=options, options=options)

            # Configure before open the browser.
            elif value1.upper() in ("MOZILLA", "FIREFOX"):
                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.download.dir", Aux.directories['DownloadFolderTemp'])
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
                driver = webdriver.Firefox(executable_path=Aux.directories["WebDriverFirefox"], firefox_profile=profile)

            # Change inside the Save function.
            elif value1.upper() in ("IE", "INTERNET", "INTERNET EXPLORER"):  # Internet Explorer 11

                options = webdriver.IeOptions()
                options.add_argument('-private')
                options.ignore_zoom_level = True
                options.set_capability("silent", True)
                options.ignore_protected_mode_settings = True
                options.initial_browser_url("")

                if not change_download_config:
                    driver = webdriver.Ie(Aux.directories["WebDriverIE"], options=options)
                else:
                    print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['DownloadingFileIE']['Msg']}"
                          f"{Aux.Textcolor.END}")
                    Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs["DownloadingFileIE"])

                    return "Aborted"

            # Change inside the Save function.
            elif value1.upper() in ("LEGACY", "ANTIGO"):  # Edge Legacy.
                Aux.otherConfigs['Browser'] = value1.upper()

                if change_download_config:
                    Main._resetEdgeLegacy(self)
                    Aux.time.sleep(5)
                    driver = webdriver.Edge(executable_path=Aux.directories["WebDriverEdgeLegacy"], port=9515)
                    Main._configureSavePath(self)
                else:
                    driver = webdriver.Edge(executable_path=Aux.directories["WebDriverEdgeLegacy"], port=9515)

            # Configure before open the browser.
            elif value1.upper() in "EDGE":  # Edge Chromium.
                options = EdgeOptions()
                options.use_chromium = True
                options.ensure_clean_session = True  # Set blank user.
                options.add_argument("-inprivate")

                # If Cookies are enabled.
                if enable_cookie:
                    options.add_argument('--profile-directory=Default')
                    options.add_argument('--user-data-dir=' + Aux.directories["Temp"] + 'EDGE_CHROMIUM')

                preferences = {
                    "download.default_directory": Aux.directories['DownloadFolderTemp'],
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                }
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_experimental_option("prefs", preferences)
                driver = Edge(executable_path=Aux.directories["WebDriverEdge"], port=9516, options=options)

            else:
                Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorOpenBrowser"])
                return "Failed"

            Aux.otherConfigs['Browser'] = value1
            driver.maximize_window()
            Main.openPage(self, value1=Aux.otherConfigs["HomePage"])

            Aux.Main.addLogs(self, message="General", value=Aux.logs["OpenBrowser"])

            # Set the page load timeout (receive in minutes from interface).
            driver.set_page_load_timeout(int(Aux.otherConfigs['TimeoutSession']) * 60)

            return "Passed"

        except requests.exceptions.RequestException:
            Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorFindBrowser']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorFindBrowser']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorFindBrowser"])

            return "Failed"

        except Exception as ex:
            Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorOpenBrowser']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorOpenBrowser']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorOpenBrowser"])

            return "Failed"

    # Verify is the browser is still opened.
    def verifyBrowser(self):
        try:
            if driver.current_url:
                driver.close()

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorVerifyBrowser"], value1=str(ex))
            return "Failed"

    # Close (windows or the whole browser).
    def close(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            if value1 is None:  # If none was informed = Close Windows.
                driver.close()
                Aux.Main.addLogs(self, message="General", value=Aux.logs["CloseWindow"])
            else:  # If something was informed = Close Browser.
                driver.quit()
                Aux.Main.addLogs(self, message="General", value=Aux.logs["CloseBrowser"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorClose"], value1=str(ex))
            return "Failed"

    # Open page address.
    def openPage(self, **kwargs):
        try:
            # kwargs arguments.
            value1 = kwargs.get('value1')

            driver.get(value1)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["OpenPage"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorOpenPage"])

            return "Failed"

    # Hightlight the component during the execution.
    def highlight(self, **kwargs):

        try:
            # kwargs variables.
            newelement = kwargs.get('newelement')
            effect_time = kwargs.get('effect_time')
            color = kwargs.get('color')
            border = kwargs.get('border')

            def apply_style(s):
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", newelement, s)

            original_style = newelement.get_attribute('style')
            apply_style("border: {0}px solid {1};".format(border, color))
            Aux.time.sleep(effect_time)
            apply_style(original_style)

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorHighLight"], value1=str(ex))

    # Reset the Edge Legacy configuration.
    def _resetEdgeLegacy(self):
        try:

            # Open the MS-Settings.
            Aux.os.system("start ms-settings:")

            # Select the Application & Resources.
            Aux.time.sleep(1)
            Aux.pyautogui.typewrite("app")
            Aux.pyautogui.typewrite(['enter', 'enter'], interval=2)

            # Select the Edge Legacy.
            Aux.time.sleep(3)
            Aux.pyautogui.typewrite(['tab'], interval=1)
            Aux.pyautogui.typewrite("Edge")
            Aux.pyautogui.typewrite(['tab', 'tab', 'tab', 'enter', 'tab', 'enter'], interval=.2)

            # Restore the Edge Legacy config.
            Aux.time.sleep(1)
            Aux.pyautogui.typewrite(['tab', 'tab', 'enter', 'enter'], interval=.5)

            # Keyboard press Alt+F4 to close the browser Configuration.
            Aux.pyautogui.keyDown('alt')
            Aux.time.sleep(.2)
            Aux.pyautogui.keyDown('F4')
            Aux.time.sleep(.2)
            Aux.pyautogui.keyUp('alt')

            Aux.Main.addLogs(self, message="General", value=Aux.logs["ResetEdgeLegacy"])
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['ResetEdgeLegacy']['Msg']}{Aux.Textcolor.END}")

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorResetEdgeLegacy"], value1=str(ex))
            return "Failed"

    # Configure the save path - Only Edge Legacy.
    def _configureSavePath(self):
        try:
            # Keyboard press Alt+x and open the browser Configuration.
            Aux.pyautogui.keyDown('alt')
            Aux.time.sleep(.2)
            Aux.pyautogui.keyDown('x')
            Aux.time.sleep(.2)
            Aux.pyautogui.keyUp('alt')

            # Navigate to the browser download folder.
            Aux.pyautogui.typewrite(['up', 'Enter', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab',
                                     'enter', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'Enter'], interval=.2)

            # Type the new path.
            Aux.time.sleep(2)
            Aux.pyautogui.typewrite(Aux.directories['DownloadFolderTemp'])
            Aux.pyautogui.typewrite(['enter', 'tab', 'enter'], interval=.2)

            # Do not ask after finisht the download.
            Aux.pyautogui.typewrite(['tab', 'space', 'esc'], interval=.2)

            Aux.Main.addLogs(self, message="General", value=Aux.logs["ConfigureSavePath"])

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorConfigureSavePath"], value1=str(ex))
            return "Failed"

    # Save the file locally.
    def saveFile(self, **kwargs):

        cont_iteration = kwargs.get("cont_iteration")

        try:
            Aux.time.sleep(5)
            while True:
                # The file found means it is still downloading.
                if Aux.Main.verifyFile(self, path=Aux.directories['DownloadFolderTemp'], extension='crdownload',
                                       msg_not_found=Aux.otherConfigs['DownloadFinished']['Msg'],
                                       msg_found=Aux.otherConfigs['DownloadingFile']['Msg']):
                    Aux.time.sleep(1)
                    continue
                else:
                    # Rename de file.
                    files = Aux.os.listdir(Aux.directories['DownloadFolderTemp'])
                    for file in files:
                        new_name = 'IT' + str(cont_iteration).zfill(2) + ' - ' + file
                        Aux.os.rename(Aux.os.path.join(Aux.directories['DownloadFolderTemp'], file),
                                      Aux.os.path.join(Aux.directories['DownloadFolderTemp'], new_name))
                        Aux.shutil.move(Aux.os.path.join(Aux.directories['DownloadFolderTemp'], new_name),
                                        Aux.os.path.join(Aux.directories['DownloadFolder'], new_name))
                    break

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorSaveFile"], value1=str(ex))
            return "Failed"

    # Save the screenshots.
    def takePicture(self, **kwargs):

        # kwargs variables:
        test_set_path = kwargs.get("test_set_path")
        image_name = kwargs.get("image_name")
        verb = kwargs.get("verb")
        list_steps = kwargs.get("list_steps")

        create = False

        try:
            if Aux.Main._checkDesktop_TC(self, list_steps=list_steps):
                Aux.pyscreenshot.grab(childprocess=False).save(test_set_path + "\\" + image_name + ".png")

            # Alert print screen.
            elif ec.alert_is_present()(driver):
                Aux.time.sleep(1)
                Aux.shutil.copyfile(Aux.os.path.join(Aux.os.getcwd(), 'Automation', 'images',
                                                     Aux.directories['UnavailablePrint']),
                                    test_set_path + "\\" + image_name + ".png")

            else:
                driver.save_screenshot(test_set_path + "\\" + image_name + ".png")

            create = True

            Aux.Main.addLogs(self, message="General", value=Aux.logs["TakePicture"])

        except AttributeError or requests.exceptions.RequestException or requests.exceptions.RetryError:
            Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorFindBrowser']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorFindBrowser']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorFindBrowser"])

            create = False

        except Exception as ex:
            Aux.MDDialogAppTest().save_messages(Aux.logs['ErrorTakePicture']['Msg'])
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorTakePicture']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(self, message="General", value=Aux.logs["ErrorTakePicture"])

            create = False

        return create
