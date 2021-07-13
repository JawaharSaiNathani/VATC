# Import Required Libraries and Functions
import keyboard

# convert numbers from words to integers
str_num = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}

# [ Function to type recieved text ]
def typeText(text):

    command = -1
    count = 0
    comment = ''

    words = text.split(' ')
    words_len = len(words)
    if words_len >= 4 and (words[-4].lower()+' '+words[-3].lower()+' '+words[-2].lower()+' '+words[-1].lower() == 'go to next line'):
        command = 0
        for i in range(words_len-4):
            comment += words[i]+' '
    elif words_len >= 3:
        if words[-3].lower() == 'clear' and (words[-1].lower() == 'words' or words[-1].lower() == 'lines' or words[-1].lower() == 'line' or words[-1].lower() == 'letters' or words[-1].lower() == 'letter'):
            try:
                count = int(words[-2].lower())
                if words[-1].lower() == 'letters' or words[-1].lower() == 'letter':
                    command = 1
                elif words[-1].lower() == 'words':
                    command = 2
                else:
                    command = 3
                for i in range(words_len-3):
                    comment += words[i]+' '
            except:
                if words[-2].lower() in str_num:
                    count = str_num[words[-2].lower()]
                    if words[-1].lower() == 'letters' or words[-1].lower() == 'letter':
                        command = 1
                    elif words[-1].lower() == 'words':
                        command = 2
                    else:
                        command = 3
                    for i in range(words_len-3):
                        comment += words[i]+' '
    elif words_len >= 2:
        if (words[-2].lower() == 'next' and words[-1].lower() == 'line') or (words[-2].lower() == 'hit' and words[-1].lower() == 'enter'):
            command = 0
            for i in range(words_len-2):
                comment += words[i]+' '
        elif words[-2].lower() == 'clear' and words[-1].lower() == 'all':
            command = 4
            for i in range(words_len-2):
                comment += words[i]+' '
    
    # Perform relevent actions based on recieved command
    if command == -1:
        keyboard.write(text+' ')
    elif command == 0:
        keyboard.write(comment)
        keyboard.press_and_release('enter')
    elif command == 1:
        keyboard.write(comment)
        for _ in range(count):
            keyboard.press_and_release('delete')
    elif command == 2:
        keyboard.write(comment)
        for _ in range(count):
            keyboard.press_and_release('alt+delete')
    elif command == 3:
        keyboard.write(comment)
        keyboard.press_and_release('command+delete')
        for _ in range(count-1):
            keyboard.press_and_release('command+delete')
            keyboard.press_and_release('command+delete')
    elif command == 4:
        keyboard.write(comment)
        keyboard.press_and_release('command+a,delete')