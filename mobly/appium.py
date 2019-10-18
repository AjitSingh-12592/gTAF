from appium import webdriver

print("start")

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['deviceId'] = '10.92.33.121:5555'
desired_caps['platformVersion'] = '7'
desired_caps['deviceName'] = 'BRAVIA 4K GB'
desired_caps['appPackage'] = 'com.google.android.youtube.tv'
desired_caps['appActivity'] = 'com.google.android.apps.youtube.tv.activity.ShellActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

print("finish")






