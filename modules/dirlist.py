import os

def run(**args):
    
    print("[*] In dirlist module")
    files = os.dirlist(".")
    
    return str(files)