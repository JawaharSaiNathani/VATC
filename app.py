# Import Required Libraries and Functions
print("Importing All Required Modules...")
import sys
import tkinter
import playsound
import time
from tkinter import *
from tkinter.ttk import *
from tkinter import font as tkfont
from Speech2Text import speech2Text
from typing_text import typeText
from codeThread import CodeThread
from dictateText import dictate
from tkinter import ttk
from Editor_Tools import scrollingtext,ColorLight
import tkinter.filedialog as tkFileDialog
import pyperclip
from tkhtmlview import HTMLLabel
from get_codes import search_web
import threading
import webbrowser

# Main App Class
class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):

        # Creating Main Window
        tkinter.Tk.__init__(self, *args, **kwargs)
        # self.attributes("-topmost",True)

        # Modify Title of Window
        self.title("V.A.T.C")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic") # Styling Window Title

        # Creating Container to Stack Frames [ Assistant , Text Editor ]
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Define dummy variables and assign them when created
        self.toolinfo = ''
        self.textbox = ''
        self.trigger_function = ''

        # Creating Frames
        self.frames = {}
        for F in (Assistant, TextEditor):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.codethread = CodeThread(self.toolinfo,0,self.textbox,self.trigger_function) # Create coding Thread
        self.codethread.start() # Start the Thread
        
        self.show_frame("Assistant") # Initially Show Assistant Frame
        self.update() # Update Window GUI
        dictate('This is VATC, your personal Virtual Assistant to Type and Code.') # Dictate Start Message

    # Function to Switch between Frames
    def show_frame(self, page_name):

        if page_name == 'Assistant':
            self.codethread.pause() # Pause ths thread when exited coding mode
            # Resize the Window
            self.minsize(520,600)
            self.geometry('520x600')
            self.resizable(width=False, height=False)
        else:
            # Resize Window
            self.minsize(1360,600)
            self.codethread.resume() # resume the thread again when started coding
            self.lift()
            self.update()
        frame = self.frames[page_name] # Select Desired Frame
        frame.tkraise() # Display Selected Frame

