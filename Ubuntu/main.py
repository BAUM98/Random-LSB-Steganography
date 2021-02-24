import PySimpleGUI as sg
from Classes.UIElements import UIElements
from Classes.Encoder import Encoder
## Temporary:
import threading
def runWindow():
    layout = UIElements().layout

    window = sg.Window("Image Viewer", layout)
    mode = None
    # Run the Event Loop
    print("asjkgfhadijlkhfjidshjkfhasdkjlhfl")
    event = ""
    while True:
        print("Event: " + event)
        event, values = window.read()
        print("start of loop")
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        #
        if event == "Encode":
            if values["-PASSWORD-"] != '':
                mode = Encoder(values["-COVERIMAGE-"], values["-MESSAGE-"], values["-OUTPUTFOLDER-"], True, values["-PASSWORD-"])
            else:
                mode = Encoder(values["-COVERIMAGE-"], values["-MESSAGE-"], values["-OUTPUTFOLDER-"], True)
            break
    print("Event: " + event)    
    mode.run() 
    window.close()

#Multithreading is dumb, so I need to do this
if __name__ == '__main__':
    runWindow()