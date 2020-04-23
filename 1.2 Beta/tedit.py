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

version = "Beta 1.2"

text = []
header = "TEDIT Version {version} - By CMinusMinus".replace("{version}",version)
log = ""
replace_seperator = "||"
always_overwrite = False
var = ""
find = None
find_ignorecase = False

syntax = {
    "py": {
        "words": {
                "yellow":["class","def","return","in","continue","pass","while","True","False","try","except","if","elif","else","with","as","is","for","break","import","from"],
                "magenta":["print","input","int","str","float","list","raise","join","append","insert","replace"],
                "comment": {"symbol":"#","color":"red"},#,"block":'"""',"blockcolor":"green"},
                "qmarks": {"color":"green"}
        }
    }
}

HELP = """
TextEDIT - CMinusMinus
Version {version}
---------- Quick-Help ----------
[LN]   = Line number you want to change
[TEXT] = Text you want to write / change / ...

Usage examples:
    tedit                   Open new file
    tedit myfile.txt        Open file
    tedit /path/myfile.txt  Open file
    tedit myfile [N]        Open file, line 1 - [N]

Arguments:
    --help   Shows help, then exits

Commands:
    Adding:
        { + [TEXT] }               Add text in a new line
        { ++ [TEXT] }              Add text on top in a new line
        { +* [LN] [TEXT] }         Insert text in a line
        { +< [LN] [TEXT] }         Insert text at the start of a line
        { +> [LN] [TEXT] }         Insert text at the end of a line

        { *< [TEXT] [LN]}          Add text at the start of multiple lines
        { *< [TEXT] [LN]}          Add text at the end of multiple lines
                                   In this case, [LN] can have many variations:
                                   Variation       Example         Explanation
                                   LN              5               Line 5
                                   LN:LN           3:5             Line 3 and 5
                                   LN-LN           3-5             Line 3, 4 and 5
                                   LN:LN-LN        2:5-7           Line 2, 5, 6 and 7
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
        cprint("="*70)
        #outtext = ['...' if k=='' and len(list(g)) >= 3 else "#"+k for k, g in groupby(text)]
        WS = " "*len(str(len(text)))
        comment_block = False
        UNDO_TEXT = text
        for ln, line in enumerate(text):
            print(str(ln+1)+WS[:len(WS)-len(str(ln))],end=" ") # PRINT LINE NUMBER
            out = line
            if filename.split(".")[-1] in syntax: # Test if file-type is available as syntax-highlighting
                extension = filename.split(".")[-1]
                ##############################################################################
                comment_symbol = syntax[extension]["words"]["comment"]["symbol"]
                comment_color = syntax[extension]["words"]["comment"]["color"]

                #comment_block_symbol = syntax[extension]["words"]["comment"]["block"]
                #comment_block_color = syntax[extension]["words"]["comment"]["blockcolor"]
                qcolor = syntax[extension]["words"]["qmarks"]["color"]

                # If there are 1 ("), 3 ("), 5 ("),... then commentblock
                if line.count("\"") % 2 == 1:
                    if comment_block:
                        comment_block = False
                        line = colored(line,qcolor)
                    else:
                        comment_block = True
                        
                if comment_block:
                    line = colored(line,qcolor)
                    
                elif line.strip()[:len(comment_symbol)] == comment_symbol:
                    line = colored(line,comment_color)
                #elif comment_block_symbol in line:
                #    comment_block = not comment_block
                else:
                    for COLOR in syntax[extension]["words"]: # Every color in syntax-dictionary
                        #input("Trying: "+str(COLOR))
                        
                        if COLOR == "comment": continue
                        if COLOR == "qmarks":
                            line = line.replace("\"",colored("\"",syntax[extension]["words"]["qmarks"]["color"]))
                            line = line.replace("'",colored("'",syntax[extension]["words"]["qmarks"]["color"]))
                            continue
                        for word in syntax[extension]["words"][COLOR]: # Every word in color
                            #print("SYNTAX",word)
                            sline = line
                            for rm in list("!?§$%&/()=,.-;:*+~{}[]"): # Temporary remove special chars [while True: | while True]
                                sline = sline.replace(rm," ")
                            #print("-> IF",word,"IN",shlex.split(sline))
                            try:
                                ssline = shlex.split(sline)
                            except ValueError:
                                continue
                            
                            if word in ssline:
                                line = line.replace(word, colored(word,COLOR))
                        """
                        STR = False
                        to_replace = []
                        e = ""
                        for letter in line:
                            if STR: e += letter
                            if letter == "\"" or letter == "'":
                                if STR == True:
                                    STR = False
                                    to_replace.append(letter+e)
                                    e = ""
                                elif STR == False:
                                    STR = True
                        #to_replace.append(letter+e)
                        for r in to_replace:
                            line = line.replace(r,colored(r,"green"))"""
                        

                                
                    #input()
            color = "white"
            if find != None: log = "Found: "
            if find == None: color = "white"
            elif find_ignorecase and find.lower() in line.lower(): color = "yellow"
            elif not find_ignorecase and find in line: color = "yellow"
            else: color = None
            if color == None:
                print(out)
            else:
                cprint(line,color)
            
        find = None
        x = input("+"*len(str(len(text)))+">")
        try: x = shlex.split(x)
        except: pass
        FOR = 1
        
        if not len(x): continue
        
        
        
        if x[0][-1] == ":" and canbeint(x[0][:-1]):
            FOR = int(x[0][:-1])
            x = x[1:]
        
        if x[0] == "undo":
            text = UNDO_TEXT
            continue

        
        
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
                        if x[1] == "*":
                            l = 0
                            for line in text:
                                text[l] = text[l].replace(to_replace,replace_with)
                                l += 1
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
                
            elif x[0] == "*<" or x[0] == "*>":
                TEXT = " ".join(x[1:-1])
                LN = x[-1]
                if len(x) < 3:
                    log = "Need text + Line-Number {*>/*< {TEXT} {*/LN/LN-LN/LN:LN:LN/LN:LN-LN}}"
                    continue
                if LN == "*":
                    l = 0
                    for line in text:
                        if x[0] == "*<":
                            text[l] = TEXT + text[l]
                        elif x[0] == "*>":
                            text[l] = text[l] + TEXT
                        l += 1
                else:
                    to_change = []
                    to_change = x[-1].split(":")
                    for t in to_change:
                        if "-" in str(t):
                            a, b = t.split("-")
                            for A in range(int(b)-int(a)+1):
                                A += int(a)
                                to_change.append(str(A))
                            del to_change[to_change.index(str(t))]
                    l = 0
                    for line in text:
                        if str(l+1) in to_change:
                            if x[0] == "*<":
                                text[l] = TEXT + text[l]
                            elif x[0] == "*>":
                                text[l] = text[l] + TEXT
                        l += 1
                

            elif x[0] == "-":
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
    
    if not "/" in filename:
        fullpath = path+filename
    else:
        fullpath = filename
    text = []
    with open(fullpath) as file:
        text = file.read().split("\n")
    # If last line is empty
    if text[-1] == "": text = text[:-1]

    try: text = text[:int(sys.argv[2])]
    except IndexError: pass
    log = "Opened file: " + str(filename).split("/")[-1]
    # Edit existing File

except FileNotFoundError:
    # New File
    input("FILE NOT FOUND "+str(fullpath))
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
