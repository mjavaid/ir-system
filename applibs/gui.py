""" gui.py -- Application GUI Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from tkinter import *
from tkinter import ttk

""" DEFAULT_TEXTBOX_TEXT = "Enter a query..." """

### createGUI:
# Creates the user interface for the application. Creates front end 
# widgets and attaches them to the appropriate handlers.
###
def createGUI(app=None):
    if app == None:
        print("No Root Provided")
        return
    
    window = ttk.Frame(app)

    """ Top menu bar """
    menubar = Menu(app)

    # File menu
    filemenu = Menu(menubar)
    filemenu.add_command(label="Upload", command=uploadHandler)
    filemenu.add_command(label="Open", command=openHandler)
    filemenu.add_command(label="Save", command=saveHandler)
    filemenu.add_command(label="Save As...", command=saveAsHandler)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=app.quit)
    
    # Command menu
    actionmenu = Menu(menubar)
    actionmenu.add_command(label="Execute", command=executeHandler)
    actionmenu.add_command(label="Run Test Queries", command=runTestCasesHandler)
    actionmenu.add_separator()
    actionmenu.add_command(label="Reset", command=resetHandler)
    
    # Help menu
    helpmenu = Menu(menubar)
    helpmenu.add_command(label="About", command=aboutHandler)
    helpmenu.add_command(label="Instructions", command=instructionsHandler)
    
    # Adding menus to menu bar
    menubar.add_cascade(menu=filemenu, label="File")
    menubar.add_cascade(menu=actionmenu, label="Actions")
    menubar.add_cascade(menu=helpmenu, label="Help")
    app.configure(menu=menubar)
    """ End top menu bar """

    """ Action buttons frame """
    btnFrame = ttk.Frame(window, padding=(5, 5))
    
    # Creating action buttons
    openBtn = ttk.Button(btnFrame, text="Open", command=openHandler)
    saveBtn = ttk.Button(btnFrame, text="Save", command=saveHandler)
    uploadBtn = ttk.Button(btnFrame, text="Upload", command=uploadHandler)

    # Adding action buttons to frame
    openBtn.grid(column=0, row=0, sticky=(W))
    saveBtn.grid(column=1, row=0, sticky=(W))
    uploadBtn.grid(column=2, row=0, sticky=(W))

    # Adding action button frame to window
    btnFrame.grid(column=0, row=0, sticky=(W,E))
    """ End action buttons frame """
    
    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(W,E))

    """ Query frame """
    queryFrame = ttk.Frame(window, padding=(5, 5))

    # Creating query widgets
    executeBtn = ttk.Button(queryFrame, text="Execute", command=executeHandler)
    queryEntry = ttk.Entry(queryFrame, textvariable=userQuery, width=50)

    # Adding query widgets to frame
    queryEntry.grid(column=0, row=0)
    executeBtn.grid(column=1, row=0)

    # Adding query widgets frame to window
    queryFrame.grid(column=0, row=2, sticky=(W,E))
    """ End query entry frame """
    
    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=3, sticky=(W,E))
    
    """ Text frame """
    """textFrame = ttk.Frame(window, padding=(5, 5))
    
    # Creating text box
    textBox = Text(textFrame, borderwidth=3, relief="sunken", width=60, height=30)
    textBox.config(font=("consolas", 12), wrap="word")
    textBox.insert('1.0', DEFAULT_TEXTBOX_TEXT)
    
    # Creating scrollbar for textbox
    textBoxScrollBar = ttk.Scrollbar(textFrame, command=textBox.yview)
    textBox.config(yscrollcommand=textBoxScrollBar.set, state=DISABLED)
    
    # Adding text box and scrollbar to the text box frame
    textBox.grid(column=0, row=0)
    textBoxScrollBar.grid(column=1, row=0, sticky=(N,S,E,W))
    
    # Adding text box frame to the window
    textFrame.grid(column=0, row=4)"""
    """ End text frame """
    
    """ Tree frame """
    treeFrame = ttk.Frame(window, padding=(5,5))
    
    treeVScrollBar = ttk.Scrollbar(treeFrame, orient=VERTICAL)
    treeHScrollBar = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
    
    resultTree = ttk.Treeview(treeFrame, columns=("docNo", "rank", "score", "tag"), yscrollcommand=treeVScrollBar.set, xscrollcommand=treeHScrollBar.set)
    
    treeVScrollBar['command'] = resultTree.yview
    treeHScrollBar['command'] = resultTree.xview
    
    resultTree.heading("#0", text="Topic ID")
    resultTree.heading("docNo", text="Doc No.")
    resultTree.heading("rank", text="Rank")
    resultTree.heading("score", text="Score")
    resultTree.heading("tag", text="Tag")
    
    resultTree.column("#0", width=100)
    resultTree.column("docNo", width=150)
    resultTree.column("rank", width=100)
    resultTree.column("score", width=100)
    resultTree.column("tag", width=100)
    
    resultTree.grid(column=0, row=0, sticky=(N,S,E,W))
    treeHScrollBar.grid(column=0, row=1, sticky=(E,W))
    treeVScrollBar.grid(column=1, row=0, sticky=(N,S))
    
    results = []
    for i in range(50):
        results.append(['a', 'b', 'c', 'd'])
    
    populateResults(resultTree, results)
    
    treeFrame.grid(column=0, row=4)
    """ End tree frame """

    # Adding main window to app
    window.grid(column=0, row=0, sticky=(N,S,E,W))

""" ACTION HANDLERS """

### uploadHandler
# param:
#   event -
###
def uploadHandler(event=None):
    print("UPLOAD")

### executeHandler
# param:
#   event -
###
def executeHandler(event=None):
    print("EXECUTE")

### resetHandler
# param:
#   event -
###
def resetHandler(event=None):
    print("RESET")

### openHandler
# param:
#   event -
###
def openHandler(event=None):
    print("OPEN")

### saveHandler
# param:
#   event -
###
def saveHandler(event=None):
    print("SAVE")

### saveAsHandler
# param:
#   event -
###
def saveAsHandler(event=None):
    print("SAVE AS")

### quitHandler
# param:
#   event -
###
def quitHandler(event=None):
    print("QUIT")

### aboutHandler
# param:
#   event -
###
def aboutHandler(event=None):
    # Create new about window
    aboutWindow = Toplevel()
    aboutWindow.title("About")
    aboutWindow.resizable(FALSE, FALSE)
    
    # Create main frame for about window
    aboutFrame = ttk.Frame(aboutWindow, padding=(5,5))
    
    # Create text box to store about information
    aboutTextBox = Text(aboutFrame, borderwidth=3, relief="sunken", width=40, height=15)
    aboutTextBox.config(font=("consolas", 12), wrap="word")
    aboutTextBox.insert('1.0', DEFAULT_TEXTBOX_TEXT)
    
    # Adding text box and main frame to the window
    aboutTextBox.grid(column=0, row=0)
    aboutFrame.grid(column=0, row=0, sticky=(N,S,E,W))

### instructionsHandler
# param:
#   event -
###
def instructionsHandler(event=None):
    print("INSTRUCTIONS")

### runTestCasesHandler
# param:
#   event -
###
def runTestCasesHandler(event=None):
    print("RUN TEST CASES")

""" END ACTION HANDLERS """

""" FUNCTIONAL METHODS """

### populateResults
# param:
#   treeview -
#   results  -
###
def populateResults(resultTree, results):
    for iid in resultTree.get_children(): resultTree.delete(iid)
    i = 0
    for result in results:
        resultTree.insert('', 'end', text=str(i), values=result)
        i += 1

""" END FUNCTIONAL METHODS """

if __name__=="__main__":
    app = Tk()
    userQuery = StringVar()
    app.title("IR System - CSI4107")
    app.resizable(FALSE, FALSE)
    createGUI(app)
    app.mainloop()


