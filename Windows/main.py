import PySimpleGUI as sg
from Classes.UIElements import UIElements
from Classes.Encoder import Encoder
from Classes.Decoder import Decoder
## Temporary:
import threading
def runWindow():
    layout = UIElements().layout

    window = sg.Window("Image Viewer", layout)
    mode = None
    # Run the Event Loop
    event = ""
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #
        if event == "Encode":
            if values["-PASSWORD-"] != '':
                mode = Encoder(values["-COVERIMAGE-"], values["-MESSAGE-"], values["-OUTPUTFOLDER-"], values["-PASSWORD-"])
            else:
                mode = Encoder(values["-COVERIMAGE-"], values["-MESSAGE-"], values["-OUTPUTFOLDER-"])
            mode.run()
        if event == "Decode":
            if values["-PASSWORD-"] != '':
                mode = Decoder(values["-FILE11-"], values["-FOLDER11-"], values["-PASSWORD2-"])
            else:
                mode = Decoder(values["-FILE11-"], values["-FOLDER11-"])
            mode.run()  
    window.close()
    
    
#Multithreading is dumb, so I need to do this
if __name__ == '__main__':
    runWindow()