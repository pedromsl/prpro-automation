import pywinauto
import keyboard
import mouse
import cv2
import win32api
import time
from desktopmagic.screengrab_win32 import getRectAsImage
import numpy as np
import easygui
from user import *



premiere_app = pywinauto.Application().connect(path=PREMIERE_PATH, backend='win32')















# ************************
# *** HELPER FUNCTIONS ***
# ************************


def getpanel(panelname):
    """
    An easier way to get the panel we're about to send commands to.

    panelname = a str of the panel name
        Options: 'project_panel', 'effect_controls', 'effects', 'timeline', 'sourcemonitor', 'programmonitor'
    """

    return PANELS[panelname]

def configpanels():
    """
    Goes through all the panels it can find and through a simple UI configures the dictionary for finding the panels
    later on on the script.

    """
    #FOR UI CONFIG
    # for panel in range(NUMBEROFPANELS):
    #     premiere_app.window(best_match='DroverLord - TabPanel WindowDroverLord - Window Class%d' % (panel + 1),
    #                         top_level_only=False).set_focus()
    #     premiere_app.window(best_match='DroverLord - TabPanel WindowDroverLord - Window Class%d' % (panel + 1),
    #                         top_level_only=False).draw_outline()

    for panelname, panelvalue in PANELS.items():

        PANELS[panelname] = premiere_app.window(best_match=panelvalue,
                                                top_level_only=False)

    print(PANELS)


def abspos_from_rel(panel, relativevalue, corner='topleft', offset=(0, 0, 0, 0)):
    try: p = getpanel(panel)
    except KeyError:
        p = panel

    if corner == 'topleft':
        x = p.rectangle().left + offset[0]
        y = p.rectangle().top + offset[1]

    elif corner == 'topright':
        x = p.rectangle().right + offset[2]
        y = p.rectangle().top + offset[1]

    elif corner == 'bottomleft':
        x = p.rectangle().left + offset[0]
        y = p.rectangle().bottom + offset[3]

    elif corner == 'bottomright':
        x = p.rectangle().right + offset[2]
        y = p.rectangle().bottom + offset[3]

    if isinstance(relativevalue[0], float):
        x = p.rectangle().width()
        x *= relativevalue[0]
        x = int(x)
    else:
        x += relativevalue[0]


    if isinstance(relativevalue[1],  float):
        x = p.rectangle().height()
        y *= relativevalue[1]
    else:
        y += relativevalue[1]

    return (x, y)


def buildeffectpositions():
    for key in EFFECTS.keys():
        EFFECTS[key]['absolutepos'] = abspos_from_rel('effect_controls', EFFECTS[key]['relativepos'])

def current_effect_pos(effect):
    EFFECTS[effect]['absolutepos'] = abspos_from_rel('effect_controls', EFFECTS[effect]['relativepos'])
    return EFFECTS[effect]['absolutepos']

def print_effect_pos(effect):
    print(current_effect_pos(effect))

configpanels()
buildeffectpositions()

def edittext(panel, textinput=None):
    """
    Finds first Edit box on panel.

    panel = a str of the panel name
                   Options: 'project_panel', 'effect_controls', 'effects', 'timeline', 'sourcemonitor', 'programmonitor'

    textinput = string of what to type on the edit box
                      Defaults to None, meaning it will only select the edit box.
    """

    p = getpanel(panel)
    editbox = p.window(best_match='Edit')

    if DRAW_OUTLINES:
        editbox.draw_outline()

    if textinput:
        editbox.set_edit_text(textinput)
    else:
        editbox.select()


def clickrelativetopanel(panel, relativevalue, corner, click='single'):
    """
    This is a cool one because it allows for mouse automation even if you resize/rescale your UI panels as long
    as you don't change their order. Since mostly everything in Premiere is designed in a "responsive" way,
    like a responsive website, you can target whatever you need using the corners attribute.


    - panel = a str of the panel name
                  Options: 'project_panel', 'effect_controls', 'effects', 'timeline', 'sourcemonitor',
                  'programmonitor'

    - relativevalue = a tuple containing (x, y) coordinates of the relative value to move or click


    - corner = which corner to start the relative move from
        options: default is 'topleft', 'topright', 'bottomleft', 'bottomright'

    -click = 'single, 'double' or 'move'
    """
    p = getpanel(panel)

    x, y = abspos_from_rel(p, relativevalue, corner)
    mouse.move(x, y)

    if click == 'single':
        mouse.click()
    elif click == 'double':
        mouse.double_click()


