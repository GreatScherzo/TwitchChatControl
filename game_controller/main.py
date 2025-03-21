"""
Entrypoint to module
Simulates keyboard input to control game
"""

import pyautogui

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

    def move_back_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('s')

    def move_right_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('d')

    def move_left_keyboard(self):
        """
        Move front by keyboard
        :return:
        """
        pyautogui.press('a')

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


if __name__ == '__main__':
    """
    Test out the function
    """
    gameController = IGameController()

    pyautogui.sleep(10)
    gameController.move_front_keyboard()