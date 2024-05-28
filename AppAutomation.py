import ctypes                               # To load the computer language.
import locale                               # To load the computer language.
import os.path
from threading import Thread

import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.button import MDButtonText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from win32api import GetSystemMetrics
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ColorProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager, ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.tab import MDTabsBadge

import modules.azureConnection as Azure
import modules.automationAux as Aux

# Sets the screen size. (width | height).
if GetSystemMetrics(0) == 1920 and GetSystemMetrics(1) == 1080:
    kivy.core.window.Window.size = (GetSystemMetrics(0) / 1.9, GetSystemMetrics(1) / 1.5)
else:
    kivy.core.window.Window.size = (GetSystemMetrics(0) / 1.7, GetSystemMetrics(1) / 1.3)


class AppAutomation(MDApp):

    def __init__(self):
        super(AppAutomation, self).__init__()
        self.initial_center = Window.top
        self.color = StringProperty('#d31010')  # Define the background default color.
        self.running_screen = None
        self.main_screen = None

    def build(self):
        self.icon = Aux.os.path.join("Automation", "images", "Robot.ico")
        self.theme_cls.accent_palette = 'Purple'

        sm = ScreenManager()
        self.running_screen = ScreenRunning(name='Running')
        self.main_screen = ScreenMain(name='ScreenMain')

        sm.add_widget(self.main_screen)
        sm.add_widget(self.running_screen)
        sm.current = 'ScreenMain'
        return sm


class TokenField(MDApp):

    def __init__(self):
        super(TokenField, self).__init__()

    def show_token_input(self):
        self.my_token = MDDialog(
            title=(Aux.otherConfigs['InformTokenPart1']['Msg'] + ' ' +
                   Aux.otherConfigs['InformTokenPart2']['Msg'] + ' ' +
                   Aux.otherConfigs['InformTokenPart3']['Msg']),
            type='custom',
            auto_dismiss=False,
            content_cls=
            MDTextField(
                mode="rectangle",
                text=''
            ),
            buttons=[
                MDButtonText(
                    text=Aux.otherConfigs['TokenExpiredButton']['Msg'],
                    on_release=TokenField.expired_token_link,
                ),
                MDButtonText(
                    text=Aux.otherConfigs['CloseTokenMenu']['Msg'],
                    on_release=lambda _: TokenField().stop(),

                ),
            ],
        )
        self.my_token.open()

    def invalid_token_msg(self):
        self.invalid_token_menu = MDDialog(
            title=Aux.otherConfigs['InvalidTokenMessage']['Msg'],
            buttons=[
                MDButtonText(
                    text=Aux.otherConfigs['TokenTryAgain']['Msg'],
                    on_release=lambda _: self.invalid_token_menu.dismiss(),
                ),
            ]
        )
        self.invalid_token_menu.open()

    def expired_token_msg(self):
        self.invalid_token_menu = MDDialog(
            title='EXPIRED',
            buttons=[
                MDButtonText(
                    text=Aux.otherConfigs['TokenTryAgain']['Msg'],
                    on_release=lambda _: self.invalid_token_menu.dismiss(),
                ),
            ]
        )
        self.invalid_token_menu.open()

    def token_input_callback(self, *args):
        token_input = TokenField().my_token.content_cls.text
        Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['TokenSavedSuccess']['Msg'])
        return token_input

    def expired_token_link(self):
        import webbrowser
        webbrowser.open(Aux.directories['TokenExpiredUrl'])


class UpdateField(MDApp):

    def __init__(self):
        super(UpdateField, self).__init__()

    def show_Update_input(self):
        self.update = MDDialog(
            title=(Aux.otherConfigs['Update']['Msg']),
            type='custom',
            auto_dismiss=False,
            text=Aux.otherConfigs['UpdateMsg']['Msg'],
            content_cls=(),
            buttons=[
                MDButtonText(
                    text=Aux.otherConfigs['UpdateButtonYes']['Msg'],
                    on_release=UpdateField.download_update,
                ),
                MDButtonText(
                    text=Aux.otherConfigs['UpdateButtonNo']['Msg'],
                    on_release=lambda _: self.update.stop(),
                ),
            ],
        )
        self.update.open()

    def download_update(self):
        Aux.Main.download_Updates(self)

    def download_update_cancel(self):
        self.update.dismiss(force=True)

    def could_not_check_for_updates_msg(self):
        self.update = MDDialog(
            title=Aux.logs['CouldNotCheckForUpdates']['Msg'],
            buttons=[
                MDButtonText(
                    text=Aux.logs['UpdateTryAgain']['Msg'],
                    on_release=lambda _: update.stop(),
                ),
            ]
        )
        self.update.open()

    def download_update_completed_msg(self):
        self.update = MDDialog(
            title=Aux.logs['DownloadUpdateCompletedTitle']['Msg'],
            buttons=[
                MDButtonText(
                    text=Aux.logs['DownloadUpdateCompletedMsg']['Msg'],
                    on_release=lambda _: update.stop(),
                ),
            ]
        )
        self.update.open()

    def download_update_fail_msg(self):
        self.update = MDDialog(
            title=Aux.logs['ErrorDownloadUpdateTitle']['Msg'],
            buttons=[
                MDButtonText(
                    text=Aux.logs['ErrorDownloadUpdate']['Msg'],
                    on_release=lambda _: update.stop(),
                ),
            ]
        )
        self.update.open()


