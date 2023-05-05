import win32clipboard
from time import sleep
import send
import runtimeREF
import requests
import threading

currentClipboard = None


def setClipboard(arg):
    global currentClipboard
    if (runtimeREF.ACTIVEIP == runtimeREF.HOSTIP):
        return
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(arg["data"])
    win32clipboard.CloseClipboard()
    currentClipboard = arg["data"]
    print(currentClipboard)


def getClipboard():
    win32clipboard.OpenClipboard()
    data = None

    # Checks if clipboard is text
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
        data = win32clipboard.GetClipboardData()
    # Checks if clipboard is a file/folder/image
    elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
        data = win32clipboard.GetClipboardData(
            win32clipboard.CF_HDROP)

    win32clipboard.CloseClipboard()
    return data


def onCopy():
    global currentClipboard
    currentClipboard = getClipboard() # To not send clipboard data on startup
    while True:
        clipboardText = getClipboard()
        if (currentClipboard == clipboardText):
            sleep(0.5)
            continue
        else:
            try:
                for i in runtimeREF.clients:
                    args = {
                        'url': f'http://{i}:8000/upload',
                        'data': clipboardText,
                        'headers': {'Content-Type': 'application/octet-stream', 'Content-Disposition': f'attachment;', "fn":"51"},
                    }
                    threading.Thread(target=requests.post, kwargs=args).start()
            except:
                continue
            currentClipboard = clipboardText
            print(currentClipboard)


if __name__ == "__main__":
    onCopy()
