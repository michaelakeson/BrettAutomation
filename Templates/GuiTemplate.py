import PySimpleGUI as sg
import csv, os
sg.theme('DarkAmber')   # Add a touch of color
#sg.theme("LightBlue")


def MyApp():
    working_directory = os.getcwd()

    col_layout = [
        [sg.Text("By: Brett Brooks", font=('Helvetica', 14))]]
    
#Main GUI layout
    layout = [  
                [sg.Text("Automation Name", font=('Helvetica', 30))],
                [sg.Text(" ", font=('Helvetica', 15))], #padding
                [sg.Text("Select excel file for processing.", font=('Helvetica', 14))],
                [sg.InputText(key="-FILE_PATH-"), 
                sg.FileBrowse(initial_folder=working_directory, file_types=[("CSV Files", "*.csv")])],
                [sg.Button('Submit'), sg.Exit()],
                [sg.Text(" ", font=('Helvetica',28))], #padding
                [sg.Column(col_layout, element_justification='left', expand_x=True)],
            ]
#Launch Gui, (add arguments to sg.window)
    window = sg.Window("A Brett Brooks Automation", layout, size=(500, 250), element_justification='c')

#loop to keep Window Running until exit button is clicked
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit":
            FilePath = values["-FILE_PATH-"]
#print FilePath 
#Or put function here to run pandas workflow using FilePath as input path.
            print(FilePath)   
    window.close()




MyApp()