# Assistant Class
class Assistant(tkinter.Frame):
    global aiml_kernel

    def __init__(self,parent,controller):

        # Creating Frame
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        canvas_1 = Canvas(self,background='black',height=510) # For Message Display System
        canvas_2 = Canvas(self,background='white',height=70) # For Buttons and Input Field

        # +++++++++++++++++++++++++ Message Display System ++++++++++++++++++++++++++++++++++++++++++++++
        # List of messages
        self.messages = tkinter.Listbox(canvas_1,height=31,bg='black',fg='white')
        self.messages.pack(fill=BOTH)

        self.msg_count = 1 # To keep track of number of messages
        self.isListening = False # Flag variable to check state of Tool

        # Input Field
        self.msg_fieldText = tkinter.StringVar()
        self.msg_fieldText.set('')
        self.msg_inputField = tkinter.Entry(canvas_2,font=('Helvetica','14'),width=40,textvariable=self.msg_fieldText)

        # +++++++++++++++++++++++++ [ Mic Button | Input Field | Send Button ] ++++++++++++++++++++++++++++++++++++++++++++++
        # Mic button UI
        photo = PhotoImage(file = "images/microphone.png")
        mic_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=photo,command=lambda: self.speak())
        mic_button.image = photo
        mic_button.pack(side=LEFT)
        self.msg_inputField.pack(side=LEFT,fill=BOTH)

        # Send Button UI
        send_photo = PhotoImage(file = "images/send.png")
        send_button = tkinter.Button(canvas_2,text='Send',height=70,padx=10,image=send_photo,command=lambda: self.send())
        send_button.image = send_photo
        send_button.pack(side=RIGHT)

        # Window UI
        canvas_1.pack(side=TOP,fill=BOTH)
        canvas_2.pack(side=BOTTOM,fill=BOTH)

    # Funtion to Add Message to Tkinter window
    def addMsg(self,msgr,type,msg):
        messanger = {0:'F.R.I.D.A.Y  =>',1:'USER  =>'}
        messanger_color = {0:'orange',1:'yellow'}
        typE = {0:'white',1:'red'}

        # [ Add the origin of message ]
        self.messages.insert(self.msg_count,messanger[msgr])
        self.messages.itemconfig(self.msg_count-1,fg=messanger_color[msgr])
        self.msg_count += 1
        self.messages.insert(self.msg_count,"")
        self.msg_count += 1

        # Divide message to fit in window
        while len(msg) > 60:
            self.messages.insert(self.msg_count,msg[:60])
            self.messages.itemconfig(self.msg_count-1,fg=typE[type])
            self.msg_count += 1
            msg = msg[60:]

        # Add message to window        
        self.messages.insert(self.msg_count,msg)
        self.messages.itemconfig(self.msg_count-1,fg=typE[type])
        self.msg_count += 1
        self.messages.insert(self.msg_count,"")
        self.msg_count += 1
    
    # Function For Typing Text
    def typing(self):
        isTyping = True

        while isTyping == True:
            self.msg_fieldText.set('Mode: typing  | State: listening ') # Set mode and state
            self.update()

            text = speech2Text() # Get text from Speech Detection module
            self.msg_fieldText.set('Mode: typing  | State: processing ') # Set mode and state
            self.update()

            if text == -1: # if text not detected
                self.msg_fieldText.set("Error: Didn't understand, Please try again ")
                self.update()
                time.sleep(2)
            else: # if text detected
                if text.lower() == 'stop typing': # Exit Typing mode
                    self.msg_fieldText.set('')
                    self.addMsg(0,0,'Done Typing')
                    dictate('Done Typing')
                    isTyping = False
                else:
                    typeText(text) # Type text using typeText module


    # Opening Text Editor
    def openEditor(self):
        self.controller.show_frame('TextEditor') # Changing Frame

    # Function to Detect Message
    def message_recieved(self,msg):
        if msg.lower() == 'start typing':
            self.addMsg(1,0,msg)
            self.addMsg(0,0,'Started Typing')
            self.update()
            dictate('Started Typing')
            self.typing()
        elif msg.lower() == 'start coding':
            self.addMsg(1,0,msg)
            self.addMsg(0,0,'Started Coding')
            self.update()
            dictate('Started Coding')
            self.addMsg(0,0,'Done Coding')
            self.openEditor()
        elif msg.lower() == 'exit' or msg.lower() == 'close':
            dictate('have a nice day, bye')
            sys.exit()
        else:
            self.addMsg(1,0,msg)
            self.addMsg(0,0,"Opening WEB BROWSER")
            msg = msg.replace(' ','+')
            url = "https://www.google.com/search?q="+msg
            webbrowser.open(url)

    # Function to Detect Speech
    def speak(self):
        if self.isListening == False: # check state
            self.isListening = True # change state
            self.msg_fieldText.set("go ahead I'm listening")
            self.msg_inputField.config(state=DISABLED)
            self.update()
            playsound.playsound('audio_files/tone.mp3',True)

            msg = speech2Text() # Get message from speech detection module
            if msg == -1:
                error = "Didn't understand, Please Try Again"
                self.addMsg(0,1,error)
            else:
                self.message_recieved(msg)

            self.msg_fieldText.set("")
            self.msg_inputField.config(state=NORMAL)
            self.isListening = False

    # Function to Process Messages Recieved from Input Field
    def send(self):
        msg = self.msg_fieldText.get() # Get message from Input Field

        # Modify the recieved message
        words = msg.split(' ')
        i = 0
        while i < len(words):
            if words[i] == '':
                words.remove(words[i])
                i -= 1
            i += 1
        msg = ' '.join(words)

        # Check state of Tool and [ if message is legit ]
        if self.isListening == False and len(msg) != 0:
            self.msg_inputField.config(state=DISABLED)
            self.message_recieved(msg)
            self.msg_fieldText.set("")
            self.msg_inputField.config(state=NORMAL)

