import PySimpleGUI as sg

class UIElements:

    __input_image_box = [
        [
            sg.Text("Image to Hide File In", key="-VirginImage-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-COVERIMAGE-"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Input File to Hide", key="-Message-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-MESSAGE-"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Output Folder", key="-Output Folder-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-OUTPUTFOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Password (optional)", key="-Password Box-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-PASSWORD-"),
        ]
    ]

    __input_out_box = [
        [
            sg.Text("Embedded File", key="-Stego Image-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-STEGOIMAGE-"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Decoded File", key="-Decoded Output-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-DECODEDOUTPUT-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Password (optional)", key="-Password Box 2-", size=(15,1)),
            sg.In(size=(25, 1), enable_events=True, key="-PASSWORD2-"),
        ]
    ]

    __encode_button = [[sg.Button("Encode")]]
    __decode_button = [[sg.Button("Decode")]]

    # ----- Full layout -----
    __encode_layout = [
        [
            sg.Column(__input_image_box),
            sg.VSeperator(),
            sg.Column(__encode_button)
        ]
    ]

    __decode_layout = [
        [
            sg.Column(__input_out_box),
            sg.VSeperator(),
            sg.Column(__decode_button)
        ]
    ]

    layout = [
        [sg.TabGroup([[sg.Tab('Encode', __encode_layout),
                    sg.Tab('Decode', __decode_layout)
                    ]])],
        [sg.Button("Exit")]]