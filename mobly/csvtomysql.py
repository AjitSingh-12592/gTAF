#!/usr/bin/python3

import sys
import csv
import MySQLdb



db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='password', db='gtafreports')
cur = db.cursor()

#cur.execute("DROP TABLE IF EXISTS MOBLYTESTREPORTS")
#CREATETABLE_MOBLYTESTREPORTS = "CREATE TABLE MOBLYTESTREPORTS (RECORDID INT NOT NULL AUTO_INCREMENT, JENKINS_ID INT, TEST_NAME VARCHAR(256), #RESULT VARCHAR(256), DEVICE_TYPE VARCHAR(256), SERIAL VARCHAR(256), TIME_STAMP DATETIME(2), STACKTRACE VARCHAR(256), PATH VARCHAR(256), #PRIMARY KEY (RECORDID));"
#cur.execute(CREATETABLE_MOBLYTESTREPORTS)

csv_data = csv.reader (open ("/home/edat/mobly_logs/execution_summary.csv",'rt'))
sqlinsert = "INSERT INTO MOBLYTESTREPORTS (JENKINS_ID, \
             TEST_NAME, RESULT, DEVICE_TYPE, SERIAL, TIME_STAMP, PATH, STACKTRACE) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
for row in csv_data:
    print(row)
    print(type(row))
    cur.execute(sqlinsert,row)
    db.commit()
# disconnect from server
db.close()
print ('script successfully executed, closing the connection, bye.')
