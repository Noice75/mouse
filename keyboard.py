import send
from pynput import keyboard
from pynput.keyboard import Controller
import ctypes
import runtimeREF
from ctypes import c_int, c_uint, Structure, WINFUNCTYPE, POINTER
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, HMODULE, LPCWSTR, HINSTANCE, HWND

LPMSG = POINTER(MSG)
ULONG_PTR = POINTER(DWORD)

keyboardController = Controller()

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.restype = HMODULE
GetModuleHandleW.argtypes = [LPCWSTR]
user32 = ctypes.WinDLL('user32', use_last_error=True)

VK_PACKET = 0xE7

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_KEYUP = 0x02
KEYEVENTF_UNICODE = 0x04


class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [("vk_code", DWORD),
                ("scan_code", DWORD),
                ("flags", DWORD),
                ("time", c_int),
                ("dwExtraInfo", ULONG_PTR)]

# Included for completeness.


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


LowLevelKeyboardProc = WINFUNCTYPE(
    c_int, WPARAM, LPARAM, POINTER(KBDLLHOOKSTRUCT))

SetWindowsHookEx = user32.SetWindowsHookExW
SetWindowsHookEx.argtypes = [c_int, LowLevelKeyboardProc, HINSTANCE, DWORD]
SetWindowsHookEx.restype = HHOOK

UnhookWindowsHookEx = user32.UnhookWindowsHookEx
UnhookWindowsHookEx.argtypes = [HHOOK]
UnhookWindowsHookEx.restype = BOOL

GetMessage = user32.GetMessageW
GetMessage.argtypes = [LPMSG, HWND, c_uint, c_uint]
GetMessage.restype = BOOL

TranslateMessage = user32.TranslateMessage
TranslateMessage.argtypes = [LPMSG]
TranslateMessage.restype = BOOL

DispatchMessage = user32.DispatchMessageA
DispatchMessage.argtypes = [LPMSG]

CallNextHookEx = user32.CallNextHookEx


def keyboardInput(arg):
    if (arg["isPressed"]):
        keyboardController.press(arg["key"])
    else:
        keyboardController.release(arg["key"])


class listner:
    def __init__(self) -> None:
        self._listner = None
        self.startListner()

    def onPress(self, key):
        if (runtimeREF.ACTIVEIP == runtimeREF.HOSTIP):
            return
        send.send(fn=0, isPressed=True, key=key)

    def onRelease(self, key):
        if (runtimeREF.ACTIVEIP == runtimeREF.HOSTIP):
            return
        send.send(fn=0, isPressed=False, key=key)

    def startListner(self):
        self._listner = keyboard.Listener(
            on_press=self.onPress, on_release=self.onRelease, suppress=False)
        self._listner.start()

    def suppress(self):
        self._listner._suppress = True

    def unSuppress(self):
        self._listner._suppress = False

    def stop(self):
        if (self._listner._running):
            self._listner.stop()
            self._isActive = False
            self._suppress = False


if __name__ == "__main__":
    pass
