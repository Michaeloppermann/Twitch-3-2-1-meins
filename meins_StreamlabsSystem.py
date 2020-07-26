#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import clr
import time
import os
import json
import threading
import codecs
import math
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "meins"
Website = " "
Description = "Count down a given value exponential in a given time"
Creator = "Opodeldog"
Version = "1.0.0"

configFile = "settings.json"
path = os.path.dirname(__file__)
timeFromLastTick = time.time()
countdown = {
    "oldCountdownText": "",
    "countdownText": "",
    "countdownFileName": "Overlay\Countdown.txt",
    "countdownJsonFileName": "Countdown.json",
    "initialCountdownTime": 0,
    "initialValue": 0.0,
    "currentValue": 0.0,
    "countdownIsRunning": False,
    "scale": 1
}

cdVariables = {
}

settings = {}
countdownThreadActive = False
threadsKeepAlive = True
debuggingMode = True


def Init():
    global configFile, path, settings, threadsKeepAlive
    path = os.path.dirname(__file__)
    Debug("Init")    

    # create subfolder if it doesnt exist
    if not os.path.exists(os.path.dirname(os.path.join(path, countdown["countdownFileName"]))):
        os.makedirs(os.path.dirname(os.path.join(path, countdown["countdownFileName"])))

    # create overlay file if they dont exist
    if not os.path.exists(os.path.join(path, countdown["countdownFileName"])):
        with open(os.path.join(path, countdown["countdownFileName"]), "w+") as f:
            f.write(" ")

    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
            Debug("settings: " + str(settings))
            countdown["currentValue"] = settings["cdInitialValue"]
            countdown["initialValue"] = settings["cdInitialValue"]
            countdown["initialCountdownTime"] = settings["cdInitialCountdownTime"] * 60
            countdown["scale"] = settings["cdScale"]
            Debug("countdown[\"currentValue\"] " + str(countdown["currentValue"]))
            Debug("countdown[\"initialValue\"] " + str(countdown["initialValue"]))
            Debug("countdown[\"scale\"] " + str(countdown["scale"]))
            Debug("countdown[\"initialCountdownTime\"] " + str(countdown["initialCountdownTime"]))
            Parent.AddCooldown(ScriptName, settings["meins"], int(settings["cdCooldown"]))
    except:
        settings = {
            "cdInitialCountdownTime": 6,
            "cdCustomText": "Countdown done. Starting soon."
        }

    # load countdown from json file
    # try:
    #     path = os.path.dirname(__file__)
    #     with codecs.open(os.path.join(path, countdown["countdownJsonFileName"]), encoding='utf-8-sig',
    #                      mode='r') as file:
    #         countdown["currentValue"] = json.load(file, encoding='utf-8-sig')["currentValue"]
    #         if countdown["currentValue"] > 0:
    #             StartCountdown()
    #         else:
    #             threadsKeepAlive = False
    # except:
    #     pass

    return


def Execute(data):
    global settings, cdVariables, countdown, threadsKeepAlive, countdownThreadActive

    Debug("Execute")
    Debug("data.IsChatMessage(), data.GetParamCount()" + " " + str(data.IsChatMessage()) + " " + str(data.GetParamCount()))

    if data.IsChatMessage():
        # sets new countdown and starts it
        if data.GetParamCount() == 3 and data.GetParam(0).lower() == settings["cdSetCountdown"].lower():
            if Parent.HasPermission(data.User, "Caster", ""):
                try:
                    countdown["initialValue"] = float(
                        data.GetParam(2))
                    Debug("param1: " + str(data.GetParam(1)))
                    countdown["currentValue"] = countdown["initialValue"]
                    countdown["initialCountdownTime"] = int(
                        data.GetParam(1)) * 60
                    if not countdown["countdownIsRunning"]:
                        StartCountdown()
                except ValueError:
                    if settings["cdShowCountdownResponse"]:
                        Parent.SendTwitchMessage(
                            ("Incorrect usage. Write " + settings["cdSetCountdown"] + " <seconds> to set the new countdown.")[:490])

        if data.GetParamCount() == 1 and data.GetParam(0).lower() == settings["meins"].lower() and countdownThreadActive and not Parent.IsOnCooldown(ScriptName, settings["meins"]):
            Parent.SendTwitchMessage(
                ( data.UserName + " hat sich das Spiel fuer " + str(int(round(countdown["currentValue"]))) + " Kekse gesnaggt!")[:490])
            threadsKeepAlive = False
            countdownThreadActive = False

        if data.GetParam(0).lower() == settings["cdSetCountdown"].lower():
            StartCountdown()

    return


#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    Debug("ReloadSettings")

    Init()
    return


def StartBySetting():
    global countdown, settings, countdownThreadActive

    Debug("StartBySetting")
    Debug("countdown[\"currentValue\"] " + str(countdown["currentValue"]))
    Debug("countdown[\"initialValue\"] " + str(countdown["initialValue"]))
    Debug("countdown[\"scale\"] " + str(countdown["scale"]))
    Debug("countdown[\"initialCountdownTime\"] " + str(countdown["initialCountdownTime"]))
    StartCountdown()


