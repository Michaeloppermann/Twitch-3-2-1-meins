# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import time
import os
import json
import threading
import codecs
import re

# ---------------------------------------
#   [Required] Script Information
# ---------------------------------------
ScriptName = "meins"
Website = " "
Description = "Count down a given value exponential in a given time"
Creator = "Opodeldog"
Version = "1.0.0"

configFile = "settings.json"
path = os.path.dirname(__file__)
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
pill2kill = threading.Event()
pause = False
pattern = re.compile("(<div class=\"subs-odometer\">.*<\/div>)+")
htmlFileName = "counter2.html"

def Init():
    global configFile, path, settings, threadsKeepAlive, pill2kill, pause
    Debug("Init")
    threadsKeepAlive = True
    pause = False
    # kill old processes
    pill2kill.set()
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
            countdown["countdownText"] = countdown["initialValue"]
            Debug(""
                  + " countdown: " + str(countdown))
            Parent.AddCooldown(ScriptName, settings["meins"], int(settings["cdCooldown"]))
        ReplaceInHtml()

    except:
        settings = {
            "cdInitialCountdownTime": 6,
            "cdCustomText": "Countdown done. Starting soon."
        }
    return


def ReplaceInHtml():
    global htmlFileName, countdown
    Debug("ReplaceInHtml: "
          + "htmlFileName: "
          + str(htmlFileName)
          + " countdown"
          + str(countdown))
    with codecs.open(os.path.join(path, htmlFileName), encoding='utf-8-sig', mode='r') as file:
        oldcontent = file.read()
        Debug("read")
        content = pattern.sub("<div class=\"subs-odometer\">"
                              + FormatCountdownString()
                              + "</div>"
                              , str(oldcontent))
        Debug("read2")
        Debug(content)
    with codecs.open(os.path.join(path, htmlFileName), encoding='utf-8-sig', mode='w+') as file:
        file.write(content)


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
            Pause()

        if data.GetParam(0).lower() == settings["cdSetCountdown"].lower():
            StartCountdown()

    return


# ---------------------------------------
# Reload Settings on Save
# ---------------------------------------
def ReloadSettings(jsonData):
    global threadsKeepAlive
    Debug("ReloadSettings")
    Init()
    return


def ResetAndStartCountdown():
    global countdownThreadActive
    Debug("ResetAndStartCountdown:"
          + " countdownThreadActive: " + str(countdownThreadActive))
    Init()
    StartCountdown()

def Pause():
    global pause
    pause = True
    Debug("Pause: "
          + " pause: " + str(pause))

def Continue():
    global pause
    pause = False
    Debug("Continue: "
          + " pause: " + str(pause))


def StartCountdown():
    global countdown, settings, countdownThreadActive, pill2kill

    Debug("StartCountdown:"
          + " countdown: " + str(countdown)
          + " settings: " + str(settings)
          + " pill2kill: " + str(pill2kill)
          + " countdownThreadActive: " + str(countdownThreadActive))
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
            pill2kill = threading.Event()
            threading.Thread(target=CountdownThread, args=(pill2kill, "task")).start()


def CountdownThread(stop_event, arg):
    global countdown, settings, countdownThreadActive, threadsKeepAlive, pause

    Debug("CountDownThread: "
          + " countdown: " + str(countdown)
          + " settings: " + str(settings)
          + " countdownThreadActive: " + str(countdownThreadActive)
          + " threadsKeepAlive: " + str(threadsKeepAlive)
          + " pause: " + str(pause)
          + " stop_event.is_set(): " + str(stop_event.is_set()))

    with codecs.open(os.path.join(path, countdown["countdownFileName"]), encoding='utf-8-sig', mode="w+") as file:
        file.write(FormatCountdownString())
    countdownThreadActive = True
    counter = 1
    countdown["countdownText"] = str(countdown["initialValue"])
    ReplaceInHtml()

    while countdown["countdownIsRunning"] and threadsKeepAlive and counter <= countdown["initialCountdownTime"] and not stop_event.is_set():
        if not pause:
            substractor = calculate_value(countdown["initialCountdownTime"], countdown["initialValue"], countdown["scale"], counter)
            Debug("substractor " + str(substractor))
            countdown["countdownText"] = str(countdown["currentValue"])
            countdown["currentValue"] = countdown["initialValue"] - substractor
            Debug("countdown[\"currentValue\"]: " + str(countdown["currentValue"]))

            if countdown["currentValue"] < 1.0:
                countdown["countdownText"] = settings["cdCustomText"]
                countdown["countdownIsRunning"] = False
                threadsKeepAlive = False

            if countdown["oldCountdownText"] != countdown["countdownText"]:
                ReplaceInHtml()
                # write countdown to overlay file
                with codecs.open(os.path.join(path, countdown["countdownFileName"]), encoding='utf-8-sig', mode="w+") as file:
                    file.write(FormatCountdownString())
                # write countdown to json file in case of "reload scripts" or streamlabs chatbot is shut down
                with codecs.open(os.path.join(path, countdown["countdownJsonFileName"]), encoding='utf-8-sig', mode='w+') as file:
                    json.dump({"currentValue": countdown["countdownText"]}, file)
                countdown["oldCountdownText"] = countdown["countdownText"]
            counter += 1
            time.sleep(1)

    countdownThreadActive = False
    threadsKeepAlive = True


def calculate_value(initialCountdownTime, initialValue, scale, counter):
    Debug("CalculateValue with values: initialCountdownTime:" + str(initialCountdownTime) + " initialValue:" + str(initialValue) + " scale:" + str(scale) + " counter:" + str(counter))
    substractor1 = pow(float(initialCountdownTime), float(scale))
    substractor2 = float(initialValue) / substractor1
    substractor3 = pow(float(counter), float(scale))
    Debug("substractor1: " + str(substractor1) + " substractor2: " + str(substractor2) + " substractor3: " + str(substractor3))
    return round(substractor2 * substractor3)


def FormatCountdownString():
    global countdown, settings
    Debug("FormatCountdownString:"
          + " countdown" + str(countdown)
          + " settings" + str(settings))
    if countdown["countdownText"] == settings["cdCustomText"]:
        return countdown["countdownText"]
    else:
        return str(int(countdown["currentValue"]))


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
    global path
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(path, "README.txt")
    os.startfile(location)
    return


def BtnOpenOverlayFolder():
    global path
    """Open the folder where the user can find the index.html"""
    location = os.path.join(path, "Overlay")
    os.startfile(location)
    return


def Unload():
    pill2kill.set()
    return