def imagesearch(im, x1, y1, x2, y2, precision=0.8, image=None, offset=None):
    """
         im = file path of image to search (needle)


         (x1, y1) = top left corner of the haystack image
         (x2, y2) = bottom right corner of the haystack image

         precision = precision factor for when it considers the image to be found

         image= file path of image to be searched (haystack), defaults to = None, which then uses the ((x1,y1)(x2,y2))
               coordinates to generate this image

        Returns a tuple (x, y) with relative coordinates to the haystack
               """

    if image is None:
        image = getRectAsImage((x1, y1, x2, y2))

    img_rgb = np.array(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(im, 0)
    #w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    loc = np.where(res >= precision)
    loclist = list(zip(*loc[::-1]))
    if max_val < precision:
        return [-1, -1]

    # Returns first image found
    return (loclist[0][0], loclist[0][1])

def pixelsearch(x1, y1, x2, y2, pixel):

    im = getRectAsImage((x1, y1, x2, y2))
    image = np.array(im)
    image = image[:, :, ::-1].copy()

    lower = np.array([pixel[2], pixel[1], pixel[0]])  # BGR-code
    upper = np.array([pixel[2], pixel[1], pixel[0]])   # BGR-code

    mask = cv2.inRange(image, lower, upper)
    coord = cv2.findNonZero(mask)
    # Returns first pixel found
    return (coord[0][0][0], coord[0][0][1])

def find_pixel_and_click(panel, pixel, offset = (0,0,0,0)):
    p = getpanel(panel)
    p.draw_outline()
    x1 = p.rectangle().left + offset[0]
    y1 = p.rectangle().top + offset[1]
    x2 = p.rectangle().right - offset[2]
    y2 = p.rectangle().bottom - offset[3]

    x, y = pixelsearch(x1, y1, x2, y2, pixel)
    absx, absy = abspos_from_rel('effect_controls', (x, y), offset=offset)
    mouse.move(absx, absy)
    mouse.click()

def find_image_and_click(panel, needle, precision=0.8, click="double", offset=(0,0,0,0)):

    cursorpos = mouse.get_position()

    try:
        panel = getpanel(panel)
    except KeyError:
        panel = panel
    if DRAW_OUTLINES:
        panel.draw_outline()


    img = cv2.imread(needle)
    height, width, channels = img.shape


    # selfpos is the needle position inside the haystack rectangle, which does not correspond to the screen space
    # coordinates
    selfpos = imagesearch(needle, panel.rectangle().left, panel.rectangle().top,
                          panel.rectangle().right, panel.rectangle().bottom, precision=precision, offset=offset)

    # now we find out where in the screen those coordinates are
    #screenpos = [panel.rectangle().left + selfpos[0], panel.rectangle().top + selfpos[1]]
    screenpos = abspos_from_rel(panel, (selfpos[0], selfpos[1]), offset=offset)

    # and let's get coordinates to the the middle of the needle, just to avoid any weird clicking slightly off a pixel
    # depending on how much padding your needle image has
    x, y = (int(screenpos[0] + width / 2), int(screenpos[1] + height / 2))

    if click == "double":
        mouse.move(x, y, duration=0)
        mouse.double_click()
        mouse.move(cursorpos[0], cursorpos[1], duration=0)
    elif click == "drag":
        mouse.drag(x, y, cursorpos[0], cursorpos[1], duration=MOUSEDELAY)
    elif click == 'move':
        mouse.move(x, y)
    print("Achei a imagem!")


#find_pixel_and_click('effect_controls', (41, 92, 77))







#find_image_and_click('effect_controls', 'imgs/relogin.png', precision=0.95, click='move', offset=(0,0,0,0))




# *****************************
# *** USER CUSTOM FUNCTIONS ***
# *****************************
#
# Now we start getting into more specific functions to speed up our custom workflow.
#
#

def applyeffect(effectname, effectype):

    edittext('effects', effectname)
    find_image_and_click(getpanel('effects'), 'imgs/%seffect.png' % effectype, precision=0.95, click="double")



def instantvfx(hotkey, effect):
    """
    the keyboard.is_pressed() function returns true even in a fast little tap... maybe use keyboard.key_down()?
    I dunno, maybe wait a little bit and then check, but then if we actually want to change the effect it might be slow.
    Have to test it

   """
    t1 = time.time()

    origx, origy = mouse.get_position()
    x, y = EFFECTS[effect]['absolutepos']

    mouse.move(x, y)
    mouse.press()

    keyboard.wait(hotkey, suppress=True, trigger_on_release=True)


    t2 = time.time()
    mouse.release()

    if t2-t1 < KEY_DELAY:
        keyboard.write(EFFECTS[effect]['defaultvalue'])
        keyboard.send('enter')

    time.sleep(0.1)
    mouse.move(origx, origy)


# def timelinescrubber():
#    """Doesn't work holding the mouse down, need to figure out a mouse.onhold loop or something.
#     It conflicts with the way the function is called via the mouse library. Right now you have to click each time
#     you want to send the hotkey.
#     """
#
#     # print('called timelinescrubber')
#     # if getpanel('timeline').is_active():
#     #     while True:
#     #         if mouse.is_pressed('right'):
#     #             print("Sent Shift \\")
#     #         elif not mouse.is_pressed('right'):
#     #             print("not pressed")
#
#     if getpanel('timeline').is_active():
#         print("Sent Shift \\")
#         keyboard.send("shift+\\")

# def releasetimelinescrubber():
#     print('called releasetimelinescrubber')
#     mouse.release('right')



getpanel('project_panel').draw_outline()



keyboard.add_hotkey("shift+c", applyeffect, args=['curves', 'video'])
keyboard.add_hotkey('ctrl+shift+t', clickrelativetopanel, args=['programmonitor', (40, -85), 'bottomleft'], suppress=True)
#keyboard.add_hotkey('F9', configpanels)
keyboard.add_hotkey("F4", instantvfx, args=['F4', 'scale'])

keyboard.add_hotkey("F3", print_effect_pos, args=['scale'])


#mouse.on_right_click(timelinescrubber)

keyboard.wait()










# FIND-EFFECT_CONTROLS-EFFECT
# PANELWIDTH*0.435


## getpanel(panel).is_active()
