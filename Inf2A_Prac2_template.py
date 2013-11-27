
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012, revised November 2013



# PART A: Processing statements

def add(item,lst):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here

class FactBase:
    """stores unary and binary relational facts"""
    # add code here

import re

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement (wlist,lx,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.



# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?


# Tags for words playing a special role in the grammar:

tagged_function_words = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in tagged_function_words]

# English nouns with identical plural forms (list courtesy of Wikipedia):

identical_plurals = ['bison','buffalo','deer','fish','moose','pike','plankton',
     'salmon','sheep','swine','trout']


def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here

def tag_word (wd,lx):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here

def tag_words (wds,lx):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (wds[0],lx)
        tag_rest = tag_words (wds[1:],lx)
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.



# PART C: Syntax and agreement checking

from statements import *
from pos_tagging import *

# Grammar for the query language (with POS tokens as terminals):

from nltk import parse_cfg
from nltk import parse
from nltk import Tree

query_grammar = parse_cfg('''
   S     -> WHO QP QM | WHICH Nom QP QM
   QP    -> VP | DO NP T
   VP    -> I | T NP | BE A | BE NP | VP AND VP
   NP    -> P | AR Nom | Nom
   Nom   -> AN | AN Rel
   AN    -> N | A AN
   Rel   -> WHO VP | NP T
   N     -> "Ns" | "Np"
   I    -> "Is" | "Ip"
   T    -> "Ts" | "Tp"
   A     -> "A"
   P     -> "P"
   BE    -> "BEs" | "BEp"
   DO    -> "DOs" | "DOp"
   AR    -> "AR"
   WHO   -> "WHO"
   WHICH -> "WHICH"
   AND   -> "AND"
   QM    -> "?"
   ''')

cp = parse.ChartParser(query_grammar)

def all_parses(wlist,lx):
    """returns all possible parse trees for all possible taggings of wlist"""
    all = []
    for tagging in tag_words(wlist,lx):
        all = all + cp.nbest_parse(tagging)
    return all

# This produces parse trees of type Tree.
# Available operations on trees:  tr.node, tr[i],  len(tr)


# Singular/plural agreement checking.

# For convenience, we reproduce the parameterized rules from the handout here:

#    S      -> WHO QP[y] QM | WHICH Nom[y] QP[y] QM
#    QP[x]  -> VP[x] | DO[y] NP[y] T[p]
#    VP[x]  -> I[x] | T[x] NP | BE[x] A | BE[x] NP[x] | VP[x] AND VP[x]
#    NP[s]  -> P | AR Nom[s]
#    NP[p]  -> Nom[p]
#    Nom[x] -> AN[x] | AN[x] Rel[x]
#    AN[x]  -> N[x] | A AN[x]
#    Rel[x] -> WHO VP[x] | NP[y] T[y]
#    N[s]   -> "Ns"  etc.

def label(t):
    if (isinstance(t,str)):
        return t
    elif (isinstance(t,tuple)):
        return t[1]
    else:
        return t.node

def top_level_rule(tr):
    if (isinstance(tr,str)):
        return ''
    else:
        rule = tr.node + ' ->'
        for t in tr:
            rule = rule + ' ' + label(t)
        return rule

def N_phrase_num(tr):
    """returns the number attribute of a noun-like tree, based on its head noun"""
    if (tr.node == 'N'):
        return tr[0][1]  # the s or p from Ns or Np
    elif  # add code here

def V_phrase_num(tr):
    """returns the number attribute of a verb-like tree, based on its head verb,
       or '' if this is undetermined."""
    if (tr.node == 'T' or tr.node == 'I'):
        return tr[0][1]  # the s or p from Is,Ts or Ip,Tp
    elif  # add code here

def matches(n1,n2):
    return (n1==n2 or n1=='' or n2=='')

def check_node(tr):
    """checks agreement constraints at the root of tr"""
    rule = top_level_rule(tr)
    if (rule == 'S -> WHICH Nom QP QM'):
        return (matches (N_phrase_num(tr[1]), V_phrase_num(tr[2])))
    elif  # add code here

def check_all_nodes(tr):
    """checks agreement constraints everywhere in tr"""
    if (isinstance(tr,str)):
        return True
    elif (not check_node(tr)):
        return False
    else:
        for subtr in tr:
            if (not check_all_nodes(subtr)):
                return False
        return True

def all_valid_parses(wlist,lx):
    """returns all possible parse trees for all possible taggings of wlist
       that satisfy agreement constraints"""
    return [t for t in all_parses(wlist,lx) if check_all_nodes(t)]

# Converter to add words back into trees.
# Strips singular verbs and plural nouns down to their stem.

