import os
import subprocess

print(str(os.system('xrandr | grep \* | cut -f 4 -d \' \'')).split()[:5])

print('\n')

print(tuple(str(os.system('xrandr | grep \* | cut -f 4 -d \' \''))))


print(type(os.system('xrandr | grep \* | cut -f 4 -d \' \'')))

x = subprocess.check_output(['xrandr | grep \* | cut -f 4 -d \' \''])