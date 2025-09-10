import omni.ext
import omni.ui as ui
from omni.kit.menu.utils import add_menu_items, remove_menu_items
from omni.kit.menu.utils import MenuItemDescription
from .window import MyWindow
from omni.kit.actions.core import get_action_registry
from omni.kit.notification_manager import post_notification

import carb

MENU_TITLE = "TestMenu"

class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id) -> None:
        self.action_registry = get_action_registry()

        self.ext_id = ext_id

        self._menu_items = []
        self._action_list = []
        self._action_func_list = []
        self._description_list = []

        self.__my_window = None

        self._menu_items.append(MenuItemDescription(name='My Window', onclick_action=(ext_id, f"my_company.exts.my_example:my_window")))
        self._action_list.append('my_company.exts.my_example:my_window')
        self._action_func_list.append(self.show_window)
        self._description_list.append('Show/Hide Test Window.')

        self._menu_items.append(MenuItemDescription(name='About Extension', onclick_action=(ext_id, f"my_company.exts.my_example:about")))
        self._action_list.append('my_company.exts.my_example:about')
        self._action_func_list.append(self.show_about)
        self._description_list.append('About this Extension.')

        self._menu_items.append(MenuItemDescription(name='Print Log Test', onclick_action=(ext_id, f"my_company.exts.my_example:print_log")))
        self._action_list.append('my_company.exts.my_example:print_log')
        self._action_func_list.append(self.print_log)
        self._description_list.append('Log Print for test.')
        
        for i in range(len(self._menu_items)):
            self.action_registry.register_action(
                self.ext_id,                                     
                self._action_list[i],     
                self._action_func_list[i],                        
                description=self._description_list[i], 
            )

        add_menu_items(self._menu_items, MENU_TITLE)

        print(f'{self.ext_id} : my_company.exts.my_example Loaded')

    def on_shutdown(self) -> None:
        if self.__my_window:
            self.__my_window.visible = False

        remove_menu_items(self._menu_items, MENU_TITLE)
        
        if self.__my_window is not None and self.__my_window.visible == True:
            self.__my_window.visible = False
            self.__my_window = None
        
        for action in self._action_list:
            self.action_registry.deregister_action(self.ext_id, action)

        print(f'my_company.exts.my_example Shutdown')

    def show_window(self):
        if self.__my_window is None:
            self.__my_window = MyWindow()

        self.__my_window.reset()
        self.__my_window.visible = not self.__my_window.visible

    def show_about(self):
        post_notification('Thanks for use. - Sooyoun')

    def print_log(self):
        carb.log_info('Info Log')
        carb.log_warn('Warning Log')
        carb.log_error('Error Log')