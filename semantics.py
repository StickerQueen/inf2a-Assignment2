from statements import *
from pos_tagging import *
from agreement import *


def sem(tr):
    """translates a syntax tree into a logical lambda expression (in string form)"""
    rule = top_level_rule(tr)
    if (tr.node == 'P'):
        return tr[0][0]
    elif (tr.node == 'N'):
        return '(\\x. ' + tr[0][0] + '(x))'   # \\ is the escape sequence for 
    elif (tr.node == 'A'):
      ret = '(\\x. (' + tr[0][0] + '(x))'
      print 'check4'
      print ret
      return ret
    elif (tr.node == 'I'):
      return '(\\x. '+tr[0][0]+'(x))'
    elif (tr.node == 'T'):
      return '(\\x. (\\y. '+tr[0][0]+'(x,y)))'

    elif (rule == 'AN -> A AN'):
        return '(\\x.(' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'
    elif (rule == 'AN -> N'):
        return '(\\x. (' + sem(tr[0]) + '(x)))'
    elif (rule == 'NP -> Nom'):
        return '(\\x. ' + sem(tr[0]) + '(x))'
    elif (rule == 'NP -> AR Nom'):
        return '(\\x. ' + sem(tr[1]) + '(x))'
    elif (rule == 'NP -> P'):
        return sem(tr[0])
    elif (rule == 'Nom -> AN'):
        return '(\\x. ' + sem(tr[0]) + '(x))'
    elif (rule == 'Nom -> AN Rel'):
        return '(\\x. (' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'
    elif (rule == 'Rel -> WHO VP'):
        return '(\\x.(' + sem(tr[0]) + '(x)))'
    elif (rule == 'Rel -> NP T'):
        return '(\\x. (exists y. ((y=' + sem(tr[0]) + ') & ' + sem(tr[1]) + '(y,x))))'
    elif (rule == 'S -> WHO QP QM'):
        ret = '(\\x. ' + sem(tr[1]) + ')'
        print 'check1'
        print ret
        return ret
    elif (rule == 'S -> WHICH Nom QP QM'):
        return '(\\x. (' + sem(tr[1]) + '&' + sem(tr[2]) + '))'
    elif (rule == 'QP -> VP'):
        ret = '(\\x. (' + sem(tr[0]) + '(x)))'
        print 'check2'
        print ret
        return ret
    elif (rule == 'QP -> DO NP T'):
        return '(\\x. (exists y. ((y=' + sem(tr[1]) + ') & ' + sem(tr[2]) + '(y,x))))'
    elif (rule == 'VP -> I'):
        return '(\\x. ' + sem(tr[0]) + '(x))'
    elif (rule == 'VP -> T NP'):
        return '(\\x. (exists y. (' + sem(tr[0]) + '(x,y) & (y=' + sem(tr[1]) + '))))'
    elif (rule == 'VP -> BE A'):
        ret =  '(\\x. ' + sem(tr[1]) + '(x))'
        print 'check3'
        print ret
        return ret
    elif (rule == 'VP -> BE NP'):
        return '(\\x. ' + sem(tr[1]) + '(x))'
    elif (rule == 'VP -> VP AND VP'):
        return '(\\x. (' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'

# Logic parser for lambda expressions

from nltk import LogicParser
lp = LogicParser()

# Lambda expressions can now be checked and simplified as follows:

A = lp.parse('(\\x.((\\P.P(x,x))(loves)))(John)')
A.simplify()

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
        print fb.queryUnary('A_orange','Mike')
        print '-------------'
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

