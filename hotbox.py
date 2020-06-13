import re
import tkinter as tk

import keyboard
import mouse

import user

hotkey = "ctrl+space"
chosen = ''
hotboxbuttons = {'Script Automator': 'scriptcutterfunc',
                 'Reverse': 'reversefunc',
                 'Warp Stabilizer': 'warpstabilizer_func'
                 #'Warp Stabilizer3': 'warpstabilizer_func',
                 #'Warp Stabilizer4': 'warpstabilizer_func',
                 #'Warp Stabilizer5': 'warpstabilizer_func',
                 #'Warp Stabilizer6': 'warpstabilizer_func',
                 #'Warp Stabilizer7': 'warpstabilizer_func',
                 #'Warp Stabilizer8': 'warpstabilizer_func',
                 #'Warp Stabilizer9': 'warpstabilizer_func',
                 #'Warp Stabilizer10': 'warpstabilizer_func',
                 #'Warp Stabilizer11': 'warpstabilizer_func',
                 }


def scriptcutterfunc():
    user.scriptautomator()
    print("Executed Script Automator")


def reversefunc():
    user.reverseclip()
    print("Executed Reverse Clip")


def warpstabilizer_func():
    user.applyeffect('Warp Stabilizer', 'video')
    print("Executed Warp Stabilizer Function")

class App(tk.Tk):
    """
    This right now is a mess. There's gotta be a way to make this better. I don't even understand clearly how it's
    working, it's basically copying and pasting various stackoverflow snippets. Pls send help.

    This is called by hotkeys.py the first time, and then it initializes the main loop.

    The hotkey is "ctrl+space"

    The weird thing is that it only activates the hideandexecute function if you release "space" first and then "ctrl",
    has to be in that order otherwise the UI stays on. Probably has something to do with the keyboard module and how it
    works.

    #\b TODO: Prettify this layout, make it so it's actually a hotbox, the buttons should be circular around the mouse without a button directly under the mouse.
    #\b TODO: If you release the hotkey outside a button, it still executes the function that corresponds to the button that was last under the mouse.

    """

    def __init__(self, *args):
        super().__init__()
        keyboard.add_hotkey(hotkey, self.show, suppress=True)
        self.hide()

        for i in hotboxbuttons.keys():
            label = tk.Label(self, text=str(i), bg='red', padx='10', pady='10')
            label.bind("<Enter>", lambda e: self.choose(e.widget['text']))
            label.pack()
            print(label)
        self.makegeo()
        print('INIT is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))

    def makegeo(self):
        geometry = self.winfo_geometry()

        width, height, top, left = [int(x) for x in re.split('[+x]', geometry)]

        mousex, mousey = mouse.get_position()

        self.geometry(f"+{mousex - round(width / 2)}+{mousey - round(height / 2)}")

    def choose(self, *args):
        global chosen
        chosen = args[0]
        print('CHOOSE is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))

    def show(self):

        self.makegeo()
        keyboard.remove_hotkey(hotkey)
        keyboard.add_hotkey(hotkey, self.hideandexecute, trigger_on_release=True, suppress=True)

        self.deiconify()
        self.lift()
        print('SHOW is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))

    def hide(self):
        self.update()
        self.withdraw()
        print('HIDE is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))

    def hideandexecute(self):
        global chosen
        print(f"Chosen {chosen}")
        keyboard.remove_hotkey(hotkey)
        keyboard.add_hotkey(hotkey, self.show, suppress=True)
        keyboard.release(hotkey)
        self.hide()
        #self.destroy()
        globals()[hotboxbuttons[chosen]]()
        print('HIDEANDEXECUTE is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))


    def on_enter(self, *args, **kwargs):
        print("mouse over")

    def on_leave(self, *args, **kwargs):
        print("mouse out")

def openhotbox():
    #events = keyboard.start_recording()
    hotbox = App()
    hotbox.lift()
    hotbox.configure(bg='white')
    hotbox.wm_attributes("-topmost", True)
    hotbox.wm_attributes("-transparentcolor", "white")
    hotbox.overrideredirect(True)
    print('OPENHOTBOX is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))
    hotbox.mainloop()



