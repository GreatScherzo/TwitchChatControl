import subprocess
import threading
import asyncio
from common.exception_handling import ErrorWithCode
import os
import time

class OBSHandler:
    """
    Class for creating object to handle obs process
    """
    def __init__(self, batch_folder_path:str= r'./batch_file',
                 #root_dir = os.path.dirname(os.path.abspath(__file__)),
                 root_dir = os.getcwd(),
                 ):
        """

        """
        # self.OBSPath: str = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
        # self.OBSRootFolder: str = r'C:/Program Files/obs-studio/bin/64bit/'
        self.process_handler = None
        self.already_running: bool = False

        # Batch file path. Change it if you want to debug it from here
        self.batch_folder_path = batch_folder_path
        self.root_dir = root_dir
        # # Instantiate own ErrorWithCode Object
        # self.errorWithCode = ErrorWithCode()
        # # Define new errors
        # self.errorWithCode.error_dict['Thread Error'] = "Thread is called more than once"

    async def _launch_obs(self):
        """
        Create thread to call OBS
        Can only be called once
        :return:
        """
        # check if there's an existing instance already
        if self.process_handler == None:
            try:
                #Old way to just run the exe file directly
                # Thread = subprocess.call(self.OBSPath, cwd=self.OBSRootFolder)

                # Run process via batch script file
                os.getcwd()

                processHandler = subprocess.Popen(os.path.join(self.root_dir, "batch_file", "obs_launch.bat") ,
                                                  cwd=self.batch_folder_path)
                # return handler from running subprocess
                self.process_handler = processHandler
                # process ran once to true
                self.already_running = True
            except FileNotFoundError as e:
                raise e
        else:
            raise ErrorWithCode("ThreadError")

    async def _kill_obs(self):
        """
        Kill OBS process
        """
        if self.process_handler:
            try:
                # kill process via batch script file
                test = subprocess.Popen(os.path.join(self.root_dir, "batch_file", "obs_kill.bat") ,
                                                  cwd=self.batch_folder_path)
                # return handler from running subprocess
                self.process_handler = None
            except Exception as e:
                raise e

    async def start_obs(self):
        """
        Public method to call obs
        :return:
        """
        # t1 = threading.Thread(target=self._call_obs)
        # t1.start()

        await self._launch_obs()
        # sleep for a while to make sure stream is up and running
        await asyncio.sleep(5)


    async def restart_obs(self):
        """
        Public method to restart obs
        :return:
        """
        await self._kill_obs()
        await asyncio.sleep(10)
        await self._launch_obs()

    async def stop_obs(self):
        """
        Public method to stop obs
        """
        await self._kill_obs()

    async def _debug_restart(self):
        await self.start_obs()
        await asyncio.sleep(10)
        await self.restart_obs()


if __name__ == '__main__':
    oBSHandler = OBSHandler(batch_folder_path=r'../batch_file', root_dir=r'C:\\Repo\\TwitchChatControl\\TwitchChatControl\\')

    # asyncio.run(oBSHandler.start_obs())
    # asyncio.run(oBSHandler._debug_restart())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(a.listen_for_orders())
