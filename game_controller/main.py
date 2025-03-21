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
        """
        Move front by keyboard
        :return:
        """

    def move_back_keyboard(self):
        """
        Move front by keyboard
        :return:
        """

    def move_right_keyboard(self):
        """
        Move front by keyboard
        :return:
        """

    def move_left_keyboard(self):
        """
        Move front by keyboard
        :return:
        """


class PokemonGameController(IGameController):
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



if __name__ == '__main__':
    """
    Test out the function
    """
    gameController = IGameController()

    pyautogui.sleep(10)
    gameController.move_front_keyboard()