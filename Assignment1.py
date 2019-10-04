# DSC 530
# Prof. Len Schubert
# By Zhaoxiong Ding (zding5)
# 9/14/2019
import pdb
import sys

class Tree:
    def __init__(self, child=[], thisType=None, data=[]):
        self.child = child
        self.type = thisType
        self.data = data

    def __str__(self,padding=0):
        spacing = 2
        out = ""
        pd = " "*padding
        for data in self.data:
            out += str(data)
            out += " "
        childStr = ""
        for child in self.child:
            childStr += child.__str__(padding+spacing)
        return "\n"+pd+"("+self.type+" "+out+childStr+")"

    def parse(self):
        global parsedLines
        # Current node info
        currLine = parsedLines[0]
        self.type = currLine[1].replace(')','')
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
    
    def createPhrases(self):
        if len(self.data)>0:
            currData = []
            for block in self.data: #['DT The) ', 'NN boy))\n']
                block = block.replace(')','').strip()
                block = block.split()
                currPhrase = Phrase(block[0],block[1])
                currData.append(currPhrase)
            self.data = currData
        for child in self.child:
            child.createPhrases()

    def indexWords(self, start=1):
        for data in self.data:
            data.number = start
            start+=1
        for child in self.child:
            start=child.indexWords(start)
        return start

    #AS2 below
    def semanticParse(self):
        parseOrder = {
                        "S" : [("NP ADVP VP", [2,3,1]), ("NP VP", [2,1]), ("VP", [1])],
                        "NP" : [("NN", [1]), ("PRP", [1]), ("PRP$ NN", [1,2]), ("NNP", [1]), ("PRP$ JJ NN", [2,3,1]), ("PRP$ JJ NNP", [3,2,1]), ("DT NNS", [1,2])],
                        "ADVP" : [("RB", [1])],
                        "VP" : [("VBZ", [1]), ("VBZ PP", [1,2]), ("VBZ S", [1,2]), ("VB S", [1,2]), ("VB NP", [1,2]), ("VBG NP", [1,2]), ("MD VP", [1,2]), ("MD RB VP", [2,3,1]), ("TO VP", [1,2])],
                        "PP" : [("IN NP", [1,2])]
                    }

        # figure out which production we're in
        correctProduction = -1
        for k,production in enumerate(parseOrder[self.type]):
            terms = production[0].split(" ")
 
            correct = True
            for i in range(len(terms)):
                try:
                    if self.child[i].type!=terms[i]:
                        correct = False
                        break
                except: #terms could be longer
                    correct = False
                    break
            if correct:
                correctProduction = k
                break
        
        ans = ""
        for childNode in parseOrder[self.type][correctProduction][1]:
            print(str(childNode)+" "+str(len(self.child)))
            ans+=self.child[childNode-1].semanticParse() #adjust by 1
        
        return ans

    
class Phrase:
    #  (ROOT
    #    (S
    #      (NP (DT The-1) (NN boy-2))
    #      (VP (VBZ is-3)
    #        (VP (VBG looking-4)
    #          (ADVP (RB eagerly-5))
    #          (PP (IN for-6)
    #            (NP (PRP$ his-7) (JJ beloved-8) (NN Juliet-9)))))
    #      (. .)))
    def __init__(self, part="", word="", number=None):
        self.part = part
        self.word = word
        self.number = number
    
    def __str__(self):
        return "("+self.part+" "+self.word+"-"+str(self.number)+")"

if __name__ == "__main__":
    ## FILE INPUT
    f = open(sys.argv[1])
    lines = f.readlines()
    f.close()

    spacing = 2

    ## BASIC PARSING
    # Parse into: [# Space][TYPE][REST]
    parsedLines = []
    for line in lines:
        currLength = len(line.split('(')[0])
        currParse = [None]*3
        currParse[0] = currLength
        currParse[1] = line.split('(')[1].strip()
        currParse[2] = line.split('(')[2:]
        parsedLines.append(currParse)

    ## DATA


    
    ## FUNCTION CALLS
    # Create and Parse Tree
    x = Tree()
    x.parse()
    x.createPhrases()
    x.indexWords()

    # AS2
    # pdb.set_trace()
    # x.semanticParse()

    # Tests
    print(x)