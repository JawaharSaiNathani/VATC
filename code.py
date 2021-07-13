# Import Required Libraries and Functions
import tkinter as tk

text_box = '' # Dummy variable for textbox in Editor
trigger_function = '' # Dummy variable for change trigger function
pos = [0,0] # To maintain tk.INSERT position
num_words={'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9} # to convert numbers 
operators=['+','-','*','/','%','>','<','=','&','|','^','!','~',' ','(',')','{','}','[',']',"'",'"','!'] # All operators from python
# All conversions made while preprocessing text command
conversions = {'Pk inter':'tKinter','Pkinter':'tKinter','Pk inter':'tKinter','Pk inter':'tKinter','closed braket':')','Pk inter':'tKinter','dot':'.','full stop':'.','Pk inter':'tKinter','apostrophe mark':'"',
'double quotes':'"','cross':'X','not equal to':'!=','not equals to':'!=','star':'*','times':'*','kama':',','coma':',','under score':'_','space':' ','colam':':','kolam':':', 'greater than equal to':'>=','greater than or equal to':'>=',
'less than equal to':'<=','less than or equal to':'<=','less than':'<','plus':'+','minus':'-','addition':'+', 'divided by':'/',  'multiplication':'*', 'multiplied to':'*',  'percentage':'%',
'open square bracket':'[','open square brackets':'[', 'open square (':'[', 'closed square bracket':']','closed square brackets':']', 'closed square (':']','open flower bracket':'{',
'open flower brackets':'{', 'open flower (':'{','closed flower bracket':'}','closed flower brackets':'}',  'closed flower (':'}', 
'power':'^', 'into':'*','percentile':'%','greater than':'>', 'less than':'<','equals to':'=','equal to':'=','double equals to':'==',
'double equal to':'==','by':'/','colin':':','collin':':','false':'False','true':'True','length':'len',
'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}

# +++++++++++++ [ Function to Move tk.INSERT position ] +++++++++++++
def move_cursor(pos):
    global text_box
    global trigger_function

    text_box.mark_set("insert", "%d.%d" % (pos[0]+1,pos[1])) # change position
    trigger_function()

# +++++++++++++ [ Function to insert text in TextBox ] +++++++++++++
def insert_text(text,position):
    global text_box
    global trigger_function

    text_box.mark_set("insert", "%d.%d" % (position[0]+1,position[1]))
    trigger_function()
    flag = 0
    if text[0] == '\n': # change line and cursor position in case of new line
        text_box.insert("%d.%d" % (position[0]+1,position[1]),text[0])
        trigger_function()
        ix = 0
        for _ in range(1000000):
            ix += 1
        position[0] += 1
        position[1] = 0
        flag = 1
    move_cursor(position)

    # Inserting text => character by character
    for i in range(flag,len(text)):
        text_box.insert(tk.INSERT,text[i])
        trigger_function()
        position[1] += 1
        move_cursor(position)
        ix = 0
        for _ in range(1000000):
            ix += 1

# +++++++++++++ [ Function to check the type of command ] +++++++++++++
def check(words):
    if (len(words) > 2) and (((words[0] == 'create' or words[0] == 'define') and words[1] == 'a' and words[2] == 'function') or (words[0] == 'write' and words[1] == 'a' and words[2] == 'function')):
        return 0
    elif (len(words) > 1) and (((words[0] == 'create' or words[0] == 'define') and words[1] == 'function') or (words[0] == 'write' and words[1] == 'function')):
        return 1
    elif len(words) > 3 and words[0] == 'go' and words[1] == 'to' and words[2] == 'next' and words[3] == 'line':
        return 3
    elif len(words) > 1 and words[0] == 'next' and words[1] == 'line':
        return 4
    elif len(words) > 2 and words[0] == 'skip' and (words[2] == 'line' or words[2] == 'lines'):
        return 5
    elif len(words) > 2 and words[0] == 'skip' and (words[2] == 'word' or words[2] == 'words'):
        return 6
    elif len(words) > 2 and words[0] == 'skip' and (words[2] == 'letter' or words[2] == 'letters'):
        return 7
    elif len(words) > 2 and words[0] == 'add' and (words[2] == 'line' or words[2] == 'lines'):
        return 8
    elif len(words) > 2 and words[0] == 'comment' and words[1] == 'this' and words[2] == 'line':
        return 9
    elif len(words) > 5 and words[0] == 'comment' and words[1] == 'lines' and words[2] == 'from' and (words[4] == 'to' or words[4] == 'two'):
        return 10
    elif len(words) > 2 and words[0] == 'comment' and words[1] == 'line':
        return 11
    elif len(words) > 2 and words[0] == 'uncomment' and words[1] == 'this' and words[2] == 'line':
        return 12
    elif len(words) > 5 and words[0] == 'uncomment' and words[1] == 'lines' and words[2] == 'from' and (words[4] == 'to' or words[4] == 'two'):
        return 13
    elif len(words) > 2 and words[0] == 'uncomment' and words[1] == 'line':
        return 14
    elif len(words) > 2 and words[0] == 'clear' and words[1] == 'this' and words[2] == 'line':
        return 15
    elif len(words) > 5 and words[0] == 'clear' and words[1] == 'lines' and words[2] == 'from' and (words[4] == 'to' or words[4] == 'two'):
        return 16
    elif len(words) > 2 and words[0] == 'go' and words[1] == 'to' and words[2] == 'line':
        return 17
    else:
        return -1

# +++++++++++++ [ Function to write function syntax ] +++++++++++++
def write_function(fun_name,pos_ind):
    global text_box
    global pos

    lines = text_box.get('1.0','end').split('\n')            
    if len(lines[pos[0]]) > 3 and lines[pos[0]][:4] == '    ':
        new_pos = 0
        for i in range(pos[0]-1,-1,-1):
            if lines[i][:3] == 'def':
                new_pos = i
                break
        insert_text('\ndef '+fun_name+'():',[new_pos-1,len(lines[new_pos-1])])
        pos = [new_pos,(5+pos_ind)]
        move_cursor(pos)
    else:
        insert_text('\ndef '+fun_name+'():',[pos[0]-1,len(lines[pos[0]-1])])
        pos = [pos[0],(5+pos_ind)]
        move_cursor(pos)

# +++++++++++++ [ Executed when user wishes to define a function ] +++++++++++++
def got_function(words):
    if len(words) > 1:
        fun_name = ''
        flag = 0

        if words[0] == 'named':
            fun_name = ''.join(words[1:])# words[1]
            flag = 1
        else:
            fun_name = ''.join(words) # words[0]
            flag = 0

        write_function(fun_name,len(fun_name))
        return words[(1+flag):]

    if len(words) == 1:
        write_function(words[0],len(words[0]))
        return []
    
    write_function('',-1)
    return []

# +++++++++++++ [ comment multiple lines ] +++++++++++++
def multi_comment(num_1,num_2):
    global pos

    lines = text_box.get('1.0','end').split('\n')
    if num_1 > num_2:
        if num_2 > 0 and num_1 <= len(lines): # comment only if the line numbers are correct
            for i in range(num_2,num_1+1):
                insert_text('#',[i-1,0])
            if pos[0] > num_2 and pos[0] < num_1: # change position of cursor if that line is commented
                pos = [pos[0],pos[1]+1]
            move_cursor(pos)
    else:
        if num_1 > 0 and num_2 <= len(lines):
            for i in range(num_1,num_2+1):
                insert_text('#',[i-1,0])
            if pos[0] > num_1 and pos[0] < num_2:
                pos = [pos[0],pos[1]+1]
            move_cursor(pos)

# +++++++++++++ [ comment single line ] +++++++++++++
def comment_line(num):
    global pos
    global text_box
    
    lines = text_box.get('1.0','end').split('\n')
    if num > 0 and num <= len(lines):
        insert_text('#',[num-1,0])
        if pos[0] == num - 1:
            pos[1] += 1
        move_cursor(pos)

# +++++++++++++ [ uncomment multiple lines ] +++++++++++++
def multi_uncomment(num_1,num_2):
    global pos
    global text_box
    global trigger_function

    lines = text_box.get('1.0','end').split('\n')
    if num_1 > num_2:
        if num_2 > 0 and num_1 <= len(lines):
            for i in range(num_2,num_1+1):
                if lines[i-1][0] == '#':
                    start_pos = str(i)+'.0'
                    end_pos = str(i)+'.1'
                    text_box.delete(start_pos,end_pos) # to delete text from TextBox
                    trigger_function()
            if pos[0] > num_2 and pos[0] < num_1:
                pos = [pos[0],pos[1]-1]
            move_cursor(pos)
    else:
        if num_1 > 0 and num_2 <= len(lines):
            for i in range(num_1,num_2+1):
                if lines[i-1][0] == '#':
                    start_pos = str(i)+'.0'
                    end_pos = str(i)+'.1'
                    text_box.delete(start_pos,end_pos)
                    trigger_function()
            if pos[0] > num_1 and pos[0] < num_2:
                pos = [pos[0],pos[1]-1]
            move_cursor(pos)

# +++++++++++++ [ uncomment single line ] +++++++++++++
def uncomment_line(num):
    global text_box
    global trigger_function
    global pos

    lines = text_box.get('1.0','end').split('\n')
    if num > 0 and num <= len(lines):
        start_pos = str(num)+'.0'
        end_pos = str(num)+'.1'
        text_box.delete(start_pos,end_pos)
        trigger_function()
        if pos[0] == num - 1:
            pos[1] -= 1
        move_cursor(pos)

# +++++++++++++ [ deleting lines from code ] +++++++++++++
def clear_lines(num_1,num_2):
    global pos
    global text_box
    global trigger_function

    lines = text_box.get('1.0','end').split('\n')
    if num_1 > num_2:
        if num_2 > 0 and num_1 <= len(lines):
            if num_2 == 1:
                pos = [0,0]
                move_cursor(pos)
                start_pos = '0.0'
                end_pos = str(num_1)+'.'+str(len(lines[num_1]))
                text_box.delete(start_pos,end_pos)
                trigger_function()
            else:
                pos = [num_2-2,len(lines[num_2-2])]
                move_cursor(pos)
                start_pos = str(num_2-1)+'.'+str(len(lines[num_2-2]))
                end_pos = str(num_1)+'.'+str(len(lines[num_1]))
                text_box.delete(start_pos,end_pos)
                trigger_function()
    else:
        if num_1 > 0 and num_2 <= len(lines):
            if num_1 == 1:
                pos = [0,0]
                move_cursor(pos)
                start_pos = '0.0'
                end_pos = str(num_2)+'.'+str(len(lines[num_2]))
                text_box.delete(start_pos,end_pos)
                trigger_function()
            else:
                pos = [num_1-2,len(lines[num_1-2])]
                move_cursor(pos)
                start_pos = str(num_1-1)+'.'+str(len(lines[num_1-2]))
                end_pos = str(num_2)+'.'+str(len(lines[num_2]))
                text_box.delete(start_pos,end_pos)
                trigger_function()

# +++++++++++++ [ Function to find if Tab is required in a new line ] +++++++++++++
def isTabReq(line):
    if len(line) >= 5:
        if line[:5] == 'while':
            return 1
    if len(line) >= 4:
        if line[:4] == 'elif' or line[:4] == 'else' or line[:4] == '    ':
            return 1
    if len(line) >= 3:
        if line[:3] == 'def' or line[:3] == 'for':
            return 1
    if len(line) >= 2:
        if line[:2] == 'if':
            return 1
    return 0

# +++++++++++++ [ Function to write command to TextBox ] +++++++++++++
def general_command(words):
    global text_box
    global pos
    global operators
    global trigger_function

    x = words[0]
    if x == 'then': # skip if you get then
        return 1
    elif x == 'clear': # clear text till any operator
        if pos[1] > 0:
            lines = text_box.get('1.0','end').split('\n')
            ini_pos = pos[1]
            pos[1] -= 1
            while pos[1] > 0:
                if lines[pos[0]][pos[1]-1] not in operators:
                    pos[1] -= 1
                else:
                    break
            start_pos = str(pos[0]+1)+'.'+str(pos[1])
            end_pos = str(pos[0]+1)+'.'+str(ini_pos)
            move_cursor(pos)
            text_box.delete(start_pos,end_pos)
            trigger_function()
        return 1

    elif x == 'top': # move cursor position to start of code
        pos = [0,0]
        move_cursor(pos)
        return 1
    elif x == 'bottom': # move cursor to end of line
        lines = text_box.get('1.0','end').split('\n')
        pos = [len(lines)-1,len(lines[-1])]
        move_cursor(pos)
        return 1
    elif x == 'start': # move cursor to start of line
        pos = [pos[0],0]
        move_cursor(pos)
        return 1
    elif x == 'end': # move cursor to end of line
        lines = text_box.get('1.0','end').split('\n')
        pos = [pos[0],len(lines[pos[0]])]
        move_cursor(pos)
        return 1
    elif x == 'right': # move cursor one step forward
        lines = text_box.get('1.0','end').split('\n')
        if pos[1] != len(lines[pos[0]]):
            pos = [pos[0],pos[1]+1]
            move_cursor(pos)
        return 1
    elif x == 'left': # move cursor one step backwards
        lines = text_box.get('1.0','end').split('\n')
        if pos[1] != 0:
            pos = [pos[0],pos[1]-1]
            move_cursor(pos)
        return 1
    elif x == 'tab': # add Tab
        lines = text_box.get('1.0','end').split('\n')
        insert_text('    ',pos)
        return 1
    elif x == 'next': # add space (' ')
        lines = text_box.get('1.0','end').split('\n')
        insert_text(' ',pos)
        return 1
    elif x == 'string': # to define a string
        lines = text_box.get('1.0','end').split('\n')
        insert_text('""',pos)
        pos = [pos[0],pos[1]-1]
        move_cursor(pos)
        return 1
    elif x == 'print': # to print something
        lines = text_box.get('1.0','end').split('\n')
        insert_text('print()',pos)
        pos = [pos[0],pos[1]-1]
        move_cursor(pos)
        return 1
    elif x == 'of' or x == 'off': # to create brackets and write something in between '(|)'
        lines = text_box.get('1.0','end').split('\n')
        insert_text('()',pos)
        pos = [pos[0],pos[1]-1]
        move_cursor(pos)
        return 1
    else: # to write the recieved text
        lines = text_box.get('1.0','end').split('\n')
        # Insert space at the end of text if last character is not an operator
        if x[-1] in operators or len(x) == 1 :
            insert_text(x,pos)
        else:
            insert_text(x+' ',pos)
        return 1

# +++++++++++++ [ Function to find the command and execute respective operations ] +++++++++++++
def decide(inp):
    global text_box
    global trigger_function
    global pos

    words = inp.split(' ')
    if len(words) > 0 and words[0] != '':
        k = check(words)
        if k == 0:
            command_left = got_function(words[3:])
            decide(' '.join(command_left))
        elif k == 1:
            command_left = got_function(words[2:])
            decide(' '.join(command_left))
        elif k == 3:
            lines = text_box.get('1.0','end').split('\n')
            new_pos = 0
            if isTabReq(lines[pos[0]]):
                insert_text('\n    ',[pos[0],len(lines[pos[0]])])
                new_pos = 4
            else:
                insert_text('\n',[pos[0],len(lines[pos[0]])])
                new_pos = 0
            pos = [pos[0]+1,new_pos]
            decide(' '.join(words[4:]))
        elif k == 4:
            lines = text_box.get('1.0','end').split('\n')
            new_pos = 0
            if isTabReq(lines[pos[0]]):
                insert_text('\n    ',[pos[0],len(lines[pos[0]])])
                new_pos = 4
            else:
                insert_text('\n',[pos[0],len(lines[pos[0]])])
                new_pos = 0
            pos = [pos[0]+1,new_pos]
            decide(' '.join(words[2:]))
        elif k == 5:
            try:
                ki = int(words[1])
                lines = text_box.get('1.0','end').split('\n')
                if len(lines) > (pos[0] + ki):
                    pos = [(pos[0]+ki),len(lines[pos[0]+ki])]
                    move_cursor(pos)
                else:
                    pos = [(len(lines)-1),len(lines[len(lines)-1])]
                    move_cursor(pos)
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 6:
            try:
                ki = int(words[1])
                lines = text_box.get('1.0','end').split('\n')
                temp = 0
                i = pos[1]
                flag = 0
                while temp < ki:
                    if flag == 1 and lines[pos[0]][i] == ' ':
                        temp += 1
                        flag = 0
                    elif flag == 0 and lines[pos[0]][i] != ' ':
                        flag = 1
                    i += 1
                    if i == len(lines[pos[0]]):
                        break
                pos = [pos[0],i]
                move_cursor(pos)
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 7:
            try:
                ki = int(words[1])
                lines = text_box.get('1.0','end').split('\n')
                if len(lines[pos[0]]) > (pos[1]+ki):
                    pos = [pos[0],(pos[1]+ki)]
                    move_cursor(pos)
                else:
                    pos = [pos[0],len(lines[pos[0]])]
                    move_cursor(pos)
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 8:
            try:
                ki = int(words[1])
                lines = text_box.get('1.0','end').split('\n')
                if isTabReq(lines[pos[0]]):
                    for i in range(ki):
                        lines = text_box.get('1.0','end').split('\n')
                        insert_text('\n    ',[pos[0],len(lines[pos[0]])])
                        pos[0] += 1
                    pos = [pos[0],4]
                else:
                    for _ in range(ki):
                        lines = text_box.get('1.0','end').split('\n')
                        insert_text('\n',[pos[0],len(lines[pos[0]])])
                        pos[0] += 1
                    pos = [pos[0],0]
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 9:
            comment_line(pos[0]+1)
            decide(' '.join(words[3:]))
        elif k == 10:
            try:
                num_1 = 0
                num_2 = 0
                if words[3] in num_words:
                    num_1 = num_words[words[3]]
                else:
                    num_1 = int(words[3])
                if words[5] in num_words:
                    num_2 = num_words[words[5]]
                else:
                    num_2 = int(words[5])
                multi_comment(num_1,num_2)
                decide(' '.join(words[6:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 11:
            try:
                num = 0
                if words[2] in num_words:
                    num = num_words[words[2]]
                elif words[2] == 'to':
                    num = 2
                else:
                    num = int(words[2])
                comment_line(num)
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 12:
            uncomment_line(pos[0]+1)
            decide(' '.join(words[3:]))
        elif k == 13:
            try:
                num_1 = 0
                num_2 = 0
                if words[3] in num_words:
                    num_1 = num_words[words[3]]
                else:
                    num_1 = int(words[3])
                if words[5] in num_words:
                    num_2 = num_words[words[5]]
                else:
                    num_2 = int(words[5])
                multi_uncomment(num_1,num_2)
                decide(' '.join(words[6:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 14:
            try:
                num = 0
                if words[2] in num_words:
                    num = num_words[words[2]]
                elif words[2] == 'to':
                    num = 2
                else:
                    num = int(words[2])
                uncomment_line(num)
                decide(' '.join(words[3:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 15:
            if pos[0] == 0:
                lines = text_box.get('1.0','end').split('\n')
                pos = [0,0]
                move_cursor(pos)
                end_pos = '1.'+str(len(lines[0]))
                text_box.delete('1.0',end_pos)
                trigger_function()
            else:
                lines = text_box.get('1.0','end').split('\n')
                pos = [pos[0]-1,len(lines[pos[0]-1])]
                move_cursor(pos)
                start_pos = str(pos[0]+1)+'.'+str(len(lines[pos[0]]))
                end_pos = str(pos[0]+2)+'.'+str(len(lines[pos[0]+1]))
                text_box.delete(start_pos,end_pos)
                trigger_function()
        elif k == 16:
            try:
                num_1 = 0
                num_2 = 0
                if words[3] in num_words:
                    num_1 = num_words[words[3]]
                else:
                    num_1 = int(words[3])
                if words[5] in num_words:
                    num_2 = num_words[words[5]]
                else:
                    num_2 = int(words[5])
                clear_lines(num_1,num_2)
                decide(' '.join(words[6:]))
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        elif k == 17:
            try:
                num = 0
                if words[3] in num_words:
                    num = num_words[words[3]]
                elif words[3] == 'to':
                    num = 2
                else:
                    num = int(words[3])
                lines = text_box.get('1.0','end').split('\n')
                pos = [num-1,len(lines[num-1])]
                move_cursor(pos)
            except:
                temp = general_command(words)
                decide(' '.join(words[temp:]))
        else:
            temp = general_command(words)
            decide(' '.join(words[temp:]))

# +++++++++++++ [ Function to code using text recieved ] +++++++++++++
def type_code(textbox, triggerFunction,command):
    global text_box
    global trigger_function
    global pos
    global conversions

    # assign dummy variable
    text_box = textbox
    trigger_function = triggerFunction
    x,y = text_box.index(tk.INSERT).split('.') # get current possition of cursor
    pos = [int(x)-1,int(y)]

    command = command.lower()
    # Preprocessing recieved text
    for x,y in conversions.items():
        if x in command and type(x) == str:
            command=command.replace(x,conversions[x])

    decide(command)
    trigger_function()