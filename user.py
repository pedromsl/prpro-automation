from objects import *
import hotkeys
import re


#\b TODO: Save new version


def instantvfx(hotkey, effect, soft=True):
    """
   """
    # \b TODO-Taran Mouse Speed Fix

    origx, origy = mouse.get_position()
    x, y = EFFECTS[effect]['absolutepos']
    if effect_controls.size_changed() or (x is None) or (y is None):
        print('Size Changed! Updating.')
        effect_controls.updatetablepositions(EFFECTS)



    x, y = EFFECTS[effect]['absolutepos']

    mouse.move(x, y)

    mouse.move(x, y)
    mouse.press()
    #attempt at Taran mouse speed fix, buggy still
    #mouse.move(400, 0, absolute=False)
    #time.sleep(0.2)
    #mouse.move(-400, 0, absolute=False)

    if soft:
        keyboard.press('ctrl')

    t1 = time.time()

    while keyboard.is_pressed(hotkey):
        continue

    mouse.release()
    keyboard.release('ctrl')
    t3 = time.time()

    if t3 - t1 < KEY_DELAY:
        keyboard.send('tab')
        keyboard.send('shift+tab')
        keyboard.write(EFFECTS[effect]['defaultvalue'])

    time.sleep(0.1)
    timeline.set_focus()
    mouse.move(origx, origy)
    #update_hotkeys()


def applyeffect(effectname, effectype):

    effects.edittext(effectname)
    effects.imagesearch('imgs/%seffect.png' % effectype, precision=0.95, click="double")

def programtimecode(timecode, active=False):
    origx, origy = mouse.get_position()
    programmonitor.set_focus()
    if not active:
        programmonitor.set_focus()
        keyboard.send('tab')
        time.sleep(0.2)
        programmonitor.edittext(timecode)
        keyboard.send('enter')
        time.sleep(0.2)
        timeline.set_focus()
        mouse.move(origx, origy)
    else:

        keyboard.send('tab')
        time.sleep(0.2)
        keyboard.send('shift+tab')
        time.sleep(0.2)
        programmonitor.edittext(timecode)
        keyboard.send('enter')

def scriptautomator(pattern='\d\d:\d\d-\d\d:\d\d', delay=0.25):
    #\b TODO: use project path from Premiere.prjpath() to use as a default location
    #\b TODO: add support for .docx
    keyboard.unhook_all_hotkeys()
    print('called script automator')
    #file = easygui.fileopenbox(msg='Select your script.', title='Select your script.', default='*.', filetypes='\*.txt')
    file = 'scripts/script.txt'
    with open(file) as f:
        script = f.read()


    cuts = re.findall(pattern, script)

    cutsmsg = '\n'.join(cuts)
    print(cutsmsg)
    #doit = easygui.buttonbox(msg=f'Found {len(cuts)} cuts.\n\n{cutsmsg}\n\nShould I execute it? If so, don\'t touch anything!',
    #                     title='Should I continue?', choices=['Continue', 'Cancel'], cancel_choice=['Cancel'], run=False)
    #doit.ui.boxRoot.attributes('-topmost', True)
    #reply = doit.run()
    #print(reply)
    reply = 'Continue'
    if reply == 'Continue':
        time.sleep(0.5)
        timeline.set_focus()
        timecodex, timecodey = timeline.abspos_from_rel((50, 40), 'topleft')

        for cut in cuts:
            cutin = '00:' + cut.split('-')[0] + ':00'
            cutout = '00:' + cut.split('-')[1] + ':00'
            print(cutin)
            print(cutout)
            #time.sleep(delay)
            print('clicking in timecode')
            mouse.move(timecodex, timecodey)
            mouse.click()

            time.sleep(delay+0.2)
            keyboard.write(cutin)
            time.sleep(delay+0.1)
            keyboard.send('enter')
            print(f'timecode {cutin} entered')
            #time.sleep(delay)
            keyboard.send('i')
            #time.sleep(delay)
            mouse.click()
            time.sleep(delay)
            keyboard.write(cutout)
            time.sleep(delay+0.1)
            print(f'timecode {cutout} entered')
            keyboard.send('enter')
            time.sleep(delay)
            keyboard.send('o')

            time.sleep(delay)
            keyboard.send('ctrl+c')
            keyboard.send('F12')
            keyboard.send('ctrl+v')
            keyboard.send('ctrl+shift+a') #deselect all

    hotkeys.config_hotkeys()

def reverseclip():
    mouse.click()
    keyboard.send('ctrl+r')
    print('REVERSECLIP1 is CTRL pressed:' + str(keyboard.is_pressed('ctrl')))
    app.window(title='Clip Speed / Duration').wait('visible')
    keyboard.release('ctrl+r')
    #time.sleep(0.2)
    keyboard.write('-100', exact='-100')
    keyboard.release('ctrl+r')
    keyboard.send('enter')



