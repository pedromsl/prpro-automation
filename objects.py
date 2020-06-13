from configs import *
import pywinauto
import keyboard
import mouse
from desktopmagic.screengrab_win32 import getRectAsImage
import numpy as np
import cv2
import easygui
import time
import configparser

config = configparser.ConfigParser()
config.read('uiconfig.ini')



class Premiere(pywinauto.Application):
    def __init__(self, path, backend):
        super().__init__()
        self.connect(path=path, backend=backend)

    def prjpath(self):
        #\b TODO: get project path
        search = self.windows()





class Panel(object):
    """
    Panel wrapper class on top of the HWD Win Specification pywinauto class.
    We set all our base function here for easier panel access, like effects.edittext
    Makes it easier to design custom functions later on.
    """
    def __init__(self, obj):

        # wrap the object
        self._wrapped_obj = obj
        self.size = self.get_current_size()

    def abspos_from_rel(self, relativevalue, corner='topleft', offset=(0, 0, 0, 0)):
        """
        This is a cool one because it allows for mouse automation even if you resize/rescale your UI panels as long
        as you don't change their order. Since mostly everything in Premiere is designed in a "responsive" way,
        like a responsive website, you can target whatever you need using the corners attribute.

        :param relativevalue: a tuple containing (x, y) coordinates of the relative value to move or click
        :param corner: which corner to start the relative move from
                       options: default is 'topleft', 'topright', 'bottomleft', 'bottomright'
        :param offset: a tuple (left, top, right, bottom) for how much to offset the panel dimensions.
                       offset crops the panel area.
        :return: a tuple (x, y) of the absolute position
        """

        p = self

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

        if isinstance(relativevalue[1], float):
            x = p.rectangle().height()
            y *= relativevalue[1]
        else:
            y += relativevalue[1]

        return (x, y)

    def clickrelativetopanel(self, relativevalue, corner='topleft', click='single'):
        """
        Clicks on a relative position in a panel.

       eg: effect.controls.clickrelativetopanel(10,30)
       Will click 10 pixels to the right and 30 pixels to the bottom of the panel Effect Controls.
       Useful for UI mouse automation, even if you change the panel sizes.

        :param relativevalue: a tuple containing (x, y) coordinates of the relative value to move or click
        :param corner: which corner to start the relative move from
                       options: default is 'topleft', 'topright', 'bottomleft', 'bottomright'
        :param click: default 'single, option to 'double' click
        """



        x, y = self.abspos_from_rel(relativevalue, corner)
        mouse.move(x, y)

        if click == 'single':
            mouse.click()
        elif click == 'double':
            mouse.double_click()
        else:
            return


    def pixelsearch(self, pixel, offset=(0,0,0,0), click=''):
        """
        Searches first pixel and if click = '', return its absolute (x, y) position.

        :param pixel: a tuple (R, G, B) of int values corresponding to the pixel values.
        :param offset: a tuple (left, top, right, bottom) for how much to offset the search area.
                offset crops the panel search area so you can control better where you want to find the pixel,
                in case it finds pixels before that are not intended.
        :param click: whether to 'click', 'double' click, 'move', or if default '', return the position.
        """
        p = self
        if DRAW_OUTLINES:
            p.draw_outline()

        #Lets set our haystack bounding box to be searched
        hx1, hy1 = p.rectangle().left + offset[0], p.rectangle().top + offset[1]
        hx2, hy2 = p.rectangle().right - offset[2], p.rectangle().bottom - offset[3]

        #save that haystack as a PIL RGB image and then as a numpy array
        im = getRectAsImage((hx1,hy1,hx2,hy2))
        image = np.array(im)

        #image is RGB, but cv2 uses BGR for searching, so we need to invert it
        image = image[:, :, ::-1].copy()

        #we're not doing an upper or lower boundary because we want exactly the pixel that we specified
        lower = np.array([pixel[2], pixel[1], pixel[0]])  # BGR-code
        upper = np.array([pixel[2], pixel[1], pixel[0]])  # BGR-code

        mask = cv2.inRange(image, lower, upper)
        coord = cv2.findNonZero(mask)

        try:
            #foundcoord = first pixel found, we could implement a way to get the next pixels too.
            #             we're not limited to the first one.
            foundcoord = (coord[0][0][0], coord[0][0][1])

            #get the absolute position
            absx, absy = self.abspos_from_rel(foundcoord, offset=offset)
            print(f'Pixel found at {absx}, {absy}')

            if click == '':
                return (absx, absy)
            else:
                mouse.move(absx, absy)

            if click == 'single':
                mouse.click()
            elif click == 'double':
                mouse.double_click()
            elif click == 'move':
                return

        except TypeError:
            print('Pixel not found!')

    def imagesearch(self, im, precision=0.8, offset=(0,0,0,0), click='', moveback=True):
        """

        :param im: file path of image to search (needle)
        :param precision: precision factor for when it considers the image to be found
        :param offset: a tuple (left, top, right, bottom) for how much to offset the search area.
                offset crops the panel search area so you can control better where you want to find the pixel,
                in case it finds pixels before that are not intended.
        :param click: whether to 'click', 'double' click, 'move', or if default '', return the position.
        :param moveback: whether to move the mouse back after completion
        """

        p = self
        origx, origy = mouse.get_position()
        #Lets set our haystack bounding box to be searched
        hx1, hy1 = p.rectangle().left + offset[0], p.rectangle().top + offset[1]
        hx2, hy2 = p.rectangle().right - offset[2], p.rectangle().bottom - offset[3]


        #save it as np array
        img_rgb = np.array(getRectAsImage((hx1,hy1,hx2,hy2)))

        #cv2.matchTemplate only accepts grayscale, so transform it from BGR to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


        template = cv2.imread(im, 0)
        height, width = template.shape

        #do the search itself
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)



        loc = np.where(res >= precision)
        coord = list(zip(*loc[::-1]))

        # image not found!
        if max_val < precision:
            print('Image not found')
            return [-1, -1]

        #returns first image found. could also change it to get other images found.
        foundcoord = (coord[0][0], coord[0][1])

        # get the absolute position
        x, y = self.abspos_from_rel(foundcoord, offset=offset)

        # and lets change that position to the middle of the image found, just because it looks nicer instead of
        # the topleft pixel.
        absx = int(x + width/2)
        absy = int(y + height/2)

        print(f'Image found at {absx}, {absy}')

        if click == '':
            return absx, absy
        if click == 'single':
            mouse.move(absx, absy)
            mouse.click()
        elif click == 'double':
            mouse.move(absx, absy)
            mouse.double_click()
        elif click == 'move':
            mouse.move(absx, absy)
        if moveback:
            mouse.move(origx, origy)
        if click == 'drag':
            mouse.drag(absx, absy, origx, origy, duration=MOUSEDELAY)



    def maketable(self, rows, columns, rowoffset, columnoffset):
        #I was trying to use this for the user.instantvfx function. Didn't work well, but might be useful
        #for some automation later.
        matrix = []
        pos = []
        for r in range(rows):
            rval = r * rowoffset
            for c in range(columns):
                cval = c * columnoffset
                pos.append([cval, rval])
            matrix.append(pos)
            pos = []
        return matrix

    def getposfromtable(self, table, row, column):
        #I was trying to use this for the user.instantvfx function. Didn't work well, but might be useful
        #for some automation later.

        return tuple(table[row][column])

    def getabsposfromtable(self, origin, table, row, column):
        #I was trying to use this for the user.instantvfx function. Didn't work well, but might be useful
        #for some automation later.

        originx, originy = origin
        relposx, relposy = self.getposfromtable(table, row, column)
        abspos = (relposx+originx, relposy+originy)
        return abspos

    def updatetablepositions(self, tabletemplate, pixel=(41, 92, 77)):
        #I was trying to use this for the user.instantvfx function. Didn't work well, but might be useful
        #for some automation later.

        rowoffset = tabletemplate['ROWOFFSET']
        columnoffset = tabletemplate['COLUMNOFFSET']
        rows = tabletemplate['ROWS']
        columns = tabletemplate['COLUMNS']

        table = self.maketable(rows,columns,rowoffset,columnoffset)

        origin = self.pixelsearch(pixel)

        for k in tabletemplate.keys():
            try:
                tabletemplate[k]['absolutepos'] = self.getabsposfromtable(origin, table, tabletemplate[k]['rowcolumn'][0], tabletemplate[k]['rowcolumn'][1])
            except TypeError:
                pass



    def get_current_size(self):
        """
        :return: tuple containing current panel size (width, height)
        """
        a = [self.rectangle().width(), self.rectangle().height()]
        return tuple(a)

    def size_changed(self):
        """
        :return: True if the panel size has changed since the script initiation or UI configuration.
        """
        if self.size == self.get_current_size():
            return False
        else:
            self.size = self.get_current_size()
            return True











    def draw(self):
        self.draw_outline()

    def edittext(self, textinput=None):
        """
        Finds first edit box on panel and if textinput=None, just selects it, otherwise types textinput.
        """

        p = self
        editbox = p.window(class_name='Edit')

        if DRAW_OUTLINES:
            editbox.draw_outline()

        if textinput:
            editbox.set_edit_text(textinput)
        else:
            editbox.select()







    def __getattr__(self, attr):
        # see if this object has attr
        # NOTE do not use hasattr, it goes into
        # infinite recurrsion
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._wrapped_obj, attr)





