

# Import stuff
import subprocess
from obs_handler import obs_handler
import threading
import asyncio

# Launch OBS
#test = subprocess.call(r'C:\Program Files\obs-studio\bin\64bit\obs64.exe', cwd='C:/Program Files/obs-studio/bin/64bit/')

#print(test)
oBSHandler = obs_handler.OBSHandler()
oBSHandler.call_obs()
print("Called OBS")
# Launch Game

# Set OBS to focus on game windows

# Instantiate game control class

# Instantiate twitch control class

