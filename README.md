# VATC
> **V**irtual **A**ssistant to **T**ype and **C**ode

VATC - tool developed from a programmers point of view. It helps programmers by writing and editing small pieces of code, searching for code snippets, libraries and helping in documentation.</br>
</br>
[![Version Status](https://img.shields.io/badge/stable-1.0.1-blue)](https://github.com/Gamemaster-007/VATC)
[![Build Status](https://img.shields.io/badge/build-passed-brightgreen)](https://github.com/Gamemaster-007/VATC)
[![Modules](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://docs.python.org/3/)

## Features

- ```Assistant Mode``` - this mode can be used to browse your queries and switch between different modes.
- ```Dictation Mode``` - this mode can be used to prepare documentation for a program or project using your voice.
- ```Coding Mode``` - this mode can be used to write code, edit pieces of code using voice, search for code snippets and find useful libraries for your program. 

## Installation

### MacOS
Clone repo
```
git clone https://github.com/Gamemaster-007/VATC
```
Activate Virtual environment
```
cd VATC/
source venv/bin/activate
```
Install dependencies
```
pip install requirements.txt
```

### Ubuntu
Clone repo
```
git clone https://github.com/Gamemaster-007/VATC
```
Activate Virtual environment
```
cd VATC/
source venv/bin/activate
```
Install dependencies
```
pip install requirements.txt
```

### Windows
Clone repo
```
git clone https://github.com/Gamemaster-007/VATC
```
Activate Virtual environment
```
cd VATC/
./venv/Scripts/activate
```
Install dependencies
```
pip install requirements.txt
```

### Usage

#### Run Tool
```
cd VATC/
python app.py
```

#### [Design](/Documentation/High_Level_Design.png)
![Design](/Documentation/Design.png)

### User Interface

#### Assistant Window
<img src="/images/Assistant_1.gif" height="500">

#### Dictation Mode
<img src="/images/Assistant_2.png" height="500">

#### Editor
![Editor](/images/Editor.gif)

### Functionalities

1. **Assistant**
  - This is the main window of the tool that appears when user executes the tool.
  - This window can be used to switch between different modes and browse your queries.
  - [Documentation](/Documentation/Assistant.md)
 
2. **Dictation Mode**
  - This mode can be used to type text using your voice.
  - It can be used to take notes, prepare documentations and other typing activities.
  - [Documentation](/Documentation/Dictation.md)
 
3. **Editor Mode**
  - This mode activates a Text Editor where user can write his program.
  - This mode also activates a voice based assistant in background that helps the programmer by editing and programming small pieces of code to make programmer task easier.
  - The Editor window contains a section where user can input his quries and get relevent libraries and code snippets.
  - In the Future builds the Editor will be developed to have functionalities like code suggestion, and a console where user can run suggested code snippets and other small codes.
  - [Documentation](/Documentation/Editor.md)


## Technologies

- [Tkinter](https://www.python.org) - Python based UI development framework.
- [Speech Recognition API](https://pypi.org/project/SpeechRecognition/) - API developed by Google to convert Speech into Text.
- [Ktrain](https://pypi.org/project/ktrain/) - Framework to develop Machine Learning models
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library used to scrape web pages and extract information.

## Contributors

- [Jawahar Nathani](https://github.com/Gamemaster-007)
- [Sagar Reddy P](https://github.com/sagar345)

## Acknowledgments

- Dr. Shridhar Chimalakonda
- Mr. Sriram


 
