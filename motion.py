import time
from datetime import datetime
import os
import RPi.GPIO as io
import urllib2
import MySQLdb

io.setmode(io.BCM)


pir_pin = 23
print_pir_info = 1

#Useless, some info required by Python
show_reset = 0
repeat_motion = 0
reset = 1

io.setup(pir_pin, io.IN)

db = MySQLdb.connect(host="10.0.1.60",
                     user="testuser",
                     passwd="test623",
                     db="testdb")

def currentTime() :
        return datetime.now().strftime('%H:%M:%S')

def getTime() :
        cur = db.cursor()
        cur.execute("Select * From nodes_test Where pin='%s'" % (pir_pin))
        for row in cur.fetchall() :
                return row[11]

if print_pir_info:
        print "Motion detection activated, PIR is connector to %s" % pir_pin
        
while True:

    if reset:
        print currentTime(), "Resetting PIR"
        urlToOpen = "http://10.0.1.60/test/running_code/test3.php?pin=%s&mode=reset" % pir_pin
        urllib2.urlopen(urlToOpen)
        reset = 0

    if io.input(pir_pin):
        if repeat_motion:
                print currentTime(), "Still motion detected"
        else :
                print currentTime(), "Motion detected."

        urlToOpen = "http://10.0.1.60/test/running_code/test3.php?pin=%s&mode=on" % pir_pin
        urllib2.urlopen(urlToOpen)

        timet = getTime()
        time.sleep(timet);
        getTime()
        show_reset = 1
        repeat_motion = 1
        wasActivated = 1

    else:

        if show_reset:
                print currentTime(), "Motion sensor reset"
                urlToOpen = "http://10.0.1.60/test/running_code/test3.php?pin=%s&mode=off" % pir_pin
                urllib2.urlopen(urlToOpen)
                show_reset = 0
                repeat_motion = 0
        time.sleep(0)

    time.sleep(1)
