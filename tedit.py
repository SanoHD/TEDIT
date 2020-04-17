import os, sys, shlex, re
from termcolor import *
from itertools import groupby

clear = lambda: os.system("clear")
clear()

path = os.getcwd() + "/"

version = "1.0"

text = []
header = "TEDIT Version {version} - By CMinusMinus".replace("{version}",version)
log = ""
replace_seperator = "||"
always_overwrite = False
var = ""
find = None
find_ignorecase = False

"""
1 Hello, world!
2 old text
3 BYE.
====================================== Change line 2
+>2 ! new text in line 2
====================================== Replace in line 2 
+>2 ? old || new
====================================== Replace in line 2, ignore case
+>2 ?* old || new
====================================== Change line 2
+>2 ! new text in line 2
"""

HELP = """
TextEDIT (tedit) by CMinusMinus
Version {version}
Created in Python 3.7.3
---HELP------------------------------

'LN' - Line number you want to change
'TEXT' - Text you want to enter

'+>' is the tedit command line prefix. Just ignore it.

------------------------------
>>> command in shell
+>  command in tedit
------------------------------

1: Open a file
    >>> tedit /my/path/myfile.txt
    * If myfile.txt exists, it opens it.
    * If myfile.txt not exists, it opens an empty file.
    * If you dont enter a filename, it opens an empty file, without
      a filename. You have to enter it, when you want to save the file.

2. Edit a file
    2.1 Adding a new line
        2.1.1 Adding line to end
            +> + {TEXT}
        2.1.2 Adding line to begin
            +> ++ {TEXT}
        2.1.3 Adding line in the middle
            +> +* {LN} {TEXT}
                Example:
                    [+* 4 Sentence in the middle of a text!] -> Inserts text 'Sentence in the...' to line 4

    2.2 Deleting a line
        2.2.1 Deleting last line
            +> -
        2.2.2 Deleting first line
            +> --
        2.2.3 Deleting line in the middle
            +> -* {LN}
                Example:
                    [-* 4] -> Deletes line 4
        2.2.4 Deleting all empty lines
            +> ---

    2.3 Rewrite a line
        +> ! {LN} {TEXT}
            Example:
                [! 3 My new line!] -> Line 3 is now 'My new line!'

    2.4 Replace in line
        2.4.1 Dont ignore case (a != A)
            +> ? {LN} {TEXT} || {NEW-TEXT}
                Example:
                    [? 3 OLD || NEW] -> (Line 3) My OLD text -> gets to -> my NEW text

        2.4.2 Ignore case (a = A)
            +> ?? {LN} {TEXT} || {NEW-TEXT}
                Example:
                    [?? 3 old || NEW] -> (Line 3) My OLD text -> gets to -> my NEW text

    2.5 Adding in a line
        2.5.1 Adding at the start
            +> +< {LN} {TEXT}
                Example:
                    [+< 2 'My new '] -> (line 2) line of text -> My new line of text
                    

        2.5.2 Adding at the end
            +> +< {LN} {TEXT}
                Example:
                    [+> 2 ' with letters'] -> (line 2) line of text -> line of text with letters
    
3. Save a file
    3.1 Normal
        +> sv
        You have to confirm, that you want to save the file. To do so, choose (y).
        Choose (n) if you dont want to save the file. Choose (always) if you dont
        want to confirm every time you want to save the file.

    3.2 As new file
        +> sv my/new/path/myfile.txt
        To save the file as a new file, type [sv] followed by the new filename.
        If the file already exists, you also have to confirm here.

    When you opened a completely new file, by just typing in [tedit] without a filename,
    you have to enter a filename, when saving normal.

4. Other commands
    4.1 Find text
        4.1.1 Dont ignore case
            +> find {TEXT}
            colors every line with {TEXT} in it yellow.

        4.1.1 Ignore case
            +> find* {TEXT}
            colors every line with {TEXT} in it yellow. Ignores cases.
         


""".replace("{version}",version)

