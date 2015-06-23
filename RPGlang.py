from __future__ import print_function
from time import sleep
import re
import sys
try:
    usesound = True
    import pyglet
except ImportError:
    usesound = False
    print('You don\'t have Pyglet installed! This program will still work, but sounds won\'t work!')

settings = {
    'CASESENSITIVE':True,
    'SWITCHREGEX':False
    }
    
def isliteral(s):
    if re.match(r'[0-9]+', s) or s[0] == '"' and s[-1] == '"':
        return True
    return False

def lexline(line):
    r=[]
    s=0
    while s < len(line):
        if re.match(r'^"[^"]*"', line[s:]):
            #print('String')
            m = re.match(r'^"[^"]*"', line[s:])
            r.append(m.group(0))
            s+=len(m.group(0))
            
        elif re.match(r'^PRINT', line[s:]):
            r.append('PRINT')
            s += 5
            
        elif re.match(r'^SWITCH', line[s:]):
            r.append('SWITCH')
            s += 6
            
        elif re.match(r'^CASE', line[s:]):
            r.append('CASE')
            s += 4
            
        elif re.match(r'^ELSE', line[s:]):
            r.append('ELSE')
            s += 4
            
        elif re.match(r'^GOTO', line[s:]):
            r.append('GOTO')
            s += 4

        elif re.match(r'^ASK', line[s:]):
            r.append('ASK')
            s += 3
            
        elif re.match(r'^[A-Z]+', line[s:]):
            m = re.match(r'^[A-Z]+', line[s:])
            r.append(m.group(0))
            s += len(m.group(0))
            
        elif re.match(r'^[0-9]+', line[s:]):
            #print('Num')
            m = re.match(r'^[0-9]+', line[s:])
            r.append(m.group(0))
            s += len(m.group(0))
            
        elif re.match(r'^\s', line[s:]):
            #print('Space')
            s += 1

        else:
            raise ValueError('Invalid String '+line[s:])
        #print(r)
    return r

def diatof(f):
    text = open(f).read()
    for line in text.split('\n'):
        if line[0] == '/':
            com = line.split()[0][1:].lower()
            line = line.split()[1:]
            if com == 'wait':
                time.sleep(float(line[0]))
            elif com == 'playsound':
                print('Playsound command Not Yet Supported!')
                print(line[1:])
            elif com == '':
                pass
                
            
        else:
            if line[0] == '\\':
                print(line[1:])
            else:
                print(line)

def parsecase(con): #Con is for construct
    i = 0
    r = {}
    while i < len(con):
        if con[i] == 'CASE':
            key = con[i+1]
            i += 2
            val = []
            while not con[i] == 'CASE' and not con[i] == 'ELSE' and not i == len(con):
                val += [con[i]]
                i += 1
            r[key] = val
                
        elif con[i] == 'ELSE':
            key = '*'
            i += 1
            val = []
            while not i == len(con):
                val += [con[i]]
                i += 1
            r[key] = val
    return r
    
def findcase(val, cases):
    if cases.get(val):
        return cases[val]
    elif cases.get('*'):
        return cases['*']
    return None

def run(script):
    env = {'ELSE': True}
    ended = False
    linenum = 0 #Starting Line
    script = script.split('\n')
    while ended != True:
        line = script[linenum]
        line = lexline(line)
        i = 0

        linedone = False
        while i < len(line) and linedone != True:
            if line[i] == 'PRINT': #Printing stuff
                if isliteral(line[i+1]): #Use variables
                    print(line[i+1].strip('"'), end='')
                else:
                    print(env[line[i+1]], end='')
                i+=2

            elif line[i] == 'DIATOF': #Dialogue from files
                if isliteral(line[i+1]): #Use variables
                    diatof(line[i+1].strip('"'), end='')
                else:
                    diatof(env[line[i+1]], end='')
                i+=2
                
            elif line[i] == 'ASK': #Get input and store it in INPUT variable
                inp = raw_input()
                if settings['CASESENSITITIVE']:
                    env['INPUT'] = inp
                else:
                    env['INPUT'] = inp.upper()

                i+=1
                
            elif line[i] == 'SWITCH':
                switchvar = line[i+1]
                if not isliteral(switchvar): #Use variables
                    switchvar = env[switchvar]
                
                switchvar = switchvar.strip('"')

                output = findcase(switchvar, parsecase(line[i+2:]))

                line = line[:i]
                line += output
                
            elif line[i] == 'GOTO':
                if isliteral(line[i+1]):
                    linenum = int(line[i+1])
                    linedone = True
                else:
                    linenum = int(env[line[i+1]])
                    linedone = True

            elif line[i] == 'END': #Terminate the Script
                linedone = True
                ended = True

if __name__ == '__main__':
    run(raw_input())
    raw_input()
