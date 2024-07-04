import time
import requests
import json
from jsonschema import validate, ValidationError

from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import Automation.modules.automationAux as Aux

driver = None


class Main:

    def __init__(self):
        pass

    # Function to search the element using the option above.
    def findElement(self, **kwargs):

        # kwargs variables.
        parameters1 = kwargs.get('parameters1')
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
                driver.implicitly_wait(1)
                new_element = driver.find_element(tag, parameters1)

                if new_element is not None:
                    Main.highlight(self, newelement=new_element, effect_time=1, color=color, border=3)

                    Aux.Main.addLogs(message="General", value=Aux.logs["FindElement"], parameters1=tag,
                                     parameters2=parameters1)

                    return new_element

            except NoSuchElementException:
                Aux.Main.addLogs(message="General", value=Aux.logs["WarningFindElement"], parameters1=tag,
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

            Aux.Main.addLogs(message="General", value=Aux.logs["FillField"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorFillField"], parameters1=str(ex))
            return "Failed"

    # Don't execute the step.
    def noExecute(self, **kwargs):

        # kwargs arguments.
        step = kwargs.get('step')

        try:
            Aux.Main.addLogs(message="General", value=Aux.logs["NoExecute"], parameters1="'" + step + "'")

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorNoExecute"],
                             parameters1="'" + step + "' - " + str(ex))
            return "Failed"

    # Execute a MS-DOS command line.
    def execute(self, **kwargs):

        path = ""

        try:
            # kwargs arguments.
            path = kwargs.get('parameters1')

            Aux.os.system('start "" "' + path + '"')

            Aux.Main.addLogs(message="General", value=Aux.logs["Execute"], parameters1="'" + path + "'")

            return path, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorExecute"], parameters1="'" + path + "' - " +
                                                                                            str(ex))
            return "Failed"

    # Click in an element.
    def click(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.click()

            Aux.Main.addLogs(message="General", value=Aux.logs["Click"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorClick"], parameters1=str(ex))
            return "Failed"

    # Double click.
    def doubleClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            element_field = Main.findElement(self, parameters1=parameters1)
            element_field.click()
            element_field.click()

            Aux.Main.addLogs(message="General", value=Aux.logs["DoubleClick"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorDoubleClick"], parameters1=str(ex))
            return "Failed"

    # Right click (mouse).
    def rightClick(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            actions = ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1)

            actions.context_click(element_field)
            actions.perform()

            Aux.Main.addLogs(message="General", value=Aux.logs["RightClick"])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorRightClick"], parameters1=str(ex))
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

            actions = ActionChains(driver)

            positions = parameters2.split(":")
            positionx = positions[0]
            positionx = positionx[1:]  # Only the numeric number.
            positiony = positions[1]
            positiony = positiony[1:]  # Only the numeric number.

            # actions.drag_and_drop_by_offset(element_field, int(positionx) * 10, int(positiony) * 10)
            actions.perform()

            Aux.Main.addLogs(message="General", value=Aux.logs['DragDrop'])

            return "Passed"
        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorDragDrop"], parameters1=str(ex))
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

            actions = ActionChains(driver)
            element_field1 = Main.findElement(self, parameters1=parameters1)
            element_field2 = Main.findElement(self, parameters1=parameters2)

            actions.drag_and_drop(element_field2, element_field1)
            actions.perform()

            Aux.Main.addLogs(message="General", value=Aux.logs["DragDropToElement"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorDragDropToElement"], parameters1=str(ex))
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

            actions = ActionChains(driver)

            if parameters1.upper() == 'RETURN' or parameters1.upper() == 'ENTER':
                for _ in range(parameters2): actions.send_keys(Keys.RETURN)
            elif parameters1.upper() == 'UP':
                for _ in range(parameters2): actions.send_keys(Keys.UP)
            elif parameters1.upper() == 'PAGE UP':
                for _ in range(parameters2): actions.send_keys(Keys.PAGE_UP)
            elif parameters1.upper() == 'DOWN':
                for _ in range(parameters2): actions.send_keys(Keys.DOWN)
            elif parameters1.upper() == 'PAGE DOWN':
                for _ in range(parameters2): actions.send_keys(Keys.PAGE_DOWN)
            elif parameters1.upper() == 'LEFT':
                for _ in range(parameters2): actions.send_keys(Keys.LEFT)
            elif parameters1.upper() == 'RIGHT':
                for _ in range(parameters2): actions.send_keys(Keys.RIGHT)
            elif parameters1.upper() == 'TAB':
                for _ in range(parameters2): actions.send_keys(Keys.TAB)
            elif parameters1.upper() == 'SPACE':
                for _ in range(parameters2): actions.send_keys(Keys.SPACE)
            elif parameters1.upper() == 'BACKSPACE':
                for _ in range(parameters2): actions.send_keys(Keys.BACKSPACE)
            elif parameters1.upper() == 'DELETE':
                for _ in range(parameters2): actions.send_keys(Keys.DELETE)
            # Alt or Ctrl + <any other key>.
            elif parameters1.upper().__contains__('CTRL') or parameters1.upper().__contains__('ALT'):
                for _ in range(parameters2):
                    Aux.pyautogui.keyDown(parameters1.upper().rsplit('+')[0])
                    Aux.time.sleep(.2)
                    Aux.pyautogui.keyDown(parameters1.upper().rsplit('+')[1])
                    Aux.time.sleep(.2)
                    Aux.pyautogui.keyUp(parameters1.upper().rsplit('+')[0])

            actions.perform()

            Aux.Main.addLogs(message="General", value=Aux.logs["PressButton"],
                             parameters1=parameters1 + " - " + str(parameters2) + "x")

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorPressButton"],
                             parameters1=parameters1 + " - " + str(ex))
            return "Failed"

    # Mouse Over.
    def mouseOver(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:

            actions = ActionChains(driver)
            element_field = Main.findElement(self, parameters1=parameters1)

            actions.move_to_element(element_field)  # Worked with XPath.
            actions.perform()

            Aux.Main.addLogs(message="General", value=Aux.logs["MouseOver"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorMouseOver"], parameters1=str(ex))
            return "Failed"

    # Wait.
    def wait(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            Aux.time.sleep(int(parameters1))

            Aux.Main.addLogs(message="General", value=Aux.logs["Wait"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorWait"], parameters1=str(ex))

            return "Failed"

    # Select DropDownList.
    def selectDropDownList(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            element_field = Select(Main.findElement(self, parameters1=parameters1))

            element_field.select_by_visible_text(parameters2)
            Aux.Main.addLogs(message="General", value=Aux.logs["SelectDropDownList"], parameters1=parameters2)

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorSelectDropDownList"], parameters1=str(ex))

            return "Failed"

    # Get the text from a elements.
    def getText(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            obtained_text = Main.findElement(self, parameters1=parameters1, color="green").text

            if obtained_text is None:
                headers = {'User-Agent': Aux.otherConfigs['Agent']}
                content = Aux.request.get(driver.current_url, headers=headers).content
                soup = BeautifulSoup(content, 'html.parser')

                for tag in Aux.searchForAttribute:
                    for component in Aux.searchForComponent:
                        table = soup.findAll(Aux.searchForComponent[component],
                                             attrs={Aux.searchForAttribute[tag]: parameters1})
                        for textFound in table:
                            Aux.Main.addLogs(message="General", value=Aux.logs["GetText"])
                            Main.findElement(self, parameters1=parameters1, color="green")
                            return textFound.contents[0], "Passed"
                        else:
                            return Aux.logs["ErrorGetText"]["Msg"], "Failed"
            else:
                return obtained_text, "Passed"

            Aux.Main.addLogs(message="General", value=Aux.logs["GetText"])

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetText"], parameters1=str(ex))

            return Aux.logs["ErrorGetText"]['Msg'], "Failed"

    @staticmethod
    def openNewTab():
        try:

            driver.execute_script("window.open('', '_blank')")

            Aux.Main.addLogs(message="General", value=Aux.logs["OpenNewTab"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorOpenNewTab"], parameters1=str(ex))

            return "Failed"

    # Get current url
    @staticmethod
    def getURL():
        try:

            url = driver.current_url
            Aux.Main.addLogs(message="General", value=Aux.logs["GetURL"])

            return url, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetURL"], parameters1=str(ex))

            return None, "Failed"

    # get Title
    @staticmethod
    def getTitle():

        try:

            title = driver.title
            Aux.Main.addLogs(message="General", value=Aux.logs["GetTitle"])

            return title, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetTitle"], parameters1=str(ex))

            return None, "Failed"

    # Back Page
    @staticmethod
    def backPage():

        try:

            driver.back()

            Aux.Main.addLogs(message="General", value=Aux.logs["BackPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorBackPage"], parameters1=str(ex))

            return "Failed"

    # Back Page.
    @staticmethod
    def forwardPage():

        try:

            driver.forward()
            Aux.Main.addLogs(message="General", value=Aux.logs["ForwardPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorForwardPage"], parameters1=str(ex))

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

            Aux.Main.addLogs(message="General", value=Aux.logs["GetAttribute"])

            return text_found, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetAttribute"], parameters1=str(ex))

            return text_found, "Failed"

    def getQuantityElements(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

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
                new_element = driver.find_elements(tag, parameters1)
                elements = len(new_element)

                if elements > 0:
                    Aux.Main.addLogs(message="General", value=Aux.logs["GetQuantityElements"], parameters1=tag,
                                     parameters2=parameters1)
                    return elements, "Passed"

                elif x > 8:
                    return elements, "Passed"

                x += 1

            except NoSuchElementException:
                Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetQuantityElements"], parameters1=tag,
                                 parameters2=parameters1)
                return None, "Failed"

    # Scroll Page
    def scrollPage(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            driver.execute_script('window.scrollTo(0, ' + parameters1 + ')')
            Aux.Main.addLogs(message="General", value=Aux.logs["ScrollPage"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorScrollPage"], parameters1=str(ex))

            return "Failed"

    # Refresh Page
    def refreshPage(self):
        try:

            driver.refresh()
            Aux.Main.addLogs(message="General", value=Aux.logs["RefreshPage"])

            return driver, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorRefreshPage"], parameters1=str(ex))

            return "Failed"

    # Checks whether the element is inactive.
    def isEnable(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        status_element = None

        try:
            status_element = Main.findElement(self, parameters1=parameters1).is_enabled()

            Aux.Main.addLogs(message="General", value=Aux.logs["IsEnable"])

            return status_element, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorIsEnable"], parameters1=str(ex))
            return status_element, "Failed"

    # Checks whether the element is visible.
    def isDisplayed(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        status_element = None

        try:
            status_element = Main.findElement(self, parameters1=parameters1).is_displayed()

            Aux.Main.addLogs(message="General", value=Aux.logs["IsDisplayed"])

            return status_element, "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorIsDisplayed"], parameters1=str(ex))

            return status_element, "Failed"

    # Checks whether a checkbox or radio button is selected (returns True or False)
    def isSelected(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:

            status_element = Main.findElement(self, parameters1=parameters1).is_selected()

            if status_element:
                Aux.Main.addLogs(message="General", value=Aux.logs["IsSelected"])
                return "True", "Passed"
            else:
                return "False", "Failed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorIsSelected"], parameters1=str(ex))
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
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the URL from the address bar (getURL).
                elif '(url)' in parameters1:
                    text_found, status = Main.getURL(self)
                    parameters2 = parameters1.replace('(url)', '')

                    if parameters2 == text_found:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])

                        parameters2 = parameters1.replace('(url)', '')
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check a part of the text was found.
                elif '*' in parameters2:  # Check part of the text.
                    text_found, status = Main.getText(self, parameters1=parameters1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if parameters2.replace('*', '') in text_found:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is active or inactive.
                elif '(?)' in parameters2:
                    text_found, status = Main.isEnable(self, parameters1=parameters1)
                    text_found = str(text_found)
                    parameters2 = parameters2.replace('(?)', '')

                    if text_found == parameters2:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether the element is visible to the user.
                elif '($)' in parameters2:
                    text_found, status = Main.isDisplayed(self, parameters1=parameters1)
                    text_found = str(text_found)
                    parameters2 = parameters2.replace('($)', '')

                    if text_found == parameters2:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks whether a checkbox or radio button is selected.
                elif '(.)' in parameters2:
                    text_found, status = Main.isSelected(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(.)', '')

                    if str(text_found) == parameters2:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if data is not available.
                elif '(!=)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(!=)', ' - ')

                    if parameters2 not in str(text_found):
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Checks if the data is available.
                elif '(!)' in parameters2:
                    text_found, status = Main.getText(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('(!)', '')

                    if parameters2 in str(text_found):
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Check some attributes.
                elif '(#title)' in parameters2 or '(#href)' in parameters2 or '(#value)' in parameters2 or '(#class)' in parameters2:
                    text_found, status = Main.getAttribute(self, parameters1=parameters1, parameters2=parameters2)
                    parameters2 = parameters2.replace('(#title)', '')
                    parameters2 = parameters2.replace('(#href)', '')
                    parameters2 = parameters2.replace('(#value)', '')
                    parameters2 = parameters2.replace('(#class)', '')

                    if parameters2 == text_found:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

                # Get the amount of elements. # ---> OK.
                elif '<' and '>' in parameters2:
                    text_found, status = Main.getQuantityElements(self, parameters1=parameters1)
                    parameters2 = parameters2.replace('<', '')
                    parameters2 = parameters2.replace('>', '')

                    if int(parameters2) == text_found:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"
                        text_found = str(text_found)

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"
                        text_found = str(text_found)

                # Validates that the text obtained from the page is the same as the expected text.
                else:
                    text_found, status = Main.getText(self, parameters1=parameters1)

                    # Remove new lines.
                    if "\n" in text_found:
                        text_found = text_found.replace("\n", "")

                    if text_found == parameters2:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                        status = "Passed"

                    else:
                        Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                        status = "Failed"

            else:  # If Alert Element.
                alert = driver.switch_to_alert()
                text_found = alert.text

                if parameters2 == text_found:
                    Aux.Main.addLogs(message="General", value=Aux.logs["ValidateData"])
                    status = "Passed"

                else:
                    Aux.Main.addLogs(message="General", value=Aux.logs["ErrorValidateData"])
                    status = "Failed"

            Aux.Main.addLogs(message="General", value=Aux.logs['ValidateDataExpected'], parameters1=parameters2)
            Aux.Main.addLogs(message="General", value=Aux.logs['ValidateDataObtained'], parameters1=text_found)

            return status

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorFunctionValidateData"], parameters1=str(ex))
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
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorAlter"], parameters1=str(ex))
            return "Failed"

    # Alter window.
    def alterWindow(self, **kwargs):
        try:
            for handle in driver.window_handles:
                driver.switch_to_window(handle)

            Aux.Main.addLogs(message="General", value=Aux.logs["AlterWindow"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorAlterWindow"], parameters1=str(ex))
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

            Aux.Main.addLogs(message="General", value=Aux.logs["AlterIframe"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorAlterIframe"], parameters1=str(ex))
            return "Failed"

    # Alter Alert and Click OK.
    def alterAlertOK(self):
        try:

            alert = driver.switch_to.alert
            alert.accept()

            Aux.Main.addLogs(message="General", value=Aux.logs["AlterAlert"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorAlterAlert"], parameters1=str(ex))
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

            Aux.Main.addLogs(message="General", value=Aux.logs["ReturnDefault"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorReturnDefault"], parameters1=str(ex))
            return "Failed"

    # Return to window.
    def returnWindow(self):
        try:
            driver.switch_to.window(driver.window_handles[0])

            Aux.Main.addLogs(message="General", value=Aux.logs["ReturnWindow"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorReturnWindow"], parameters1=str(ex))
            return "Failed"

    # Return to default.
    def returnFrame(self):
        try:

            driver.switch_to.default_content()

            Aux.Main.addLogs(message="General", value=Aux.logs["ReturnIframe"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorReturnIframe"], parameters1=str(ex))
            return "Failed"

    # Choose an option in a browser alert screen.
    def inform(self, **kwargs):
        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')
            parameters2 = kwargs.get('parameters2')

            wait = WebDriverWait(driver, timeout=2)
            alert = wait.until(lambda d: d.switch_to.alert)

            # Validate de Alert content (Text).
            if parameters2 is not None:
                status = Main.validateData(self, alert='AlertScreen', parameters1=alert.text, parameters2=parameters2)

            # Actions inside de Alert.
            if parameters1.upper() in ("OK", "ACEPTAR"):
                alert.accept()
                time.sleep(3)

            elif parameters1.upper() in ("CANCELAR", "CANCEL"):
                alert.dismiss()
                time.sleep(3)

            else:  # Fill the Alert textbox.
                alert.send_keys(parameters1)
                time.sleep(3)

            Aux.Main.addLogs(message="General", value=Aux.logs["Inform"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorInform"], parameters1=str(ex))
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

                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

            # Configure before open the browser.
            elif parameters1.upper() in ("MOZILLA", "FIREFOX"):
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

                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

            # Configure before open the browser.
            elif parameters1.upper() in "EDGE":  # Edge Chromium.

                options = webdriver.EdgeOptions()

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
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

            else:
                Aux.Main.addLogs(message="General", value=Aux.logs["ErrorOpenBrowser"])
                return "Failed"

            Aux.otherConfigs['Browser'] = parameters1
            driver.maximize_window()
            Main.openPage(self, parameters1=Aux.otherConfigs["HomePage"])

            Aux.Main.addLogs(message="General", value=Aux.logs["OpenBrowser"])

            # Set the page load timeout (receive in minutes from interface).
            driver.set_page_load_timeout(int(Aux.otherConfigs['TimeoutSession']) * 60)

            return "Passed"

        except requests.exceptions.RequestException:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorFindBrowser']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorFindBrowser"])

            return "Failed"

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorOpenBrowser']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorOpenBrowser"], parameters1=str(ex))

            return "Failed"

    # Verify is the browser is still opened.
    def verifyBrowser(self):

        try:
            if driver.current_url:
                driver.close()

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorVerifyBrowser"], parameters1=str(ex))
            return "Failed"

    # Close (windows or the whole browser).
    def close(self, **kwargs):

        try:
            # kwargs arguments.
            parameters1 = kwargs.get('parameters1')

            if parameters1 is None:  # If none was informed = Close Windows.
                driver.close()
                Aux.Main.addLogs(message="General", value=Aux.logs["CloseWindow"])
            else:  # If something was informed = Close Browser.
                driver.quit()
                Aux.Main.addLogs(message="General", value=Aux.logs["CloseBrowser"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorClose"], parameters1=str(ex))
            return "Failed"

    # Open page address.
    def openPage(self, **kwargs):

        # kwargs arguments.
        parameters1 = kwargs.get('parameters1')

        try:
            driver.get(parameters1)

            Aux.Main.addLogs(message="General", value=Aux.logs["OpenPage"])

            return "Passed"

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorOpenPage"], parameters1=str(ex))

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
            Aux.time.sleep(effect_time)
            apply_style(original_style)

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorHighLight"], parameters1=str(ex))

    # Configure the save path - Only Edge Legacy.
    @staticmethod
    def _configureSavePath():
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

            # Do not ask after finish the download.
            Aux.pyautogui.typewrite(['tab', 'space', 'esc'], interval=.2)

            Aux.Main.addLogs(message="General", value=Aux.logs["ConfigureSavePath"])

        except Exception as ex:
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorConfigureSavePath"], parameters1=str(ex))
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
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorSaveFile"], parameters1=str(ex))
            return "Failed"

    # Save the screenshots.
    def takePicture(self, **kwargs):

        # kwargs variables:
        test_set_path = kwargs.get("test_set_path")
        image_name = kwargs.get("image_name")

        try:
            # Alert print screen.
            if ec.alert_is_present()(driver):
                Aux.time.sleep(1)
                Aux.shutil.copyfile(Aux.os.path.join(Aux.os.getcwd(), 'Automation', 'images',
                                                     Aux.directories['UnavailablePrint']),
                                    test_set_path + "\\" + image_name + ".png")

            else:
                driver.save_screenshot(test_set_path + "\\" + image_name + ".png")

            Aux.Main.addLogs(message="General", value=Aux.logs["TakePicture"])

            return True

        except AttributeError or requests.exceptions.RequestException or requests.exceptions.RetryError:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorTakePicture']['Msg']}{Aux.Textcolor.END}")
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorTakePicture"])

            return False

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorTakePicture']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorTakePicture"])

            return False

# --------------------------------------------- API Functions ----------------------------------------------------------
    def request_api(self, **kwargs):

        # kwargs variables:
        parameters1 = kwargs.get("parameters1")
        api_action = kwargs.get("api_action")

        # Variables
        submit = False
        Aux.otherConfigs['APIStep'] = True
        api_result = None

        try:
            if parameters1.upper() != 'SUBMIT':
                tag = parameters1[:parameters1.find(':')]
                if tag.upper() == 'ENDPOINT':
                    Aux.otherConfigs['API_Endpoint'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'AUTHORIZATION':
                    Aux.otherConfigs['API_Authorization'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'HEADERS':
                    Aux.otherConfigs['API_Headers'] = parameters1[parameters1.find(':') + 1:].strip()
                elif tag.upper() == 'BODY':
                    Aux.otherConfigs['API_Body'] = parameters1[parameters1.find(':') + 1:parameters1.rfind('\"')].strip()
                    ### ERRO ESTA RETORNANDO 401.
                elif tag.upper() == 'PARAMS':
                    Aux.otherConfigs['API_Params'] = parameters1[parameters1.find(':') + 1:].strip()

                if Aux.otherConfigs['API_Endpoint'] is None:
                    print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorAPIMissingInfo']['Msg']}{Aux.Textcolor.END}")
                    Aux.Main.addLogs(message="General", value=Aux.logs["ErrorAPIMissingInfo"])
                    raise TypeError(Aux.logs['ErrorAPIMissingInfo']['Msg'])
            else:
                submit = True

            if submit and api_action.upper() == "GET":
                api_result = requests.get(Aux.otherConfigs['API_Endpoint'],
                                          params=Aux.otherConfigs['API_Params'],
                                          headers={'Authorization': Aux.otherConfigs['API_Authorization']},
                                          verify=False,
                                          data=json.dumps(Aux.otherConfigs['API_Body']))
            elif submit and api_action.upper() == "POST":
                api_result = requests.post(Aux.otherConfigs['API_Endpoint'],
                                           params=Aux.otherConfigs['API_Params'],
                                           headers={'Authorization': Aux.otherConfigs['API_Authorization']},
                                           verify=False,
                                           data=json.dumps(Aux.otherConfigs['API_Body']))

                Aux.otherConfigs['StatusCodeAPI'] = api_result.status_code
                if api_result.status_code == 200:
                    # Filter some fields.
                    resp = json.loads(api_result.text)
                    if resp is not []:
                        Aux.otherConfigs['ResponseAPI'] = resp

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorGetAPI']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorGetAPI"])

    def responseAPI(self, **kwargs):

        # kwargs variables:
        parameters1 = kwargs.get("parameters1")
        find_content = None
        status_code = None
        schema = None

        Aux.otherConfigs['APIStep'] = True

        try:
            tag = parameters1[:parameters1.find(':')]
            param = parameters1[parameters1.find(':') + 1:]

            # Status Code.
            if tag.upper() == "STATUS CODE" and int(param) == Aux.otherConfigs['StatusCodeAPI']:
                status_code = "Passed"
            elif tag.upper() == "STATUS CODE" and int(param) != Aux.otherConfigs['StatusCodeAPI']:
                status_code = "Failed"
            elif tag.upper() == "SCHEMA":
                param = param.replace(" ", "")
                validate(instance=Aux.otherConfigs['ResponseAPI'], schema=param)
                ### Jogar a validação do SCHEMA na evidência.

            else:  # tag.upper() != "STATUS CODE":
                find_content = Aux.Main.find_content_json(self, tag=tag, param=param)

            if status_code == "Failed" or find_content == "Failed" or schema == "Failed":
                Aux.Main.addLogs(message="General", value=Aux.logs["ErrorResponseAPI"],
                                 value1=f"Expected: {tag} - Result {param}")

                return "Failed"
            else:
                return "Passed"

        except Exception as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorResponseAPI']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorResponseAPI"])

            return "Failed"

        except ValidationError as ex:
            print(f"{Aux.Textcolor.FAIL}{Aux.logs['ErrorResponseAPI']['Msg']}{Aux.Textcolor.END}", ex)
            Aux.Main.addLogs(message="General", value=Aux.logs["ErrorResponseAPI"])

            return "Failed"
