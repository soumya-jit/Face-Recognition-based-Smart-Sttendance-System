'''import os
import sys
print("First file started")
os.startfile("MainMenu.py")
sys.exit()
'''


'''
from os import system
from threading import Thread
from sys import exit

thread = Thread()
thread.run = lambda: system('MainMenu.py')
thread.start()
exit()
'''


import os
cmd = 'cmd /c "D:\Python_Projects\Smart_Attendance_System\MainMenu.py"'
a = os.system(cmd)
print(a)




'''
import sys
import subprocess
subprocess.Popen(["py", "MainMenu.py"])
sys.exit()
'''


'''
#not tested
import ctypes
import os
import win32process

hwnd = ctypes.windll.kernel32.GetConsoleWindow()      
if hwnd != 0:      
    ctypes.windll.user32.ShowWindow(hwnd, 0)      
    ctypes.windll.kernel32.CloseHandle(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    os.system('taskkill /PID ' + str(pid) + ' /f')
'''
