"""
Entrypoint to module
Simulates keyboard input to control game
"""

import pyautogui
# seems like big company games block pyautogui. Gotta use pydirectinput to simulate windows direct input
import pydirectinput

class IGameController:
    """
    provide wrappers to keyboard input
    Factory for other game-specific controller
    """
    def __init__(self):
        self.CurrentMonitorSizeWidth = pyautogui.size()[0]
        self.CurrentMonitorSizeHeight = pyautogui.size()[1]

    def move_front_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_back_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_right_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_left_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_front_long_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_back_long_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_right_long_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def move_left_long_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_accept_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_cancel_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_accept_repeatfire_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_cancel_repeatfire_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_pause_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_pause_alt_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_L1_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

    def press_R1_keyboard(self):
        raise NotImplementedError("Method not implemented yet")

class GameBoyAdvanceController(IGameController):
    def __init__(self):
        super().__init__()

    def move_front_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('w')
        # with pyautogui.hold('w'):
        #     pyautogui.sleep(1)

    def move_back_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('s')
        # with pyautogui.hold('s'):
        #     pyautogui.sleep(1)

    def move_right_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('d')
        # with pyautogui.hold('d'):
        #     pyautogui.sleep(1)

    def move_left_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('a')
        # with pyautogui.hold('a'):
        #     pyautogui.sleep(1)

    def move_front_long_keyboard(self):
        with pyautogui.hold('w'):
            pyautogui.sleep(3)

    def move_back_long_keyboard(self):
        with pyautogui.hold('s'):
            pyautogui.sleep(3)

    def move_right_long_keyboard(self):
        with pyautogui.hold('d'):
            pyautogui.sleep(3)

    def move_left_long_keyboard(self):
        with pyautogui.hold('a'):
            pyautogui.sleep(3)

    def press_accept_keyboard(self):
        pyautogui.press('l')

    def press_cancel_keyboard(self):
        pyautogui.press('k')

    def press_accept_repeatfire_keyboard(self):
        repeat_range = 10
        for i in range(repeat_range):
            pyautogui.press('l')
            pyautogui.sleep(0.5)

    def press_cancel_repeatfire_keyboard(self):
        repeat_range = 10
        for i in range(repeat_range):
            pyautogui.press('k')
            pyautogui.sleep(0.5)

    def press_pause_keyboard(self):
        pyautogui.press('enter')

    def press_pause_alt_keyboard(self):
        pyautogui.press('backspace')

    def press_L1_keyboard(self):
        pyautogui.press('i')

    def press_R1_keyboard(self):
        pyautogui.press('o')

class UmamusumeController(IGameController):
    def __init__(self):
        super().__init__()

    ##### accept, cancel
    def press_accept_keyboard(self):
        pydirectinput.press('enter')

    def press_cancel_keyboard(self):
        pydirectinput.press('esc')

    ##### tabs
    def tab_left_keyboard(self):
        pydirectinput.press('q')

    def tab_right_keyboard(self):
        pydirectinput.press('e')

    ##### pause
    def pause_menu_keyboard(self):
        pydirectinput.press('tab')

    ##### scroll
    def scroll_up_keyboard(self):
        pydirectinput.press('pageup')

    def scroll_down_keyboard(self):
        pydirectinput.press('pagedown')

    # navigation
    def move_front_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pydirectinput.press('up')

    def move_left_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pydirectinput.press('left')

    def move_back_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pydirectinput.press('down')

    def move_right_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pydirectinput.press('right')

    # Right Menu Tabs
    def shortcut_jukebox_keyboard(self):
        pydirectinput.press('z')

    def shortcut_sparks_keyboard(self):
        pydirectinput.press('x')

    def shortcut_log_keyboard(self):
        pydirectinput.press('c')

    def shortcut_careerprofile_keyboard(self):
        pydirectinput.press('v')

    def shortcut_agenda_keyboard(self):
        pydirectinput.press('b')

    def shortcut_itemrequest_keyboard(self):
        pydirectinput.press('n')

    def shortcut_menu_keyboard(self):
        pydirectinput.press('m')

class GameControllerFactory:
    """
    Author: Zarin
    Bot Factory
    """

    def __init__(self):
        pass

    def get_controller(self, controller_type: str):
        """
        below returns the class, not the instance of the class
        instantiate it after getting it
        Args:
            datatable_type: insert datatabletype selections

        Returns:

        """
        if controller_type == 'gameboy_adv':
            return GameBoyAdvanceController
        elif controller_type == 'pc_game':
            raise NotImplementedError("Generic ")
        elif controller_type == 'umamusume':
            return UmamusumeController

if __name__ == '__main__':
    """
    Test out the function
    """
    gameController = IGameController()

    pyautogui.sleep(10)
    gameController.move_front_keyboard()