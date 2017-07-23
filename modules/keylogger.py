import sys,os,re
from subprocess import PIPE,Popen

def get_active_window_title():
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
                return match.group("name")

    return "Active window not found"

while True:
    print get_active_window_title()
