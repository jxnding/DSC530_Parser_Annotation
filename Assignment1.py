# DSC 530
# Prof. Len Schubert
# By Zhaoxiong Ding (zding5)
# 9/14/2019
import pdb
import sys

### WILL
PUNCTUATION_TAGS = [',', ':', '.', '``', '\'\'', '-LRB-', '-RRB', '-LSB-', '-RSB-', '$', '#']

# A subset of the phrase type tags recognized by the Penn Treebank. See the
# README for more details on how the subset was selected.
PHRASE_TYPES = ['S', 'NP', 'VP', 'PP', 'ADJP', 'ADVP', 'SBAR', 'SBARQ', 'SQ', 'WHADJP', 'WHADVP', 'WHPP']

def read_data(fp):
	"""Reads in a file containing a phrase structure parse as a single string

	Arguments:
	  fp -- Path to the file to be read in

	Return Values:
	  s -- The phrase structure parse as a string
	"""
	file = open(fp, 'r')
	s = ''
	for line in file:
		s += line.strip()
	return s

def parenthesize(s):
	"""Parenthesizes a string

	Arguments:
	  s -- The string to parenthesize

	Return Values:
	  The parenthesized string
	"""
	return '(' + s + ')'

def index_words(s, idx=1):
	"""Appends indices to words in a phrase structure parse based on their order in
   the sentence.

   Arguments:
     s -- The phrase structure parse to be indexed (a string)
     idx -- The highest index that has been already been applied to a word in
       the parse. The indexing starts at 1 by default.

   Return values:
     indexed_constituents_str -- A string consisting of the indexed phrase
       structure parse
     indexed_constituents -- A list of lists (whose structure reflects the
       nesting structure of the PST), with all words indexed.
     idx -- Same as in the arguments.
	"""
	# If no paren is present in the string, it means
	# we've hit a pair of atoms (a tag and a word).
	if '(' not in s:

		# Identify the tag and the word
		tag, word = s.split()

		# If the token is a puncutation mark, we shouldn't index it 
		# (or increment the index counter), so just return them as is
		if tag in PUNCTUATION_TAGS:
			return parenthesize(s), [s], idx

		# Otherwise, we have a token that's *not* a punctuation mark, which
		# means we need to index it and increment the index counter.
		else:
			return parenthesize(s + '-' + str(idx)), [s + '-' + str(idx)], idx + 1

	# A paren in the string indicates that we still have a phrase that needs to
	# be parsed. We now need to determine the constituents of the phrase. 		
	start_idx = s.index('(')
	tag = s[:start_idx]

	# A list to hold all of the constituents of the current phrase. This will
	# actually end up being a list of lists of varying depths as the recursive
	# calls pile up.
	constituents = []

	# A string for capturing a constituent between parentheses
	expression = ''

	# A counter to keep track of the number of unmatched parentheses
	unmatched_count = 0

    # Iterate over the string, matching parentheses.  
	for i,c in enumerate(s[start_idx:]):

		# Found a closing paren, so decrement the unmatched count
		if c == ')':
			unmatched_count -= 1

		# If the number of unmatched parens is greater than 0, it means we're
		# still building out the current constituent, so append the current
		# character to that constituent.	
		if unmatched_count > 0:
			expression += c

		# Found an open paren, so increment the unmatched count	
		if c == '(':
			unmatched_count += 1

		# All parens have been matched, which means we've found a complete
		# constituent. Append the constituent to the list of all constituents
		# in the phrase and reset the builder string.
		# TODO: explain why isspace is necessary
		if unmatched_count == 0 and not c.isspace():
			constituents.append(expression)
			expression = ''

	# Constituents that have been indexed		
	indexed_constituents = [tag]
	indexed_constituents_str = tag

	# Recurse on each constituent that was found, appending the results to the
	# list of already-indexed constituents.
	for constituent in constituents:
		indexed_str, indexed, idx = index_words(constituent, idx)
		indexed_constituents.append(indexed)
		indexed_constituents_str += indexed_str

    # When we're at the root, don't double-parenthesize the whole parse
	if tag != 'ROOT':
		indexed_constituents_str = parenthesize(indexed_constituents_str)

	return indexed_constituents_str, indexed_constituents, idx
### WILL

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

    def addChild(self,node):
        self.child.append(node)
    def parse2(self,currList):
        if len(currList)>0:
            # currList = inputList
            
            self.type = currList[0]
            print(self.type)
            # pdb.set_trace()
            for nextInput in currList[1:]:
                # pdb.set_trace()
                newNode = Tree()
                newNode.child = [] #????
                newNode.parse2(nextInput)
                self.child.append(newNode)
                # self.child+=newNode
    
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
    # f = open(sys.argv[1])
    # lines = f.readlines()
    # f.close()

    # spacing = 2

    # ## BASIC PARSING
    # # Parse into: [# Space][TYPE][REST]
    # parsedLines = []
    # for line in lines:
    #     currLength = len(line.split('(')[0])
    #     currParse = [None]*3
    #     currParse[0] = currLength
    #     currParse[1] = line.split('(')[1].strip()
    #     currParse[2] = line.split('(')[2:]
    #     parsedLines.append(currParse)

    s = read_data(sys.argv[1])
    indexed_constituents_str, indexed_constituents, idx = index_words(s)
    ## DATA


    
    ## FUNCTION CALLS
    # Create and Parse Tree
    x = Tree()
    x.parse2(indexed_constituents[1])
    # x.createPhrases()
    # x.indexWords()

    # AS2
    pdb.set_trace()
    # x.semanticParse()

    # Tests
    print(x)