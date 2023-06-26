import PySimpleGUI as sg
import csv, os
import time
import queue
import threading

sg.theme('DarkAmber')   # Add a touch of color
#sg.theme("LightBlue")


#update this function with process.
def long_function_wrapper(FilePath,work_id, gui_queue):
    # this is our "long running function call"
    x = 0
    while True:
        print(x)
        time.sleep(1.2)
        x = x + 1
        if x == 5:
            break
    # at the end of the work, before exiting, send a message back to the GUI indicating end
    gui_queue.put('{} ::: done'.format(work_id))
    # at this point, the thread exits
    return 


# no editing is needed below this point 
############################# GUI Code #############################
def GetLayout():
    #Create the layout for the interface window.
    #Elements
    working_directory = os.getcwd()
    col_layout = [
        [sg.Text("By: Brett Brooks", font=('Helvetica', 14))],
        [sg.Text(size=(25, 1), key='_Runtime_')]
        ]
    #Main GUI layout
    layout = [  
            [sg.Text("Automation Name", font=('Helvetica', 30))],
            [sg.Text(" ", font=('Helvetica', 15))], #padding
            [sg.Text("Select excel file for processing.", font=('Helvetica', 14))],
            [sg.InputText(key="-FILE_PATH-"), sg.FileBrowse(initial_folder=working_directory)],
            [sg.Button('Submit'), sg.Exit()],
            [sg.Text(size=(25, 1), key='_OUTPUT_')],
            [sg.Text(size=(25, 1), key='_OUTPUT2_')],
            [sg.Text(" ", font=('Helvetica',5))], #padding
            [sg.Column(col_layout, element_justification='left', expand_x=True)]
            ]
    return layout


def MyApp():
   #default set up
    working_directory = os.getcwd()
    gui_queue = queue.Queue()  # queue used to communicate between the gui and long-running code
   
#Main GUI layout
    layout = GetLayout()  

#Create Main Gui, (add arguments to sg.window)
    window = sg.Window("A Brett Brooks Automation", layout, size=(500, 270), element_justification='c')

# --------------------- EVENT LOOP ---------------------
    work_id = 0
    while True:
        event, values = window.Read(timeout=100)  # wait for up to 100 ms for a GUI event

        if event is None or event == 'Exit':
            # sg.PopupAnimated(None)
            break
        if event == "Submit":  # clicking "Go" starts a long running work item by starting thread
            start = time.time()
            FilePath = values["-FILE_PATH-"]
            window.Element('_OUTPUT_').Update('Processing...')
            # LOCATION 2
            # STARTING long run by starting a thread
            thread_id = threading.Thread(target=long_function_wrapper, args=(FilePath, work_id, gui_queue,), daemon=True)
            thread_id.start()
            work_id = work_id + 1   


        # --------------- Read next message coming in from threads ---------------
        try:
            message = gui_queue.get_nowait()  # see if something has been posted to Queue
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # nothing in queue so do nothing
        # if message received from queue, then some work was completed
        if message is not None:
            # this is the place you would execute code at ENDING of long running task
            # You can check the completed_work_id variable to see exactly which long-running function completed
            completed_work_id = int(message[:message.index(' :::')])
            runtime = str(round(time.time() - start,1))
            window.Element('_OUTPUT_').Update('Finished')
            window.Element('_OUTPUT2_').Update('Process Completed: %s' % runtime)
            work_id -= 1
            if not work_id:
                sg.PopupAnimated(None)

        if work_id:
            runtime = str(round(time.time() - start,1))
            window.Element('_OUTPUT2_').Update('Runtime: %s' % runtime)

    # if user exits the window, then close the window and exit the GUI func
    window.Close()




############################# Main #############################
if __name__ == '__main__':
    MyApp()
    print('Exiting Program') 
