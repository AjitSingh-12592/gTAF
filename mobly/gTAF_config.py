import json


#from mobly.test_runner import dev_model, dev_type

# Provide device type
dev_type = "mobile"
gTAF_home = "/home/edat/Desktop/gTAF/mobly/"
execution_summary_csv_file = "/gtaflog/execution_summary.csv"
html_report_file = "/gtaflog/gTAF_report.html"
html_updated_report = "/gtaflog/gTAF_report_updated.html"
gtaf_config_json = gTAF_home + 'gtaf_config.json'
sender_mail = "hclgtafreport@gmail.com"
sender_mail_pwd = "gtaf@2019"
smtp_server = 'smtp.gmail.com:587'
report_mail_to_list = ['arvind-s@hcl.com', 'harish_ku@hcl.com', 'aiytest11111@gmail.com']
log_path = "/gtaflog/"
jenkins_home = "/var/lib/jenkins"
bkp_log_path = log_path + "log_backup"
sql_db_host = '127.0.0.1'
sql_db_name = 'gtafreports'
sql_db_table_name = 'GTAFREPORTS'


map_test_device_id = "FA6BA0300749"
YT_TEST_DEVICE_SERIAL = "FA6BA0300749"
YT_BT_TARGET_SERIAL = "FA6A40300536"
YT_BT_DISCOVERER_SERIAL = "FA6BA0300749"

#CONTACT_APP_TEST_DEVICE_SERIAL = "FA6A40300536"
OCULUS_APP_TEST_DEVICE_SERIAL = "FA6A40300536"
GMAP_AUDIO_PALAYER_DEVICE_SERIAL = "FA6A40300536"
GMAP_SEARCH_AUDIO_FILE = "map_search_HCL.wav"

uiElement = []

def load_device_config(dev_model=None, android_version=None):

    global uiElement
    dev_model = dev_model.strip()
    android_version = android_version.strip()
    with open(gtaf_config_json) as json_file:
        data = json.load(json_file)
        if dev_type == 'mobile':
            if dev_model == 'Pixel' and android_version == '9':
                print("Device type selected :- ", dev_type)
                print("Device model selected :- ", dev_model)
                print("Android version selected :- ", android_version)
                uiElement = data['mobiledevice'][dev_model]['android9']
                #print(uiElement)
            if dev_model == 'Pixel 2' and android_version == '9':
                print("Device type selected :- ", dev_type)
                print("Device model selected :- ", dev_model)
                print("Android version selected :- ", android_version)
                uiElement = data['mobiledevice'][dev_model]['android9']
            if dev_model == 'Pixel 3' and android_version == '10':
                print("Device type selected : ", dev_type)
                print("Device model selected : ", dev_model)
                print("Android version selected : ", android_version)
                uiElement = data['mobiledevice'][dev_model]['android10']
            if dev_model == 'Pixel 3a' and android_version == '10':
                print("Device type selected : ", dev_type)
                print("Device model selected : ", dev_model)
                print("Android version selected : ", android_version)
                uiElement = data['mobiledevice'][dev_model]['android10']
            if dev_model == 'SM-G930F' and android_version == '8.0.0':
                print("Device type selected : " + dev_type)
                print("Device model selected : " + dev_model)
                print("Android version selected : " + android_version)
                uiElement = data['mobiledevice']['Samsung']['Galaxy S7']['android8']
            if dev_model == 'SM-G900H' and android_version == '6.0.1':
                print("Device type selected : ", dev_type)
                print("Device model selected : ", dev_model)
                print("Android version selected : ", android_version)
                uiElement = data['mobiledevice']['Samsung']['Galaxy S5']['android6']

        if 'iot' == dev_type:
            print("Device type selected : ", dev_type)
            print("Device model selected : ", dev_model)
            uiElement = data['iotdevice'][dev_model]
        if 'desktop' == dev_type:
            print("Device type selected : ", dev_type)
            print("Device model selected : ", dev_model)
            uiElement = data['desktop'][dev_model]
        if dev_type == 'TV':
            if android_version == '7.0':
                print("Device type selected : ", dev_type)
                print("Device model selected : ", dev_model)
                uiElement = data['TV'][dev_model]['build7.0']
            if android_version == '8.0':
                print("Device type selected : ", dev_type)
                print("Device model selected : ", dev_model)
                uiElement = data['TV'][dev_model]['build8.0']



