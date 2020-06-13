import user
import keyboard
import hotbox
import configs

def config_hotkeys():
    #keyboard.add_hotkey('ctrl+shift+t', programmonitor.clickrelativetopanel, args=[(40, -85), 'bottomleft'], suppress=True)
    keyboard.add_hotkey("F4", user.instantvfx, args=['F4', 'scale'])
    keyboard.add_hotkey("F3", user.instantvfx, args=['F3', 'rotation'])
    keyboard.add_hotkey("F2", user.instantvfx, args=['F2', 'opacity'])
    keyboard.add_hotkey("shift+c", user.applyeffect, args=['curves', 'video'])
    #keyboard.add_hotkey('ctrl+shift+t', user.programtimecode, args=['00:00:50:00'], suppress=True, trigger_on_release=True)
    #keyboard.add_hotkey('F10', user.scriptautomator, args=['scripts/script.txt'], suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('F8', user.scriptautomator, suppress=False)
    keyboard.add_hotkey('F12', user.updatepanels, args=(configs.PANELS, 'uiconfig=False'), suppress=False)
    keyboard.add_hotkey('ctrl+space', hotbox.openhotbox(), suppress=True)
    #keyboard.add_hotkey('ctrl+space', hotbox.closedhotbox, args=['executou on release hotbox'], trigger_on_release=True, suppress=True)


def update_hotkeys():
    keyboard.unhook_all_hotkeys()
    config_hotkeys()


