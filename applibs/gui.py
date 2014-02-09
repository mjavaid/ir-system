""" gui.py -- Application GUI Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
"""

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ParseError
import csv

from preprocessing import filterQuery
from resultfetching import getDocsForTokens, getSim
import json

from utils import DOCUMENTS, DOCUMENTS_CACHE_FILE, TABLE_LIST_CACHE_FILE, TEST_RESULTS_DIR

import utils

""" DEFAULT_TEXTBOX_TEXT = "Enter a query..." """

### createGUI:
# Creates the user interface for the application. Creates front end 
# widgets and attaches them to the appropriate handlers.
###
class APPLICATION(Tk):
    USER_QUERY = None
    APP_STATUS = None
    MODIFIED = False
    SAVE_FILE = False
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("IR System - CSI4107")
        self.resizable(FALSE, FALSE)
        self.wm_protocol("WM_DELETE_WINDOW", self.quitHandler)
        self.APP_STATUS = StringVar()
        self.USER_QUERY = StringVar()
        self.createGUI()

    def createGUI(self):
        if self == None:
            print("No Root Provided")
            return

        window = ttk.Frame(self)

        """ Top menu bar """
        menubar = Menu(self)

        # File menu
        filemenu = Menu(menubar)
        filemenu.add_command(label="Upload", command=self.uploadHandler)
        filemenu.add_command(label="Open", command=self.openHandler)
        filemenu.add_command(label="Save", command=self.saveHandler)
        filemenu.add_command(label="Save As...", command=self.saveAsHandler)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quitHandler)
    
        # Command menu
        actionmenu = Menu(menubar)
        actionmenu.add_command(label="Execute", command=self.executeHandler)
    
        # Help menu
        helpmenu = Menu(menubar)
        helpmenu.add_command(label="About", command=self.aboutHandler)
        helpmenu.add_command(label="Instructions", command=self.instructionsHandler)
    
        # Adding menus to menu bar
        menubar.add_cascade(menu=filemenu, label="File")
        menubar.add_cascade(menu=actionmenu, label="Actions")
        menubar.add_cascade(menu=helpmenu, label="Help")
        self.configure(menu=menubar)
        """ End top menu bar """

        """ Action buttons frame """
        btnFrame = ttk.Frame(window, padding=(5, 5))
    
        # Creating action buttons
        openBtn = ttk.Button(btnFrame, text="Open", command=self.openHandler)
        saveBtn = ttk.Button(btnFrame, text="Save", command=self.saveHandler)
        uploadBtn = ttk.Button(btnFrame, text="Upload Queries", command=self.uploadHandler)

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
        executeBtn = ttk.Button(queryFrame, text="Execute", command=self.executeHandler)
        queryEntry = ttk.Entry(queryFrame, textvariable=self.USER_QUERY, width=50)

        # Adding query widgets to frame
        queryEntry.grid(column=0, row=0)
        executeBtn.grid(column=1, row=0)

        # Adding query widgets frame to window
        queryFrame.grid(column=0, row=2, sticky=(W,E))
        """ End query entry frame """
    
        ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=3, sticky=(W,E))
    
        """ Tree frame """
        treeFrame = ttk.Frame(window, padding=(5,5))
    
        # Creating vertical and horizontal scrollbars
        treeVScrollBar = ttk.Scrollbar(treeFrame, orient=VERTICAL)
        treeHScrollBar = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
    
        # Creating treeview for query results
        self.RESULT_TREE = ttk.Treeview(treeFrame,
            columns=("docNo", "rank", "score", "tag"),
            yscrollcommand=treeVScrollBar.set,
            xscrollcommand=treeHScrollBar.set
        )
    
        # Adding scrollbar functionality to treeview
        treeVScrollBar['command'] = self.RESULT_TREE.yview
        treeHScrollBar['command'] = self.RESULT_TREE.xview
    
        # Adding columns headings to treeview
        self.RESULT_TREE.heading("#0", text="Topic ID")
        self.RESULT_TREE.heading("docNo", text="Doc No.")
        self.RESULT_TREE.heading("rank", text="Rank")
        self.RESULT_TREE.heading("score", text="Score")
        self.RESULT_TREE.heading("tag", text="Tag")
    
        # Adding columns to the treeview
        self.RESULT_TREE.column("#0", width=100)
        self.RESULT_TREE.column("docNo", width=150)
        self.RESULT_TREE.column("rank", width=100)
        self.RESULT_TREE.column("score", width=100)
        self.RESULT_TREE.column("tag", width=100)
    
        # Adding treeview to the frame
        self.RESULT_TREE.grid(column=0, row=0, sticky=(N,S,E,W))
        treeHScrollBar.grid(column=0, row=1, sticky=(E,W))
        treeVScrollBar.grid(column=1, row=0, sticky=(N,S))
    
        # Populating treeview for demo purposes
        #results = []
        #for i in range(50):
        #results.append([str(i), 'a', 'b', 'c', 'd'])
        #self.populateResults(results)

        # Adding treeview frame to the window
        treeFrame.grid(column=0, row=4)
        """ End tree frame """

        ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=5, sticky=(W,E))

        """ App status frame """
        statusFrame = ttk.Frame(window, padding=(5,5))

        # Creating status label
        statusLabel = ttk.Label(statusFrame, textvariable=self.APP_STATUS)

        # Creating progress bar
        self.PROGRESS_BAR = ttk.Progressbar(statusFrame, orient=HORIZONTAL,
            length=100, mode="determinate")
        self.PROGRESS_BAR['value'] = 0

        # Adding status components to the status frame
        self.PROGRESS_BAR.grid(column=0, row=0, sticky=(E), padx=(5, 5))
        ttk.Separator(statusFrame, orient=VERTICAL).grid(column=1, row=0, sticky=(N,S))
        statusLabel.grid(column=2, row=0, sticky=(W), padx=(5, 5))

        # Adding status frame to window
        statusFrame.grid(column=0, row=6, sticky=(E,W))

        #setTaskProgress({"maximum":0, "value":0})
        """ End app status frame """

        # Adding main window to app
        window.grid(column=0, row=0, sticky=(N,S,E,W))
        
        self.setAppStatus("Application Initialized.")

    """ ACTION HANDLERS """

    ### uploadHandler
    # param:
    #   event -
    ###
    def uploadHandler(self, event=None, filename=None):
        progressInfo = {"maximum": 4, "value": 0}
        if filename == None:
            uploadFileName = filedialog.askopenfilename(filetypes=(
                ('Text File', '*.txt'),
                ('XML File', '*.xml'),
                ('All Files', '*.*')
            ))
        else: openFileName = filename
        if uploadFileName == "": return
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        try:
            self.setAppStatus("Uploading query file... %s" % ((uploadFileName).split("/"))[-1])
            progressInfo["value"] += 1
            self.setTaskProgress(progressInfo)
        except FileNotFoundError:
            self.setAppStatus("Error: File Not Found")
            progressInfo["value"] = progressInfo["maximum"]
            self.setTaskProgress(progressInfo)
            return
        self.setAppStatus("Parsing file...")
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        try:
            topics = parse(uploadFileName)
        except ParseError:
            self.setAppStatus("Error: Invalid File Structure")
            progressInfo["value"] = progressInfo["maximum"]
            self.setTaskProgress(progressInfo)
            return
        for topic in topics.findall('top'):
            topicNum = topic.findtext('num').strip().split(" ")[1]
            query = topic.findtext('title').strip()
            self.executeHandler(None, True, query)
            self.SAVE_FILE = TEST_RESULTS_DIR + topicNum + "_Results.txt"
            self.saveHandler(None)
        self.setAppStatus("Test queries executed. Saved in: [%s]" % TEST_RESULTS_DIR)
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        self.USER_QUERY.set("[USER_QUERIES]")


    ### executeHandler
    # param:
    #   event -
    ###
    def executeHandler(self, event=None, fromUpload=False, query=None):
        if not fromUpload: query = self.USER_QUERY.get()
        self.setAppStatus("Executing query... \"%s\"" % query)
        queryTokens = query.split(" ")
        queryTokens = filterQuery(queryTokens)
        docs = getDocsForTokens(queryTokens)
        docs = list(set(docs))
        simResults = []
        for doc in docs:
            simResults.append({"doc": doc, "score": getSim(doc,queryTokens)})
        simResults = sorted(simResults, key=lambda k:k['score'], reverse=True)
        self.populateResults(simResults)

    ### openHandler
    # param:
    #   event -
    ###
    def openHandler(self, event=None):
        progressInfo = {"maximum": 4, "value": 0}
        VALID_LENGTH = 5
        openFileName = filedialog.askopenfilename(filetypes=(
            ('Text File', '*.txt'),
            ('All Files', '*.*')
        ))
        if openFileName == "": return
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        try:
            self.setAppStatus("Opening file... %s" % ((openFileName).split("/"))[-1])
            input = open(openFileName, "r")
            progressInfo["value"] += 1
            self.setTaskProgress(progressInfo)
        except FileNotFoundError:
            self.setAppStatus("Error: File Not Found")
            progressInfo["value"] = progressInfo["maximum"]
            self.setTaskProgress(progressInfo)
            return
        fileContents = (input.read()).split("\n")
        results = [result.split(",") for result in fileContents if result != ""]
        if not results or len(results[0]) != VALID_LENGTH:
            self.setAppStatus("Error: Invalid File Format")
            progressInfo["value"] = progressInfo["maximum"]
            self.setTaskProgress(progressInfo)
            return
        self.setAppStatus("Populating results...")
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        if self.SAVE_FILE != False and self.MODIFIED:
            shouldSave = messagebox.askquestion("Unsaved Changes",
                "Save Changes?", icon="warning")
            if shouldSave: saveHandler()
        self.SAVE_FILE = False
        self.populateResults(results, True)
        self.SAVE_FILE = openFileName
        self.MODIFIED = False
        self.setAppStatus("Results populated.")
        progressInfo["value"] += 1
        self.setTaskProgress(progressInfo)
        input.close()

    ### saveHandler
    # param:
    #   event -
    ###
    def saveHandler(self, event=None):
        if len(self.RESULT_TREE.get_children()) == 0: return
        else:
            if self.SAVE_FILE == False: self.saveAsHandler(event)
            else: self.saveResults(self.SAVE_FILE)

    ### saveAsHandler
    # param:
    #   event -
    ###
    def saveAsHandler(self, event=None):
        if len(self.RESULT_TREE.get_children()) == 0: return
        saveAsFileName = filedialog.asksaveasfilename(filetypes=[
            ('Text File', '*.txt'),
            ('All Files', '*.*')
        ])
        if saveAsFileName: self.saveResults(saveAsFileName)

    ### quitHandler
    # param:
    #   event -
    ###
    def quitHandler(self, event=None):
        global DOCUMENTS_CACHE_FILE, TABLE_LIST_CACHE_FILE, DOCUMENTS
        if self.MODIFIED:
            shouldSave = messagebox.askquestion("Unsaved Changes", "Save Changes?", icon="warning")
            if shouldSave == "yes": self.saveHandler()
        self.setAppStatus("Caching Documents...")
        with open(DOCUMENTS_CACHE_FILE, "w") as outfile:
            json.dump(DOCUMENTS, outfile)
        outfile.close()
        self.setAppStatus("Caching Index Table...")
        with open(TABLE_LIST_CACHE_FILE, "w") as outfile:
            json.dump(utils.TABLE_LIST, outfile)
        self.quit()

    ### aboutHandler
    # param:
    #   event -
    ###
    def aboutHandler(self, event=None):
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
    def instructionsHandler(self, event=None):
        print("TODO: INSTRUCTIONS")

    """ END ACTION HANDLERS """

    """ FUNCTIONAL METHODS """

    ### populateResults
    # param:
    #   treeview -
    #   results  -
    ###
    def populateResults(self, results, fromOpen=False):
        global DOCUMENTS
        for iid in self.RESULT_TREE.get_children(): self.RESULT_TREE.delete(iid)
        i = 1
        for result in results:
            if not fromOpen:
                doc = result['doc']
                value = ["MB01", str(DOCUMENTS[int(doc[1:])][doc]['id']), i, result['score'], "myRun"]
                if i == 1000: break
                i += 1
            else:
                value = result
            self.RESULT_TREE.insert('', 'end', text=value[0], values=value[1:])
            
        self.MODIFIED = True

    ### saveResults
    # param:
    #   filename -
    ###
    def saveResults(self, filename):
        self.setAppStatus("Saving results...")
        results = []
        i = 0
        for iid in self.RESULT_TREE.get_children():
            result = (self.RESULT_TREE.item(iid))['values']
            result.insert(0, i)
            results.append(result)
            i += 1
        with open(filename, "w") as output:
            writer = csv.writer(output)
            writer.writerows(results)
        self.setAppStatus("Results saved to: [%s]" % (filename.split("/"))[-1])
        self.MODIFIED = False

    ### setAppStatus
    # param:
    #   message -
    ###
    def setAppStatus(self, message):
        self.APP_STATUS.set(message)
        self.update_idletasks()

    ### setTaskProgress
    # param:
    #   progressInfo -
    ###
    def setTaskProgress(self, progressInfo):
        if self.PROGRESS_BAR['maximum'] != progressInfo['maximum']:
            self.PROGRESS_BAR['maximum'] = progressInfo['maximum']
        self.PROGRESS_BAR['value'] = progressInfo['value']
        self.update_idletasks()

    """ END FUNCTIONAL METHODS """

if __name__=="__main__":
    populateStopWords()
    app = APPLICATION()
    app.mainloop()
