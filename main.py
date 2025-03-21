

# Import stuff
import subprocess
from obs_handler import obs_handler
import threading
from common.xml_handler import XMLHandler
from game_controller.main import GameBoyAdvanceController
from twitch_handler.twitch_handler import Bot

if __name__ == '__main__':
# Launch OBS
#test = subprocess.call(r'C:\Program Files\obs-studio\bin\64bit\obs64.exe', cwd='C:/Program Files/obs-studio/bin/64bit/')

#print(test)
# oBSHandler = obs_handler.OBSHandler()
# oBSHandler.call_obs()
# print("Called OBS")
# Launch Game

# Set OBS to focus on game windows



# Instantiate game control class



# Instantiate twitch control class

 # Get config data
    xmlHandler = XMLHandler('config.xml')
    print("Config loaded")
    gameController = GameBoyAdvanceController()
    twitchBot = Bot(gameController, access_token=xmlHandler.access_token)
    twitchBot.run()