def StartCountdown():
    global countdown, settings, countdownThreadActive

    Debug("StartCountdown")

    countdown["oldCountdownText"] = " "
    with codecs.open(os.path.join(path, countdown["countdownFileName"]), encoding='utf-8-sig', mode='w+') as file:
        file.write(" ")
    with codecs.open(os.path.join(path, countdown["countdownJsonFileName"]), encoding='utf-8-sig', mode='w+') as file:
        json.dump({"currentValue": 0}, file)

    countdown["countdownIsRunning"] = True
    if not countdownThreadActive:
        if settings["cdShowCountdownResponse"]:
            Parent.SendTwitchMessage(
                ("New countdown set to " + str(int(countdown["initialCountdownTime"] / 60)) + " minutes and " + str(
                    int(countdown["initialValue"])) + " Kekse.")[:490])
        thread = threading.Thread(target=CountdownThread, args=()).start()


def CountdownThread():
    global cdVariables, countdown, settings, timeFromLastTick, countdownThreadActive, threadsKeepAlive

    Debug("CountDownThread, countdown[\"currentValue\"] " + str(countdown["currentValue"]))
    with codecs.open(os.path.join(path, countdown["countdownFileName"]), encoding='utf-8-sig', mode="w+") as file:
        file.write(FormatCountdownString())
    countdownThreadActive = True
    counter = 0
    scale = countdown["scale"]
    correctfactor = scale * float(countdown["initialValue"]) / 10
    base = float(GetBase(countdown["initialValue"] - correctfactor, countdown["initialCountdownTime"]))
    substractor = base
    Debug("substractor " + str(substractor))
    Debug("countdown[\"currentValue\"] " + str(countdown["currentValue"]))
    Debug("countdown[\"initialCountdownTime\"] " + str(countdown["initialCountdownTime"]))

    Debug("threadsKeepAlive " + str(threadsKeepAlive))
    while countdown["countdownIsRunning"] and threadsKeepAlive and counter <= countdown["initialCountdownTime"]:
        counter += 1
        Debug("counter: " + str(counter))
        Debug("threadsKeepAlive: " + str(threadsKeepAlive))
        Debug("countdown[\"currentValue\"] " + str(countdown["currentValue"]))
        Debug("(float(countdown[\"initialCountdownTime\"]) / float(counter): " + str(float(countdown["initialCountdownTime"]) / float(counter)))
        # Debug("scaleFactor: " + str(math.sqrt(float(countdown["initialCountdownTime"]) / float(counter))))
        substract = pow(substractor, float(counter)) + (correctfactor * (float(counter) / countdown["initialCountdownTime"]))
        Debug("substract " + str(substract))
        countdown["countdownText"] = str(countdown["currentValue"])
        if countdown["currentValue"] < 1:
            countdown["countdownText"] = settings["cdCustomText"]
            countdown["countdownIsRunning"] = False

        else:
            countdown["currentValue"] = countdown["initialValue"] - substract

        if countdown["oldCountdownText"] != countdown["countdownText"]:
            # write countdown to overlay file
            with codecs.open(os.path.join(path, countdown["countdownFileName"]), encoding='utf-8-sig', mode="w+") as file:
                file.write(FormatCountdownString())
            # write countdown to json file in case of "reload scripts" or streamlabs chatbot is shut down
            with codecs.open(os.path.join(path, countdown["countdownJsonFileName"]), encoding='utf-8-sig', mode='w+') as file:
                json.dump({"currentValue": countdown["countdownText"]}, file)
            countdown["oldCountdownText"] = countdown["countdownText"]
        time.sleep(1)
    countdownThreadActive = False
    threadsKeepAlive = True


def GetBase(x, y):
    Debug("GetBase x, y, 1/y, pow(x,1/y)" + str(x) + ", " + str(y) + ", " + str(1.0/y) + ", " + str(pow(x, 1.0/y)))
    return pow(x, 1.0/y)


def FormatCountdownString():
    global cdVariables, countdown, settings
    Debug("FormatCountdownString")
    if countdown["countdownText"] == settings["cdCustomText"]:
        return countdown["countdownText"]
    else:
        return str(int(round(countdown["currentValue"])))


def Debug(message):
    global debuggingMode
    if debuggingMode:
        Parent.Log("!meins", message)


def Tick():
    return


def ScriptToggled(state):
    global threadsKeepAlive
    # if enabled again tell the script to keep the threads running again
    if state:
        threadsKeepAlive = True
    # if the script gets disabled, stop all timers and resets the textfiles
    else:
        threadsKeepAlive = False
    return


def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)
    return


def BtnOpenOverlayFolder():
    """Open the folder where the user can find the index.html"""
    location = os.path.join(os.path.dirname(__file__), "Overlay")
    os.startfile(location)
    return