# Frame to display Code Snippets.
class Section(Frame):
    def __init__(self,parent,snippet,source,link):
        Frame.__init__(self,parent)
        self.html_code = f"""
                <h5> Source : <b style="color:red"> {source} </b> </h5>
                <a href="{link}">original code link</a>
        """
        self.source = HTMLLabel(self,html=self.html_code,height=5,background='white')
        self.source.pack(side='top')
        self.snippet = snippet

        self.code = Text(self, wrap='none', undo=1,background='black',fg='white',height=10)
        self.code.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.code.pack(side='top')
        self.code.insert(END,snippet)
        self.code.config(state=DISABLED)

        self.code_syntax_color=ColorLight.ColorLight(txtbox=self.code)
        self.code_syntax_color.trigger()

        self.copy = Button(self,text='COPY',command=self.copy_code)
        self.copy.pack(side='top')
    
    def copy_code(self):
        pyperclip.copy(self.snippet)

# Text Editor Class
class TextEditor(tkinter.Frame):
    def __init__(self,parent,controller):

        # Creating Frame
        tkinter.Frame.__init__(self,parent)
        self.controller = controller

        # [Shortcut Bar Main Frame]
        self.shortcut_bar=ttk.Frame(self)
        self.shortcut_bar.pack(expand='no', fill='x')

        self.left = tkinter.Frame(self)
        self.left.pack(side='left',fill='both',expand='no')

        # +++++++++++++++++++++++++ Text Box System ++++++++++++++++++++++++++++++++++++++++++++++
        # Frame For [Text Box]
        frame=ttk.Frame(self.left, borderwidth=5)
        frame.pack(expand='yes', fill='both')
        frame1=ttk.Frame(frame)
        frame1.pack(side='top', expand='yes', fill='both')
        self.text_box=tkinter.Text(frame1, wrap='none', undo=1)
        self.text_box.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.text_box.pack()

        # Assign the dummy variables
        self.controller.textbox = self.text_box
        self.controller.trigger_function = self.trigger

        # Adding Features On Text Box
        self.box=scrollingtext.featured_text(root=frame1, textbox=self.text_box, main=frame)

        #++++++++++++++++++++++++ [System Close] ++++++++++++++++++++++++++++++++++++++++++++++
        # Function For Scrolling Text widget number line Together
        self.cursurinfo=ttk.Label(self.text_box, text='Line 1 | Column 1',padding=3)
        self.cursurinfo.pack(expand='no', fill=None, side='right',anchor='se')

        self.controller.toolinfo=ttk.Label(self.text_box, text='State: - - - ',padding=3)
        self.controller.toolinfo.pack(expand='no', fill=None, side='left',anchor='se')

        self.micState = True # Check mic State

        space=tkinter.Label(self.left, text=' ',width=70)
        space.pack(expand='no', fill=None, side='left')

        # Pause/Resume Button
        space1=tkinter.Label(self.left, text=' ',width=7)
        space1.pack(expand='no', fill=None, side='right')
        self.pauseResumeButton=tkinter.Button(self.left, text='Pause',padx=10,pady=6,command=self.switch_state)
        self.pauseResumeButton.pack(expand='no', fill=None, side='right')

        # Stop Coding Button
        space2=tkinter.Label(self.left, text=' ',width=7)
        space2.pack(expand='no', fill=None, side='right')
        stopCodingButton=tkinter.Button(self.left, text='STOP CODING',padx=10,pady=6,command=self.stopCoding)
        stopCodingButton.pack(expand='no', fill=None, side='right')

        # Adding Syntax Highlighting Feature
        self.syntax_color=ColorLight.ColorLight(txtbox=self.text_box)

        # Binding Triggers
        self.bind_all('<Any-KeyPress>',self.trigger)

        # Right Frame to maintain Code Snippets suggestion section.
        self.right=tkinter.Frame(self,width=350,background='white')
        self.right.pack(side='right',fill='both',expand=1)

        # Frame to display MIC, Input Field, Search Button.
        self.search_frame = tkinter.Frame(self.right)
        self.search_frame.pack(side='top', fill='x',expand='no')

        self.msg_fieldText = tkinter.StringVar()    # Message Variable.
        self.msg_fieldText.set('')
        self.msg_inputField = tkinter.Entry(self.search_frame,font=('Helvetica','14'),width=40,textvariable=self.msg_fieldText)

        self.mic_listening = False  # State of Search Frame MIC
        self.display_frame = ""

        #++++++++++++++++++++++++ [Search Section] ++++++++++++++++++++++++++++++++++++++++++++++
        photo = tkinter.PhotoImage(file = "images/microphone.png")
        mic_button = tkinter.Button(self.search_frame,text='Speak',width=30,height=25,image=photo,command=self.mic_click)
        mic_button.image = photo
        mic_button.pack(side='left',fill=None,expand='no')
        self.msg_inputField.pack(side='left',fill=None)

        search_photo = tkinter.PhotoImage(file = "images/search.png")
        search_button = tkinter.Button(self.search_frame,text='Send',height=25,width=30,image=search_photo,command=self.search_click)
        search_button.image = search_photo
        search_button.pack(side='left')

        self.sections = []

    # Function for MIC actions
    def mic_click(self):
        if self.mic_listening == False:
            self.mic_listening = True
            self.controller.codethread.pause()  # Pause Current Assistant Thread.
            self.add_msg_frame(1)
            self.display_frame.update()
            playsound.playsound('audio_files/tone.mp3',True)

            msg = speech2Text() # Get message from speech detection module
            if msg == -1:
                self.add_msg_frame(-1)
            else:
                self.create_suggestions_frame(command=msg)  # Send recieved message to code searching module.

            self.mic_listening = False
            self.controller.codethread.resume() # Resume Assistant Thread.

    # Function for Search Button actions.
    def search_click(self):
        if self.mic_listening == False:
            msg = self.msg_fieldText.get() # Get message from Input Field

            # Modify the recieved message
            words = msg.split(' ')
            i = 0
            while i < len(words):
                if words[i] == '':
                    words.remove(words[i])
                    i -= 1
                i += 1
            msg = ' '.join(words)
            if len(msg) > 0:
                self.create_suggestions_frame(command=msg)

    # Function to add State of MIC
    def add_msg_frame(self,typeofmsg):

        # Destroy the existing Code Display Frame.
        if type(self.display_frame) is tkinter.Frame:
            self.display_frame.destroy()

        #++++++++++++++++++++++++ [New Code Display Section] ++++++++++++++++++++++++++++++++++++++++++++++
        self.display_frame = tkinter.Frame(self.right)
        self.display_frame.pack(side='top',fill=BOTH,expand=1)

        self.canvas = tkinter.Canvas(self.display_frame)
        self.canvas.pack(side='left',fill=tkinter.BOTH,expand=1)

        self.scrollbar = ttk.Scrollbar(self.display_frame,orient=tkinter.VERTICAL,command=self.canvas.yview)
        self.scrollbar.pack(side='right',fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>',lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.sec_frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0,0),window=self.sec_frame,anchor='nw',width=385)

        # Set MIC Status.
        if typeofmsg == 1:
            self.htmlsnippet = '''
                <div style="background-color:white;">
                <h5 style="color: blue">I'm Listening...</h5>
                <p>speak after the sound</p>
                </div>
            '''         # HTML div to display MIC status.
        else:
            self.htmlsnippet = '''
                <div style="background-color:white;">
                <h5 style="color: red">Error</h5>
                <p>Didn't understand, Please try again</p>
                </div>
            '''      # HTML div to display Error Message.

        self.msg_display = HTMLLabel(self.sec_frame,html=self.htmlsnippet,height=6,background='white')  # Display Status of Tool and MIC
        self.msg_display.pack()

    # Function to Display Searching Message.
    def display_searching(self):

        if type(self.display_frame) is tkinter.Frame:
            self.display_frame.destroy()

        self.display_frame = tkinter.Frame(self.right)
        self.display_frame.pack(side='top',fill=BOTH,expand=1)

        self.canvas = tkinter.Canvas(self.display_frame)
        self.canvas.pack(side='left',fill=tkinter.BOTH,expand=1)

        self.scrollbar = ttk.Scrollbar(self.display_frame,orient=tkinter.VERTICAL,command=self.canvas.yview)
        self.scrollbar.pack(side='right',fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>',lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.sec_frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0,0),window=self.sec_frame,anchor='nw',width=385)

        self.htmlsnippet = '''
            <div style="background-color:white;">
            <h5 style="color: orange">Searching for top results ...</h5>
            </div>
            '''     # HTML template for Searching Message.

        self.msg_display = HTMLLabel(self.sec_frame,html=self.htmlsnippet,height=6,background='white')
        self.msg_display.pack() 

    #++++++++++++++++++++++++ [Code Suggestion Thread] ++++++++++++++++++++++++++++++++++++++++++++++
    # Function to search for Code Snippets and Displaying them.
    def search_thread(self,command):

        self.display_searching()    # Display Searching Message.
        self.snippets = search_web(command) # Get Code Snippets
        self.display_frame.destroy()    # destroy existing display frame.

        # create Display Frame for displaying Search Query and Code Snippets.
        self.display_frame = tkinter.Frame(self.right)
        self.display_frame.pack(side='top',fill=BOTH,expand=1)

        self.canvas = tkinter.Canvas(self.display_frame)
        self.canvas.pack(side='left',fill=tkinter.BOTH,expand=1)

        self.scrollbar = ttk.Scrollbar(self.display_frame,orient=tkinter.VERTICAL,command=self.canvas.yview)
        self.scrollbar.pack(side='right',fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>',lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.sec_frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0,0),window=self.sec_frame,anchor='nw',width=385)

        self.htmlsnippet = f'''
            <div style="background-color:white;">
            <h5 style="color: green">Recieved Command</h5>
            <p>{command}</p>
            </div>
        '''     # HTML template for recieved message.

        self.msg_display = HTMLLabel(self.sec_frame,html=self.htmlsnippet,height=6,background='white')
        self.msg_display.pack()

        self.separator = Label(self.sec_frame,text='--------------------------------------------------------------')
        self.separator.pack(side='top',fill='x',expand='no')

        # Display Code snippets.
        for i in range(len(self.snippets)):
            if len(self.snippets[i][2]) > 0:
                frami = Section(self.sec_frame,self.snippets[i][2],self.snippets[i][0],self.snippets[i][1])
                frami.pack(side='top',fill='x',expand=1)
                self.sections.append(frami)

        # Update Controller.
        self.controller.geometry("1361x600")
        self.controller.update()
        self.controller.geometry("1360x600")
        self.controller.update()
    
    # Function to find code snippets.
    def create_suggestions_frame(self,command):

        self.searching_thread = threading.Thread(target = self.search_thread, args =(command, ))    # create thread for searching code snippets.
        self.searching_thread.setDaemon(True)
        self.searching_thread.start()

    # [ Function to Chnage State of Pause/Resume Button and call Pause/Resume Functions ]
    def switch_state(self):
        if self.mic_listening == False:
            if self.micState:
                self.pauseResumeButton.configure(text='Resume')
                self.update()
                self.controller.codethread.pause()
                self.micState = False
            else:
                self.pauseResumeButton.configure(text='Pause')
                self.update()
                self.controller.codethread.resume()
                self.micState = True

    # [ Function to save textbox text as a python file ]
    def Save_as(self):
        ExtType=[('.py', '*.py')]
        path=tkFileDialog.asksaveasfile(title='Save As', defaultextension='*.py',filetypes=ExtType)
        storeobj=self.text_box.get('1.0', END)
        if path:
            filetmp=open(path.name,'a')
            filetmp.write(storeobj)
            filetmp.close()

    # [ Function to exit Coding State ]
    def stopCoding(self):
        self.Save_as() # Save the text as python file
        time.sleep(3)
        self.controller.show_frame('Assistant') # Change Frame to Assiatant Frame
        self.update() # Update Window GUI
        #dictate('Done Coding')
        

    # [Function to Update Cursor Position]
    def update_cursor_info_bar(self, event=None):
        row, col = self.text_box.index(tkinter.INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col)+1) # colstarts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        self.cursurinfo.configure(text=infotext)

    # All-Key Trigger
    def trigger(self, event=None):
        self.box.changed()
        self.update_cursor_info_bar()
        self.syntax_color.trigger()
    
if __name__=='__main__':
    app = App() # Main App Class Object
    app.mainloop() # start Main Window GUI