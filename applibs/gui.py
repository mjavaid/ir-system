""" gui.py -- Application GUI Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
except ImportError:
    from Tkinter import *
    import ttk
    import TkFileDialog as filedialog

import time
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ParseError

""" DEFAULT_TEXTBOX_TEXT = "Enter a query..." """
RESULT_TREE = None
USER_QUERY = None
APP_STATUS = None
PROGRESS_BAR = None

### createGUI:
# Creates the user interface for the application. Creates front end 
# widgets and attaches them to the appropriate handlers.
###
def createGUI(app=None):
    if app == None:
        print("No Root Provided")
        return
    
    global RESULT_TREE, APP_STATUS, PROGRESS_BAR, USER_QUERY

    APP_STATUS = StringVar()
    USER_QUERY = StringVar()

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
    ttk.Separator(btnFrame, orient=VERTICAL).grid(column=2, row=0, sticky=(N,S), padx=(10, 10))
    uploadBtn.grid(column=3, row=0, sticky=(W))

    # Adding action button frame to window
    btnFrame.grid(column=0, row=0, sticky=(W,E))
    """ End action buttons frame """
    
    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(W,E))

    """ Query frame """
    queryFrame = ttk.Frame(window, padding=(5, 5))

    # Creating query widgets
    executeBtn = ttk.Button(queryFrame, text="Execute", command=executeHandler)
    queryEntry = ttk.Entry(queryFrame, textvariable=USER_QUERY, width=50)

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
    
    # Creating vertical and horizontal scrollbars
    treeVScrollBar = ttk.Scrollbar(treeFrame, orient=VERTICAL)
    treeHScrollBar = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
    
    # Creating treeview for query results
    RESULT_TREE = ttk.Treeview(treeFrame,
        columns=("docNo", "rank", "score", "tag"),
        yscrollcommand=treeVScrollBar.set,
        xscrollcommand=treeHScrollBar.set
    )
    
    # Adding scrollbar functionality to treeview
    treeVScrollBar['command'] = RESULT_TREE.yview
    treeHScrollBar['command'] = RESULT_TREE.xview
    
    # Adding columns headings to treeview
    RESULT_TREE.heading("#0", text="Topic ID")
    RESULT_TREE.heading("docNo", text="Doc No.")
    RESULT_TREE.heading("rank", text="Rank")
    RESULT_TREE.heading("score", text="Score")
    RESULT_TREE.heading("tag", text="Tag")
    
    # Adding columns to the treeview
    RESULT_TREE.column("#0", width=100)
    RESULT_TREE.column("docNo", width=150)
    RESULT_TREE.column("rank", width=100)
    RESULT_TREE.column("score", width=100)
    RESULT_TREE.column("tag", width=100)
    
    # Adding treeview to the frame
    RESULT_TREE.grid(column=0, row=0, sticky=(N,S,E,W))
    treeHScrollBar.grid(column=0, row=1, sticky=(E,W))
    treeVScrollBar.grid(column=1, row=0, sticky=(N,S))
    
    # Populating treeview for demo purposes
    results = []
    for i in range(50):
        results.append([str(i), 'a', 'b', 'c', 'd'])
    populateResults(RESULT_TREE, results)

    # Adding treeview frame to the window
    treeFrame.grid(column=0, row=4)
    """ End tree frame """

    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=5, sticky=(W,E))

    """ App status frame """
    statusFrame = ttk.Frame(window, padding=(5,5))

    # Creating status label
    statusLabel = ttk.Label(statusFrame, textvariable=APP_STATUS)

    # Creating progress bar
    PROGRESS_BAR = ttk.Progressbar(statusFrame, orient=HORIZONTAL,
        length=100, mode="determinate")
    PROGRESS_BAR['value'] = 0

    # Adding status components to the status frame
    PROGRESS_BAR.grid(column=0, row=0, sticky=(E), padx=(5, 5))
    ttk.Separator(statusFrame, orient=VERTICAL).grid(column=1, row=0, sticky=(N,S))
    statusLabel.grid(column=2, row=0, sticky=(W), padx=(5, 5))

    # Adding status frame to window
    statusFrame.grid(column=0, row=6, sticky=(E,W))

    #setTaskProgress({"maximum":0, "value":0})
    """ End app status frame """

    # Adding main window to app
    window.grid(column=0, row=0, sticky=(N,S,E,W))

""" ACTION HANDLERS """

### uploadHandler
# param:
#   event -
###
def uploadHandler(event=None, filename=None):
    progressInfo = {"maximum": 4, "value": 0}
    global USER_QUERY
    if filename == None:
        uploadFileName = filedialog.askopenfilename(filetypes=(
            ('Text File', '*.txt'),
            ('XML File', '*.xml'),
            ('All Files', '*.*')
        ))
    else: openFileName = filename
    if uploadFileName == "": return
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    time.sleep(2)
    try:
        setAppStatus("Uploading query file... %s" % ((uploadFileName).split("/"))[-1])
        progressInfo["value"] += 1
        setTaskProgress(progressInfo)
        time.sleep(2)
    except FileNotFoundError:
        setAppStatus("Error: File Not Found")
        progressInfo["value"] = progressInfo["maximum"]
        setTaskProgress(progressInfo)
        return
    setAppStatus("Parsing file...")
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    time.sleep(2)
    try:
        topics = parse(uploadFileName)
    except ParseError:
        setAppStatus("Error: Invalid File Structure")
        progressInfo["value"] = progressInfo["maximum"]
        setTaskProgress(progressInfo)
        return
    for topic in topics.findall('top'):
        print(topic.findtext('num'))
    setAppStatus("User queries set. Press <EXECUTE> to run.")
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    USER_QUERY.set("[USER_QUERIES]")
    time.sleep(2)


### executeHandler
# param:
#   event -
###
def executeHandler(event=None):
    print("EXECUTE")
    global USER_QUERY
    setAppStatus("Executing query... \"%s\"" % USER_QUERY.get())

### resetHandler
# param:
#   event -
###
def resetHandler(event=None):
    print("RESET")
    setAppStatus("Resetting...")

### openHandler
# param:
#   event -
###
def openHandler(event=None):
    progressInfo = {"maximum": 4, "value": 0}
    VALID_LENGTH = 5
    openFileName = filedialog.askopenfilename(filetypes=(
        ('Text File', '*.txt'),
        ('All Files', '*.*')
    ))
    if openFileName == "": return
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    time.sleep(2)
    try:
        setAppStatus("Opening file... %s" % ((openFileName).split("/"))[-1])
        input = open(openFileName, "r")
        progressInfo["value"] += 1
        setTaskProgress(progressInfo)
        time.sleep(2)
    except FileNotFoundError:
        setAppStatus("Error: File Not Found")
        progressInfo["value"] = progressInfo["maximum"]
        setTaskProgress(progressInfo)
        return
    fileContents = (input.read()).split("\n")
    results = [result.split(",") for result in fileContents if result != ""]
    if len(results[0]) != VALID_LENGTH:
        setAppStatus("Error: Invalid File Format")
        progressInfo["value"] = progressInfo["maximum"]
        setTaskProgress(progressInfo)
        return
    setAppStatus("Populating results...")
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    time.sleep(2)
    populateResults(RESULT_TREE, results)
    setAppStatus("Results populated.")
    progressInfo["value"] += 1
    setTaskProgress(progressInfo)
    time.sleep(2)
    input.close()

### saveHandler
# param:
#   event -
###
def saveHandler(event=None):
    print("SAVE")
    setAppStatus("Saving results...")

### saveAsHandler
# param:
#   event -
###
def saveAsHandler(event=None):
    print("SAVE AS")
    setAppStatus("Saving results...")

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
    
    ABOUT_INFO_FILE = "../resources/AboutInfo.txt"
    aboutInfo = open(ABOUT_INFO_FILE, "r")
    
    # Create main frame for about window
    aboutFrame = ttk.Frame(aboutWindow, padding=(10,10))#, width=100, height=25)
    
    # Create text box to store about information
    aboutTextBox = Text(aboutFrame, width=50, height=22)
    aboutTextBox.config(font=("consolas", 12), wrap="word")
    aboutTextBox.insert('1.0', aboutInfo.read())
    aboutTextBox.config(state=DISABLED)
    
    # Adding text box and main frame to the window
    aboutTextBox.grid(column=0, row=0, sticky=(N,S,E,W))
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
    setAppStatus("Running test cases...")

""" END ACTION HANDLERS """

""" FUNCTIONAL METHODS """

### populateResults
# param:
#   treeview -
#   results  -
###
def populateResults(resultTree, results):
    for iid in resultTree.get_children(): resultTree.delete(iid)
    for result in results:
        resultTree.insert('', 'end', text=result[0], values=result[1:])

### setAppStatus
# param:
#   message -
###
def setAppStatus(message):
    global APP_STATUS
    APP_STATUS.set(message)

### setTaskProgress
# param:
#   progressInfo -
###
def setTaskProgress(progressInfo):
    global PROGRESS_BAR
    if PROGRESS_BAR['maximum'] != progressInfo['maximum']:
        PROGRESS_BAR['maximum'] = progressInfo['maximum']
    PROGRESS_BAR['value'] = progressInfo['value']

""" END FUNCTIONAL METHODS """

if __name__=="__main__":
    app = Tk()
    app.title("IR System - CSI4107")
    app.resizable(FALSE, FALSE)
    createGUI(app)
    app.mainloop()
