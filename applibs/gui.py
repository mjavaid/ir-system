""" gui.py -- Application GUI Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from tkinter import *
from tkinter import ttk

""" createGUI:
# Creates the user interface for the application. Creates front end 
# widgets and attaches them to the appropriate handlers.
"""
def createGUI(app=None):
    if app == None:
        print("No Root Provided")
        return
    
    window = ttk.Frame(app)

    """ Top menu bar """
    menubar = Menu(app)

    # File menu
    filemenu = Menu(menubar)
    filemenu.add_command(label="Upload", command=None)
    filemenu.add_command(label="Open", command=None)
    filemenu.add_command(label="Save", command=None)
    filemenu.add_command(label="Save As...", command=None)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=app.quit)
    
    # Command menu
    actionmenu = Menu(menubar)
    actionmenu.add_command(label="Execute", command=None)
    actionmenu.add_command(label="Reset", command=None)
    
    # Help menu
    helpmenu = Menu(menubar)
    helpmenu.add_command(label="About", command=None)
    helpmenu.add_command(label="Instructions", command=None)
    
    # Adding menus to menu bar
    menubar.add_cascade(menu=filemenu, label="File")
    menubar.add_cascade(menu=actionmenu, label="Actions")
    menubar.add_cascade(menu=helpmenu, label="Help")
    app.configure(menu=menubar)
    """ End top menu bar """

    """ Action buttons frame """
    btnFrame = ttk.Frame(window, padding=(5, 5))
    
    # Creating action buttons
    openBtn = ttk.Button(btnFrame, text="Open", command=None)
    saveBtn = ttk.Button(btnFrame, text="Save", command=None)
    uploadBtn = ttk.Button(btnFrame, text="Upload", command=None)

    # Adding action buttons to frame
    openBtn.grid(column=0, row=0, sticky=(W))
    saveBtn.grid(column=1, row=0, sticky=(W))
    uploadBtn.grid(column=2, row=0, sticky=(W))

    # Adding action button frame to window
    btnFrame.grid(column=0, row=0, sticky=(W,E))
    """ End action buttons frame """

    """ Query frame """
    queryFrame = ttk.Frame(window, padding=(5, 5))

    # Creating query widgets
    executeBtn = ttk.Button(queryFrame, text="Execute", command=None)
    queryEntry = ttk.Entry(queryFrame, textvariable=userQuery)

    # Adding query widgets to frame
    queryEntry.grid(column=0, row=0)
    executeBtn.grid(column=1, row=0)

    # Adding query widgets frame to window
    queryFrame.grid(column=0, row=1, sticky=(W,E))
    """ End query entry frame """

    window.grid(column=0, row=0, sticky=(N,S,E,W))


if __name__=="__main__":
    app = Tk()
    userQuery = StringVar()
    app.title("IR System - CSI4107")
    app.resizable(FALSE, FALSE)
    createGUI(app)
    app.mainloop()


