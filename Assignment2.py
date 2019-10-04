# DSC 530
# Prof. Len Schubert
# By Zhaoxiong Ding (zding5)
# 9/14/2019
import pdb
import sys

############# NOT MY CODE, WILL'S CODE BELOW ##############
PUNCTUATION_TAGS = [',', ':', '.', '``', '\'\'', '-LRB-', '-RRB', '-LSB-', '-RSB-', '$', '#']

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
			return parenthesize(s), [s], idx + 1

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
		indexed_constituents_str = "" ############parenthesize(indexed_constituents_str)

	return indexed_constituents_str, indexed_constituents, idx
############### END WILL'S CODE #################

class Tree:
    def __init__(self, child=[], thisType=None, word=""):
        self.child = child
        self.type = thisType
        self.word = word

    def __str__(self,padding=0):
        spacing = 2
        out = ""
        pd = " "*padding
        childStr = ""
        for child in self.child:
            childStr += child.__str__(padding+spacing)
        return "\n"+pd+"("+self.type+" "+self.word+childStr+")"

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

    # new parse function
    def parse2(self,currList):
        if len(currList)>0:
            currList[0] = currList[0].strip()
            self.type = currList[0].split(" ")[0]
            # if it's a leaf, just directly add word to node (so no separate node for leaf)
            if len(currList[0].split(" "))>1:
                self.word = currList[0].split(" ")[1]
            for nextInput in currList[1:]:
                newNode = Tree()
                newNode.child = [] #????
                newNode.parse2(nextInput)
                self.child.append(newNode)

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
        grammar = {
                        "S" : [("NP ADVP VP", [2,3,1], "((2 3) 1)"), ("NP VP", [2,1], "(2 1)"), ("VP", [1], "(ka 1)")],
                        "NP" : [("NN", [1],"(k 1)"), ("PRP", [1],"1"), ("PRP$ NN", [1,2],"(1 2)"), ("NNP", [1],"1"), ("PRP$ JJ NN", [2,3,1],"(1 (2 3))"), ("PRP$ JJ NNP", [3,2,1],"(1 (2 (= 3)))"), ("DT NNS", [1,2],"(1 2)")],
                        "ADVP" : [("RB", [1], "1")],
                        "VP" : [("VBZ", [1], "1"), ("VBZ PP", [1,2], "(1 2)"), ("VBZ S", [1,2], "(1 2)"), ("VB S", [1,2], "(1 2)"), ("VB NP", [1,2], "(1 2)"), ("VBG NP", [1,2], "(1 2)"), ("MD VP", [1,2], "(1 2)"), ("MD RB VP", [2,3,1], "(1 (2 3))"), ("TO VP", [1,2], "(1 2)")],
                        "PP" : [("IN NP", [1,2], "(1 2)")]
                    }
        lexicon = {
                        "NN" : [0,".n"],
                        "NNS": ["(plur ", 0, ".n)"],
                        "NNP" : [0,".c"],
                        "PRP" : [0,".pro"],
                        "PRP$" : [0,".d"],
                        "DT" : [0,".d"],
                        "JJ" : [0,".a"],
                        "RB" : [0,".adv"],
                        "RB" : [0,".adv"],
                        "MD" : [0,".v-aux"],
                        "VBZ" : [1, 2, 0, ".v", 2, 1],
                        "VBG" : [3, 4, 0, ".v", 4, 3],
                        "VB" : [5, 6, 0, ".v", 6, 5],
                        "TO" : ["ka"],
                        "IN" : [0,".p"],
                    }

        # SKIP ROOT
        if self.type=="ROOT":
            return self.child[-1].semanticParse()

        # For productions
        try:        
            # figure out which production we're in
            correctProduction = -1
            for k,production in enumerate(grammar[self.type]): #loop through productions
                terms = production[0].split(" ")
    
                correct = True
                for i in range(len(terms)): #loop through rules within production
                    try:
                        if self.child[i].type!=terms[i]:
                            correct = False
                            break
                    except: #terms could be longer
                        correct = False
                        break
                if correct:
                    if len(terms)==len(self.child): #check to see that the production's satisfied
                        correctProduction = k
                        break
                    else:
                        pass
            if correctProduction == -1:
                print("ERROR: Unable to find correct production in grammar for: "+self.type+" --> "+"".join([x.type+" " for x in self.child]), file=sys.stderr)
            
            # Apply production
            ansStr = {}
            # Use the order of the production, ex. S -> NP ADVP VP; ((2 3) 1) would go to the 3rd item first
            for i,childNode in enumerate(grammar[self.type][correctProduction][1]):
                currLogic=self.child[childNode-1].semanticParse()+" " #adjust by 1, recursive call
                if i>0: #try to use rules
                    ans = ansStr[grammar[self.type][correctProduction][1][i-1]]
                    unboundedVarLoc = ans.find("λ")
                    # Lambda
                    if unboundedVarLoc!= -1: #if there is an unbounded variable
                        unboundedVar = ans[unboundedVarLoc+1]
                        ans = ans.replace("λ"+str(unboundedVar),"")
                        ans = ans.replace(str(unboundedVar),currLogic)
                        ansStr[grammar[self.type][correctProduction][1][i-1]] = ""
                        ansStr[childNode] = ans
                    else: #no unbounded variable
                        ansStr[childNode] = currLogic
                else:
                    ansStr[childNode]=currLogic
            
            # Apply formatting
            ans = ""
            for char in grammar[self.type][correctProduction][2]:
                if char.isdigit():
                    ans+=ansStr[int(char)]
                else:
                    ans+=char
        # For words
        except KeyError:
            ans = ""
            if self.type in lexicon:
                currLexicon = lexicon[self.type]
                var = {} #store found vars
                for logic in currLexicon:
                    if type(logic)==type(""):
                        ans+=logic
                    elif logic==0: #0 represents word
                        ans+=self.word
                    else:
                        try: #only add the lambda symbol the first time the var is used
                            var[logic]
                            ans+=" "+str(logic)+" "
                        except:
                            var[logic] = 0
                            ans+=" λ"+str(logic)+" "
            else: #catch case
                ans = self.word
        return ans
    
class Phrase:
    def __init__(self, part="", word="", number=None):
        self.part = part
        self.word = word
        self.number = number
    
    def __str__(self):
        return "("+self.part+" "+self.word+"-"+str(self.number)+")"

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Format: [Input File]")
        sys.exit()

    ## FILE INPUT
    f = open(sys.argv[1], 'r')
    lines = "".join([line.strip() for line in f])
    _, indexed_constituents, _ = index_words(lines)

    ## FUNCTION CALLS
    # Create and Parse Tree
    x = Tree()
    x.parse2(indexed_constituents[1])

    ## AS2
    print(x.semanticParse())
