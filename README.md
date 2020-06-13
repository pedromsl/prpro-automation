# Premiere Pro - Automation  
  
This is my try to automate Adobe Premiere and to eventually get a nice hotbox setup, like in some VFX programs.  
  
I'm basically winging it because my python experience is very limited and help is very appreciated!  
  
Heavily inspired by [Taran's Premiere AHK scripts](https://github.com/TaranVH/2nd-keyboard), but I decided to do it in Python to have a greater functionality and accessibility. AHK also has some limitations being a scripting language.  
  
We're using mainly [pywinauto](https://github.com/pywinauto/pywinauto) as a base for everything.  
  
I'll update this ReadMe file soon. For now, I've set up a [discord server](https://discord.gg/Uy5X7xn) that you can contact me on if you have any doubts or you want to help out in any way.   

## Functionality 
**Hotbox**
![enter image description here](https://i.imgur.com/pk2EZ1Y.gif)
The hotbox can be used to run any custom function. It's activated by holding the hotkey "ctrl+space". When the hotkey is released, the function under the user's mouse is executed. In this case, it's a simple function to apply an effect(could be a preset, video or audio effect, etc)


  
**Instant VFX**
![enter image description here](https://i.imgur.com/XkJ9krz.gif)
Straight rip-off from Tarans Instant VFX. Here, we can configure hotkeys to change scale, rotation, opacity.
When the user holds down the hotkey for 'scale' for example, the mouse is redirected to the scale controls. The user can then just move the mouse left to right to change scale, and when the hotkey is released, mouse goes back to where it was.

If the user gives a quick tap to the hotkey, the scale value will be reset to the default.

Cool thing here is that you can resize the Effect Controls panel at will and everything will work, as long as you don't move the panels around, which would require you to do a UI configuration.


**Ui Configurator**
![enter image description here](https://i.imgur.com/9ULM0HN.gif)
UI Configurator to make sure all the panels are recognized and the program works well. Recommended to run on the first time, or whenever you change workspaces. Will write the configuration to the uiconfig.ini file.

**The future - Script Automator**
![enter image description here](https://i.imgur.com/FpuGupd.gif)
This function here shows how powerful this automation can be. We're reading timecodes from a script and automagically cutting them and putting them at the end of timeline. If you're used to working like that, when you send a big "raw audio" clip for a producer or someone to develop a script, this can save a lot of time. Of course the intention is to accept .docx files in the future, make sure we can have various types of scripts. But this shows that we can save a lot of time automating these kinds of repetitive tasks.

#### Requirements  
  
keyboard==0.13.5  
  
mouse==0.7.1  
  
pywinauto==0.6.8  
  
numpy==1.18.5  
  
opencv-python==4.2.0.34  
  
easygui==0.98.1  
  
Desktopmagic==14.3.11  
  
pywin32==227