import sys
import csv
import gTAF_config
import os

print("Adding header to :", gTAF_config.execution_summary_csv_file)

if os.path.exists(gTAF_config.log_path):
    print("path exist already")
else:
    print("creating path :", gTAF_config.log_path)
    os.system("mkdir -p " + gTAF_config.log_path)

rows = []

if os.path.exists(gTAF_config.execution_summary_csv_file):
    print("CSV file already exist")
    with open(gTAF_config.execution_summary_csv_file, 'r') as fl:
        data = csv.reader(fl)
        fields = data.next()
        for row in data:
            rows.append(row)
else:
    print("Adding header in csv file")
    with open(gTAF_config.execution_summary_csv_file, 'a+') as ex:
        ex.write("  Jenkins ID  ")
        ex.write(",")
        ex.write(" Test Case  ")
        ex.write(",")
        ex.write("  Result  ")
        ex.write(",")
        ex.write("  Device Type  ")
        ex.write(",")
        ex.write("  Device Serial  ")
        ex.write(",")
        ex.write(" Date & Time  ")
        ex.write(",")
        ex.write(" Log Path  ")
        ex.write(",")
        ex.write(" Exception  ")
        ex.write("\n")
    ex.close()