if "--help" in sys.argv:
    print(HELP)
    sys.exit()

def fileexist(fn):
    try:
        with open(fn) as tmpfile: pass
        return True
    except:
        return False



def canbeint(i):
    try:
        int(i)
        return True
    except:
        return False

def editor():
    global text, log, always_overwrite, find, fullpath, path
    while True:
        clear()
        print(header)
        cprint("LOG: "+str(log),"yellow")
        print("="*70)
        #outtext = ['...' if k=='' and len(list(g)) >= 3 else "#"+k for k, g in groupby(text)]
        WS = " "*len(str(len(text)))
        for ln, line in enumerate(text):
            out = str(ln)+WS[:len(WS)-len(str(ln))]+" "+line
            color = "white"
            if find != None: log = "Found: "
            if find == None: color = "white"
            elif find_ignorecase and find.lower() in line.lower(): color = "yellow"
            elif not find_ignorecase and find in line: color = "yellow"
            else: color = "white"
            cprint(out,color)
            
        find = None            
        x = input("+"*len(str(len(text)))+">")
        try: x = shlex.split(x)
        except: pass
        if not len(x):
            continue
        elif canbeint(x[0]):
            ln = int(x[0])-1
            try:
                x[1]
            except IndexError:
                log = "Invalid command. Type {help} to get help"
                continue
            if x[1] == "!": # Set
                try:
                    text[ln] = " ".join(x[2:])
                    log = "Line changed"
                except IndexError:
                    log = "Invalid line"
            elif x[1] == "?": # Replace
                try:
                    ysdtzfgsudrgj = ""
                    to_replace = " ".join(x[2:x.index(replace_seperator)])
                    replace_with = " ".join(x[x.index(replace_seperator)+1:])
                    text[ln] = text[ln].replace(to_replace,replace_with)
                    log = "Line changed"
                except ValueError:
                    log = "Missing seperator ("+str(replace_seperator)+")"

            elif x[1] == "?*": # Replace, ignore case
                try:
                    to_replace = " ".join(x[2:x.index(replace_seperator)])
                    replace_with = " ".join(x[x.index(replace_seperator)+1:])
                    r = re.compile(re.escape(to_replace),re.IGNORECASE)
                    text[ln] = r.sub(replace_with,text[ln])
                    log = "Line changed"
                except ValueError:
                    log = "Missing seperator ("+str(replace_seperator)+")"
                    
        elif x[0] == "+":
            try:
                text.append(" ".join(x[1:]))
            except IndexError:
                log = "Need text. {+ text to add}"
                
        elif x[0] == "++":
            try:
                text.insert(0," ".join(x[1:]))
            except IndexError:
                log = "Need text. {++ text to add}"
                
        elif x[0] == "+*":
            try:
                LN = int(x[1])
                try:
                    to_insert = " ".join(x[2:])
                    
                except IndexError:
                    log = "Need text {+* {LN} text to insert}"
                text.insert(LN-1,to_insert)
            except ValueError:
                log = "Need Line-Number {+* {LN} text to insert}"
            except IndexError:
                log = "Invalid position"

        elif x[0] == "+<":
            try:
                LN = int(x[1])
                try:
                    to_add = " ".join(x[2:])
                    text[LN-1] = to_add + text[LN-1]
                except IndexError:
                    log = "Need text {+< {LN} text to insert in line}"
            except ValueError:
                log = "Need Line-Number {+< {LN} text to insert in line}"
        elif x[0] == "+>":
            try:
                LN = int(x[1])
                try:
                    to_add = " ".join(x[2:])
                    text[LN-1] = text[LN-1] + to_add
                except IndexError:
                    log = "Need text {+> {LN} text to insert in line}"
            except ValueError:
                log = "Need Line-Number {+> {LN} text to insert in line}"

        elif x[0] == "-" or x[0] == "--" or x[0] == "-*" or x[0] == "---":
            if len(text) == 0:
                log = "No lines to delete"
            else:
                if x[0] == "-":
                    text = text[:-1]
                    log = "Deleted last line"
                elif x[0] == "--":
                    text = text[1:]
                    log = "Deleted first line"
                elif x[0] == "-*":
                    text = text[:-1]
                    log = "Deleted line"
                elif x[0] == "---":
                    _text = text
                    text = []
                    for line in _text:
                        if line != "": text.append(line)
                    log = "Deleted empty lines"



        elif x[0] == "find":
            try:
                find = " ".join(x[1:])
                find_ignorecase = False
            except IndexError:
                find = None
                log = "Need text {find text to find}"
        elif x[0] == "find*":
            try:
                find = " ".join(x[1:])
                find_ignorecase = True
            except IndexError:
                find = None
                log = "Need text {find text to find}"
        
        elif x[0] == "sv":
            # If the user entered a already existing file as new file, he first has to confirm.
            # Thats why the 'fileexist(new)' part can raise an IndexError.
            try:
                new = x[1]
                if "/" in new:
                    if fileexist(new):
                        fullpath = new
                        raise IndexError
                    try:
                        with open(new,"w+") as tmp: pass
                        with open(new,"a") as file:
                            for line in text:
                                file.write(line+"\n")
                        log = "File saved: "+str(new)
                    except IsADirectoryError:
                        log = "Error; Location is a directory"
                else:
                    if fileexist(new):
                        fullpath = path+new
                        raise IndexError
                    
                    with open(path+new,"w+") as tmp: pass
                    with open(path+new,"a") as file:
                        for line in text:
                            file.write(line+"\n")
                    log = "File saved: "+str(path+new)
                    
            except IndexError:
                if not always_overwrite:
                    yn = input("Overwrite? (y/n/always) ")
                else:
                    yn = "y"
                if yn == "y" or yn == "always":
                    if yn == "always": always_overwrite = True
                    with open(fullpath,"w+") as tmp: pass
                    with open(fullpath,"a") as file:
                        for line in text:
                            file.write(line+"\n")
                    log = "File saved: "+str(fullpath)
                elif yn == "n":
                    log = "File not saved"


        elif x[0] == "help":
            clear()
            print(header)
            log = "Help"
            print("LOG:",log)
            print("="*70)
            WS = " "*len(str(len(HELP.split("\n"))))
            for ln, line in enumerate(HELP.split("\n")): print(str(ln+1)+WS[:len(WS)-len(str(ln))], line)
            print("--== next / quit ==--")
            x = input(">HELP>")
            log = ""
            

        

