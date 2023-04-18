from pynput import mouse
from pynput.mouse import Button, Controller
import ctypes
from ctypes import c_int32, c_int,  c_long, Structure, CFUNCTYPE, POINTER
from ctypes.wintypes import DWORD, MSG, WPARAM, LPARAM, UINT
import ctypeswrappers as cws
import send

LPMSG = POINTER(MSG)
SENSITIVITY = send.SENSITIVITY

HWND_MESSAGE = -3

WM_QUIT = 0x0012
WM_INPUT = 0x00FF
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

HID_USAGE_PAGE_GENERIC = 0x01

RIDEV_NOLEGACY = 0x00000030
RIDEV_INPUTSINK = 0x00000100
RIDEV_CAPTUREMOUSE = 0x00000200

RID_HEADER = 0x10000005
RID_INPUT = 0x10000003

RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RIM_TYPEHID = 2

PM_NOREMOVE = 0x0000
user32 = ctypes.WinDLL('user32', use_last_error=True)
mouseController = Controller()


class MSLLHOOKSTRUCT(Structure):
    _fields_ = [("x", c_long),
                ("y", c_long),
                ('data', c_int32),
                ('reserved', c_int32),
                ("flags", DWORD),
                ("time", c_int),
                ]


LowLevelMouseProc = CFUNCTYPE(c_int, WPARAM, LPARAM, POINTER(MSLLHOOKSTRUCT))
SetWindowsHookEx = user32.SetWindowsHookExA
UnhookWindowsHookEx = user32.UnhookWindowsHookEx
GetMessage = user32.GetMessageW
NULL = c_int(0)


def wnd_proc(hwnd, msg, wparam, lparam):  # Callback
    if (send.activeIP == send.HOSTIP):
        return cws.DefWindowProc(hwnd, msg, wparam, lparam)
    if msg == WM_INPUT:
        size = UINT(0)
        res = cws.GetRawInputData(ctypes.cast(lparam, cws.PRAWINPUT), RID_INPUT, None, ctypes.byref(
            size), ctypes.sizeof(cws.RAWINPUTHEADER))
        if res == UINT(-1) or size == 0:
            print_error(text="GetRawInputData 0")
            return 0
        buf = ctypes.create_string_buffer(size.value)
        res = cws.GetRawInputData(ctypes.cast(lparam, cws.PRAWINPUT), RID_INPUT, buf, ctypes.byref(
            size), ctypes.sizeof(cws.RAWINPUTHEADER))
        if res != size.value:
            print_error(text="GetRawInputData 1")
            return 0
        ri = ctypes.cast(buf, cws.PRAWINPUT).contents
        head = ri.header
        if head.dwType == RIM_TYPEMOUSE:
            data = ri.data.mouse.to_string()
            captured_outputX, captured_outputY = data.split(
                "lLastX: ")[-1].split("\n")[0], data.split(
                "lLastY: ")[-1].split("\n")[0]
            send.send(fn="move", x=int(float(captured_outputX)) *
                      SENSITIVITY, y=int(float(captured_outputY)) *
                      SENSITIVITY)
        elif head.dwType == RIM_TYPEKEYBOARD:  # If anyone want to convert Keyboard rawinput, GoodLuck!
            data = ri.data.keyboard
            if data.VKey == 0x1B:
                cws.PostQuitMessage(0)
        elif head.dwType == RIM_TYPEHID:
            data = ri.data.hid
        else:
            print("Wrong raw input type!!!")
            return 0
    return cws.DefWindowProc(hwnd, msg, wparam, lparam)


def print_error(code=None, text=None):
    text = text + " - e" if text else "E"
    code = cws.GetLastError() if code is None else code
    print(f"{text}rror code: {code}")


def register_devices(hwnd=None):
    flags = RIDEV_INPUTSINK
    generic_usage_ids = (0x01, 0x02, 0x04, 0x05, 0x06, 0x07, 0x08)
    devices = (cws.RawInputDevice * len(generic_usage_ids))(
        *(cws.RawInputDevice(HID_USAGE_PAGE_GENERIC, uid, flags, hwnd) for uid in generic_usage_ids)
    )
    if cws.RegisterRawInputDevices(devices, len(generic_usage_ids), ctypes.sizeof(cws.RawInputDevice)):
        print("Successfully registered input device(s)!")
        return True
    else:
        print_error(text="RegisterRawInputDevices")
        return False


def getMouseRawInput():
    wnd_cls = "SO049572093_RawInputWndClass"
    wcx = cws.WNDCLASSEX()
    wcx.cbSize = ctypes.sizeof(cws.WNDCLASSEX)
    wcx.lpfnWndProc = cws.WNDPROC(wnd_proc)
    wcx.hInstance = cws.GetModuleHandle(None)
    wcx.lpszClassName = wnd_cls
    res = cws.RegisterClassEx(ctypes.byref(wcx))
    if not res:
        print_error(text="RegisterClass")
        return 0
    hwnd = cws.CreateWindowEx(0, wnd_cls, None, 0, 0,
                              0, 0, 0, 0, None, wcx.hInstance, None)
    if not hwnd:
        print_error(text="CreateWindowEx")
        return 0
    if not register_devices(hwnd):
        return 0
    msg = MSG()
    pmsg = ctypes.byref(msg)
    print("Start loop (press <ESC> to exit)...")
    while res := cws.GetMessage(pmsg, None, 0, 0):
        if res < 0:
            print_error(text="GetMessage")
            break
        cws.TranslateMessage(pmsg)
        cws.DispatchMessage(pmsg)


class listner:
    def __init__(self) -> None:
        self._listner = None
        self.startListner()

    def onClick(self, x, y, button, pressed):
        if (send.activeIP == send.HOSTIP):
            return
        send.send(fn='clickMouseButton', isPressed=pressed, btn=button)

    def onScroll(self, x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    def startListner(self):
        self._listner = mouse.Listener(
            on_click=self.onClick, on_scroll=self.onScroll, suppress=False)
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


def clickMouseButton(arg):
    if (arg['isPressed']):
        if ("left" in str(arg['btn'])):
            mouseController.press(Button.left)
            return
        mouseController.press(Button.right)
    else:
        if ("left" in str(arg['btn'])):
            mouseController.release(Button.left)
            return
        mouseController.release(Button.right)


def move(arg):
    mouseController.move(arg["x"], arg["y"])


if __name__ == "__main__":
    x = listner()
    x.start()
    import time
    time.sleep(5)
    x.suppress()
    time.sleep(5)
    x.unSuppress()
    time.sleep(2)
    x.suppress()
    time.sleep(2)
    x.stop()
    getMouseRawInput()
