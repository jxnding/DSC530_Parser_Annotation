#@Author: Zhaoxiong Ding
import sys 

def findFirstLambda(s):
    firstVar = ""
    start = s.find("λ")+1
    while firstVar == "":
        if s[start].isalpha():
            firstVar = s[start]
        else:
            start+=1
    return firstVar, start

def findB(s):
    section = s.split(" ")[-1].strip()
    section = section.replace(")","")
    return section

def lambdaConvert(s,var,loc,b):
    s = s[loc+1:] #get rid of beginning
    s = s.replace(b,"") #get rid of b (ex. Juliet.c)
    s = s.strip()

    s = s.replace(var,b)
    return s

def stripOuterParen(s):
    while True:
        s=s.strip()
        if s[0]=="(" and s[-1]==")":
            s = s[1:-1]
        else:
            break
    return s

if len(sys.argv)<2:
    print("Format: [Phrase]")
    sys.exit()

s = stripOuterParen(sys.argv[1].strip())
p,l = findFirstLambda(s)
b = findB(s)
s = lambdaConvert(s,p,l,b)

print(s)