class Manager(ScreenManager):
    screen_main = ObjectProperty(None)
    screen_running = ObjectProperty(None)


class KivyTextColor:
    red = ColorProperty('#e34b4b')
    yellow = ColorProperty('#fce94f')
    blue = ColorProperty('#3e98ed')
    white = ColorProperty('#ffffff')
    orange = ColorProperty('#fcba03')
    green = ColorProperty('#51c966')


class ScreenMain(Screen):

    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)

        self.icons = list(md_icons.keys())[15:30]
        self.projects_menu = None
        self.projects_menu_tab_2 = None
        self.test_plan_menu = None
        self.test_plan_menu_t2 = None
        self.test_suit_menu = None
        self.menu_lang = None
        self.menu_help = None
        self.do_dropdown = True

        Window.bind(on_key_down=self._on_keyboard_down)

        # Read any language to load the directories and paths.
        Aux.Main.loadConfigs(self, language='pt', interface=True)

        # Create the log directory.
        Aux.Main.createDirectory(self, path_folder=Aux.directories['LogFolder'])

        # Create the evidence folder.
        Aux.Main.createDirectory(self, path_folder=Aux.directories['EvidenceFolder'])

        # Create the export directory.
        Aux.Main.createDirectory(self, path_folder=Aux.directories['DownloadFolder'])
        Aux.Main.createDirectory(self, path_folder=Aux.directories['DownloadFolderTemp'])

        # Clear the export folder, if already exist.
        Aux.Main.deleteFiles(self, path_log=Aux.directories['DownloadFolder'], extension='*')
        Aux.Main.deleteFiles(self, path_log=Aux.directories['DownloadFolderTemp'], extension='*')

        # Install the new version.
        if os.path.isdir(Aux.directories['UpdateFolder']):
            Aux.Main.install_Update(self)
        else:
            Aux.Main.check_Updates(self)

        # Load the Windows DLL's to inform the computer language.
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()

        # Load the correct file according the language.
        language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        ### language = 'es'     ### For test.
        ### language = 'en_US'  ### For test.
        ### language = 'pt_BR'  ### For test.

        if 'es' in language:
            language = language[:2]  # Any spanish language.

        if language not in ('es', 'en_US', 'pt_BR'):
            print(f"{Aux.Textcolor.FAIL}{Aux.otherConfigs['LanguageError']['Msg']}{Aux.Textcolor.END}")
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['LanguageError']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()
            Aux.Main.addLogs(self, message="General", value=Aux.otherConfigs["LanguageError"])
            ###exit(1)

        # Configure the languages.
        Aux.Main.setLanguage(self, language=language, interface=True)

        # Set language global variable.
        Aux.otherConfigs['Language'] = language

        self.evidence_checked = False
        self.cookie_checked = False
        self.automation_checked = 'n'
        self.compare_checked = 'n'
        self.items_list = []
        self.list_of_projects_name = []

        # Fields tab 1.
        self.ids.tab1_testcase_label.opacity = 0
        self.ids.compare_button.opacity = 0

        # Fields tab 2.
        self.ids.tab2_testcase.opacity = 0
        self.ids.tab2_testcase_label.opacity = 0

        # Labels from .kv to translate.
        self.ids.compare_button.text = Aux.otherConfigs['Tab1CompareButton']['Msg']
        self.ids.evidence_button.text = Aux.otherConfigs['Tab2ButtonEvidence']['Msg']
        self.ids.execute_button.text = Aux.otherConfigs['Tab1ExecuteButton']['Msg']
        self.ids.help_timeout_value.text = Aux.otherConfigs['Tab1HelpTimeout']['Msg']
        self.ids.note_compare.text = Aux.otherConfigs['Tab1NoteCompareLabel']['Msg']
        self.ids.note_cookie.text = Aux.otherConfigs['Tab1NoteCookieLabel']['Msg']
        self.ids.note_evidence.text = Aux.otherConfigs['Tab1NoteEvidenceLabel']['Msg']
        self.ids.note_execution.text = Aux.otherConfigs['Tab1NoteExecutionLabel']['Msg']
        self.ids.note_isolate.text = Aux.otherConfigs['Tab1NoteIsolateLabel']['Msg']
        self.ids.running_screen.text = Aux.otherConfigs['GoToConsole']['Msg']
        self.ids.syntax_label.text = Aux.otherConfigs['Tab3Syntax']['Msg']
        self.ids.tab1.text = Aux.otherConfigs['Tab1Title']['Msg']
        self.ids.tab1_choose_automation.text = Aux.otherConfigs['ChooseAutomation']['Msg']
        self.ids.tab1_choose_between.text = Aux.otherConfigs['ChooseBetweenAutomationCompare']['Msg']
        self.ids.tab1_choose_compare.text = Aux.otherConfigs['ChooseCompare']['Msg']
        self.ids.tab1_choose_testcase.text = Aux.otherConfigs['Tab2ChooseTestCase']['Msg']
        self.ids.tab1_cookie_label.text = Aux.otherConfigs['Tab1CookieLabel']['Msg']
        self.ids.tab1_evidence_label.text = Aux.otherConfigs['Tab1EvidenceLabel']['Msg']
        self.ids.tab1_project_label.text = Aux.otherConfigs['TabProjectLabel']['Msg']
        self.ids.tab1_testcase_label.text = Aux.otherConfigs['TabTestCaseLabel']['Msg']
        self.ids.tab1_testplan_label.text = Aux.otherConfigs['TabTestPlanLabel']['Msg']
        self.ids.tab1_timeout.text = Aux.otherConfigs['Tab1Timeout']['Msg']
        self.ids.tab2.text = Aux.otherConfigs['Tab2Title']['Msg']
        self.ids.tab2_choose_testcase_label.text = Aux.otherConfigs['Tab2ChooseTestCase']['Msg']
        self.ids.tab2_project_label.text = Aux.otherConfigs['TabProjectLabel']['Msg']
        self.ids.tab2_run_id_label.text = Aux.otherConfigs['Tab2RunIDLabel']['Msg']
        self.ids.tab2_running_screen.text = Aux.otherConfigs['GoToConsole']['Msg']
        self.ids.tab2_testcase_label.text = Aux.otherConfigs['TabTestCaseLabel']['Msg']
        self.ids.tab5.text = Aux.otherConfigs['Tab5Title']['Msg']

        # Tab help.
        self.ids.tab4_help.text = Aux.otherConfigs['TabHelpTitle']['Msg']
        self.ids.languages.text = Aux.otherConfigs['TabHelpLanguages']['Msg']
        self.ids.verb.text = Aux.otherConfigs['TabHelpVerb']['Msg']
        self.ids.functions.text = Aux.otherConfigs['TabHelpFunctions']['Msg']
        self.ids.explanation.text = Aux.otherConfigs['TabHelpExplanation']['Msg']

        # Screen Running label's text.
        # MDApp.get_running_app().running_screen.ids.clear_console.text = Aux.otherConfigs['CleanConsole']['Msg']
        # MDApp.get_running_app().running_screen.ids.go_screen_main.text = Aux.otherConfigs['GoBack']['Msg']
        # MDApp.get_running_app().running_screen.ids.execute_button_log.text = \
        #     Aux.otherConfigs['Tab1ExecuteButton']['Msg']
        # MDApp.get_running_app().running_screen.ids.evidence_button_log.text = \
        #     Aux.otherConfigs['Tab2ButtonEvidence']['Msg']

        # tab 1 - projects
        self.list_of_projects_name = []
        menu_items_projects = [{"icon": "folder-outline", "text": f"{i}"}
                               for i in sorted(self.list_of_projects_name)]

        self.projects_menu = self.create_mddropdown_menu(menu_items=menu_items_projects,
                                                         item_id=self.ids.tab1_project)

        self.projects_menu.bind(on_release=self.set_projects)

        # tab 1 - testplan.
        self.list_test_plans = []
        menu_items_test_plan = [{"icon": "folder-outline", "text": f"{i}"} for i in sorted(self.list_test_plans)]

        self.test_plan_menu = self.create_mddropdown_menu(item_id=self.ids.tab1_testplan,
                                                          menu_items=menu_items_test_plan)

        self.test_plan_menu.bind(on_release=self.set_test_suit)

        # tab 1 - Test suit.
        self.list_test_suit = []
        menu_items_test_suit = [{"icon": "folder-outline", "text": f"{i}"} for i in sorted(self.list_test_suit)]

        self.test_suit_menu = self.create_mddropdown_menu(item_id=self.ids.tab1_testsuit,
                                                          menu_items=menu_items_test_suit)

        self.test_suit_menu.bind(on_release=self.set_test_suit)

        # tab 2 - projects name.
        self.list_of_projects_name = []
        menu_items_projects_tab_2 = [{"icon": "folder-outline", "text": f"{i}"}
                                     for i in sorted(self.list_of_projects_name)]

        self.projects_menu_tab_2 = self.create_mddropdown_menu(menu_items=menu_items_projects_tab_2,
                                                               item_id=self.ids.tab2_project)

        self.projects_menu_tab_2.bind(on_release=self.set_project_name_tab_2)

        # Create an empty menu for the verbs in tab 4 (help) so it doesn't close the application.
        first_items_list = []
        menu_items_help = [{"text": f"{i}"} for i in sorted(first_items_list)]

        self.menu_help = self.create_mddropdown_menu(menu_items=menu_items_help, item_id=self.ids.verbs)

        self.menu_help.bind(on_release=self.set_help_items)

        # Hover.
        self.ids.evidence_button.add_widget(HoverItem())
        self.ids.execute_button.add_widget(HoverItem())
        self.ids.compare_button.add_widget(HoverItem())
        self.ids.running_screen.add_widget(HoverItem())
        self.ids.tab2_running_screen.add_widget(HoverItem())

        # About.
        self.load_readme()

    # Load projects on pre enter.
    def load_projects_pre_enter(self):

        # Request the token.
        Aux.Main.accessAzure(self)

        # Capture azure projects.
        try:
            self.list_of_projects_name = []

            self.list_of_projects_id = Azure.AzureConnection.getProjects(self)

            # If it is None, it means that your token is either wrong or it doesn't exist.
            while self.list_of_projects_id is None:
                self.list_of_projects_id = Azure.AzureConnection.getProjects(self)

        except Exception as e:
            Aux.MDDialogAppTest().save_messages(e)
            Aux.MDDialogAppTest().show_mddialog()

        # Loading projects.
        for index in range(0, len(self.list_of_projects_id)):
            self.separator = self.list_of_projects_id[index].find(' | ')
            self.list_of_projects_name.append(self.list_of_projects_id[index][:self.separator])

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.tab1_project.focus is True and len(self.ids.tab1_project.text) > 1 and keycode == 42:
            self.ids.tab1_project.text = ''
        if self.ids.tab1_testplan.focus is True and len(self.ids.tab1_testplan.text) > 1 and keycode == 42:
            self.ids.tab1_testplan.text = ''
        if self.ids.tab1_testsuit.focus is True and len(self.ids.tab1_testsuit.text) > 1 and keycode == 42:
            self.ids.tab1_testsuit.text = ''
        if self.ids.tab2_project.focus is True and len(self.ids.tab2_project.text) > 1 and keycode == 42:
            self.ids.tab2_project.text = ''
        if self.ids.which_language.focus is True and len(self.ids.which_language.text) > 1 and keycode == 42:
            self.ids.which_language.text = ''
        if self.ids.verbs.focus is True and len(self.ids.verbs.text) > 1 and keycode == 42:
            self.ids.verbs.text = ''

    def filter_projects_tab1(self):
        # Do not open a dropdown if the text was changed by the dropdown.
        if not self.do_dropdown:
            return

        # If dropdown is already open, close it.
        if self.projects_menu:
            self.projects_menu.dismiss()
            self.projects_menu = None

        if self.ids.tab1_project.on_focus:
            prefix = self.ids.tab1_project.text.upper()
            filtered_projects = filter(lambda l: prefix in l.upper(), self.list_of_projects_name)
            menu_items_projects = [{"icon": "folder-outline", "text": f"{i}"}
                                   for i in sorted(filtered_projects)]
            if len(menu_items_projects) < 1:
                return

            self.projects_menu = self.create_mddropdown_menu(menu_items=menu_items_projects,
                                                             item_id=self.ids.tab1_project)
            self.projects_menu.open()
            self.projects_menu.bind(on_release=self.set_projects)

    def filter_projects_tab2(self):
        # Do not open a dropdown if the text was changed by the dropdown.
        if not self.do_dropdown:
            return

        # If dropdown is already open, close it.
        if self.projects_menu_tab_2:
            self.projects_menu_tab_2.dismiss()
            self.projects_menu_tab_2 = None

        if self.ids.tab2_project.on_focus:
            prefix = self.ids.tab2_project.text.upper()
            filtered_projects = filter(lambda l: prefix in l.upper(), self.list_of_projects_name)

            menu_items_projects_tab_2 = [{"icon": "folder-outline", "text": f"{i}"}
                                         for i in sorted(filtered_projects)]

            if len(menu_items_projects_tab_2) < 1:
                return

            self.projects_menu_tab_2 = self.create_mddropdown_menu(menu_items=menu_items_projects_tab_2,
                                                                   item_id=self.ids.tab2_project)
            self.projects_menu_tab_2.open()
            self.projects_menu_tab_2.bind(on_release=self.set_project_name_tab_2)

    # Test case's checkbox.
    def is_shown_test_case(self, instance, value):
        if value is True:
            self.ids.tab1_testcase_label.opacity = 1
            self.ids.tab1_testcase.opacity = 1
        else:
            self.ids.tab1_testcase_label.opacity = 0
            self.ids.tab1_testcase.opacity = 0

    # Test case's checkbox (Tab evidence = Tab 2).
    def is_shown_test_case_tab2(self, instance, value):
        if value is True:
            self.ids.tab2_testcase_label.opacity = 1
            self.ids.tab2_testcase.opacity = 1
            self.ids.tab2_testcase_label.opacity = 1
            self.ids.tab2_testcase.opacity = 1
        else:
            self.ids.tab2_testcase_label.opacity = 0
            self.ids.tab2_testcase.opacity = 0
            self.ids.tab2_testcase_label.opacity = 0
            self.ids.tab2_testcase.opacity = 0

    # Compare's checkbox.
    def is_shown_compare(self, instance, value):
        if value is True:
            self.ids.execute_button.height = dp(1)
            self.ids.execute_button.opacity = 0
            self.ids.tab1_evidence_label.opacity = 0
            self.ids.evidence_checkbox.opacity = 0
            self.ids.tab1_cookie_label.opacity = 0
            self.ids.cookie_checkbox.opacity = 0
        else:
            self.ids.execute_button.height = dp(35)
            self.ids.execute_button.opacity = 1
            self.ids.tab1_evidence_label.opacity = 1
            self.ids.evidence_checkbox.opacity = 1
            self.ids.tab1_cookie_label.opacity = 1
            self.ids.cookie_checkbox.opacity = 1

    # Execution's checkbox.
    def is_shown_execution(self, instance, value):
        if value is True:
            self.ids.compare_button.height = dp(1)
            self.ids.compare_button.opacity = 0
        else:
            self.ids.compare_button.height = dp(35)
            self.ids.compare_button.opacity = 1

    # Enable Cookies's checkbox.
    def is_enable_cookies(self, instance, value):
        if value is True:
            self.ids.compare_button.height = dp(1)
            self.ids.compare_button.opacity = 0
        else:
            self.ids.enable_cookies.height = dp(35)
            self.ids.compare_button.opacity = 1

    def on_tab_switch(self, *args):
        pass

    @staticmethod
    def clear_fields(label_id):
        label_id.text = ''

    @staticmethod
    def replace_labels(kivy_id, name_in_dict):
        kivy_id.text = Aux.otherConfigs[f'{name_in_dict}']['Msg']

    theme_cls = ThemeManager()

    def create_mddropdown_menu(self, menu_items, item_id):
        menu_name = MDDropdownMenu(
            caller=item_id,
            items=menu_items,
            position="auto",
            width_mult=7,
            max_height=250,
            # selected_color=self.theme_cls.primary_dark_hue

        )
        return menu_name

    def create_substring(self, substring_before):
        index = substring_before.find('|')
        self.substring_after = substring_before[index + 1:]
        return self.substring_after

    # Creates a hanging menu.
    @staticmethod
    def custom_snackbar(text):
        MDSnackbar(bg_color=(0.4, 0, 0.922, 1),
                 snackbar_x="10dp",
                 snackbar_y="10dp",
                 height="45dp",
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                 text=text).open()

    # tab 1 - sets the project name and test plan.
    def set_projects(self, instance_menu, instance_menu_item):

        # default from drop-down.
        def set_item(interval):
            self.do_dropdown = False
            self.ids.tab1_project.text = instance_menu_item.text
            instance_menu.dismiss()
            self.projects_menu = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.project_name = instance_menu_item.text

        for index in range(0, len(self.list_of_projects_id)):
            self.separator = self.list_of_projects_id[index].find(' | ')
            if self.list_of_projects_id[index][:self.separator] == self.project_name:
                self.project_id = self.list_of_projects_id[index][self.separator + 3:]

        self.can_get_testplan = True
        self.custom_snackbar(self.project_name)

        if self.can_get_testplan:
            try:
                self.list_test_plans = Azure.AzureConnection.getTestPlans(self, project=self.project_name)

            except Exception as e:
                Aux.MDDialogAppTest().save_messages(e)
                Aux.MDDialogAppTest().show_mddialog()

    def filter_testplan_tab1(self):

        if not self.do_dropdown:
            return

        if self.test_plan_menu:
            self.test_plan_menu.dismiss()
            self.test_plan_menu = None

        if self.ids.tab1_testplan.on_focus:
            prefix = self.ids.tab1_testplan.text.upper()
            filtered = filter(lambda l: prefix in l.upper(), self.list_test_plans)
            menu_items_test_plan = [{"icon": "folder-outline", "text": f"{i}"}
                                    for i in sorted(filtered)]
            if len(menu_items_test_plan) < 1:
                return

            self.test_plan_menu = self.create_mddropdown_menu(menu_items=menu_items_test_plan,
                                                              item_id=self.ids.tab1_testplan)
            self.test_plan_menu.open()
            self.test_plan_menu.bind(on_release=self.set_test_plan)

    # tab 1 - test plan
    def set_test_plan(self, instance_menu, instance_menu_item):

        # default from drop-down
        def set_item(interval):
            self.do_dropdown = False
            self.ids.tab1_testplan.text = instance_menu_item.text
            instance_menu.dismiss()
            self.test_plan_menu = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.test_plan = instance_menu_item.text
        self.can_get_testsuit = True
        self.custom_snackbar(self.test_plan)

        self.create_substring(self.test_plan)
        self.test_plan_substring = self.substring_after

        # create test suit menu
        if self.can_get_testsuit:

            try:
                self.list_test_suit = \
                    Azure.AzureConnection.getTestSuits(self, project=self.project_name,
                                                       id_test_plan=self.test_plan_substring,
                                                       checkbox_state=self.compare_checked)
            except Exception as e:
                Aux.MDDialog(text="error: " + str(e)).open()

    def filter_testsuit_tab1(self):
        # Do not open a dropdown if the text was changed by the dropdown.
        if not self.do_dropdown:
            return

        # If dropdown is already open, close it.
        if self.test_suit_menu:
            self.test_suit_menu.dismiss()
            self.test_suit_menu = None

        if self.ids.tab1_testsuit.on_focus:
            prefix = self.ids.tab1_testsuit.text.upper()
            filtered = filter(lambda l: prefix in l.upper(), self.list_test_suit)

            menu_items_test_suit = [{"icon": "folder-outline", "text": f"{i}"}
                                    for i in sorted(filtered)]

            self.test_suit_menu = self.create_mddropdown_menu(menu_items=menu_items_test_suit,
                                                              item_id=self.ids.tab1_testsuit)

            self.test_suit_menu.open()
            self.test_suit_menu.bind(on_release=self.set_test_suit)

    # tab 1 - test suit
    def set_test_suit(self, instance_menu, instance_menu_item):

        # default from drop-down
        def set_item(interval):
            self.do_dropdown = False
            self.ids.tab1_testsuit.text = instance_menu_item.text
            instance_menu.dismiss()
            self.test_suit_menu = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.test_suit = instance_menu_item.text
        self.custom_snackbar(self.test_suit)
        self.create_substring(self.test_suit)
        self.test_suit_substring = self.substring_after
        return self.test_suit

    def set_test_plan_tab_2(self, instance_menu, instance_menu_item):

        # default from drop-down.
        def set_item(interval):
            self.do_dropdown = False
            self.ids.tab2_testplan.text = instance_menu_item.text
            instance_menu.dismiss()
            self.test_plan_menu_t2 = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)

        self.test_plan_t2 = instance_menu_item.text
        index = self.test_plan_t2.find('|')
        self.test_plan_t2_sub = self.test_plan_t2[:index]
        self.custom_snackbar(self.test_plan_t2)
        self.create_substring(self.test_plan_t2)
        self.test_plan_tab_2_substring = self.substring_after

    # tab 2 - project name
    def set_project_name_tab_2(self, instance_menu, instance_menu_item):

        # default from drop-down.
        def set_item(interval):
            self.do_dropdown = False
            self.ids.tab2_project.text = instance_menu_item.text
            instance_menu.dismiss()
            self.projects_menu_tab_2 = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.project_name_tab_2 = instance_menu_item.text

        for index in range(0, len(self.list_of_projects_id)):
            self.separator = self.list_of_projects_id[index].find(' | ')
            if self.list_of_projects_id[index][:self.separator] == self.project_name_tab_2:
                self.project_id_tab_2 = self.list_of_projects_id[index][self.separator + 3:]

        self.can_get_testplan_t2 = True
        self.custom_snackbar(self.project_name_tab_2)

        if self.can_get_testplan_t2:

            try:
                self.list_test_plans_tab_2 = Azure.AzureConnection.getTestPlans(self, project=self.project_name_tab_2)

            except Exception as e:
                Aux.MDDialogAppTest().save_messages(e)
                Aux.MDDialogAppTest().show_mddialog()

        return self.project_name_tab_2

    # set help items
    def set_help_items(self, instance_menu, instance_menu_item):

        # default from drop-down
        def set_item(interval):
            self.do_dropdown = False
            self.ids.verbs.text = instance_menu_item.text
            instance_menu.dismiss()
            self.menu_help = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.verbs = instance_menu_item.text
        can_go = True
        self.custom_snackbar(self.verbs)

        if can_go:
            try:
                for index in range(0, len(self.items_list)):
                    if self.verbs == self.items_list[index][0]:
                        self.ids.function_id.text = self.items_list[index][1]['Function']
                        self.ids.phrase.text = self.items_list[index][1]['Phrase']
                        self.ids.syntax_field.text = self.items_list[index][1]['Syntax'].replace("\\", '')

            except KeyError:
                self.ids.syntax_field.text = Aux.otherConfigs['EmptySyntax']['Msg']

    def set_lang_items(self, instance_menu, instance_menu_item):
        def set_item(interval):
            self.do_dropdown = False
            self.ids.which_language.text = instance_menu_item.text
            instance_menu.dismiss()
            self.menu_lang = None
            self.do_dropdown = True

        Clock.schedule_once(set_item, 0.5)
        self.which_language = instance_menu_item.text
        can_go = True

        if can_go:

            self.first_items_list = []

            self.items_list = []
            for items in Aux.verbs.items():
                self.items_list.append(items)

            for self.index in range(0, len(self.items_list)):
                if self.which_language == 'Portuguese':
                    if self.items_list[self.index][1]['Language'] == 'Portuguese':
                        self.first_items_list.append(self.items_list[self.index][0])
                elif self.which_language == 'Spanish':
                    if self.items_list[self.index][1]['Language'] == 'Spanish':
                        self.first_items_list.append(self.items_list[self.index][0])
                elif self.which_language == 'English':
                    if self.items_list[self.index][1]['Language'] == 'English':
                        self.first_items_list.append(self.items_list[self.index][0])

    def filter_menu_help(self):
        try:
            # Do not open a dropdown if the text was changed by the dropdown.
            if not self.do_dropdown:
                return

            # If dropdown is already open, close it.
            if self.menu_help:
                self.menu_help.dismiss()
                self.menu_help = None

            if self.ids.verbs.on_focus:
                prefix = self.ids.verbs.text.upper()
                filtered = filter(lambda l: prefix in l.upper(), self.first_items_list)

                menu_items_help = [{"text": f"{i}"} for i in sorted(filtered)]
                self.menu_help = self.create_mddropdown_menu(menu_items=menu_items_help, item_id=self.ids.verbs)
                self.menu_help.open()
                self.menu_help.bind(on_release=self.set_help_items)

        except AttributeError:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()

    def filter_language(self):

        if not self.do_dropdown:
            return

        if self.menu_lang:
            self.menu_lang.dismiss()
            self.menu_lang = None

        language_list = ['Portuguese', 'Spanish', 'English']

        if self.ids.which_language.on_focus:
            prefix = self.ids.which_language.text.upper()
            filtered = filter(lambda l: prefix in l.upper(), language_list)
            menu_items_lang = [{"text": f"{i}"} for i in sorted(filtered)]
            if len(menu_items_lang) < 1:
                return
            self.menu_lang = self.create_mddropdown_menu(menu_items=menu_items_lang,
                                                         item_id=self.ids.which_language)
            self.menu_lang.open()
            self.menu_lang.bind(on_release=self.set_lang_items)

    def run_id(self):
        self.run_ids = self.ids.tab2_runid.text

    @staticmethod
    def opacity_on(widget_id):
        widget_id.text_color = (1, 1, 1, 0)
        widget_id.md_bg_color = (0.4, 0, 0.922, 0)

    @staticmethod
    def opacity_off(widget_id):
        widget_id.text_color = (1, 1, 1, 1)
        widget_id.md_bg_color = (0.4, 0, 0.922, 1)

    def set_evidence_checkbox(self, instance, value):
        if value is True:
            self.evidence_checked = True
            return self.evidence_checked
        else:
            self.evidence_checked = False
            return self.evidence_checked

    def set_cookie_checkbox(self, instance, value):
        if value is True:
            self.cookie_checked = True
            return self.cookie_checked
        else:
            self.cookie_checked = False
            return self.cookie_checked

    def set_automation_checkbox(self, instance, value):
        if value is True:
            self.ids.compare_checkbox.active = False
            self.automation_checked = 'Automation'
            return self.automation_checked
        else:
            if self.ids.compare_checkbox.active is False:
                self.ids.automation_checkbox.active = True
            self.automation_checked = 'n'

    def set_compare_checkbox(self, instance, value):
        if value is True:
            self.ids.note_evidence.opacity = 0
            self.ids.note_cookie.opacity = 0
            self.ids.automation_checkbox.active = False
            self.opacity_off(self.ids.compare_button)
            self.compare_checked = 'Compare'
            return self.compare_checked
        else:
            self.ids.note_evidence.opacity = 1
            self.ids.note_cookie.opacity = 1
            if self.ids.automation_checkbox.active is False:
                self.ids.compare_checkbox.active = True
            self.compare_checked = 'n'

    def set_test_case(self, kivy_id_test_case):
        self.test_case = kivy_id_test_case.text
        if self.test_case:
            pass
        return self.test_case

    def set_testcase_checkbox(self, instance, value, item_id):
        if value is True:
            pass
        elif value is not True:
            item_id.text = ''

    def load_readme(self):

        # ReadMe path file.
        readme_path = Aux.directories['ReadMeFile']
        if not Aux.os.path.exists(readme_path):
            readme_path = Aux.os.path.join(Aux.os.getcwd(), 'README.md')

        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()
            sentences = content.split('\\n')
            for sentence in sentences:
                pass
            for string in ["<font color='red'>**__", "__**</font>", "<em>", "</em>"]:
                sentence = sentence.replace(string, "")
            self.ids.read_me.text = str(sentence)
            self.ids['scroll1'].scroll_y = 1

    def change_screen_evidence(self):

        try:
            if len(self.ids.tab2_runid.text) > 1:
                try:
                    Aux.messages.clear()
                    self.manager.current = 'Running'
                    Thread(target=self.generate_evidence).start()
                except AttributeError:
                    Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
                    Aux.MDDialogAppTest().show_mddialog()
                except IndexError:
                    pass
            else:
                raise AttributeError

        except AttributeError:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()

    def change_screen_execute(self):
        try:
            if len(self.ids.tab1_testsuit.text) > 1:
                try:
                    self.manager.current = 'Running'
                    Thread(target=self.execute_automation).start()
                except AttributeError:
                    Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
                    Aux.MDDialogAppTest().show_mddialog()
                except IndexError:
                    pass
            else:
                raise AttributeError

        except AttributeError:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()

    def change_screen_compare(self):
        try:
            if len(self.ids.tab1_testsuit.text) > 1:
                try:
                    self.manager.current = 'Running'
                    Thread(target=self.compare).start()
                except AttributeError:
                    Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
                    Aux.MDDialogAppTest().show_mddialog()

                except IndexError:
                    pass
            else:
                raise AttributeError

        except AttributeError:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()

    def execute_automation(self):
        from modules.automatizationCore_Azure import Main as Execute
        self.set_test_case(self.ids.tab1_testcase)
        self.time_out = self.ids.tab1_timeout_value.text
        Aux.messages.clear()

        try:
            Execute.main(self, project_name=self.ids.tab1_project.text, project_id=self.project_id,
                         id_test_plan=self.test_plan_substring, id_test_suit=self.test_suit_substring,
                         test_case_id_list_all=self.test_case, evidence=self.evidence_checked,
                         cookie=self.cookie_checked, timeout=self.time_out)

        except Exception as e:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["InterfaceEmptyFieds"], value1=str(e))

    def compare(self):
        from modules.automaticCompareFiles import Main as Compare
        self.set_test_case(self.ids.tab1_testcase)
        Aux.messages.clear()

        try:
            Compare.main(self, project_id=self.project_id, id_test_plan=self.test_plan_substring,
                         id_test_suit=self.test_suit_substring, test_case_id_list_all=self.test_case)

        except Exception as e:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["InterfaceEmptyFieds"], value1=str(e))

    def generate_evidence(self):
        from modules.generateManualEvidence import Main as Evidence
        self.run_id()
        self.set_test_case(self.ids.tab2_testcase)
        Aux.messages.clear()

        try:
            Evidence.main(self, project_name=self.ids.tab2_project.text, project_id=self.project_id_tab_2,
                          test_run_id=self.run_ids, id_test_case=self.test_case)

        except Exception as e:
            Aux.MDDialogAppTest().save_messages(Aux.otherConfigs['InterfaceEmptyFieds']['Msg'])
            Aux.MDDialogAppTest().show_mddialog()
            Aux.Main.addLogs(self, message="General", value=Aux.logs["InterfaceEmptyFieds"], value1=str(e))