try:
    filename = sys.argv[1]
    fullpath = path+filename
    text = ""
    with open(fullpath) as file: text = file.read().split("\n")[:-1]
    # Edit existing File

except FileNotFoundError:
    # New File
    text = []

except IndexError:
    # New File, no Filename
    text = []
    filename = ""

try:
    editor()
except KeyboardInterrupt:
    while True:
        yn = input("Do you want to save? (y/n)")
        if yn == "n": break
        elif yn == "y":
            if not fullpath: new = input("Please enter filename:")
            else: new = fullpath
            try:
                if "/" in new:
                    if fileexist(new):
                        fullpath = new
                        raise IndexError
                    try:
                        with open(new,"w+") as tmp: pass
                        with open(new,"a") as file:
                            for line in text:
                                file.write(line+"\n")
                        break
                    except IsADirectoryError:
                        input("INVALID PATH: IS DIRECTORY [enter]")
                        continue
                else:
                    if fileexist(new):
                        fullpath = path+new
                        raise IndexError
                    
                    with open(path+new,"w+") as tmp: pass
                    with open(path+new,"a") as file:
                        for line in text:
                            file.write(line+"\n")
                    break
                    
            except IndexError:
                yn = input("Overwrite? (y/n) ")
                if yn == "y":
                    with open(fullpath,"w+") as tmp: pass
                    with open(fullpath,"a") as file:
                        for line in text:
                            file.write(line+"\n")
                    break
                elif yn == "n":
                    pass





















        else: continue

