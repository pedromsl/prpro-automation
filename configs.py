#\b TODO: Save everything in the uiconfig.ini file


#  * Your main Premiere Pro Path
PREMIERE_PATH = "C:\Program Files\Adobe\Adobe Premiere Pro 2020\Adobe Premiere Pro.exe"

# Total Number of Panels, guide to figure this out: https://www.dropbox.com/s/3yl1r09a6zddfc1/panelhowto.png
# Main monitor is always MONITOR2
# Max 2 monitors right now, have to figure some stuff out for more monitors



# Mouse delay when using drag and drop
MOUSEDELAY = 0.15

# Key hold delay to consider it a key being held or a tap
KEY_DELAY = 0.15


# Determine if outlines should be drawn while the script is executing. Useful for debugging.
DRAW_OUTLINES = True


# Windows UI Scaling Settings, not implemented yet, maybe in the future, need to figure out the math :}. Shouldn't
# be too hard since mostly everything is done on a panel basis, with relative coordinates.
WINDOWS_SCALING = 1.0

#
# *************************************
# *** CHANGE THIS DICTIONARY BELOW! ***
# *************************************
#
# It's a default for my setup so I don't have to configure it all the time when running the script.
# It should only change if you change workspaces. For all of this to work it's recommended that you keep using a single
# workspace. If you change workspaces, you'll need to reconfigure it again.
#
PANELS = {'project_panel': 'DroverLord - TabPanel WindowDroverLord - Window Class1',
          'effect_controls': 'DroverLord - TabPanel WindowDroverLord - Window Class2',
          'effects': 'DroverLord - TabPanel WindowDroverLord - Window Class3',
          'sourcemonitor': 'DroverLord - TabPanel WindowDroverLord - Window Class4',
          'programmonitor': 'DroverLord - TabPanel WindowDroverLord - Window Class5',
          None: 'DroverLord - TabPanel WindowDroverLord - Window Class9',
          'timeline': 'DroverLord - TabPanel WindowDroverLord - Window Class7'}



EFFECTS = {
    'ROWOFFSET' : 22,
    'COLUMNOFFSET': 60,
    'ROWS': 12,
    'COLUMNS': 2,
    'positionx': {'defaultvalue': '960', 'rowcolumn': [0, 0], 'absolutepos': (None, None), 'taborder' : 1},
    'positiony': {'defaultvalue': '540', 'rowcolumn': [0, 1], 'absolutepos': (None, None), 'taborder' : 2},
    'scale': {'defaultvalue': '100', 'rowcolumn': [1,0], 'absolutepos': (None, None), 'taborder' : 3},
    'rotation': {'defaultvalue': '0', 'rowcolumn': [4,0], 'absolutepos': (None, None), 'taborder' : 5},
    'anchorx': {'defaultvalue': '960', 'rowcolumn': [5,0], 'absolutepos': (None, None), 'taborder' : 6},
    'anchory': {'defaultvalue': '540', 'rowcolumn': [5,1], 'absolutepos': (None, None), 'taborder' : 7},
    'opacity': {'defaultvalue': '100', 'rowcolumn': [9,0], 'absolutepos': (None, None), 'taborder' : 9},
}



panelchoices = ['project_panel', 'effect_controls', 'effects', 'timeline', 'sourcemonitor', 'programmonitor']