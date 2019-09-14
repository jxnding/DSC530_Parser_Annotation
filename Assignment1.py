# DSC 530
# Prof. Len Schubert
# By Zhaoxiong Ding (zding5)
# 9/14/2019
import pdb

class Tree:
    def __init__(self, child=[], thisType=None, data=None):
        self.child = child
        self.type = thisType
        self.data = data

    def parse(self):
        global parsedLines
        print("Hello: "+str(len(parsedLines)))
        # Current node info
        currLine = parsedLines[0]
        self.type = currLine[1]
        self.data = currLine[2]
        del parsedLines[0]

        currChild = []
        for i in range(len(parsedLines)): #iterate downwards
            if parsedLines[i][0] == currLine[0]+spacing: #is line a child?
                currChild.append( Tree() )
            if parsedLines[i][0] < currLine[0]+spacing:
                break

        for child in currChild:
            child.parse()
        self.child = currChild
    
class Phrase():
    #  (ROOT
    #    (S
    #      (NP (DT The-1) (NN boy-2))
    #      (VP (VBZ is-3)
    #        (VP (VBG looking-4)
    #          (ADVP (RB eagerly-5))
    #          (PP (IN for-6)
    #            (NP (PRP$ his-7) (JJ beloved-8) (NN Juliet-9)))))
    #      (. .)))
    def __init__(self, child=[], thisType=None, data=None):
        self.child = child
        self.type = thisType
        self.data = data       

if __name__ == "__main__":
    f = open("input.txt")
    lines = f.readlines()
    f.close()

    spacing = 2

    # Parse into: [# Space][TYPE][REST]
    parsedLines = []
    for line in lines:
        currLength = len(line.split('(')[0])
        currParse = [None]*3
        currParse[0] = currLength
        currParse[1] = line.split('(')[1].strip()
        currParse[2] = line.split('(')[2:]
        parsedLines.append(currParse)
    
    x = Tree()
    x.parse()
    pdb.set_trace()