app = Premiere(path=PREMIERE_PATH, backend='win32')

def updatepanels(panelsdict=PANELS, uiconfig=False):
    """
    #\b TODO: Don't use dictionaries, build all of this into the uiconfig.ini so the user doesn't need to update the config.py file.
    :param panelsdict: a dictionary containing the panelnames and their Droverlord Frame Window class
    :param uiconfig: defaults False, which reads from panelsdict. If True, starts the UI configurator and builds the dictionary.
    """
    #try:

    if uiconfig:
        app['Premiere Pro'].set_focus()

        #need to know the number of monitors before we start
        numberofmonitors = easygui.choicebox('What\'s the number of monitors?', 'What\'s the number of monitors?', ['1', '2'])

        for monitor in range(int(numberofmonitors)):
            monitorid = app.window(found_index=monitor, visible_only=True)
            monitorid.draw_outline(thickness=15)

            numberofpanels = easygui.integerbox('How many panels in this monitor?', 'How many panels?')

            for panel in range(numberofpanels):
                #now we want to know which panel is which on this monitor
                panelctrl = monitorid['DroverLord - Frame Window%d' % (panel + 1)]
                panelctrl.draw_outline(thickness=15)
                time.sleep(0.5)
                panelname = easygui.choicebox("Which panel is this?", 'Config Panels', panelchoices)

                if panelname is None:
                    #user selected "Cancel" on the ui, or pressed "esc". We don't care about that panel, let's go to
                    #the next one.
                        continue

                else:
                    #we now know what panel this is and on what monitor it's on. Let's save it to store on the uiconfig.ini file.
                    config[panelname]['monitor'] = str(monitor)
                    config[panelname]['class'] = f'DroverLord - Frame Window{panel+1}'
                    panelsdict[panelname] = "DroverLord - Frame Window%d" % (panel + 1)

        with open('uiconfig.ini', 'w') as configfile:
            #we went through all the UI config, now let's write it on the file.
            config.write(configfile)

    #Now we read it again from the config file and initiate the Panel instances accordingly.
    for panel in config.sections():
        k = config[panel]['monitor']
        v = config[panel]['class']

        globals()[panel] = Panel(app.window(found_index=int(k)).window(best_match=v, top_level_only=False))
        #Print it out in a way the user can copy and paste it to the config.ui file.
        print(f'[{panel}]')
        print(f'monitor = {k}')
        print(f'class = {v}\n')

    #except:
    #    print('Either you have UI disabled or no panel dictionary was provided. Try enabling UI config.')



updatepanels(PANELS, uiconfig=False)
effect_controls.updatetablepositions(EFFECTS)


if DRAW_OUTLINES:
    project_panel.draw_outline()
    effects.draw_outline()
    sourcemonitor.draw_outline()
    programmonitor.draw_outline()
    timeline.draw_outline()

# project_panel = Panel(app.window(best_match=PANELS['project_panel'], top_level_only=False))
# effect_controls = Panel(app.window(best_match=PANELS['effect_controls'], top_level_only=False))
# effects = Panel(app.window(best_match=PANELS['effects'], top_level_only=False))
# sourcemonitor = Panel(app.window(best_match=PANELS['sourcemonitor'], top_level_only=False))
# programmonitor = Panel(app.window(best_match=PANELS['programmonitor'], top_level_only=False))
# timeline = Panel(app.window(best_match=PANELS['timeline'], top_level_only=False))

