I had a major misunderstanding of the PST
Used will's code


how i do lambda

Implementation:
    First, I take in an input file (specified through first argument) containing a PST. Then I use Will's code to output a list representation of the PST. Then I use my own code to create an explicit tree from this list. Each tree node contains a list of children, a type, and a word.
    Semantic Parsing:
        I implemented a semanticParse() function in my Tree() class.
        The function contains both the grammar and the lexicon. After skipping the ROOT node (if applicable), I try to use either the grammar or the lexicon dictionaries (depending on where the tag exists as a key).
        Once in grammar, I try to find the correct production by checking the tags of all the child nodes. Then I recursively call semanticParse() on all the child nodes.
    Grammar:
        The grammar is stored as a dictionary (in the semanticParse function of the Tree class) in which the keys are the tags (S, NP, ADVP, etc), and the value is a list of the possible productions.
            Example: "ADVP" : [("RB", [1], "1")]. 
        In this case, the list contains only 1 production. Each production is a 3-ple, with the 1st item being a string representing the part of speech, the 2nd representing the order of parse, and the 3rd representing the logic format (order of printing and location of parentheses)

        I then apply the lambda functions by checking for an unbounded variable. If found, I replace it with the previous child's recursive semanticParse() output (IN THE ORDER OF THE GRAMMAR, so for "S -> NP VP; (2 1)" I visit the 2nd child then the 1st child).
    Lexicon:
        The lexicon is stored as a dictionary (same place) in which the keys are tags (NN, NNP, VBZ, etc) and the values are lists containing the lambda functions. Note: there is no hardbaked lexicon, so I actually support any NN, any JJ, any, VB, etc -- so long as they are properly tagged in the input PST.
            Example: "VBZ" : [1, 2, 0, ".v", 2, 1],
        Here, the number 0 represents the word itself. Any strings are literally added to the resulting string. All other numbers are used as variables.
    Error Handling:


Use of Will's Code to "Parse":
    Part of Will's code is in my code, from Line 8 to Line 131, clearly marked by comments. This is the execution flow of my program:
    1. Read lines from file specified by user via std.in
    2. Strip whitespace and merge lines into giant string
    3. (WILL) Input string in Will's function and store the output list of format:
        ['', ['S', ['NP ', ['NNP Romeo']], ['VP ', ['VBZ longs'], ['PP ', ['IN for'], ['NP ', ['PRP$ his'], ['JJ beloved'], ['NNP Juliet']]]]]]