def add(item,lst):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
      self.cat_dict = {'P':[], 'N':[], 'A':[], 'I':[], 'T':[]}

    def add(self, stem, cat):
      """adds the given stem to the dictionary entry
        for a category"""
      if cat in self.cat_dict.keys():
        if not stem in self.cat_dict[cat]:  self.cat_dict[cat].append(stem)
      else:
        return 'Error: not a valid tag'
    
    def getAll(self, cat):
      """returns all stems with a given category"""
      return self.cat_dict[cat]

class FactBase:
    """stores unary and binary relational facts"""


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
                        
