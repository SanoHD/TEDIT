#!/usr/bin/env python3
import os, sys, shlex, re
from termcolor import *
from itertools import groupby
try:
    clear = lambda: os.system("clear")
except OSError:
    clear = lambda: os.system("cls")
clear()

path = os.getcwd().replace("\\","/") + "/"

version = "1.1"

text = []
header = "TEDIT Version {version} - By CMinusMinus".replace("{version}",version)
log = ""
replace_seperator = "||"
always_overwrite = False
var = ""
find = None
find_ignorecase = False


HELP = """
TextEDIT - CMinusMinus
Version {version}
---------- Quick-Help ----------
[LN]   = Line number you want to change
[TEXT] = Text you want to write / change / ...

Arguments:
    --help   Shows help, then exits

Commands:
    Adding:
        { + [TEXT] }               Add text in a new line
        { ++ [TEXT] }              Add text on top in a new line
        { +* [LN] [TEXT] }         Insert text in a line
        { +< [LN] [TEXT] }         Insert text at the start of a line
        { +> [LN] [TEXT] }         Insert text at the end of a line
    Deleting:
        { - }                      Delete last line
        { -- }                     Delete first line
        { -* [LN] }                Delete line
        { --- }                    Delete all empty lines
        { -< [LN] }                Delete first letter of a line
        { -> [LN] }                Delete last letter of a line
    Writing & Replacing:
        { ! [LN] [TEXT] }          Rewrite a line
        { ? [LN] [OLD] || [NEW] }  Replace text in line
        { ?* [LN] [OLD] || [NEW] } Replace text in line, ignores case
    Saving:
        { sv [FILENAME] }          [FILENAME] is optional. If not given,
                                   the programm will ask you to overwrite.
                                   If given but without a path, the programm
                                   will save the file in the current location.
                                   If the file already exists, the programm will
                                   again ask you to overwrite.
    Other:
        { find [TEXT] }            Colors every line with [TEXT] in it yellow
        { find* [TEXT] }           Like above, but ignores case
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
            out = str(ln+1)+WS[:len(WS)-len(str(ln))]+" "+line
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
        FOR = 1
        if x[0][-1] == ":" and canbeint(x[0][:-1]):
            FOR = int(x[0][:-1])
            x = x[1:]
        
        for a in range(FOR):
            if not len(x): continue

            if x[0] == "!": # Set
                try:
                    text[int(x[1])-1] = " ".join(x[2:])
                    log = "Line changed"
                except IndexError:
                    log = "Invalid line"
                except ValueError:
                    log = "Need Line-Number {! {LN} New text}"
            elif x[0] == "?": # Replace
                try:
                    ysdtzfgsudrgj = ""
                    to_replace = " ".join(x[2:x.index(replace_seperator)])
                    replace_with = " ".join(x[x.index(replace_seperator)+1:])
                    try:
                        text[int(x[1])-1] = text[int(x[1])-1].replace(to_replace,replace_with)
                        log = "Line changed"
                    except IndexError:
                        log = "Invalid line"
                    except ValueError:
                        log = "Need Line-Number {? {LN} Old text || New text}"
                except ValueError:
                    log = "Missing seperator ("+str(replace_seperator)+")"

            elif x[0] == "?*": # Replace, ignore case
                try:
                    to_replace = " ".join(x[2:x.index(replace_seperator)])
                    replace_with = " ".join(x[x.index(replace_seperator)+1:])
                    r = re.compile(re.escape(to_replace),re.IGNORECASE)
                    try:
                        text[int(x[1])-1] = r.sub(replace_with,text[int(x[1])-1])
                        log = "Line changed"
                    except IndexError:
                        log = "Invalid line"
                    except ValueError:
                        log = "Need Line-Number {?* {LN} Old text || New text}"
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


            if x[0] == "-":
                text = text[:-1]
                log = "Deleted last line"
                
            elif x[0] == "--":
                text = text[1:]
                log = "Deleted first line"
                
            elif x[0] == "-*":
                try:
                    LN = int(x[1])
                    try:
                        del text[LN]
                        log = "Deleted line"
                    except IndexError:
                        log = "Invalid line"
                except IndexError:
                    log = "Need Line-Number {-* {LN}}"

            elif x[0] == "---":
                _text = text
                text = []
                for line in _text:
                    if line != "": text.append(line)
                log = "Deleted empty lines"

            elif x[0] == "-<" or x[0] == "->":
                try:
                    LN = int(x[1])-1
                    try:
                        if x[0] == "-<": text[LN] = text[LN][1:]
                        elif x[0] == "-<": text[LN] = text[LN][:-1]
                        
                    except IndexError:
                        log = "Invalid line"
                
                except IndexError:
                    log = "Need Line-Number {-< {LN}}"
                except ValueError:
                    log = "Need Line-Number {-< {LN}}"




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
                        except FileNotFoundError:
                            log = "Error; Invalid path"
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
                    except FileNotFoundError:
                        input("INVALID PATH: DIRECTORY DOES NOT EXIST? [enter]")
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

