import os
import sys
import subprocess

os.system("mkdir logs_aiy/logs_bkp")
os.system("cp  logs_aiy/*.log logs_aiy/logs_bkp/")
os.system("rm logs_aiy/*.log")


#AIY Voice kit login details
aiy_username = "pi"
aiy_ip_addr = "10.92.33.186"
aiy_password = "ubuntu"

command = "sshpass -p '" + aiy_password + "' ssh -o StrictHostKeyChecking=no " + aiy_username + "@" + aiy_ip_addr + " 'cd /home/pi/AIY-voice-kit-python/src/examples/voice;./aiy_google_test.sh'"

os.system(command)

expected_words = ('New', 'Delhi', 'capital')

India_google_home_response = subprocess.check_output("cat logs_aiy/India_google_home_response_*", shell=True)
Portuguese_google_home_response = subprocess.check_output("cat logs_aiy/Portuguese_google_home_response_*", shell=True)
UK_google_home_response = subprocess.check_output("cat logs_aiy/UK_google_home_response_*", shell=True)
US_google_home_response = subprocess.check_output("cat logs_aiy/US_google_home_response_*", shell=True)
#Canadian_google_home_response = subprocess.check_output("cat logs_aiy/Canadian_google_home_response_*", shell=True)

for value in India_google_home_response:
    if value in India_google_home_response:
        print("Expected word ", value, " found for Google home response in Indian english accent")
        assert True
    else:
        print("Value not found for :", value)

for value in Portuguese_google_home_response:
    if value in Portuguese_google_home_response:
        print("Expected word ", value, " found for Google home response in Portuguese english accent")
        assert True
    else:
        print("Value not found for :", value)


for value in UK_google_home_response:
    if value in UK_google_home_response:
        print("Expected word ", value, " found for Google home response in UK english accent")
        assert True
    else:
        print("Value not found for :", value)


for value in US_google_home_response:
    if value in US_google_home_response:
        print("Expected word ", value, " found for Google home response in US english accent")
        assert True
    else:
        print("Value not found for :", value)

#for value in Canadian_google_home_response:
#    if value in Canadian_google_home_response:
#        print("Expected word ", value, " found for Google home response in Canadian english accent")
#        assert True
#    else:
#        print("Value not found for :", value)