class ScreenRunning(Screen):

    def __init__(self, **kwargs):
        super(ScreenRunning, self).__init__(**kwargs)
        self.ids.clear_console.add_widget(HoverItem())
        self.ids.go_screen_main.add_widget(HoverItem())

    def write_message_on_console(self, message):
        if len(message.replace('[color=#', '')) >= 100:
            message_substring = ' '
            message_index = [i for i in range(len(message)) if message.startswith(message_substring, i)]
            index_to_break_line = int(len(message_index) / 2)
            if len(message[index_to_break_line:]) > 99:
                message_substring = ' '
                message_index = [i for i in range(len(message)) if message.startswith(message_substring, i)]
                index_to_break_line = message_index[int(len(message_index) / 2)]
            self.ids.console_output.text += message[:index_to_break_line] + '\n' + message[index_to_break_line:] \
                                            + '\n' + '\n'
        else:
            self.ids.console_output.text += message + '\n' + '\n'
        self.ids.console_scroll.scroll_y = 0

    def clear_console(self):
        self.ids.console_output.text = ''


# Implementing hover behavior.
class HoverItem(MDBoxLayout, ThemableBehavior, HoverBehavior):

    def on_enter(self, *args):
        Window.set_system_cursor("hand")

    def on_leave(self, *args):
        Window.set_system_cursor("arrow")


# Class that makes it possible to create tabs.
class Tab(FloatLayout, MDTabsBadge):
    pass


if __name__ == "__main__":
    AppAutomation().run()
