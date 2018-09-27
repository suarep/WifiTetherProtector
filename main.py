from builtins import print
import os
import subprocess
import sched, time, threading
import ast
import psutil
import datetime

s = sched.scheduler(time, time.sleep)
goTimer= True
Killed = False
appInterval = 0


class main:

    def __init__(self):
        d = datetime.datetime.now()
        print("Main is initiated! ",d)
        print("Starting timers in init.")
        startTimer()


def startTimer():
    print("Starting timers...")

    global Killed
    global appName
    global t

    while goTimer:
        getSettings("settings.txt")
        ssid = subprocess.check_output("netsh wlan show interfaces")
        print("Checking Wifi")

        ssidString = ssid.decode("utf-8")

        for nameAPone in nameAP:
            if nameAPone in ssidString:
                if Killed is False:
                    if checkProgramRunning():
                        manageApp("kill")
                        print("Using tether! "+appName+" is killed!")
                        Killed = True
                    else:
                        print("Using tether but "+appName+" is not active.")
                else:
                    print("Using tether and "+appName+" is already killed.")
            else:
                if checkProgramRunning() is False:
                    t = threading.Thread(target=manageApp)
                    t.start()
                    print("Using safe WIFI. "+appName+" is starting.")
                    Killed = False
                else:
                    print("Not started anything")

        time.sleep(appInterval)


def manageApp(param="start"):
    global appName
    global fileUrl
    global t

    print("manageApp init!")

    if(param is "kill"):
        os.system("TASKKILL /F /IM "+appName)
        print(appName+" killed")
    else:
        subprocess.call([fileUrl])
        print(appName+" is started")



def getSettings(fileName):
    global nameAP
    global appName
    global fileUrl
    global settings
    global appInterval

    print("Gettings settings...")

    f = open(fileName, "r")
    fContent = ast.literal_eval(f.read())

    nameAP = fContent.get("ssid").split(",")
    appName = fContent.get("appName")
    fileUrl = fContent.get("fileUrl")
    appInterval = fContent.get("interval")
    nameAPString = ",".join(nameAP)
    appNameString = ",".join(appName)

    print("Target APs: "+nameAPString)
    print("Interval: ", appInterval)
    print("Target Apps: " + appNameString)
    print("Target URL: " + fileUrl)

def checkProgramRunning():
    global appName
    isRunning = False

    pythons_psutil = []
    for p in psutil.process_iter():
        try:
            if p.name() == appName:
                isRunning = True
        except psutil.Error:
            pass
    return isRunning


#Start the engine!
m = main()
