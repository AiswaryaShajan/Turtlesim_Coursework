# This is a comment to simply check the GitHub integration.
#!/usr/bin/env python3
from pynput.keyboard import Key, Listener
def on_press(key):
    try:    
        if key == Key.up:
            print('move forward initiated')
        elif key == Key.left:
            print('rotate left initiated')
        elif key == Key.down:
            print('move backword initiated')
        elif key == Key.right:
            print('rotate right initiated')
        else:
            pass
    except: AttributeError
    
def on_release(key):
    try:
        if key == Key.up:
            print('move forward terminated')
        elif key == Key.left:
            print('rotate left terminated')
        elif key == Key.down:
            print('move backword terminated')
        elif key == Key.right:
            print('rotate right terminated')
        else:
            pass
    except: AttributeError

try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # This line blocks the program until the listener stops
except KeyboardInterrupt:
    pass