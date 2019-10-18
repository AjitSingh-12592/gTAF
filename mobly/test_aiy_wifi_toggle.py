import os
import sys

print("Wi-Fi toggle test on IOT(AIY) device")
command = "sshpass -p 'ubuntu' ssh -o StrictHostKeyChecking=no pi@10.92.33.252 'cd /home/pi/AIY-voice-kit-python/src/examples/voice;python toggle_wifi.py'"

os.system(command)

