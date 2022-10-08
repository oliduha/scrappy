# Convert the ScrapPy Project to .exe

We used the [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) module to create an executable.

However, it seems that some antivirus programs detect this exe and report an alert blocking program.

To avoid any alert, you just need to do the conversion on your machine.

The procedure is simple, just follow the few instructions below.

### 1 - Preparation

To avoid polluting the global environment, it is *strongly recommended* to have previously
created a virtual environment for the project (pyCharm does it automatically when you load the project
and create or assign a configuration to it).

So, to create the virtual environment and connect to it, if not already done, in a terminal at  the project root :
```
virtualenv venv
venv\Scripts\activate.bat
```
The terminal prompt must show up (venv) at the beginning of the line.

- Import the easy-py-to-exe module into the project

For this a simple command to be passed in the terminal:
```
pip install auto-py-to-exe
```
Validate any requests and execute:
```
auto-py-to-exe
```
The tool window opens.

### 2 - Configuration

Start by loading the project specific options by clicking **"Settings"** at the bottom of the window. 
In the unfolded section, under "Settings", click the "Import [...] JSON" button and select 
the file `config_exe.json` in the project folder. 

All that remains is to adapt this configuration to your environment:

- At the top of the window, at "Script Location", select the ``main.py`` file of the project with the "Browse" button.
- Keep the option "One file".
- Keep the option "Window based (hide the console)".
- In the section **"Icon "**, specify the icon file ``scrappy.ico`` located in the ``img`` sub folder of the project
by clicking on the "Browse" button.

The configuration is finished!

### 3 - Conversion

All you have to do now is click on the button at the window bottom
named ``CONVERT .PY TO .EXE`` to begin conversion. If all goes well without errors, 
a ``ScrapPy.exe`` file should now sit in the ``output`` sub folder of the project, access it via the 
button ``OPEN OUTPUT FOLDER''.

### 4 - A bit more?

To get a version that displays the console at runtime, 2 simple steps:
- Choose "Console based" in the section **"Console Window"**.
- Change the "name" option under **"Advanced settings "** section.
For example ``ScrapPy_console``.
Click the "CLEAR CONSOLE" button and then "CONVERT .PY TO .EXE" to start a new conversion.

It is also possible to specify an output folder under "Output Directory" in **"Settings"** section.

Enjoy !