def restore_words_aux(tr,wds):
    if (isinstance(tr,str)):
        wd = wds.pop()
        if (tr=='Is'):
            return ('I_' + verb_stem(wd), tr)
        elif (tr=='Ts'):
            return ('T_' + verb_stem(wd), tr)
        elif (tr=='Np'):
            return ('N_' + noun_stem(wd), tr)
        elif (tr=='Ip' or tr=='Tp' or tr=='Ns' or tr=='A'):
            return (tr[0] + '_' + wd, tr)
        else:
            return (wd, tr)
    else:
        return Tree(tr.node, [restore_words_aux(t,wds) for t in tr])

def restore_words(tr,wds):
    """adds words back into syntax tree, sometimes tagged with POS prefixes"""
    wdscopy = wds+[]
    wdscopy.reverse()
    return restore_words_aux(tr,wdscopy)

# Example:

# lx.add('John','P')
# lx.add('like','T')
# tr0 = all_valid_parses(['Who','likes','John','?'],lx)[0]
# tr.draw()
# tr = restore_words(tr0,['Who','likes','John','?'])

# End of PART C.



# PART D: Semantics for the Query Language.

from statements import *
from pos_tagging import *
from agreement import *

def sem(tr):
    """translates a syntax tree into a logical lambda expression (in string form)"""
    rule = top_level_rule(tr)
    if (tr.node == 'P'):
        return tr[0][0]
    elif (tr.node == 'N'):
        return '(\\x.' + tr[0][0] + '(x))'   # \\ is the escape sequence for \
    elif  # add code here
    
    elif (rule == 'AN -> A AN'):
        return '(\\x.(' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'
    elif  # add more code here
    

# Logic parser for lambda expressions

from nltk import LogicParser
lp = LogicParser()

# Lambda expressions can now be checked and simplified as follows:

#   A = lp.parse('(\\x.((\\P.P(x,x))(loves)))(John)')
#   B = lp.parse(sem(tr))  # for some tree tr
#   A.simplify()
#   B.simplify()


# Model checker

from nltk.sem.logic import *

# Can use: A.variable, A.term, A.term.first, A.term.second, A.function, A.args

def interpret_const_or_var(s,bindings,entities):
    if (s in entities): # s a constant
        return s
    else:               # s a variable
        return [p[1] for p in bindings if p[0]==s][0]  # finds most recent binding

def model_check (P,bindings,entities,fb):
    if (isinstance (P,ApplicationExpression)):
        if (len(P.args)==1):
            pred = P.function.str()
            arg = interpret_const_or_var(P.args[0].str(),bindings,entities)
            return fb.queryUnary(pred,arg)
        else:
            pred = P.function.function.str()
            arg0 = interpret_const_or_var(P.args[0].str(),bindings,entities)
            arg1 = interpret_const_or_var(P.args[1].str(),bindings,entities)
            return fb.queryBinary(pred,arg0,arg1)
    elif (isinstance (P,EqualityExpression)):
        arg0 = interpret_const_or_var(P.first.str(),bindings,entities)
        arg1 = interpret_const_or_var(P.second.str(),bindings,entities)
        return (arg0 == arg1)
    elif (isinstance (P,AndExpression)):
        return (model_check (P.first,bindings,entities,fb) and
                model_check (P.second,bindings,entities,fb))
    elif (isinstance (P,ExistsExpression)):
        v = str(P.variable)
        P1 = P.term
        for e in entities:
            bindings1 = [(v,e)] + bindings
            if (model_check (P1,bindings1,entities,fb)):
                return True
        return False

def find_all_solutions (L,entities,fb):
    v = str(L.variable)
    P = L.term
    return [e for e in entities if model_check(P,[(v,e)],entities,fb)]


# Interactive dialogue session

def fetch_input():
    s = raw_input('$$ ')
    while (s.split() == []):
        s = raw_input('$$ ')
    return s    

def output(s):
    print ('     '+s)

def dialogue():
    lx = Lexicon()
    fb = FactBase()
    output('')
    s = fetch_input()
    while (s.split() == []):
        s = raw_input('$$ ')
    while (s != 'exit'):
        if (s[-1]=='?'):
            sent = s[:-1] + ' ?'  # tolerate absence of space before '?'
            wds = sent.split()
            trees = all_valid_parses(wds,lx)
            if (len(trees)==0):
                output ("Eh??")
            elif (len(trees)>1):
                output ("Ambiguous!")
            else:
                tr = restore_words (trees[0],wds)
                lam_exp = lp.parse(sem(tr))
                L = lam_exp.simplify()
                # print L  # useful for debugging
                entities = lx.getAll('P')
                results = find_all_solutions (L,entities,fb)
                if (results == []):
                    if (wds[0].lower() == 'who'):
                        output ("No one")
                    else:
                        output ("None")
                else:
                    buf = ''
                    for r in results:
                        buf = buf + r + '  '
                    output (buf)
        else:
            if (s[-1]=='.'):
                s = s[:-1]  # tolerate final full stop
            wds = s.split()
            msg = process_statement(wds,lx,fb)
            if (msg == ''):
                output ("OK.")
            else:
                output ("Sorry - " + msg)
        s = fetch_input()

# End of PART D.
