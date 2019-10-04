DSC 530: Assignment 2
10/2/19
Zhaoxiong Ding

How to Run:
    python3 replace.py "bunny" "b" "f"
    funny

    python3 lambda-convert.py "((λ y (λ x (like.v x y))) Juliet.c)"
    (λ x (like.v x Juliet.c)))

    python3 Assignment2.py input.txt
    (((     try.v will.v-aux   (ka (ka  (     cover.v will.v-aux   (all.d  (plur sentences.n) )   ) ) )   )  (not.adv  ))  We.pro  )

List of Files:
    README.txt - This readme
    as2 - Your assignment prompt
    input.txt - Sample input for my as2
    output.txt - Sample output for my input

    replace.py - outputs to std.out
        Usage: [Input] [To Be Replaced] [Replacer]
    lambda-convert.py - outputs to std.out
        Usage: [Phrase]
    Assignment2.py - outputs to std.out
        Usage: [Input File]

Implementation:
    First, I take in an input file (specified through first argument) containing a PST. Then I use Will's code to output a list representation of the PST. Then I use my own code to create an explicit tree from this list. Each tree node contains a list of children, a type, and a word (can be null). I then call semanticParse(), which does not require any inputs since the tree is already annotated with tags and words.

    Semantic Parsing:
        I implemented a semanticParse() function in my Tree() class.
        The function contains both the grammar and the lexicon. After skipping the ROOT node (if applicable), I try to use either the grammar or the lexicon dictionaries (depending on where the tag exists as a key).
        Once in grammar, I try to find the correct production by checking the tags of all the child nodes. Then I recursively call semanticParse() on all the child nodes.
        Once I have the correct production, I apply the semantic rules by attempting to find an unbounded variable.
        After the semantic rule is applied, I format the string and return it.

        In lexicon, the process is simpler. I apply the lexicon rules (ex. "(plur sentence.n)" ) to its word.
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
        All of my programs check for input and output a helpful message
        Assignment2.py will output to std.err if it cannot find a production (rule) for a node on the tree. It will attempt to continue anyways.

Test Sentences:
    Romeo likes Juliet
        There's no NP --> NNP NNP NNP production so my program cannot parse this sentence.

    Romeo longs for his beloved Juliet
    ( (     longs.v Romeo.c    (for.p  (his.d  (beloved.a  (= Juliet.c ))) )   ) )
    
    My dog also likes eating sausage
    ((also.adv   ) (     likes.v (My.d  dog.n )   (ka (    λ4 eating.v 4  (k sausage.n )   ) )   ) )

    We will not try to cover all sentences
    (((     try.v will.v-aux   (ka (ka  (     cover.v will.v-aux   (all.d  (plur sentences.n) )   ) ) )   )  (not.adv  ))  We.pro  )

    The future of NLP is exciting
    ( (     is.v ((The.d  future.n )  (of.p  NLP.c  ) )      ) )
        Unable to find productions for: VP --> VBZ ADJP, NP --> NP PP, NP --> DT NN

    Every Tuesday I had two apples
    ((had  (two  (plur apples.n) ) )  (Every.d  Tuesday.c ) )
        Unable to find productions for: VP --> VBD NP, NP --> CD NNS, NP --> DT NNP NN


Use of Will's Code to "Parse":
    Part of Will's code is in my code, from Line 8 to Line 112, clearly marked by comments. This is the execution flow of my program:
    1. Read lines from file specified by user via std.in
    2. Strip whitespace and merge lines into giant string
    3. (WILL) Input string in Will's function and store the output list of format:
        ['', ['S', ['NP ', ['NNP Romeo']], ['VP ', ['VBZ longs'], ['PP ', ['IN for'], ['NP ', ['PRP$ his'], ['JJ beloved'], ['NNP Juliet']]]]]]
    4. Generate (and tag) my explicit tree with this list
    5. Semantic parse with application of semantic grammar

    I chose to use Will's code to generate the list from the input PST because I realized rather late in the process for as2 that I made a fundamental misunderstanding of the relations within a PST in as1. For example:
        (S
            (NP (NNP Romeo))
            (VP (VBZ longs)
                (PP (IN for)
                (NP (PRP$ his) (JJ beloved) (NNP Juliet)))))
    I previously thought that the lines and whitespace was crucial to the structure (and not the parentheses). As a result, I thought that expressions on the same line were a different kind of "child" than the following lines. In as1, I would attach VBZ to the VP node itself under a "data" list, while only the PP and NP nodes would be proper children. Similarly, the bottommost NP would have 0 children, and all of PRP$, JJ, and NNP would be under its "data" list.

    Since I realized this misunderstanding at the last moment, I decided to use Will's code to parse the input PST. After that point everything is my code and logic. It's my belief these functions are not what as2 is really testing our knowledge of (rather as1 did). Thus, I'm justified in using -- with proper citation -- a portion of Will's code as a precursor to my as2 assignment. 
