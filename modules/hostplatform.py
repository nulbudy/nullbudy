import platform

def run(**args):
    print("[*] In platform module")
    
    return str(platform.uname())
