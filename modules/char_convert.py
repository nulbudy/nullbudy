#!/usr/bin/python

def char_to_ascii():
    message = raw_input("Enter message to encode: ").strip()
    print "Decoded string (in ASCII):"
    for ch in message:
        print ord(ch),
    print "\n\n"

def ascii_to_char():
    message = raw_input("Enter ASCII codes: ")
    decodedMessage = ""
    for item in message.split():
        decodedMessage += chr(int(item))   

    print "Decoded message:", decodedMessage
    
def main():
    char_to_ascii()
    ascii_to_char()


main()