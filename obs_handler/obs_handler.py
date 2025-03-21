import subprocess
import threading
from common.exception_handling import ErrorWithCode

class OBSHandler():
    """
    Class for creating object to handle obs process
    """
    def __init__(self):
        """

        """
        self.OBSPath: str = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
        self.OBSRootFolder: str = r'C:/Program Files/obs-studio/bin/64bit/'
        self.ThreadReturnVal: dict = {"CallOBS": None}
        self.ThreadOnceFlag: bool = False

        # # Instantiate own ErrorWithCode Object
        # self.errorWithCode = ErrorWithCode()
        # # Define new errors
        # self.errorWithCode.error_dict['Thread Error'] = "Thread is called more than once"
    def _call_obs(self):
        """
        Create thread to call OBS
        Can only be called once
        :return:
        """
        if self.ThreadOnceFlag == False:

            try:
                threadReturnVal = subprocess.call(self.OBSPath, cwd=self.OBSRootFolder)
                self.ThreadReturnVal["CallOBS"] = threadReturnVal
            except FileNotFoundError as e:
                raise e
        else:
            raise ErrorWithCode("ThreadError")


    def call_obs(self):
        """
        Public method to call obs
        :return:
        """
        t1 = threading.Thread(target=self._call_obs)
        t1.start()
