"""
Module to hold exception handling class
"""
import sys
import traceback
import wx


# def initialize_error_handler():
#     """
#     To use the class, you must first use this function to create a global object
#     of the class, so that it can be used throughout the program
#
#     :return: error_with_code
#     """
#     global error_with_code
#     error_with_code = ErrorWithCode()

class ErrorWithCode(Exception):
    """
    Error handling class with custom codes

    _Parameter
    ==========
    error_dict:
        holds the code and corresponding descriptions for it
    """

    error_dict = {
        '1': 'Unexpected Error',
        'ThreadError': "Thread is called more than once"
    }

    def __init__(self, code="0000"):
        super().__init__()
        self.code = code
        self.description = self.error_dict.get(code, "No Errors")
        self.stack_trace = traceback.format_exc()
        self.exception_type = sys.exc_info()[0]
        self.exception_message = sys.exc_info()[1]

        self.__fail_color = '\033[91m'
        self.__end_color = '\033[0m'
        # end color needs to be inputted so that new line that will be
        # inputted into the terminal would return to its original colour

    def __str__(self):
        return repr(self.code)

    def print_exception(self):
        print(f"{self.__fail_color}Exception occured\nCode: %s \nDescription: %s \nTraceback: %s"
              f" \nException Type: %s \nException Message: %s"
              % (self.code, self.description, self.stack_trace, self.exception_type, self.exception_message)
              + f"{self.__end_color}")


def show_tb(passed_exc):
    """
    Function to display traceback as messagebox and show in debug console
    Args:
        passed_exc:

    Returns:

    """
    # print the exception to debug console first
    tb = traceback.format_exc()
    print(tb)

    tb = "Exception occured.\n" + tb
    wx.MessageBox(message=tb, caption="Error Occurred", style=wx.OK | wx.ICON_ERROR)


"""
Below is the global variable for the ErrorHandler
"""
error_with_code = ErrorWithCode()

if __name__ == "__main__":
    # Debugging class
    # Below shows implementation example
    try:
        raise ErrorWithCode("1000")
    except ErrorWithCode as e:
        e.print_exception()
